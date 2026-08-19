from django.core import mail
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Experience, Project, SkillGroup, Skill, ContactMessage


class ApiReadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Project.objects.create(
            slug="nisc", name="NISC", role="Backend", context="c",
            challenge="ch", result="99.9% uptime", stack_tags=["Django"],
        )
        group = SkillGroup.objects.create(label="Backend")
        Skill.objects.create(group=group, name="Django", level=Skill.Level.EXPERT)

    def test_projects_list(self):
        res = self.client.get("/api/projects/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["slug"], "nisc")

    def test_skills_nested(self):
        res = self.client.get("/api/skills/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()[0]["skills"][0]["level_display"], "Expert")

    def test_experiences_list(self):
        Experience.objects.create(
            company="Tech Yao", role="Backend Developer", start="2022", end="",
        )
        res = self.client.get("/api/experiences/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()[0]["company"], "Tech Yao")


class ContactTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_contact_creates_and_emails(self):
        res = self.client.post(
            "/api/contact/",
            {"name": "Jane", "email": "jane@example.com", "message": "Hi"},
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_honeypot_drops_message_silently(self):
        res = self.client.post(
            "/api/contact/",
            {"name": "Bot", "email": "bot@x.com", "message": "spam", "website": "http://spam"},
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
