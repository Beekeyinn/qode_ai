import PropTypes from "prop-types";

const ErrorPage = ({ message = "Page Not Found", status }) => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center p-6 bg-white shadow-md rounded-lg">
        <div className="text-6xl">⚠️</div>
        <h1 className="text-6xl font-bold text-red-600 mt-4">{status}</h1>
        <h2 className="text-2xl font-semibold text-gray-800 mt-4">{message}</h2>

        <a
          href="/"
          className="inline-block mt-6 px-6 py-3 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition-colors"
        >
          Go Back Home ➡️
        </a>
      </div>
    </div>
  );
};

ErrorPage.propTypes = {
  message: PropTypes.string,
  status: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
};

export default ErrorPage;
