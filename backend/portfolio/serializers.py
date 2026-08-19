from rest_framework import serializers

from .models import (
    Certification,
    ContactMessage,
    Education,
    Experience,
    Project,
    Skill,
    SkillGroup,
)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "slug",
            "name",
            "role",
            "context",
            "challenge",
            "result",
            "stack_tags",
            "repo_url",
            "demo_url",
            "cover",
            "order",
        ]


class SkillSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source="get_level_display", read_only=True)

    class Meta:
        model = Skill
        fields = ["name", "level", "level_display"]


class SkillGroupSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillGroup
        fields = ["label", "order", "skills"]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["school", "degree", "start_year", "end_year", "order"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ["name", "issuer", "year", "credential_url", "order"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "company",
            "role",
            "location",
            "start",
            "end",
            "description",
            "stack_tags",
            "order",
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    # Honeypot: bots fill hidden fields, humans don't. Never persisted.
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message", "website"]
