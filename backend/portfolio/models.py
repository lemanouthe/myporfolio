from django.db import models


class Project(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    context = models.TextField()
    challenge = models.TextField()
    result = models.CharField(max_length=200)  # badge résultat chiffré
    stack_tags = models.JSONField(default=list)  # ["Django", "PostgreSQL", ...]
    repo_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    cover = models.ImageField(upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class SkillGroup(models.Model):
    label = models.CharField(max_length=50)  # "Backend", "Infra & Cloud"...
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return self.label


class Skill(models.Model):
    class Level(models.TextChoices):
        EXPERT = "expert", "Expert"
        AVANCE = "avance", "Avancé"
        INTERMEDIAIRE = "intermediaire", "Intermédiaire"

    group = models.ForeignKey(
        SkillGroup, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    level = models.CharField(
        max_length=20, choices=Level.choices, default=Level.INTERMEDIAIRE
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Education(models.Model):
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)  # null = en cours
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]

    def __str__(self):
        return f"{self.degree} — {self.school}"


class Certification(models.Model):
    name = models.CharField(max_length=150)
    issuer = models.CharField(max_length=100)  # AWS, Docker, PostgreSQL...
    year = models.PositiveIntegerField()
    credential_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year"]

    def __str__(self):
        return f"{self.name} ({self.issuer})"


class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    start = models.CharField(max_length=20)  # "2022", "Jan 2022"...
    end = models.CharField(max_length=20, blank=True)  # vide = poste actuel
    description = models.TextField(blank=True)
    stack_tags = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start"]

    def __str__(self):
        return f"{self.role} @ {self.company}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
