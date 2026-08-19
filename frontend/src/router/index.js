import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", name: "home", component: () => import("../views/HomeView.vue") },
  { path: "/projets", name: "projets", component: () => import("../views/ProjectsView.vue") },
  { path: "/contact", name: "contact", component: () => import("../views/ContactView.vue") },
  // La prise de RDV vit dans la page Contact.
  { path: "/rendez-vous", redirect: "/contact" },
  // Stack & parcours ne sont plus des pages : leur contenu reste sur la Home.
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});
