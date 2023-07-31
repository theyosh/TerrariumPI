import svelte from "rollup-plugin-svelte";
import commonjs from "@rollup/plugin-commonjs";
import resolve from "@rollup/plugin-node-resolve";
import replace from "@rollup/plugin-replace";
import html from "@rollup/plugin-html";
import postcss from "rollup-plugin-postcss";
import copy from "rollup-plugin-copy";
import livereload from "rollup-plugin-livereload";
import sveltePreprocess from "svelte-preprocess";
import gzipPlugin from 'rollup-plugin-gzip';
import json from "@rollup/plugin-json";
import esbuild from "rollup-plugin-esbuild";
import del from "rollup-plugin-delete";
import template from "./html-template.js";
import { spawn } from "child_process";

const production = process.env.NODE_ENV === "prod";

function serve() {
  let server;

  function toExit() {
    if (server) server.kill(0);
  }

  return {
    writeBundle() {
      if (server) return;
      server = spawn("npm", ["run", "start"], {
        stdio: ["ignore", "inherit", "inherit"],
        shell: true
      });

      process.on("SIGTERM", toExit);
      process.on("exit", toExit);
    }
  };
}

export default {
  input: "gui/main.js",
  output: {
    sourcemap: !production,
    format: "iife",
    name: "app",
    dir: "public",
    inlineDynamicImports: true
  },
  plugins: [
    production && del({
      targets: 'public/*',
    }),
    replace({
      preventAssignment: true,
      values: {
        "process.env.APP_URL": "window.location.origin",
        "process.env.API_URL": JSON.stringify(process.env.API_URL),
        "process.env.BASE_HTML_TITLE": JSON.stringify(process.env.BASE_HTML_TITLE),
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'dev'),
        'process.env.MIX_ENV': JSON.stringify(process.env.MIX_ENV || 'dev')
      }
    }),
    json(),
    svelte({
      emitCss: true,
      compilerOptions: {
        // enable run-time checks when not in production
        dev: !production
      },
      preprocess: sveltePreprocess(),
      onwarn() { }
    }),
    postcss({
      extract: true
    }),

    resolve({
      browser: true,
      dedupe: ["svelte"]
    }),

    commonjs(),

    esbuild({
      minify: production,
      target: "es2016"
    }),
    html({
      title: process.env.BASE_HTML_TITLE,
      template
    }),

    // copy files that are not frequently modified (for other assets create separate copy plugin)
    copy({
      copyOnce: true,
      verbose: true,
      targets: [{
        src: "node_modules/jquery/dist/jquery.min.js",
        dest: "./public/js",
        rename: "jquery.min.js"
      },
      {
        src: "node_modules/admin-lte/plugins/jquery-knob/jquery.knob.min.js",
        dest: "./public/js",
        rename: 'jquery.knob.min.js'
      },

      {
        src: "node_modules/fullcalendar/main.min.js",
        dest: "./public/js",
        rename: 'fullcalendar.min.js'
      },
      {
        src: "node_modules/fullcalendar/locales-all.min.js",
        dest: "./public/js",
        rename: "fullcalendar-locales.min.js"
      },

      {
        src: "node_modules/admin-lte/plugins/select2/js/select2.min.js",
        dest: "./public/js",
        rename: 'select2.min.js'
      },

      {
        src: "node_modules/admin-lte/plugins/datatables/jquery.dataTables.min.js",
        dest: "./public/js",
        rename: 'jquery.dataTables.min.js'
      },
      {
        src: "node_modules/admin-lte/plugins/datatables-bs4/js/dataTables.bootstrap4.min.js",
        dest: "./public/js",
        rename: 'dataTables.bootstrap4.min.js'
      },
      {
        src: "node_modules/admin-lte/plugins/datatables-responsive/js/dataTables.responsive.min.js",
        dest: "./public/js",
        rename: 'dataTables.responsive.min.js'
      },
      {
        src: "node_modules/admin-lte/plugins/datatables-responsive/js/responsive.bootstrap4.min.js",
        dest: "./public/js",
        rename: 'responsive.bootstrap4.min.js'
      },

      {
        src: "node_modules/swagger-ui-dist/swagger-ui-bundle.js",
        dest: "./public/js",
        rename: "swagger-ui-bundle.js"
      },
      {
        src: "node_modules/swagger-ui-dist/swagger-ui-standalone-preset.js",
        dest: "./public/js",
        rename: "swagger-ui-standalone-preset.js"
      },
      {
        src: "node_modules/swagger-ui-dist/swagger-ui.css",
        dest: "./public/css",
        rename: "swagger-ui.css"
      },

      {
        src: "node_modules/trumbowyg/dist/ui/icons.svg",
        dest: "./public/css",
        rename: 'icons.svg'
      },
      {
        src: "node_modules/@fortawesome/fontawesome-free/webfonts",
        dest: "./public"
      },

      {
        src: "gui/assets/static/*",
        dest: "./public"
      },
      ]
    }),
    production && gzipPlugin({
      additionalFiles: [
        'public/js/jquery.min.js',
        'public/js/jquery.knob.min.js',
        'public/js/fullcalendar.min.js',
        'public/js/fullcalendar-locales.min.js',
        'public/js/jquery.dataTables.min.js',
        'public/js/dataTables.bootstrap4.min.js',
        'public/js/dataTables.responsive.min.js',
        'public/js/responsive.bootstrap4.min.js',
        'public/js/select2.min.js',

        'public/js/fireworks.js',
        'public/js/swagger-ui-bundle.js',
        'public/js/swagger-ui-standalone-preset.js',
        'public/js/redoc.standalone.js',

        'public/css/swagger-ui.css',

        'public/api/redoc.html',
        'public/api/swagger.html',
        'public/api/terrariumpi.json',
        'public/api/terrariumpi.yaml'
      ]
    }),

    production && del({
      // We do not want an index.html.gz file as that will not work with Python variables to fill by the webserver
      targets: 'public/index.html.gz',
      verbose: true,
      hook: 'closeBundle'
    }),
    !production && serve(),

    // Watch the `public` directory and refresh the
    // browser on changes when not in production
    !production && livereload("public")
  ],
  watch: {
    clearScreen: true
  }
}
