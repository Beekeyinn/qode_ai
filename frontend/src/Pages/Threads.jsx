import { Fragment } from "react";
import { Outlet } from "react-router-dom";

// ? Just a Container for the page dont add any logic or api calls here
const Threads = () => {
  return (
    <Fragment>
      <div>Here is the List of Threads for the Assistants</div>
      <div>
        <Outlet />
      </div>
    </Fragment>
  );
};

export default Threads;
