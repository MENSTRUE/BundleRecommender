import React from "react";
import { createRoot } from "react-dom/client";
import Workspace from "./pages/Workspace";
import "./styles/main.css";

const container = document.getElementById("root");
if (!container) throw new Error("Missing #root element");

createRoot(container).render(
  <React.StrictMode>
    <Workspace />
  </React.StrictMode>
);
