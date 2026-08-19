<script setup>
import { onMounted, ref } from "vue";

const props = defineProps({
  // URL de ton type d'événement Calendly (ex: .../mamoutoudoumbia89/30min)
  url: { type: String, required: true },
});

const container = ref(null);
const failed = ref(false);
const SCRIPT_SRC = "https://assets.calendly.com/assets/external/widget.js";

function loadScript() {
  return new Promise((resolve, reject) => {
    if (window.Calendly) return resolve();
    let s = document.querySelector(`script[src="${SCRIPT_SRC}"]`);
    if (s) {
      s.addEventListener("load", resolve);
      s.addEventListener("error", reject);
      if (window.Calendly) resolve();
      return;
    }
    s = document.createElement("script");
    s.src = SCRIPT_SRC;
    s.async = true;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

onMounted(async () => {
  try {
    await loadScript();
    // Conteneur SANS la classe .calendly-inline-widget : on évite l'auto-scan
    // de widget.js (qui lit data-url et plante si absent). On initialise nous-mêmes.
    if (window.Calendly?.initInlineWidget && container.value) {
      window.Calendly.initInlineWidget({
        url: props.url,
        parentElement: container.value,
      });
    } else {
      failed.value = true;
    }
  } catch {
    failed.value = true;
  }
});
</script>

<template>
  <div class="cal-embed">
    <div v-if="failed" class="fallback mono">
      Impossible de charger le calendrier.
      <a :href="url" target="_blank" rel="noopener">Réserver sur Calendly ↗</a>
    </div>
    <div v-else ref="container" class="cal-frame"></div>
    <p class="note mono">
      La réservation crée un lien Google Meet et l'envoie par email aux deux participants.
    </p>
  </div>
</template>

<style scoped>
.cal-embed {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.cal-frame {
  min-width: 300px;
  height: 700px;
}
.fallback {
  padding: 24px;
  color: var(--text-muted);
  font-size: 13px;
}
.fallback a {
  color: var(--amber);
  display: inline-block;
  margin-top: 8px;
}
.note {
  color: var(--text-muted);
  font-size: 11.5px;
  padding: 10px 14px;
  border-top: 1px solid var(--border);
}
</style>
