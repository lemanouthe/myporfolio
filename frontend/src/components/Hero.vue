<script setup>
import { RouterLink } from "vue-router";
import TrafficDots from "./TrafficDots.vue";
</script>

<template>
  <header class="hero">
    <div class="wrap">
      <div class="eyebrow">
        <span class="pulse-dot"></span> DISPONIBLE POUR NOUVEAUX PROJETS
      </div>

      <h1>
        Doumbia Mamoutou <TrafficDots class="sep" />
        <span class="fn">Backend Engineer</span>
      </h1>

      <p class="lead">
        Je conçois et j'industrialise des <strong>APIs backend robustes</strong>
        (Django, PostgreSQL, Redis/Celery, Docker, AWS) pour des équipes produit
        qui ont besoin que ça tienne en charge, pas juste que ça marche en local.
      </p>

      <div class="cta-row">
        <RouterLink to="/contact" class="btn btn-primary">→ Démarrer un projet</RouterLink>
        <RouterLink to="/projets" class="btn btn-ghost">Voir les projets</RouterLink>
      </div>

      <div class="console">
        <div class="console-bar">
          <span class="tf tf1"></span><span class="tf tf2"></span><span class="tf tf3"></span>
          <span class="console-title">zsh · mamoutou@remote</span>
        </div>
        <div class="console-body">
          <div class="line"><span class="prompt">$</span> stack --list --profile=mamoutou</div>
          <div class="out">
            SELECT expertise FROM engineer<br />
            WHERE stack IN ('Django','DRF','PostgreSQL','Redis','Celery','Docker','AWS')<br />
            AND remote = true;
          </div>
        </div>
      </div>

      <div class="metrics">
        <div class="metric"><div class="val">5+ ans</div><div class="lbl">Expérience backend</div></div>
        <div class="metric"><div class="val">Remote</div><div class="lbl">Full remote</div></div>
        <div class="metric"><div class="val">FR · EN</div><div class="lbl">Langues</div></div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.hero {
  padding: 90px 0 60px;
}
h1 {
  font-family: var(--mono);
  font-size: clamp(34px, 6vw, 56px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
}
h1 .fn {
  color: var(--text-muted);
  font-weight: 400;
}
.sep {
  transform: translateY(2px);
}
.lead {
  font-size: 18px;
  color: var(--text-muted);
  max-width: 580px;
  margin-bottom: 34px;
}
.lead strong {
  color: var(--text);
  font-weight: 600;
}
.cta-row {
  display: flex;
  gap: 14px;
  margin-bottom: 52px;
  flex-wrap: wrap;
}
</style>
