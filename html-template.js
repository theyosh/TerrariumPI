import {
  readFile
} from "fs/promises"
import path from "path"
import {
  makeHtmlAttributes
} from "@rollup/plugin-html"

function withPublicPathPrefix(publicPath, fileName) {
  return path.posix.join(publicPath, fileName)
}

function toScriptTags(js, publicPath, attributes) {
  return js
    .map(({
      fileName
    }) => {
      const attrs = makeHtmlAttributes(attributes.script)
      return `<script defer src="${withPublicPathPrefix(publicPath, fileName)}"${attrs}></script>`
    })
    .join("\n")
}

function toLinkTags(css, publicPath, attributes) {
  return css
    .map(({
      fileName
    }) => {
      const attrs = makeHtmlAttributes(attributes.link)
      return `<link href="${withPublicPathPrefix(publicPath, fileName)}" rel="stylesheet"${attrs}>`
    })
    .join("\n")
}

function toMetaTags(meta) {
  return meta
    .map(input => {
      const attrs = makeHtmlAttributes(input)
      return `<meta${attrs}>`
    })
    .join("\n")
}

export default async function(data) {
  const {
    attributes,
    files,
    meta,
    publicPath
  } = data

  const scripts = toScriptTags(files.js || [], publicPath, attributes)
  const links = toLinkTags(files.css || [], publicPath, attributes)
  const metas = toMetaTags(meta)

  const indexFileHtml = await readFile("./gui/assets/index.template.html", "utf8")

  return indexFileHtml
    .replace("__HTML_ATTRS__", makeHtmlAttributes(attributes.html))
    .replace("<!-- __METAS__ -->", metas)
    .replace("<!-- __LINKS__ -->", links)
    .replace("<!-- __SCRIPTS__ -->", scripts)
}