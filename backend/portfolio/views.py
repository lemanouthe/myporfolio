import logging

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Certification, Education, Experience, Project, SkillGroup
from .serializers import (
    CertificationSerializer,
    ContactMessageSerializer,
    EducationSerializer,
    ExperienceSerializer,
    ProjectSerializer,
    SkillGroupSerializer,
)

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "slug"


class SkillGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SkillGroup.objects.prefetch_related("skills").all()
    serializer_class = SkillGroupSerializer


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ContactMessageSerializer
    throttle_scope = "contact"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Honeypot tripped -> pretend success, create nothing.
        if data.pop("website", ""):
            logger.info("Contact honeypot triggered, dropping message silently.")
            return Response(status=status.HTTP_201_CREATED)

        message = serializer.save()
        self._notify(message)
        return Response(
            {"detail": "Message envoyé."}, status=status.HTTP_201_CREATED
        )

    def _notify(self, message):
        try:
            send_mail(
                subject=f"[Portfolio] Nouveau message de {message.name}",
                message=f"De: {message.name} <{message.email}>\n\n{message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:  # noqa: BLE001 - never let email break the response
            logger.exception("Failed to send contact notification email.")
