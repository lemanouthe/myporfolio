<script setup>
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";
// Photo en background du site. Remplace mamoutou.svg par ta photo (mamoutou.jpg)
// dans src/assets/ et adapte l'import ci-dessous.
import bg from "./assets/mamoutou.svg";
</script>

<template>
  <div class="site-bg" :style="{ backgroundImage: `url(${bg})` }"></div>
  <AppHeader />
  <main>
    <router-view v-slot="{ Component, route }">
      <transition name="fade" mode="out-in">
        <div :key="route.path" class="route-view">
          <component :is="Component" />
        </div>
      </transition>
    </router-view>
  </main>
  <AppFooter />
</template>

<style scoped>
main {
  min-height: 70vh;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
