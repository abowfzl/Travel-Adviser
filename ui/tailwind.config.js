/** @type {import('tailwindcss').Config} */

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  presets: [require("@neo4j-ndl/base").tailwindConfig],
  prefix: "",
  theme: {
    extend: {
      colors: {
        'dark-bg': '#1a202c',
        'dark-surface': '#2d3748',
        "dark-text": "#F3F4F6",
        'dark-border': '#4a5568',

        'light-bg': '#f7fafc',
        'light-surface': '#ffffff',
        "light-text": "#1F2937",
        'light-border': '#e2e8f0',

        'red-600': '#e53e3e',
        'red-400': '#fc8181',

        'yellow-600': '#d69e2e',
        'yellow-400': '#f6e05e',

        'green-500': '#48bb78',
        'green-600': '#38a169',

        'blue-300': '#63b3ed',
        "blue-100": "#DBEAFE",
        "blue-200": "#BFDBFE",
        "blue-300": "#93C5FD",
        "blue-400": "#60A5FA",
        "blue-500": "#3B82F6",
        "blue-600": "#2563EB",
        "blue-700": "#1D4ED8",
        "blue-800": "#1E40AF",
        "blue-900": "#1E3A8A",

        "gray-100": "#F3F4F6",
        "gray-200": "#E5E7EB",
        "gray-600": "#4B5563",
        "gray-700": "#374151",
        "gray-800": "#1F2937",
        "gray-900": "#111827",

        "white": "#FFFFFF"
      },
    },
  },
  darkMode: 'class',
  safelist: [
    {
      pattern:
        /^(hover:)?text-(light|primary|danger|warning|success|blueberry|mint|neutral)-/,
      variants: ["hover"],
    },
    {
      pattern:
        /^(hover:)?bg-(light|primary|danger|warning|success|blueberry|mint|neutral)-/,
      variants: ["hover"],
    },
    {
      pattern: /^(active:)?bg-light-/,
      variants: ["active"],
    },
    {
      pattern: /^(hover:)?border-light-/,
      variants: ["hover"],
    },
  ],
  plugins: [require("daisyui"), require('@tailwindcss/typography')],
};
