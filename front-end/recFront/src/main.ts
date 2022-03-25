import { createApp } from "vue";
import router from "./router/index";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import lazyPlugin from "vue3-lazy";
import App from "./App.vue";

createApp(App)
  .use(lazyPlugin, {
    loading: "./public/nbsps.png",
    error: "./public/error.png",
  })
  .use(ElementPlus)
  .use(router)
  .mount("#app");
