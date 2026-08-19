<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { api } from "../api.js";
import Hero from "../components/Hero.vue";
import ExperienceTimeline from "../components/ExperienceTimeline.vue";
import SkillManifest from "../components/SkillManifest.vue";
import EducationTimeline from "../components/EducationTimeline.vue";
import CertGrid from "../components/CertGrid.vue";
import AboutBlock from "../components/AboutBlock.vue";

const experiences = ref([]);
const skills = ref([]);
const education = ref([]);
const certifications = ref([]);
const error = ref("");

onMounted(async () => {
  try {
    [experiences.value, skills.value, education.value, certifications.value] =
      await Promise.all([
        api.experiences(),
        api.skills(),
        api.education(),
        api.certifications(),
      ]);
  } catch (e) {
    error.value = e.message;
  }
});
</script>

<template>
  <Hero />

  <p v-if="error" class="wrap err mono">Erreur API : {{ error }}</p>

  <!-- Description / profil -->
  <section class="section">
    <div class="wrap">
      <span class="tag">[PROFIL]</span>
      <h2 class="section-title">À propos</h2>
      <p class="section-sub">Qui je suis et comment je travaille.</p>
      <AboutBlock />
    </div>
  </section>

  <!-- Expériences professionnelles -->
  <section class="section">
    <div class="wrap">
      <span class="tag">[EXPÉRIENCES]</span>
      <h2 class="section-title">Expériences professionnelles</h2>
      <p class="section-sub">Mon parcours en entreprise et en mission.</p>
      <ExperienceTimeline v-if="experiences.length" :items="experiences" />
      <p v-else class="dim mono">À compléter depuis l'admin.</p>
    </div>
  </section>

  <!-- Compétences & stack technique -->
  <section class="section">
    <div class="wrap">
      <span class="tag">[COMPÉTENCES]</span>
      <h2 class="section-title">Compétences &amp; stack technique</h2>
      <p class="section-sub">Les domaines que je couvre et les technologies au quotidien.</p>

      <div v-if="skills.length" class="domains">
        <span v-for="g in skills" :key="g.label" class="stack-tag domain">{{ g.label }}</span>
      </div>
      <SkillManifest :groups="skills" />
    </div>
  </section>

  <!-- Formation & éducation -->
  <section class="section">
    <div class="wrap">
      <span class="tag">[FORMATION]</span>
      <h2 class="section-title">Formation &amp; éducation</h2>
      <p class="section-sub">Diplômes et certifications.</p>

      <EducationTimeline v-if="education.length" :items="education" />
      <p v-else class="dim mono">À compléter depuis l'admin.</p>

      <template v-if="certifications.length">
        <span class="tag" style="margin-top: 40px">[CERTIFICATIONS]</span>
        <CertGrid :items="certifications" />
      </template>
    </div>
  </section>

  <!-- CTA final -->
  <section class="section">
    <div class="wrap cta-final">
      <div>
        <h2 class="section-title">Un projet backend en tête ?</h2>
        <p class="section-sub" style="margin-bottom: 0">
          Écris-moi ou réserve directement un créneau.
        </p>
      </div>
      <RouterLink to="/contact" class="btn btn-primary">→ prendre rendez-vous</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.err {
  color: var(--danger);
  padding: 16px 24px;
}
.dim {
  color: var(--text-muted);
}
.domains {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}
.domain {
  color: var(--teal);
  border-color: rgba(79, 179, 169, 0.3);
  background: rgba(79, 179, 169, 0.08);
}
.cta-final {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}
</style>
