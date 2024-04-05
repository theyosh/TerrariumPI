import { removeAllTrailingChars } from '../helpers/string-helpers';

export const AppUrl = removeAllTrailingChars(process.env.APP_URL || window.location);
export const ApiUrl = removeAllTrailingChars(process.env.API_URL || AppUrl);

export const WebsocketUrl = `${ApiUrl}/live/`.replace(/http/gm, 'ws');

// https://datatables.net/plug-ins/i18n/
export const DataTablesLanguageUrl = 'https://cdn.datatables.net/plug-ins/2.0.3/i18n';
