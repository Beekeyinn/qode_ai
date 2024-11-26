import { createBrowserRouter } from "react-router-dom";

import "./index.css";
import Home from "./Pages/Home";
import ErrorBoundary from "./PureComponents/error/ErrorBoundary";

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    errorElement: <ErrorBoundary />,
  },
]);
