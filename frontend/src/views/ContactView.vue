<script setup>
import ContactLinks from "../components/ContactLinks.vue";
import CalendlyEmbed from "../components/CalendlyEmbed.vue";
import DashDots from "../components/DashDots.vue";

// Lien Calendly (type d'événement). Les paramètres après "?" thèment le widget.
const CALENDLY_URL =
  "https://calendly.com/mamoutoudoumbia89/30min" +
  "?hide_gdpr_banner=1&background_color=10131a&text_color=e9eaf0&primary_color=d9a54b";
</script>

<template>
  <section class="section first">
    <div class="wrap">
      <span class="tag">[CONTACT]</span>
      <h2 class="section-title">Démarrons un projet</h2>
      <p class="section-sub">
        <DashDots text="Écris-moi sur le canal qui te convient, ou réserve un créneau dans le calendrier — un lien Google Meet t'est envoyé automatiquement." />
      </p>

      <div class="stack">
        <div class="join">
          <h3 class="col-title mono">// me joindre</h3>
          <ContactLinks />
        </div>
        <div>
          <h3 class="col-title mono">// prendre rendez-vous</h3>
          <CalendlyEmbed :url="CALENDLY_URL" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.first {
  border-top: none;
}
.stack {
  display: flex;
  flex-direction: column;
  gap: 36px;
}
.col-title {
  color: var(--teal);
  font-size: 13px;
  margin-bottom: 14px;
}
.join {
  text-align: center;
}
</style>
