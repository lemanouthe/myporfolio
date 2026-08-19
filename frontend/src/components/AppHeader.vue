<script setup>
import { ref } from "vue";

const open = ref(false);

const links = [
  { to: "/", label: "Home" },
  { to: "/projets", label: "Projects" },
  { to: "/contact", label: "Contact" },
];
</script>

<template>
  <nav class="site-nav">
    <div class="wrap bar">
      <router-link to="/" class="logo" @click="open = false">
        doumbia <span>mamoutou</span>
      </router-link>

      <button class="burger" :aria-expanded="open" aria-label="Menu" @click="open = !open">
        {{ open ? "✕" : "≡" }}
      </button>

      <div class="navlinks" :class="{ open }">
        <router-link
          v-for="l in links"
          :key="l.to"
          :to="l.to"
          class="nlink"
          @click="open = false"
        >
          {{ l.label }}
        </router-link>
        <!-- <router-link to="/contact" class="btn btn-primary rdv" @click="open = false">
          → prendre rdv
        </router-link> -->
      </div>
    </div>
  </nav>
</template>

<style scoped>
.site-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(16, 19, 26, 0.85);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}
.bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}
.logo {
  font-family: var(--mono);
  font-weight: 600;
  font-size: 15px;
  color: var(--text);
}
.logo span {
  color: var(--amber);
}
.navlinks {
  display: flex;
  align-items: center;
  gap: 28px;
  font-family: var(--mono);
  font-size: 13px;
  color: var(--text-muted);
}
.nlink {
  color: var(--text-muted);
  transition: color 0.15s ease;
}
.nlink:hover {
  color: var(--amber);
}
.nlink.router-link-active {
  color: var(--teal);
}
.rdv {
  padding: 8px 14px;
}
.rdv.router-link-active {
  color: #1a1206;
}
.burger {
  display: none;
  background: none;
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 5px;
  font-size: 1.1rem;
  width: 38px;
  height: 38px;
  cursor: pointer;
}

@media (max-width: 640px) {
  .burger {
    display: block;
  }
  .navlinks {
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 20px 24px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: none;
  }
  .navlinks.open {
    display: flex;
  }
  .rdv {
    align-self: stretch;
    justify-content: center;
  }
}
</style>
