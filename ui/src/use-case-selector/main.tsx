import React from "react";
import { createRoot } from "react-dom/client";

import "@neo4j-ndl/base/lib/neo4j-ds-styles.css";
import "./index.css";

const container = document.getElementById("root");
const root = createRoot(container!);

root.render(
  <React.StrictMode>
    <div className="flex flex-col min-h-screen gap-8 max-w-3xl w-[80%] mx-auto mt-12 p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-5xl font-extrabold text-center text-blue-600">
        Explore Your Travel Destinations
      </h1>
      <p className="text-lg text-gray-700 leading-relaxed">
        Welcome to the Travel Adviser demo! Discover how to interact with a Knowledge Graph using natural language and build a Knowledge Graph from unstructured data. Dive into the innovative features that simplify your travel planning.
      </p>
      <p className="text-lg text-gray-700 leading-relaxed">
        Select an option below to explore the unique capabilities of our demo.
      </p>
      <div className="flex flex-col items-center w-full gap-4 mt-6">
        <a
          href="use-cases/chat-with-kg/index.html"
          className="bg-blue-500 text-white font-medium py-3 px-6 rounded-md shadow-md hover:bg-blue-600 transition duration-300 w-full max-w-xs text-center"
        >
          Chat with the K-G
        </a>
      </div>
    </div>
  </React.StrictMode>
);
