import axios from "axios";

axios.defaults.baseURL = import.meta.env.VITE_API_URL;
axios.defaults.timeout = 180000;

const postAnalyze = (videoId) => {
  return axios.post(`/analyze?videoId=${videoId}`);
};

const getResult = (videoId, page, sortBy = "like") => {
  return axios.get(
    `/result?videoId=${videoId}&page=${page}&limit=10&sortBy=${sortBy}`
  );
};

export { postAnalyze, getResult };
