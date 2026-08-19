from django.contrib import admin

from .models import (
    Certification,
    ContactMessage,
    Education,
    Experience,
    Project,
    Skill,
    SkillGroup,
)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ("label", "order")
    inlines = [SkillInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "result", "order")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "school", "start_year", "end_year", "order")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "issuer", "year", "order")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start", "end", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        return False
