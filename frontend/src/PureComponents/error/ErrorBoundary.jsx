import { useRouteError } from "react-router-dom";


const ErrorBoundary = () => {
  const error = useRouteError();

  if (import.meta.env.MODE === "development") {
    console.error("Message: ", error.message);
    console.error("STACK", error.stack);
    return (
      <div className="grid h-full place-items-center">
        <div className="flex flex-col gap-6">
          <h1 className="font-extrabold font-primary text-6xl text-red-600 text-center">
            Something went wrong
          </h1>
          <h2 className="text-3xl font-semibold text-red-600">
            Message: {error.message}
          </h2>
          <div className="text-lg bg-slate-800 p-5 rounded-lg ">
            <pre className="whitespace-normal text-red-500 font-mono">
              {error.stack}
            </pre>
          </div>
        </div>
      </div>
    );
  } else {
    return (
      <div className="grid h-full place-items-center">
        <div className="flex flex-col gap-6 text-center">
          <h1 className="font-extrabold font-primary text-6xl">Oops !!</h1>
          <p>Sorry, an Unexpected error has occurred.</p>

          <p className="text-gray-300 font-semibold">Not Found</p>
        </div>
      </div>
    );
  }
};

export default ErrorBoundary;
