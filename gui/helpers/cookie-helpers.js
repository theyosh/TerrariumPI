export const getCookie = (key) => {
  let cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.split(/=(.*)/s);
    if (cookie[0] === key) {
      return cookie[1].replace(/^"+/, '').replace(/"+$/, '');
    }
  }
};