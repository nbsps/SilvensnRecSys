<template>
  <el-container>
    <el-header>
      <a href=".">
        <el-image
          style="height: 59px"
          src="silvensnrecsys.png"
          fit="contain"
        ></el-image>
      </a>
      <el-select
        v-model="value"
        filterable
        default-first-option
        placeholder="CHOOSE YOUR UID"
        @change="userchange"
      >
        <el-option
          v-for="item in users"
          :key="item.userId"
          :label="'USER' + item.userId"
          :value="item.userId"
        ></el-option>
      </el-select>
    </el-header>
    <el-main>
      <hot-rec />
      <main-rec :userId="userId" />
    </el-main>
    <el-footer>
      @{{ date }}-{{ date + 1 }} By
      <el-link href="https://github.com/nbsps"> Silvensn </el-link>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { UserService } from "@/api/api.ts";
import MainRec from "./MainRec.vue";
import HotRec from "./HotRec.vue";

let userId = ref(1);
let users = ref([]);
const value = ref("");
const date = new Date().getFullYear();

onMounted(() => {
  getAllUsers();
});

const getAllUsers = async () => {
  const params = {};
  const res = await UserService.allus(params);
  res.data.forEach((i) => {
    users.value.push(i);
  });
};

const userchange = (val) => {
  userId.value = val;
  UserService.changeu({ uid: val });
};
</script>

<style lang="less">
#app > .el-container {
  min-height: 100%;
}

.el-header {
  a {
    text-decoration: none;
    font-size: 40px;
    font-weight: 900;
    float: left;
    background: transparent;
  }
  .el-select {
    position: absolute;
    top: 50%;
    right: 2vw;
    transform: translateY(-50%);
    margin: auto;
  }
  color: var(--el-text-color-primary);
  height: 60px;
  width: 100%;
  position: fixed;
  top: 0;
  z-index: 999;
  background-color: #ffffff;
  border-bottom: 1px solid #ddd;
}

.el-footer {
  height: 120px;
  width: 100%;
  background-color: #b3c0d1;
  line-height: 120px;
  font-size: 20px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  .el-link {
    font: inherit;
  }
}

.el-main {
  background-color: #e9eef3;
  color: var(--el-text-color-primary);
  padding: 10px;
  margin-top: 60px;
  padding-bottom: 20px;
  height: 100%;
}
</style>
