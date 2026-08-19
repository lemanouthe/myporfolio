from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("portfolio.urls")),
    # WhiteNoise handles /static; media (uploads) is served by Django in all envs.
    # Fine for a low-traffic personal site — no separate file server needed.
    re_path(
        r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}
    ),
]

# SPA catch-all: anything not matched above returns the Vue index.html, whose
# assets live under /static/ (served by WhiteNoise). Same origin, no CORS.
# Only wired when the build is present (in dev, Vite serves the SPA on :5173).
if (settings.FRONTEND_DIST / "index.html").exists():
    urlpatterns += [
        re_path(
            r"^(?!api/|admin/|static/|media/).*$",
            TemplateView.as_view(template_name="index.html"),
        ),
    ]
