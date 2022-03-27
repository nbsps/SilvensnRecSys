<template>
  <div class="block">
    <span class="demonstration">💥 TOP HOT MOVIES 💥</span>
    <el-carousel :interval="4000" type="card" height="300px">
      <el-carousel-item v-for="item in movies" :key="item">
        <el-image
          style="width: auto; height: 100%"
          :src="static_domain + 'posters/' + item.movieId + '.jpg'"
          lazy
        />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { MovieService } from "../api/api.ts";

const static_domain = import.meta.env.VITE_STATIC_DOMAIN;
const movies = ref([]);

onMounted(() => {
  hotms();
});

const hotms = async () => {
  const params = {
    size: 10,
  };
  const res = await MovieService.hotms(params);
  res.data.forEach((i) => {
    movies.value.push(i);
  });
};
</script>

<style lang="less">
.block {
  margin-bottom: 20px;
  span {
    font-size: 30px;
    font-weight: 900;
  }
}
.el-carousel__mask {
  background-color: rgba(233, 238, 243);
}
.el-carousel__item.is-active .el-carousel__mask {
  background-color: transparent;
}
</style>
