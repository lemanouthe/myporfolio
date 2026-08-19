<script setup>
import DashDots from "./DashDots.vue";

defineProps({
  project: { type: Object, required: true },
});
</script>

<template>
  <article class="project">
    <div class="project-head">
      <span class="tf tf1"></span><span class="tf tf2"></span><span class="tf tf3"></span>
      <span class="project-name">{{ project.slug }}/</span>
    </div>
    <div class="project-body">
      <h3><DashDots :text="project.name" /></h3>
      <div class="role">Rôle : {{ project.role }}</div>

      <p v-if="project.context">{{ project.context }}</p>

      <div v-if="project.stack_tags?.length" class="stack-tags">
        <span v-for="t in project.stack_tags" :key="t" class="stack-tag">{{ t }}</span>
      </div>

      <p v-if="project.challenge">
        <strong style="color: var(--text)">Défi technique :</strong> {{ project.challenge }}
      </p>

      <div v-if="project.result" class="result-badge">
        <span class="arrow">→</span> {{ project.result }}
      </div>

      <div v-if="project.repo_url || project.demo_url" class="links mono">
        <a v-if="project.repo_url" :href="project.repo_url" target="_blank" rel="noopener">code →</a>
        <a v-if="project.demo_url" :href="project.demo_url" target="_blank" rel="noopener">démo →</a>
      </div>
    </div>
  </article>
</template>

<style scoped>
.links {
  display: flex;
  gap: 18px;
  margin-top: 16px;
  font-size: 13px;
}
.links a {
  color: var(--amber);
}
</style>
