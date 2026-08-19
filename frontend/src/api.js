// Same-origin in prod (Django sert le SPA), proxied in dev (vite.config.js).
const BASE = "/api";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} -> ${res.status}`);
  return res.json();
}

async function post(path, payload) {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    // DRF renvoie soit {detail}, soit {champ: [msg]}
    const msg =
      data.detail ||
      Object.values(data).flat().join(" ") ||
      `Erreur ${res.status}`;
    throw new Error(msg);
  }
  return res.json().catch(() => ({}));
}

export const api = {
  projects: () => get("/projects/"),
  skills: () => get("/skills/"),
  education: () => get("/education/"),
  certifications: () => get("/certifications/"),
  experiences: () => get("/experiences/"),
  contact: (payload) => post("/contact/", payload),
};
