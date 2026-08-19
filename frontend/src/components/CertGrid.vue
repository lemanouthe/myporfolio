<script setup>
defineProps({
  items: { type: Array, default: () => [] },
});
</script>

<template>
  <div class="cert-grid">
    <component
      :is="c.credential_url ? 'a' : 'div'"
      v-for="(c, i) in items"
      :key="i"
      class="cert-card"
      :href="c.credential_url || undefined"
      :target="c.credential_url ? '_blank' : undefined"
      rel="noopener"
    >
      <div class="cert-check">✓</div>
      <div>
        <h4>{{ c.name }}</h4>
        <div class="cert-meta">{{ c.issuer }} · {{ c.year }}</div>
      </div>
    </component>
  </div>
</template>
