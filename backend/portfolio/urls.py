from rest_framework.routers import DefaultRouter

from .views import (
    CertificationViewSet,
    ContactViewSet,
    EducationViewSet,
    ExperienceViewSet,
    ProjectViewSet,
    SkillGroupViewSet,
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("skills", SkillGroupViewSet, basename="skill")
router.register("education", EducationViewSet, basename="education")
router.register("certifications", CertificationViewSet, basename="certification")
router.register("experiences", ExperienceViewSet, basename="experience")
router.register("contact", ContactViewSet, basename="contact")

urlpatterns = router.urls
