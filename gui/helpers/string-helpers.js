import { countryCodeEmoji } from 'country-code-emoji';

const _getRandomCharCode = () => {
  return 65 + Math.round(Math.random() * 25);
};

export const getRandomString = (length) => {
  let randomNumbers = [];

  for (let i = 0; i < length; i++) randomNumbers.push(_getRandomCharCode());

  return String.fromCharCode(...randomNumbers);
};

export const capitalize = ([first, ...rest]) => {
  return first.toLocaleUpperCase() + rest.join('');
};

export const removeDiacritics = (str) => {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
};

export const capitalizeFirstLetter = (string) => {
  return string[0].toUpperCase() + string.slice(1);
};

// https://stackoverflow.com/a/6680877
export const removeAllTrailingChars = (str, char = '/') => {
  let i = str.length;
  /*eslint no-empty: "error"*/
  while (str[--i] === char) {
    /* empty */
  }
  return str.slice(0, i + 1);
};

// https://stackoverflow.com/a/12042044
export const externalLinks = (content) => {
  let container = document.createElement('div');
  container.innerHTML = content;
  for (let links = container.getElementsByTagName('a'), i = 0, a; (a = links[i]); i++) {
    if (a.host !== location.host) {
      a.target = '_blank';
    }
  }
  return container.innerHTML;
};

export const nl2br = (text) => {
  return text.replace(/\n/g, '<br />');
};

export const languageFlag = (language) => {
  let flag = language.slice(-2);

  switch (flag) {
    case 'ja':
      flag = 'jp';
      break;
    case 'ca':
      flag = 'es';
      break;
  }
  return countryCodeEmoji(flag);
};

export const enclosureNameSort = (a, b) => {
  const startWithNumber = /^\d+/;

  let numberA = a.match(startWithNumber);
  let numberB = b.match(startWithNumber);

  if (numberA && numberB) {
    // Sorting based on integers
    numberA = 1 * numberA[0];
    numberB = 1 * numberB[0];

    if (numberA > numberB) {
      return 1;
    } else if (numberA < numberB) {
      return -1;
    } else {
      return 0;
    }
  }

  // Normal text compare
  return a.localeCompare(b);
};

export const areaObjectSort = (a, b) => {
  // Main lights area always first
  if (a.type === 'lights' && a.setup.main_lights) {
    return -1;
  } else if (b.type === 'lights' && a.setup.main_lights) {
    return 1;
  }

  // Normal text compare
  return enclosureNameSort(a.name, b.name);
};
