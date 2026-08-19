<script setup>
// ⚠️ GitHub encore à confirmer (déduit de ton image ghcr.io/lemanouthe/...).
const links = [
  {
    key: "linkedin",
    label: "LinkedIn",
    value: "in/doumbiamamoutou",
    href: "https://www.linkedin.com/in/doumbiamamoutou/",
    external: true,
  },
  {
    key: "github",
    label: "GitHub",
    value: "github.com/lemanouthe",
    href: "https://github.com/lemanouthe",
    external: true,
  },
  {
    key: "email",
    label: "Email",
    value: "mamoutoudoumbia89@gmail.com",
    href: "mailto:mamoutoudoumbia89@gmail.com",
    external: false,
  },
  {
    key: "phone",
    label: "Téléphone",
    value: "+225 01 53 65 65 07",
    href: "tel:+2250153656507",
    external: false,
  },
];
</script>

<template>
  <div class="links">
    <a
      v-for="l in links"
      :key="l.key"
      class="icon-link"
      :href="l.href"
      :target="l.external ? '_blank' : undefined"
      :rel="l.external ? 'noopener' : undefined"
      :aria-label="`${l.label} : ${l.value}`"
      :title="l.value"
    >
      <!-- linkedin -->
      <svg v-if="l.key === 'linkedin'" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
        <path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.76-2.05 4.02 0 4.76 2.65 4.76 6.1V21H17.7v-5.4c0-1.3-.02-2.97-1.8-2.97-1.8 0-2.08 1.4-2.08 2.87V21H9z"/>
      </svg>
      <!-- github -->
      <svg v-else-if="l.key === 'github'" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
        <path d="M12 2a10 10 0 00-3.16 19.49c.5.09.68-.22.68-.48l-.01-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.36 1.09 2.93.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.6 9.6 0 015 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85l-.01 2.75c0 .27.18.58.69.48A10 10 0 0012 2z"/>
      </svg>
      <!-- email -->
      <svg v-else-if="l.key === 'email'" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8">
        <rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>
      </svg>
      <!-- phone -->
      <svg v-else viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8">
        <path d="M4 5c0-1 .9-2 2-2h1.5c.5 0 .9.3 1 .8l.8 3c.1.4 0 .8-.3 1.1L7.6 9.3a12 12 0 005 5l1.4-1.4c.3-.3.7-.4 1.1-.3l3 .8c.5.1.8.5.8 1V16c0 1.1-.9 2-2 2A14 14 0 014 6z"/>
      </svg>
    </a>
  </div>
</template>

<style scoped>
.links {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}
.icon-link {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--teal);
  transition: border-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
}
.icon-link:hover {
  border-color: var(--amber);
  color: var(--amber);
  transform: translateY(-2px);
}
</style>
