import { createSlice } from "@reduxjs/toolkit";
import { updateLoading } from "../reducers/uiReducer";
import { updateToast } from "../reducers/uiReducer";
export const uiSlice = createSlice({
  name: "ui",
  initialState: {
    toast: {
      message: null,
      type: null,
    },
    loading: { state: false, message: "", type: "" },
  },
  reducers: {
    updateLoading,
    updateToast,
  },
});

export default uiSlice;
