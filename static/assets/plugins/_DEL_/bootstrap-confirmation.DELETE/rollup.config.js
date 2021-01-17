import babel from 'rollup-plugin-babel';
import replace from 'rollup-plugin-replace';

const pkg = require('./package.json');

export default {
  output  : {
    format   : 'umd',
    name     : 'bootstrap-confirmation',
    sourcemap: true,
    exports  : 'none',
    globals  : {
      'jquery': 'jQuery'
    },
    banner   : `/*!
 * Bootstrap Confirmation (v${pkg.version})
 * @copyright 2013 Nimit Suwannagate <ethaizone@hotmail.com>
 * @copyright 2014-2018 Damien "Mistic" Sorel <contact@git.strangeplanet.fr>
 * @licence Apache License, Version 2.0
 */`
  },
  external: [
    'jquery',
    'bootstrap'
  ],
  plugins : [
    replace({
      delimiters: ['', ''],

      '$VERSION'                                         : pkg.version,
      'import Popover from \'bootstrap/js/src/popover\';': 'import Popover from \'./popover\';',
      'export default Confirmation;'                     : ''
    }),
    babel({
      exclude: 'node_modules/**'
    })
  ]
};
