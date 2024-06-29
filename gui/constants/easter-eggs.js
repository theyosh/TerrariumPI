export const fireworks = (time) => {
  const start = new Date(time.getFullYear() - (time.getMonth() === 0 ? 1 : 0) + '-12-30 00:00:00');
  const end = new Date(start.getTime() + 3 * 86400000); // + days in ms

  const documentBody = document.querySelector('aside.main-sidebar');
  const fireworks = documentBody !== null && start <= time && time <= end;
  const fireworksJS = document.createElement('script');
  fireworksJS.setAttribute('type', 'text/javascript');
  fireworksJS.setAttribute('src', 'js/fireworks.js');

  let fireworksCanvas = document.querySelector('canvas#fireworks');

  if (fireworks) {
    if (!fireworksCanvas) {
      fireworksCanvas = document.createElement('canvas');
      fireworksCanvas.id = 'fireworks';
      fireworksCanvas.style = 'position:absolute; z-index:-1; height:100%; width:100%; top: 0px; left:0px';
      documentBody.appendChild(fireworksCanvas);
      document.querySelector('head').appendChild(fireworksJS);
    }
  } else if (fireworksCanvas) {
    fireworksCanvas.remove();
    fireworksCanvas = null;
  }
};

export const christmas = (time) => {
  const start = new Date(time.getFullYear() - (time.getMonth() === 0 ? 1 : 0) + '-12-20 00:00:00');
  const end = new Date(start.getTime() + 14 * 86400000); // + days in ms

  return start <= time && time <= end;
};

export const showBirthdayCake = (time) => {
  const start = new Date('2024-08-01 00:00:00');
  const end = new Date(start.getTime() + 31 * 86400000); // + days in ms

  const itIsTime = start <= time && time <= end;

  if (itIsTime) {
    const loadedJS =
      [...document.getElementsByTagName('script')].filter(
        (script) => script.src.indexOf('tsparticles.confetti.bundle.min.js') !== -1,
      ).length === 1;

    if (!loadedJS) {
      const particleJS = document.createElement('script');
      particleJS.setAttribute('type', 'text/javascript');
      particleJS.setAttribute(
        'src',
        'https://cdn.jsdelivr.net/npm/@tsparticles/confetti@3.0.3/tsparticles.confetti.bundle.min.js',
      );
      document.querySelector('head').appendChild(particleJS);
    }
  }
  return itIsTime;
};
