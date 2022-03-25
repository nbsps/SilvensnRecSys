<template>
  <el-tabs type="border-card">
    <el-tab-pane label="ForYou">
      <movie-row typ="foryou" :id="userId" />
    </el-tab-pane>
    <el-tab-pane v-for="g in genres" :label="g" :key="g" lazy>
      <movie-row :cls="g" />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { MovieService } from "@/api/api.ts";
import MovieRow from "./row/MovieRow.vue";

const genres = ref([]);

const props = defineProps({
  userId: {
    type: Number,
    default: 1,
  },
});

watch(
  () => props.userId,
  (n, o) => {
    console.log({ n, o });
  }
);

onMounted(() => {
  getGenres();
});

const getGenres = async () => {
  const params = {};
  const res = await MovieService.genres(params);
  res.data.forEach((i) => {
    genres.value.push(i);
  });
};
</script>

<style lang="less" scoped>
.el-tab {
  margin-bottom: 20px;
}
</style>
