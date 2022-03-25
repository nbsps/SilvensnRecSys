import { request } from "./axios";

export class UserService {
  static async allus(params: {} | undefined) {
    return request("/getAllUsers", params, "get");
  }
  static async changeu(params: {} | undefined) {
    return request("/changeUid", params, "get");
  }
}

export class MovieService {
  static async countm(params: {} | undefined) {
    return request("/movieclick", params, "get");
  }
  static async minfo(params: {} | undefined) {
    return request("/getmovie", params, "get");
  }
  static async hotms(params: {} | undefined) {
    return request("/getHotMovies", params, "get");
  }
  static async genres(params: {} | undefined) {
    return request("/getAllGenres", params, "get");
  }
  static async getsim(params: {} | undefined) {
    return request("/getsimilarmovie", params, "get");
  }
  static async getrecforyou(params: {} | undefined) {
    return request("/getrecforyou", params, "get");
  }
  static async getRcMs(params: {} | undefined) {
    return request("/getRecommendMovie", params, "get");
  }
}
