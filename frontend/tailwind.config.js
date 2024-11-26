/** @type {import('tailwindcss').Config} */
export default {
    content: ["./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
      extend: {
        colors: {
          black: {
            1: "#1E1E1E",
          },
          gray: {
            1000: "#F8F8F8",
            1500: "#EBEBEB",
            2000: "#D9D9D9",
            3000: "#6F6F6F",
            4000: "#4B4B4B",
            6000: "#898989",
            7000: "#535353",
          },
          green: {
            5000: "#628B5F",
          },
        },
        width: {
          400: "400px",
        },
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui"],
        serif: ["ui-serif", "Georgia"],
        mono: ["ui-monospace", "SFMono-Regular"],
        primary: ["Montserrat"],
        secondary: ["Josefin Sans"],
      },
    },
    plugins: [],
  };
  