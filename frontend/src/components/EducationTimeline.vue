<script setup>
import DashDots from "./DashDots.vue";

defineProps({
  items: { type: Array, default: () => [] },
});
</script>

<template>
  <div class="timeline">
    <div v-for="(e, i) in items" :key="i" class="timeline-item">
      <div class="t-date">{{ e.start_year }} → {{ e.end_year || "en cours" }}</div>
      <h3>{{ e.degree }}</h3>
      <p><DashDots :text="e.school" /></p>
    </div>
  </div>
</template>
