import axios from "axios";
import { showMessage } from "./status";
import { ElMessage } from "element-plus";

axios.defaults.timeout = 60000;

// @ts-ignore
axios.defaults.baseURL = import.meta.env.VITE_API_DOMAIN;
// axios.defaults.baseURL = "http://127.0.0.1:5000";

axios.interceptors.request.use(
  (config) => {
    config.headers = {
      "Content-Type": "application/json;charset=UTF-8",
    };
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const { response } = error;
    if (response) {
      showMessage(response.status);
      return Promise.reject(response.data);
    } else {
      ElMessage.warning("网络异常,请稍后再试!");
    }
  }
);

export function request(url = "", params = {}, type = "POST") {
  return new Promise((resolve, reject) => {
    let promise;
    if (type.toUpperCase() === "GET") {
      promise = axios({
        url,
        params,
      });
    } else if (type.toUpperCase() === "POST") {
      promise = axios({
        method: "POST",
        url,
        data: params,
      });
    }
    promise
      ?.then((res) => {
        resolve(res);
      })
      .catch((err) => {
        reject(err);
      });
  });
}
