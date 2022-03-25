<template>
  <el-row>
    <el-col
      v-for="(m, index) in movies"
      :key="index"
      :span="4"
      :offset="index % 5 == 0 ? 0 : 1"
      :xs="{ span: 7, offset: index % 3 == 0 ? 0 : 1 }"
    >
      <Movie :movie="m" />
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { MovieService } from "@/api/api.ts";
import Movie from "../basic/Movie.vue";

const movies = ref([]);

const props = defineProps({
  cls: {
    type: String,
    default: "Adventure",
  },
  id: {
    type: Number,
    default: 13,
  },
  typ: {
    type: String,
    default: "genre", // genre similar foryou
  },
});

onMounted(() => {
  getRcMs();
});

const getRcMs = async () => {
  let params;
  let res;
  switch (props.typ) {
    case "genre":
      params = {
        genre: props.cls,
        size: 32,
        sortby: "rating",
      };
      res = await MovieService.getRcMs(params);
      res.data.forEach((i) => {
        movies.value.push(i);
      });
      break;
    case "similar":
      console.log(props.id);
      params = {
        movieId: props.id,
        size: 32,
        model: "emb",
      };
      res = await MovieService.getsim(params);
      res.data.forEach((i) => {
        movies.value.push(i);
      });
      break;
    case "foryou":
      params = {
        id: props.id,
        size: 32,
        model: "emb",
      };
      res = await MovieService.getrecforyou(params);
      res.data.forEach((i) => {
        movies.value.push(i);
      });
      break;
  }
};
</script>

<style></style>
