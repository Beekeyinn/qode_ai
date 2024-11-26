import { configureStore } from "@reduxjs/toolkit";
import allApi from "./api";
import uiSlice from "./slice/uiSlice";


const store = configureStore({
  reducer: {
    [allApi.reducerPath]: allApi.reducer,
    ui: uiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(allApi.middleware),
});

export { store };
export const uiAction = uiSlice.actions;
