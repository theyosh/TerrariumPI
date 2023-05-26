import { init, getLocaleFromNavigator, locale, addMessages } from 'svelte-i18n';
import { writable } from "svelte/store";

import { getCustomConfig } from "../config";

import de from './de.json';
import de_AT from './de_AT.json';
import ca from './ca.json';
import en_GB from './en_GB.json';
import en_US from './en_US.json';
import es from './es.json';
import es_AR from './es_AR.json';
import fr_BE from './fr_BE.json';
import it_IT from './it_IT.json';
import ja from './ja.json';
import nb_NO from './nb_NO.json';
import nl_NL from './nl_NL.json';
import pl from './pl.json';
import pt_BR from './pt_BR.json';

let settings = getCustomConfig();

const locales = {
  'de': de,
  'de-AT': de_AT,
  'ca': ca,
  'en-GB': en_GB,
  'en-US': en_US,
  'es': es,
  'es-AR': es_AR,
  'fr-BE': fr_BE,
  'it-IT': it_IT,
  'ja': ja,
  'nb-NO': nb_NO,
  'nl-NL': nl_NL,
  'pl': pl,
  'pt-BR': pt_BR
};

const langs = [
  {
    "code": "de",
    "title": "Deutsch",
    'currency': ['eur']
  },
  {
    "code": "de-AT",
    "title": "Deutsch (AT)",
    'currency': ['eur']
  },
  {
    "code": "ca",
    "title": "Català (ES)",
    'currency': ['eur']
  },
  {
    "code": "en-GB",
    "title": "English (GB)",
    'currency': ['gbp']
  },
  {
    "code": "en-US",
    "title": "English (US)",
    'currency': ['usd']
  },
  {
    "code": "es",
    "title": "Español",
    'currency': ['eur']
  },
  {
    "code": "es-AR",
    "title": "Español (AR)",
    'currency': ['ars']
  },
  {
    "code": "fr-BE",
    "title": "Français (BE)",
    'currency': ['eur']
  },
  {
    "code": "it-IT",
    "title": "Italiano",
    'currency': ['eur']
  },
  {
    "code": "ja",
    "title": "日本語",
    'currency': ['jpy']
  },
  {
    "code": "nb-NO",
    "title": "Norsk Bokmål",
    'currency': ['nok']
  },
  {
    "code": "nl-NL",
    "title": "Nederlands (NL)",
    'currency': ['eur']
  },
  {
    "code": "pl",
    "title": "Polski",
    'currency': ['pln']
  },
  {
    "code": "pt-BR",
    "title": "Português (BR)",
    'currency': ['eur', 'brl']
  }
];

export { locale, locales, langs };
export const languages = langs;
export const currencies = [...new Set([...[].concat(...langs.map(language => language.currency))])];
export const currency = writable(settings.currency);

export const saveLanguageFile = (json, lang) => {
  addMessages(lang, json);
  localStorage.setItem(lang + '-locale', JSON.stringify(json));
};

export const deleteSaveLocals = () => {
  let keys, i;
  keys = Object.keys(localStorage);
  i = keys.length;

  while (i--) {
    if (keys[i].substring(3) === 'locale') {
      localStorage.removeItem(keys[i]);
    }
  }
  location.reload();
};

export const changeLang = (lang) => {
  if (languages.find((x) => x.code === lang)) {
    locale.set(lang);
  }
};

const initialize = () => {
  langs.forEach((lang) => {
    let lc = localStorage.getItem(lang.code + '-locale');
    if (lc !== null) {
      addMessages(lang.code, { ...JSON.parse(lc), ...{ units: settings.units } });
      locales[lang.code] = { ...JSON.parse(lc), ...{ units: settings.units } };
    } else {
      addMessages(lang.code, { ...locales[lang.code], ...{ units: settings.units } });
    }
  });

  init({
    fallbackLocale: 'en-GB',
    initialLocale: settings.language || localStorage.getItem('language') || getLocaleFromNavigator()
  });
  changeLang(settings.language);
};

initialize();