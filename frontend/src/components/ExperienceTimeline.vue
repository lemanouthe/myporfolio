<script setup>
defineProps({
  items: { type: Array, default: () => [] },
});
</script>

<template>
  <div class="timeline">
    <div v-for="(x, i) in items" :key="i" class="timeline-item">
      <div class="t-date">{{ x.start }} → {{ x.end || "présent" }}</div>
      <h3>{{ x.role }}</h3>
      <div class="t-org">
        {{ x.company }}<template v-if="x.location"> · {{ x.location }}</template>
      </div>
      <p v-if="x.description">{{ x.description }}</p>
      <div v-if="x.stack_tags?.length" class="stack-tags" style="margin-top: 12px">
        <span v-for="t in x.stack_tags" :key="t" class="stack-tag">{{ t }}</span>
      </div>
    </div>
  </div>
</template>
