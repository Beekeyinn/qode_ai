import { RouterProvider } from "react-router-dom";
import { routes } from "./Routes";
import ReduxProvider from "./Provider/ReduxProvider";
import { ToastContainer } from "react-toastify";
function App() {
  return (
    <ReduxProvider>
      <ToastContainer />
      <RouterProvider router={routes} />
    </ReduxProvider>
  );
}

export default App;
