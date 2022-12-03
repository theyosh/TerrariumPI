<script>
  export let code = 500;
  export let message = '';
  export let email = '';
</script>

<div id="error-page">
  <div class="header">
    <!-- <img src="/logo/Logo_GLICP_ Two_Line_Negative.png" alt="GCP Logo" /> -->
  </div>
  <div class="error">
    <h1 class="error-status-code">{code}</h1>
    <p title="TraceId dotazu: @Model.RequestId">{message}</p>
    <div class="links">
      <a href="/" class="home-btn">Back home</a>
      <a href="mailto:{email}" class="contact-btn">Contact us</a>
    </div>
  </div>
</div>

<style>
  /* @font-face {
	font-family: 'Montserrat';
	font-style: normal;
	font-weight: 700;
	src: url(/fonts/Montserrat/JTURjIg1_i6t8kCHKm45_dJE3gTD_u50.woff2) format('woff2');
	unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
} */

  :global {
    * {
      -webkit-box-sizing: border-box;
      box-sizing: border-box;
    }

    body {
      padding: 0;
      margin: 0;
    }
  }

  #error-page {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background-color: #c21b17;
    min-height: 100vh;
  }

  #error-page .header {
    /* For logo */
  }

  #error-page .header img {
    max-width: calc(30vw - 2rem);
  }

  #error-page .error {
    /* For error box */

    align-self: center;
    flex: 1;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 30rem;
    font-family: 'Montserrat', sans-serif;
  }

  #error-page .error .error-status-code {
    font-size: 220px;
    font-weight: 900;
    margin: 0px;
    color: #fff;
    line-height: 0.9;
    text-transform: uppercase;
    letter-spacing: 10px;
  }

  #error-page .error p {
    font-size: 22px;
    font-weight: 700;
    text-transform: uppercase;
    color: #fff;
    margin-top: 20px;
    margin-bottom: 15px;
  }

  #error-page .error .links {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #error-page .error .links a {
    font-weight: 700;
    text-decoration: none;
    background-color: transparent;
    border: 2px solid transparent;
    text-transform: uppercase;
    padding: 13px 25px;
    font-size: 18px;
    border-radius: 40px;
    margin: 7px;
    -webkit-transition: 0.2s all;
    transition: 0.2s all;
  }

  #error-page .error .links a:hover {
    opacity: 0.9;
  }

  #error-page .error .links .home-btn {
    color: rgba(255, 0, 36, 0.7);
    background: #fff;
  }

  #error-page .error .links .contact-btn {
    border: 2px solid rgba(255, 255, 255, 0.9);
    color: rgba(255, 255, 255, 0.9);
  }

  /* XLarge */
  @media screen and (max-width: 1600px) {
    #error-page .header img {
      max-width: calc(35vw - 2rem);
    }
  }

  /* Large */
  @media screen and (max-width: 1200px) {
    #error-page .header img {
      max-width: calc(40vw - 2rem);
    }
  }

  /* Medium */
  @media screen and (max-width: 992px) {
    #error-page .header img {
      max-width: calc(60vw - 2rem);
    }
  }

  /* Small */
  @media screen and (max-width: 768px) {
    #error-page .header img {
      max-width: calc(75vw - 2rem);
    }

    #error-page .error .error-status-code {
      font-size: 160px;
    }

    #error-page .error p {
      font-size: 15px;
    }
  }

  /* XSmall */
  @media screen and (max-width: 576px) {
    #error-page .header img {
      max-width: calc(90vw - 2rem);
    }

    #error-page .error .error-status-code {
      font-size: 120px;
    }

    #error-page .error p {
      font-size: 15px;
    }
  }
</style>
