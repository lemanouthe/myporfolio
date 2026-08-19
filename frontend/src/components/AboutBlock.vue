<script setup>
// Description / profil — texte + carte d'infos (mockup .about-grid + .info-card).
</script>

<template>
  <div class="about-grid">
    <div>
      <p>
        Développeur backend, je me concentre sur des <strong>APIs Django</strong>
        qui doivent tenir en production : architecture de données propre, tâches
        asynchrones fiables, déploiements reproductibles.
      </p>
      <p>
        Je travaille en <strong>full remote</strong> et j'aime les projets où la
        qualité du backend compte vraiment (scalabilité, sécurité, maintenabilité)
        plutôt que du code jetable.
      </p>
      <p>
        Côté outillage : Docker au quotidien, PostgreSQL, Redis/Celery pour
        l'asynchrone, CI/CD GitHub Actions, déploiement sur VPS/AWS.
      </p>
    </div>

    <div class="info-card">
      <div class="info-row"><span class="k">STATUS</span><span class="v status-up">● disponible</span></div>
      <div class="info-row"><span class="k">FOCUS</span><span class="v">Backend / API</span></div>
      <div class="info-row"><span class="k">STACK</span><span class="v">Django · PostgreSQL</span></div>
      <div class="info-row"><span class="k">MODE</span><span class="v">Full remote</span></div>
      <div class="info-row"><span class="k">LANGUES</span><span class="v">FR, EN</span></div>
    </div>
  </div>
</template>
