/* Build date: 07/11/11 14:11:45 */
/*
  Copyright (c) 2011, Mark Watkinson <markwatkinson@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Mark Watkinson BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



passStrengthify - a password strength notification plugin for jQuery
Usage:
  <input type='password' id='pass'>
  ...
  $('#pass').passStrengthify( [options] );
  

Options:
  { 
    security: int [0, 3) (default: 1)
    output:  $element,
    rawEntropy: bool,  // show raw entropy instead of a text description
    minimum:  int >= 0,
    levels: Array, (str - Text descriptions)
    colours: Array (str - CSS colours),
    tests: Array (regex)

    
    labels: { // text for labels
      passwordStrength : 'Password Strength:',
      tooShort: 'Too short'
    }
  }
  
  The levels/colours/tests arrays are as follows:
    levels - a list of descriptions where each index corresponds to the 
              number of tests passed
    colours - a list of colours which correspond to the number of tests passed
    tests - a list of regex tests to perform (match == pass)
    If any of these are given, the size of levels and colours must be equal and
    it must be one greater than the size of 'tests'. The default size of tests
    is 8. The first colour is used as the default background colour.
    
*/

(function($){  
  $.fn.passStrengthify = function(options) {
    var $el = $(this),
        $out_el,        
        // Test boundary presets, corresponds to the security option.
        // These steps aren't supposed to be linear.        
        presets = [
          [0, 8, 16, 32, 48, 64, 72],
          [0, 16, 32, 48, 64, 78, 92],
          [0, 32, 64, 78, 92, 108, 128]
        ],
        // These next two should be the same size ...
        levels = ['Very weak', 'Very weak', 'Weak', 'Weak', 'Moderate', 
          'Good', 'Strong', 'Very strong'],
        colours = ['gray', 'red', 'red', '#C00000', 'orange', 
          '#0099FF', 'blue', 'green'],
        // and this one should be one fewer.
        // see presets.
        tests = presets[0],
        text = $('<span>').css('margin-left', '1em'),
        progress_blocks = [],
        i = 0,
        minimum=0,
        rawEntropy = false,
        // Creates the output for a given score.
        makeOutput = function(score, entropy, tooshort) {
          var max = progress_blocks.length,
                    progress_colour,
                    default_colour,
                    text_colour,
                    text_;
          if (tooshort)
            text_ = options.labels.tooShort;
          else if(rawEntropy)
            text_ = Math.round(entropy*100)/100 + ' bits';
          else 
            text_ = levels[score];
          
          text_colour = colours[score];     
          progress_colour = colours[score];   
          default_colour = colours[0];
          text.text(text_).css('color', text_colour);
          
          for (i=0; i<max; i++)
            progress_blocks[i].css('background-color',
              (i<score)? progress_colour : default_colour);
        },
        regexTest = function(regex, password) {
          return password.search(regex) != -1;
        },
        
        charEntropy = function(password, index, alphabet_size) {
          var char_ = password.charAt(index);
          // Basic A-Z freq distribution.          
          var chars = [
            0.080642499002080981, 0.015373768624831691, 0.026892340312538593, 
            0.043286671390026357, 0.12886234260657689, 0.024484713711692099, 
            0.019625534749730816, 0.060987267963718068, 0.06905550211598431, 
            0.0011176940633901926, 0.0062521823678781188, 0.041016761327711163, 
            0.025009719347800208, 0.069849754102356679, 0.073783151266212627, 
            0.017031440203182008, 0.0010648594165322703, 0.06156572691936394, 
            0.063817324270355996, 0.090246649949305979, 0.027856851020401599, 
            0.010257964235274787, 0.021192261444145363, 0.0016941732664605912, 
            0.01806326249861108, 0.0009695838238376564
          ];
          // Basic A-Z freq distribution of first letters.
          var first_letter = [
            0.11617102232902775, 0.047081205567237411, 
            0.035155702413137084, 0.02673475518173626, 0.020026033843997197,
            0.037839190948232702, 0.019525382997897269, 0.072414138379893869, 
            0.062941824371683192, 0.0063182136777811164, 0.0069089816761790327,
            0.027085210774006212, 0.043796936016821872, 0.023680785020526691,
            0.062721537999399224, 0.025483128066486435, 0.00043055972764593971,
            0.016551516972063685, 0.077650946230099133, 0.16692700510663863,
            0.014889356163011918, 0.0061980574747171327, 0.066696705717432664,
            5.0065084609992999e-05, 0.01622108741363773, 0.00050065084609992997            
          ];
          // digrams as a 26*26 array with s[i-1] vertically and s[i]           
          // horizontally, each letter in [0,26)
          var digrams = [0.0002835, 0.0228302, 0.0369041, 0.0426290, 0.0012216,
            0.0075739, 0.0171385, 0.0014659, 0.0372661, 0.0002353, 0.0110124, 
            0.0778259, 0.0260757, 0.2145354, 0.0005459, 0.0195213, 0.0001749, 
            0.1104770, 0.0934290, 0.1317960, 0.0098029, 0.0306574, 0.0088799, 
            0.0009562, 0.0233701, 0.0018701, 0.0580027, 0.0058699, 0.0000791, 
            0.0022625, 0.3416714, 0.0002057, 0.0004272, 0.0003639, 0.0479084,
            0.0076894, 0.0000000, 0.1150560, 0.0012816, 0.0003481, 0.0966553, 
            0.0000158, 0.0000000, 0.0740301, 0.0226884, 0.0107430, 0.1196127, 
            0.0011550, 0.0000316, 0.0000000, 0.0864502, 0.0000000, 0.1229841, 
            0.0000271, 0.0215451, 0.0005246, 0.1715916, 0.0000090, 0.0000000, 
            0.1701716, 0.0565490, 0.0000000, 0.0453966, 0.0488879, 0.0000000, 
            0.0000362, 0.1759242, 0.0000090, 0.0017185, 0.0376812, 0.0010492, 
            0.0906756, 0.0358361, 0.0000000, 0.0000000, 0.0000000, 0.0041969,
            0.0000090, 0.0280345, 0.0005057, 0.0002585, 0.0081086, 0.1224833, 
            0.0006799, 0.0054844, 0.0007080, 0.0794902, 0.0003484, 0.0001911, 
            0.0092662, 0.0021466, 0.0030456, 0.0397283, 0.0001630, 0.0000225, 
            0.0178918, 0.0307037, 0.0009159, 0.0178805, 0.0027759, 0.0013655, 
            0.0000000, 0.0076478, 0.0000000, 0.0545873, 0.0012798, 0.0224322, 
            0.0843434, 0.0317097, 0.0085640, 0.0052834, 0.0017762, 0.0127186, 
            0.0002605, 0.0010967, 0.0339975, 0.0186268, 0.0815271, 0.0032334, 
            0.0101307, 0.0021424, 0.1307517, 0.0712793, 0.0241537, 0.0014289, 
            0.0157312, 0.0070879, 0.0105139, 0.0125997, 0.0001831, 0.0638579, 
            0.0002384, 0.0003179, 0.0002086, 0.0928264, 0.0500293, 0.0000199, 
            0.0000993, 0.0820576, 0.0000000, 0.0000199, 0.0266638, 0.0000397, 
            0.0000894, 0.1545186, 0.0001689, 0.0000099, 0.0825344, 0.0039539, 
            0.0341940, 0.0334986, 0.0000099, 0.0001987, 0.0000000, 0.0015200, 
            0.0000000, 0.0592435, 0.0003842, 0.0005205, 0.0020078, 0.1482326, 
            0.0002727, 0.0101631, 0.1420108, 0.0501091, 0.0000248, 0.0000372, 
            0.0395122, 0.0029870, 0.0127906, 0.0573224, 0.0005577, 0.0000000, 
            0.0884686, 0.0261142, 0.0062466, 0.0256309, 0.0000372, 0.0003470, 
            0.0000000, 0.0032720, 0.0001363, 0.1580232, 0.0007737, 0.0020460, 
            0.0005185, 0.4597035, 0.0004627, 0.0000359, 0.0000718, 0.1252667, 
            0.0000000, 0.0000040, 0.0014278, 0.0013042, 0.0012922, 0.0700557, 
            0.0000439, 0.0003191, 0.0117178, 0.0022056, 0.0297253, 0.0131497, 
            0.0000000, 0.0010290, 0.0000000, 0.0072309, 0.0000000, 0.0166996, 
            0.0069144, 0.0486793, 0.0363474, 0.0480664, 0.0271435, 0.0307856, 
            0.0000775, 0.0004826, 0.0000035, 0.0073125, 0.0526842, 0.0412929, 
            0.2618995, 0.0497818, 0.0062698, 0.0004333, 0.0437620, 0.1157982, 
            0.1198384, 0.0007010, 0.0235788, 0.0000211, 0.0018810, 0.0000000, 
            0.0032265, 0.2106638, 0.0000000, 0.0000000, 0.0000000, 0.1906420, 
            0.0000000, 0.0000000, 0.0000000, 0.0004353, 0.0000000, 0.0000000, 
            0.0000000, 0.0000000, 0.0000000, 0.2644178, 0.0000000, 0.0000000, 
            0.0000000, 0.0000000, 0.0000000, 0.3299238, 0.0000000, 0.0000000, 
            0.0000000, 0.0002176, 0.0000000, 0.0169234, 0.0011671, 0.0005058, 
            0.0017118, 0.3321662, 0.0041628, 0.0004669, 0.0007781, 0.1300965, 
            0.0000000, 0.0003112, 0.0185963, 0.0009726, 0.1009570, 0.0113601, 
            0.0012060, 0.0000000, 0.0004279, 0.0613523, 0.0022954, 0.0029956, 
            0.0000000, 0.0041239, 0.0000000, 0.0086757, 0.0000000, 0.1016800, 
            0.0005515, 0.0020459, 0.0668636, 0.1657445, 0.0134024, 0.0011801, 
            0.0001542, 0.1107889, 0.0000119, 0.0053728, 0.1355180, 0.0055389, 
            0.0009726, 0.0826499, 0.0022654, 0.0000059, 0.0018443, 0.0230153, 
            0.0180635, 0.0144461, 0.0041630, 0.0025797, 0.0000000, 0.0968765, 
            0.0000237, 0.1539307, 0.0285939, 0.0001653, 0.0025384, 0.2496134, 
            0.0017798, 0.0000195, 0.0003015, 0.0877464, 0.0000195, 0.0000000, 
            0.0015756, 0.0221846, 0.0029567, 0.1098532, 0.0485124, 0.0000000, 
            0.0169910, 0.0249954, 0.0008461, 0.0385435, 0.0000292, 0.0001167, 
            0.0000000, 0.0505257, 0.0000000, 0.0240107, 0.0005432, 0.0423173, 
            0.1767352, 0.0849166, 0.0053036, 0.1188694, 0.0028799, 0.0295789, 
            0.0012223, 0.0071353, 0.0087755, 0.0006582, 0.0085073, 0.0653564, 
            0.0003343, 0.0009716, 0.0004144, 0.0427003, 0.0956004, 0.0093814, 
            0.0033500, 0.0008497, 0.0003343, 0.0121150, 0.0001288, 0.0083175, 
            0.0072923, 0.0127087, 0.0203076, 0.0029439, 0.1135873, 0.0060659, 
            0.0018527, 0.0087857, 0.0001978, 0.0106912, 0.0268647, 0.0580447, 
            0.1459838, 0.0330625, 0.0138659, 0.0002308, 0.1175433, 0.0322680, 
            0.0492657, 0.1337201, 0.0164801, 0.0488371, 0.0005374, 0.0033923, 
            0.0008571, 0.1284508, 0.0004427, 0.0004427, 0.0004713, 0.2213542, 
            0.0001428, 0.0000857, 0.0221226, 0.0538854, 0.0000286, 0.0001143, 
            0.0957597, 0.0010854, 0.0005856, 0.1212242, 0.0607692, 0.0000000, 
            0.1362487, 0.0222939, 0.0408603, 0.0270926, 0.0000000, 0.0011711, 
            0.0000000, 0.0042274, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 
            0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 
            0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 
            0.0000000, 0.0000000, 0.0002284, 0.0002284, 0.0000000, 0.9949749, 
            0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0733524, 
            0.0032081, 0.0116789, 0.0284070, 0.2345530, 0.0056616, 0.0107385, 
            0.0026432, 0.0792432, 0.0000435, 0.0087196, 0.0117263, 0.0192448, 
            0.0221961, 0.0919374, 0.0048043, 0.0000316, 0.0189406, 0.0459213, 
            0.0421561, 0.0173721, 0.0070603, 0.0019873, 0.0000040, 0.0284504, 
            0.0055945, 0.0349781, 0.0006441, 0.0157796, 0.0015208, 0.1179849, 
            0.0010558, 0.0004688, 0.0569819, 0.0506053, 0.0000495, 0.0053780, 
            0.0114497, 0.0065520, 0.0022488, 0.0491264, 0.0287844, 0.0008309, 
            0.0001906, 0.0463897, 0.1269191, 0.0330152, 0.0000800, 0.0053856, 
            0.0000000, 0.0020925, 0.0000000, 0.0393295, 0.0001590, 0.0037195, 
            0.0000674, 0.0892434, 0.0009218, 0.0000404, 0.3352928, 0.0666758, 
            0.0000054, 0.0000162, 0.0146273, 0.0009110, 0.0011051, 0.0913053, 
            0.0000809, 0.0000027, 0.0310281, 0.0245378, 0.0171177, 0.0185732, 
            0.0000027, 0.0078702, 0.0000000, 0.0121422, 0.0002776, 0.0261517, 
            0.0181796, 0.0459729, 0.0223272, 0.0308931, 0.0058765, 0.0505571, 
            0.0000699, 0.0298191, 0.0000087, 0.0001572, 0.1066327, 0.0308669, 
            0.1156002, 0.0020170, 0.0448465, 0.0001746, 0.1626908, 0.1207345, 
            0.1249869, 0.0000349, 0.0009343, 0.0002008, 0.0008819, 0.0002969, 
            0.0010042, 0.1022242, 0.0000000, 0.0000000, 0.0049559, 0.6796927, 
            0.0000000, 0.0000000, 0.0002371, 0.1467561, 0.0000000, 0.0000000, 
            0.0001423, 0.0000000, 0.0128284, 0.0429195, 0.0000000, 0.0000000, 
            0.0008299, 0.0003083, 0.0000000, 0.0025847, 0.0005928, 0.0000000, 
            0.0000000, 0.0038888, 0.0000000, 0.1832539, 0.0003329, 0.0002984,
            0.0018938, 0.1605624, 0.0013085, 0.0000344, 0.1893372, 0.1788924,
            0.0000000, 0.0005050, 0.0089412, 0.0002755, 0.0372798, 0.0933831,
            0.0000803, 0.0000115, 0.0082066, 0.0126485, 0.0018135, 0.0011707,
            0.0000000, 0.0003214, 0.0000000, 0.0006887, 0.0000000, 0.0600144, 
            0.0000000, 0.1573582, 0.0010050, 0.0554200, 0.0000000, 0.0001436, 
            0.0132089, 0.1122757, 0.0000000, 0.0000000, 0.0014358, 0.0001436, 
            0.0000000, 0.0055994, 0.2157933, 0.0031587, 0.0000000, 0.0027279, 
            0.2360373, 0.0195262, 0.0051687, 0.0001436, 0.0093324, 0.0020101, 
            0.0000000, 0.0072178, 0.0039321, 0.0011985, 0.0020738, 0.0562745, 
            0.0015217, 0.0003097, 0.0007137, 0.0141393, 0.0000135, 0.0000269, 
            0.0031914, 0.0039051, 0.0022488, 0.1205478, 0.0027875, 0.0000000, 
            0.0048882, 0.0324935, 0.0109613, 0.0005925, 0.0000673, 0.0016025, 
            0.0001347, 0.0000943, 0.0002020, 0.4219769, 0.0007526, 0.0060211, 
            0.0067737, 0.3038133, 0.0000000, 0.0000000, 0.0005018, 0.0709985, 
            0.0002509, 0.0000000, 0.0198194, 0.0000000, 0.0000000, 0.0730055, 
            0.0000000, 0.0000000, 0.0002509, 0.0017561, 0.0005018, 0.0037632, 
            0.0010035, 0.0000000, 0.0000000, 0.0100351, 0.0268440];            
            
          // Map symbols to letters if we can.
          var map = {'1':'l', '3':'e', '4':'a', '5':'s', '7':'t',
            '@':'a', '$':'s'};            
          if (typeof(map[char_]) != 'undefined')
            char_ = map[char_];
          // don't know, assume equiprobable.  
          if (!char_.match(/^[a-zA-Z]$/))
            return 1/alphabet_size;
          var i = char_.toLowerCase().charCodeAt(0) - 'a'.charCodeAt(0);
          var rel_freq;
          var lb = null;
          if (index) {
            lb = password.charAt(index-1);
            if (typeof(map[lb]) != 'undefined')
              lb = map[lb];
          }
 
          var digram = (lb != null && lb.match(/^[a-zA-Z]$/));
          if (digram) {
            var j;
            j = lb.toLowerCase().charCodeAt(0) - 'a'.charCodeAt(0);
            rel_freq = digrams[i + 26*j];    
          } else {
            var check_array = index? chars : first_letter;
            rel_freq = check_array[i];
            
          }
          // normalise this so as to consider it as part of the whole alphabet,
          // not just a-z
          
          // this might occur if we've mapped a symbol but don't have a full
          // alphabet.
          if (alphabet_size >= 26)
            rel_freq *= (26/alphabet_size);
          return rel_freq;
        },
        
        calculateEntropy = function(password) {
          var alphabet_size = 0,
              passed = 0,
              regexes = {
                "[a-z]": 26, 
                "[A-Z]": 26, 
                // we don't regard a simple numeric append as a real 
                // increase in complexity.
                "(\\d[^\\d])|(^\\d+$)" : 10,
                "[\\W_]": 32 // there are 32 other printable ascii chars
              };
              
          // we're going to be mean here and apply some preprocessing.               
          // Collapse repetition.
          password = password.replace(/(.)(\1)(\1)+/gi, '$1$2');
          // Collapse sequences.
          password = password.replace(
/(a)(b(c(d(e(f(g(h(i(j(k(l(m(n(o(p(q(r(u(v(w(x(y(z)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?)?/gi, '$1');
          password = password.replace(
            /(0)(1(2(3(4(5(6(7(8(9)?)?)?)?)?)?)?)?)?/g, '$1');
          password = password.replace(
            /(1)(2(3(4(5(6(7(8(9(0)?)?)?)?)?)?)?)?)?/g, '$1');          
          // collapse trailing numbers
          password = password.replace(/([^\d])(\d)(\d)+$/, '$1$2');
          
          if (!password.length)
            return 0;
          for (var r in regexes) {
            if (regexTest(new RegExp(r), password))
              alphabet_size += regexes[r];
          }
          if (!alphabet_size)
            return 0;
          // log2 x = loge x/loge 2          
          var total_entropy = 0;          
          for (var i=0; i<password.length; i++)  {
            var e = charEntropy(password, i, alphabet_size);
            // This can get pretty whacky on hugely unlikely sequences but 
            // we trim it to 7 for sanity.
            total_entropy += Math.max(-7, (Math.log(e)/0.69314718055994529));
          }          
          return -1 * total_entropy;
        },
        
        // Counts the number of test passes.
        test = function(pass) {
          var passed = 0, entropy = 0;
          entropy = calculateEntropy(pass);
          
          if (tests.length && tests[0] instanceof RegExp) {
            jQuery.each(tests, function(i, e) {
              passed += regexTest(e, pass);
            });
          } else {            
            for (i=0; i<tests.length; i++){
              if (entropy < tests[i])
                break;
              passed = i+1;
            }
          }
          return [entropy, passed];
        },        
        change = function(e) {
          var pass = $(this).val(),
              tooshort = (!pass.length || pass.length < minimum),
              entropy, passes, a;
          a = test(pass);
          entropy = a[0];
          passes = tooshort? 0 : a[1];
          makeOutput(passes, entropy, tooshort);
        };
        
    // load the options object. This is ugly.
    if (typeof(options) == 'undefined')
      options = {};

    if (typeof options.labels === 'undefined') {
      options.labels = {}
    }
    options.labels = $.extend({
        tooShort: 'Too short',
        passwordStrength : 'Password strength:'
    }, options.labels);
    
    $out_el = $('<span>').css('display', 'inline-block')
                .addClass('passStrengthify');
    

    // this needs a good rewrite
    return $(this).each(function() {
      if (!options.element) {
        $(this).parent().append($out_el);
      } else {
        options.element.append($out_el);
      }
      if (options.minimum)
        minimum = options.minimum;

      if (typeof options.security == 'undefined')
        options.security = 1;
      if (options.security >= 0 && options.security < presets.length)
        tests = presets[options.security];

      if (!options.levels)
        options.levels = levels;
      if (!options.colours)
        options.colours = colours;
      if (!options.tests)
        options.tests = tests;

      if (options.levels && options.colours && options.tests) {
        if (options.levels.length == options.colours.length
            && options.colours.length == options.tests.length+1) {
          levels = options.levels;
          colours = options.colours;
          tests = options.tests;
        }
      }
      if (options.rawEntropy)
        rawEntropy = true;

      $out_el.append(
        $('<div>').append(
          $('<span>').css('font-size', 'smaller')
            .text(options.labels.passwordStrength).append(text)
        )
      );

      var max_width = 125.0;
      var margin = 3;
      var width = Math.round((max_width - margin*tests.length)/tests.length);

      for(i=0; i<tests.length; i++) {
        var $e = $('<span>').css('height', '3px')
                  .css('width', width + 'px')
                  .css('margin-right', margin + 'px')
                  .css('max-height', '3px')
                  .css('font-size',  '1px') // for IE 6
                  .css('float', 'left');
        progress_blocks.push($e);
        $out_el.append($e);
      }

      // keypress fires all the time when a user holds down a key, but it fires
      // before this.val() is updated. So we bind to both keypress and keyup
      $el.keypress(change);
      $el.keyup(change);

      $el.trigger('keyup');
    });
  };
})(jQuery);