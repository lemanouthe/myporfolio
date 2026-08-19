<script setup>
defineProps({
  email: { type: String, default: "mamoutoudoumbia89@gmail.com" },
  github: { type: String, default: "https://github.com/lemanouthe" },
  linkedin: { type: String, default: "https://www.linkedin.com/in/doumbiamamoutou/" },
});
</script>

<template>
  <footer class="site-footer">
    <div class="wrap inner">
      <div class="copyline">© {{ new Date().getFullYear() }} Doumbia Mamoutou. Tous droits réservés.</div>
      <div class="flinks">
        <a :href="github" target="_blank" rel="noopener">GitHub</a>
        <a :href="linkedin" target="_blank" rel="noopener">LinkedIn</a>
        <a :href="`mailto:${email}`">Email</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  padding: 32px 0;
  border-top: 1px solid var(--border);
  margin-top: 40px;
}
.inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.copyline {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-muted);
}
.flinks {
  display: flex;
  gap: 20px;
  font-family: var(--mono);
  font-size: 13px;
  color: var(--text-muted);
}
.flinks a:hover {
  color: var(--amber);
}
</style>
