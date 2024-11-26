import axios from "axios";
const BASE_URL = import.meta.env.VITE_BASE_API_URL;
import { toast } from "react-toastify";

axios.defaults.baseURL = BASE_URL;

const refreshToken = async () => {
  const keys = JSON.parse(localStorage.getItem("token"));

  const response = await fetch(`${BASE_URL}auth/token/refresh/`, {
    method: "post",
    body: JSON.stringify({ refresh: keys?.refresh }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (response.status == 200) {
    const data = await response.json();
    return data;
  } else {
    toast.error(
      "Token expired. Please login again. Redirecting to login page..."
    );
    setTimeout(() => {
      localStorage.clear();
      sessionStorage.clear();
      window.location.href = "/login";
    }, 2000);
    throw new Error("Token expired. Please login again.");
  }
};

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const value = JSON.parse(localStorage.getItem("token"));
    config.headers.Authentication = `Bearer ${value?.access}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    // You can modify the response data here, e.g., handling pagination
    return response;
  },
  async function (error) {
    const originalRequest = error.config;
    originalRequest.__retry = false;
    if (
      (error.response.status === 403 || error.response.status === 401) &&
      !originalRequest.__retry
    ) {
      originalRequest._retry = true;
      const token = await refreshToken();
      localStorage.setItem("token", JSON.stringify(token));
      axios.defaults.headers.common["Authentication"] =
        "Bearer " + token?.access;
      originalRequest.headers["Authentication"] = "Bearer " + token?.access;
      return axios(originalRequest);
    }
    return Promise.reject(error);
  }
);

export const interceptedAxios = axiosInstance;
export const uninterceptedAxios = axios;
