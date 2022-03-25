<template>
  <el-card class="box-card" v-if="movieInfo.movieId">
    <el-image :src="static_domain + 'posters/' + movieInfo.movieId + '.jpg'">
    </el-image>
    <div class="movie-info-title">{{ movieInfo.title }}</div>
    <el-descriptions class="margin-top" :column="3" :size="size" border>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">Release Year</div>
        </template>
        {{ movieInfo.releaseYear }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">stars</div>
        </template>
        <el-icon color="#409EFC"><star-filled /></el-icon>
        {{ movieInfo.averageRating.toPrecision(2) }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">Link</div>
        </template>
        <el-link
          type="success"
          :href="'http://www.themoviedb.org/movie/' + movieInfo.tmdbId"
          target="_blank"
        >
          imdb
        </el-link>
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">Give Star</div>
        </template>
        <el-rate v-model="value" allow-half />
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">Genres</div>
        </template>
        <el-tag v-for="(t, i) in movieInfo.genres" :key="i" size="small">
          {{ t }}
        </el-tag>
      </el-descriptions-item>
    </el-descriptions>
    <h2 class="margin-top" title="Similar Movies">Similar Movies</h2>
    <movie-row typ="similar" :id="movieInfo.movieId" v-if="movieInfo.movieId" />
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { StarFilled } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";
import { MovieService } from "@/api/api.ts";
import MovieRow from "./row/MovieRow.vue";

const movieInfo = ref({});
const static_domain = import.meta.env.VITE_STATIC_DOMAIN;
const value = ref();
const size = ref("");

onMounted(() => {
  getGenres();
});

const getGenres = async () => {
  const params = {
    id: useRouter().currentRoute.value.params.id,
  };
  const res = await MovieService.minfo(params);
  movieInfo.value = res.data;
};
</script>

<style lang="less">
.movie-info-title {
  margin-top: 10px;
  font-weight: 900;
  font-size: 26px;
}
.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
.el-image__inner {
  height: 200px;
}
.box-card {
  height: auto;
  max-height: none;
}
.el-tag {
  margin-right: 2%;
}
</style>
