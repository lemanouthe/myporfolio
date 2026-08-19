<script setup>
import { onMounted, ref } from "vue";
import { api } from "../api.js";
import ProjectCard from "../components/ProjectCard.vue";

const projects = ref([]);
const error = ref("");
const loading = ref(true);

onMounted(async () => {
  try {
    projects.value = await api.projects();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="section first">
    <div class="wrap">
      <span class="tag">[PROJETS]</span>
      <h2 class="section-title">Études de cas</h2>
      <p class="section-sub">
        Projets backend représentatifs : du problème métier à l'architecture livrée.
      </p>

      <p v-if="loading" class="dim mono">chargement…</p>
      <p v-else-if="error" class="err mono">{{ error }}</p>
      <p v-else-if="!projects.length" class="dim mono">
        Aucun projet publié pour l'instant.
      </p>

      <ProjectCard v-for="p in projects" :key="p.slug" :project="p" />
    </div>
  </section>
</template>

<style scoped>
.first {
  border-top: none;
}
.dim {
  color: var(--text-muted);
}
.err {
  color: var(--danger);
}
</style>
