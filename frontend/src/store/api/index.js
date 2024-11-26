/* eslint-disable no-undef */
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { getCsrfToken } from "../../utils"


export const allApi = createApi({
  reducerPath: "assistant",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.VITE_BASE_API_URL,
    credentials: "include",
    // eslint-disable-next-line no-unused-vars
    prepareHeaders: (headers, { getState }) => {
      const csrf = getCsrfToken();
      headers.set("X-CSRFToken", csrf);
      return headers;
    },
  }),
  tagTypes: ["assistants", "threads", "messages", "identity"],
  endpoints: () => ({}),
});

export default allApi;
