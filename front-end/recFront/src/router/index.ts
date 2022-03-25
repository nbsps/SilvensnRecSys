import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/index.html",
    redirect: "/",
  },
  {
    path: "/",
    name: "index",
    component: () => import("@/components/Home.vue"),
  },
  {
    path: "/movie/:id",
    name: "movie",
    component: () => import("@/components/MovieInfo.vue"),
  },
  // {
  //   path: "/user",
  //   name: "user",
  //   component: () => import("@/components/UserInfo.vue"),
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
