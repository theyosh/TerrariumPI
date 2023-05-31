import { getCustomConfig } from '../config';
import { de } from '@fancyapps/ui/dist/fancybox/l10n/de.esm.js';
import { en } from '@fancyapps/ui/dist/fancybox/l10n/en.esm.js';
import { en as es } from '@fancyapps/ui/dist/fancybox/l10n/es.esm.js';
import { fr } from '@fancyapps/ui/dist/fancybox/l10n/fr.esm.js';
import { it } from '@fancyapps/ui/dist/fancybox/l10n/it.esm.js';
import { js as ja } from '@fancyapps/ui/dist/fancybox/l10n/ja.esm.js';
import { pl } from '@fancyapps/ui/dist/fancybox/l10n/pl.esm.js';

export const TypingDebounceDelay = 300;

// these constants are used for rendering loading notifications
// do not show loader if response arrives before `waitForLoader` time
// and do not hide loader, if the response arrives after `waitForLoader` and before `leaveLoaderFor`
export const waitForLoader = 45;
export const leaveLoaderFor = 234;

export const BaseHtmlTitle = process.env.BASE_HTML_TITLE;

export const fancyAppsLanguage = () => {
    let language = getCustomConfig().language.substring(0,2);
    switch(language) {
        case 'de':
          language = de;
          break;
        case 'en':
          language = en;
          break;
        case 'es':
          language = es;
          break;
        case 'fr':
          language = fr;
          break;
        case 'it':
          language = it;
          break;
        case 'ja':
          language = ja;
          break;
        case 'pl':
          language = pl;
          break;
        default:
          language = en;
      }

    return language;
}