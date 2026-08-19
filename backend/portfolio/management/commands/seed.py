"""Remplit la base avec des données de démo (éditables ensuite dans l'admin).

    python manage.py seed          # (ré)initialise le contenu de démo

N'affecte pas les messages de contact ni les rendez-vous.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import (
    Certification,
    Education,
    Experience,
    Project,
    Skill,
    SkillGroup,
)

PROJECTS = [
    dict(
        slug="nisc",
        name="NISC — Plateforme de gestion d'inventaire",
        role="Backend Developer",
        context="API de suivi de stock multi-entrepôts pour une PME logistique : "
        "réceptions, mouvements, alertes de seuil et exports comptables.",
        challenge="Requêtes d'agrégation lourdes sur l'historique des mouvements. "
        "Refonte du schéma + index composites et mise en cache Redis des tableaux de bord.",
        result="Temps de réponse des dashboards réduit de 4,2 s à 380 ms",
        stack_tags=["Django REST Framework", "PostgreSQL", "Redis", "Docker", "GitHub Actions"],
        order=1,
    ),
    dict(
        slug="tech-yao",
        name="TECH YAO — Traitement de commandes asynchrone",
        role="Backend Developer",
        context="Back-office e-commerce : génération de factures PDF, notifications "
        "et synchronisation avec un service de livraison externe.",
        challenge="Les tâches longues bloquaient les requêtes web. Passage à Celery "
        "pour l'asynchrone, avec files prioritaires et reprise sur échec.",
        result="0 timeout en production, ~12k tâches/jour traitées",
        stack_tags=["Django", "Celery", "Redis", "AWS", "Docker"],
        order=2,
    ),
    dict(
        slug="nan-business",
        name="NaN Business — API SaaS multi-tenant",
        role="Backend Developer",
        context="Plateforme SaaS B2B avec isolation des données par client, "
        "facturation à l'usage et rôles/permissions fins.",
        challenge="Isolation multi-tenant fiable et sécurisée sans dupliquer la logique. "
        "Middleware de scoping + permissions DRF centralisées.",
        result="Onboarding d'un nouveau client en < 5 min, 99,9% de disponibilité",
        stack_tags=["Django REST Framework", "PostgreSQL", "AWS", "Docker"],
        order=3,
    ),
]

SKILL_GROUPS = [
    ("Backend", 1, [
        ("python", Skill.Level.EXPERT),
        ("django", Skill.Level.EXPERT),
        ("djangorestframework", Skill.Level.EXPERT),
    ]),
    ("Données & Files", 2, [
        ("postgresql", Skill.Level.AVANCE),
        ("redis", Skill.Level.AVANCE),
        ("celery", Skill.Level.AVANCE),
    ]),
    ("Infra & Cloud", 3, [
        ("docker", Skill.Level.AVANCE),
        ("aws", Skill.Level.AVANCE),
        ("github-actions", Skill.Level.AVANCE),
    ]),
    ("Frontend (appoint)", 4, [
        ("vue.js", Skill.Level.INTERMEDIAIRE),
    ]),
]

EXPERIENCES = [
    dict(
        company="NaN Business",
        role="Backend Developer",
        location="Remote",
        start="2023",
        end="",
        description="Conception et maintenance d'APIs SaaS multi-tenant en Django/DRF : "
        "modélisation, permissions, facturation à l'usage, CI/CD et déploiement Docker.",
        stack_tags=["Django REST Framework", "PostgreSQL", "AWS", "Docker"],
        order=1,
    ),
    dict(
        company="TECH YAO",
        role="Backend Developer",
        location="Abidjan / Remote",
        start="2021",
        end="2023",
        description="Développement de back-offices e-commerce, traitement asynchrone "
        "avec Celery/Redis et intégrations de services externes (paiement, livraison).",
        stack_tags=["Django", "Celery", "Redis", "AWS"],
        order=2,
    ),
    dict(
        company="Freelance",
        role="Développeur Web",
        location="Remote",
        start="2019",
        end="2021",
        description="Sites et APIs pour des TPE/PME : Django, PostgreSQL, déploiement "
        "sur VPS et premières mises en place de conteneurs Docker.",
        stack_tags=["Django", "PostgreSQL", "Docker"],
        order=3,
    ),
]

EDUCATION = [
    dict(school="Université — Informatique", degree="Master Génie Logiciel",
         start_year=2017, end_year=2019, order=1),
    dict(school="Université — Informatique", degree="Licence Informatique",
         start_year=2014, end_year=2017, order=2),
]

CERTIFICATIONS = [
    dict(name="AWS Certified Cloud Practitioner", issuer="Amazon Web Services",
         year=2023, order=1),
    dict(name="Docker Foundations", issuer="Docker", year=2022, order=2),
    dict(name="PostgreSQL for Developers", issuer="EDB", year=2022, order=3),
    dict(name="Meta Backend Developer", issuer="Coursera / Meta", year=2021, order=4),
]


class Command(BaseCommand):
    help = "Remplit la base avec des données de démo."

    @transaction.atomic
    def handle(self, *args, **options):
        # Reset du contenu vitrine (pas les messages ni les RDV).
        for model in (Project, Skill, SkillGroup, Experience, Education, Certification):
            model.objects.all().delete()

        for data in PROJECTS:
            Project.objects.create(**data)

        for label, order, skills in SKILL_GROUPS:
            group = SkillGroup.objects.create(label=label, order=order)
            for i, (name, level) in enumerate(skills):
                Skill.objects.create(group=group, name=name, level=level, order=i)

        for data in EXPERIENCES:
            Experience.objects.create(**data)
        for data in EDUCATION:
            Education.objects.create(**data)
        for data in CERTIFICATIONS:
            Certification.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(
            f"Seed OK — {Project.objects.count()} projets, "
            f"{Skill.objects.count()} skills, {Experience.objects.count()} expériences, "
            f"{Education.objects.count()} formations, "
            f"{Certification.objects.count()} certifications."
        ))
