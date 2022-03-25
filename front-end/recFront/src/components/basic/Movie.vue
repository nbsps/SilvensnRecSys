<template>
  <el-card :body-style="{ padding: '0px' }" @click="movieclick">
    <img
      v-lazy="static_domain + 'posters/' + movie.movieId + '.jpg'"
      class="image"
    />
    <div style="padding: 14px">
      <span class="title">{{ movie.title }}</span>
      <div class="bottom">
        <el-tag v-for="(t, i) in movie.genres" :key="i" size="small">
          {{ t }}
        </el-tag>
      </div>
      <div class="bottom">
        <time class="time">{{ movie.releaseYear }}</time>
        <div v-if="movie.onhot">🔥</div>
        <div class="star">
          <el-icon color="#409EFC"><star-filled /></el-icon>
          {{ movie.averageRating.toPrecision(2) }}
        </div>
      </div>
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { StarFilled } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";
import { MovieService } from "@/api/api.ts";

const router = useRouter();
const currentDate = ref(new Date());
const static_domain = import.meta.env.VITE_STATIC_DOMAIN;

const movieclick = async () => {
  await MovieService.countm({ movieId: props.movie.movieId });
  router.push({ path: "/movie/" + props.movie.movieId });
};

const props = defineProps({
  movie: {
    type: Object,
    default: {
      averageRating: 5,
      genres: ["Adventure"],
      imdbId: "112453.0",
      movieId: 13,
      releaseYear: 1995,
      title: "Balto",
      tmdbId: "21032.0",
    },
  },
});
</script>

<style>
.el-card {
  max-height: 400px;
  margin-top: 5px;
  margin-bottom: 5px;
}

.time {
  font-size: 13px;
  color: #999;
}

.el-icon {
  position: relative;
  top: 2px;
}

.title {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  -o-text-overflow: ellipsis;
}

.bottom {
  margin-top: 5px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}

.image {
  width: 100%;
  display: block;
}
</style>
