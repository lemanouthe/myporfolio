<script setup>
import { computed } from "vue";
import TrafficDots from "./TrafficDots.vue";

// Rend un texte en remplaçant chaque " — " par les 3 points colorés (feux).
const props = defineProps({
  text: { type: String, default: "" },
});

const parts = computed(() => props.text.split(/\s*—\s*/));
</script>

<template>
  <span class="dashdots">
    <template v-for="(p, i) in parts" :key="i">
      <TrafficDots v-if="i > 0" class="sep" />
      <span class="seg">{{ p }}</span>
    </template>
  </span>
</template>

<style scoped>
.dashdots {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
.sep {
  transform: translateY(1px);
}
</style>
