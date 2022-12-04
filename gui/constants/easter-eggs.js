export const fireworks = () => {
  const today = new Date();
  const newyear = (today.getMonth() === 11 && today.getDate() >= 31) || (today.getMonth() === 0 && today.getDate() <= 1);
  let fireworksCanvas = document.querySelector('canvas#fireworks');

  if (newyear) {
    if (!fireworksCanvas) {
      fireworksCanvas = document.createElement('canvas');
      fireworksCanvas.id = 'fireworks';
      fireworksCanvas.style = 'position:absolute; z-index:-1; height:100%; width:100%; top: 0px; left:0px';
      document.querySelector('aside.main-sidebar').appendChild(fireworksCanvas);

      const fireworksJS = document.createElement('script');
      fireworksJS.setAttribute('type', 'text/javascript');
      fireworksJS.setAttribute('src', 'js/fireworks.js');
      document.querySelector('head').appendChild(fireworksJS);
    };
  } else if (fireworksCanvas) {
    fireworksCanvas.remove();
  };
};

export const christmas = () => {
  const today = new Date();
  const christmas = (today.getMonth() === 11 && today.getDate() >= 18) || (today.getMonth() === 0 && today.getDate() <= 3);
  const hat = document.querySelector('img.christmashat');

  if (christmas) {
    hat.classList.remove('d-none');
  } else {
    hat.classList.add('d-none');
  };
};