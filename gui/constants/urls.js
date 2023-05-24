import { removeAllTrailingChars } from "../helpers/string-helpers";

export const AppUrl = removeAllTrailingChars(process.env.APP_URL || window.location);
export const ApiUrl = removeAllTrailingChars(process.env.API_URL || AppUrl);

export const WebsocketUrl = `${ApiUrl}/live/`.replace(/http/gm, 'ws');