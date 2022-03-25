<template>
  <router-view :key="$route.fullPath" />
</template>

<script setup lang="ts">
import Home from "./components/Home.vue";
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
body {
  margin: 0;
  height: 100vh;
}
</style>
