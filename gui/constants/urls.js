import { removeAllTrailingChars } from '../helpers/string-helpers';

export const AppUrl = removeAllTrailingChars(process.env.APP_URL || window.location);
export const ApiUrl = removeAllTrailingChars(process.env.API_URL || AppUrl);

export const WebsocketUrl = `${ApiUrl}/live/`.replace(/http/gm, 'ws');

export const DataTablesLanguageUrl = 'https://cdn.datatables.net/plug-ins/1.13.7/i18n';
