import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./App.jsx";
import HomePage from "./components/HomePage.jsx";
import NotFound from "./components/NotFound.jsx";
import Result from "./components/Result.jsx";
import Model from "./components/Model.jsx";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./i18n";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<HomePage />} />
          <Route path="model" element={<Model />} />
          <Route path="result/:videoId" element={<Result />} />
        </Route>
        <Route path="not-found" element={<NotFound />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme={document.querySelector("html").getAttribute("data-bs-theme")}
      />
    </BrowserRouter>
  </React.StrictMode>
);
