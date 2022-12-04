import { BaseHtmlTitle } from "../constants/ui";
import { getCustomConfig } from "../config";
const settings = getCustomConfig();

export const setHtmlTitle = (newTitle, absolute = false) => {
  document.title = absolute
    ? newTitle
    : (newTitle && `${newTitle} - ${settings.name} - ${settings.version}` || BaseHtmlTitle)
}
