import './assets/css/main.scss';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import 'admin-lte/dist/js/adminlte';
import App from './App.svelte';
import Error from './Error.svelte';

import {  getCustomConfig} from './config';

let target = document.getElementById('app');

const app = new App({target});

/* jslint unparam: true */
window.addEventListener('error', (event) => {
  app.$destroy();
  target.innerHTML = '';
  window.location = '#/error';

  let config = getCustomConfig();

  new Error({
    target,
    props: {
      code: 502,
      message: 'Hello',
      email: config.ContactEmail
    }
  });

  window.dispatchEvent(new Event('resize'));
});
/* jslint unparam: false */

export default app;