export const updateLoading = (state, action) => {
  state.loading.state = action.payload.state;
  state.loading.message = action.payload.message;
  state.loading.type = action.payload.type;
};

export const updateToast = (state, action) => {
  state.toast.message = action.payload.message;
  state.toast.type = action.payload.type;
};
