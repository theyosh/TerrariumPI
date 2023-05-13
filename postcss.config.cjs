const production = process.env.MIX_ENV === "prod";

module.exports = {
  plugins: [
    require("postcss-import"),
    require("autoprefixer"),
    production ? require("cssnano") : false
  ]
};