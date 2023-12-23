<template>
  <div>
    <div v-if="loading" class="loading-spinner-overlay">
      <img ref="logo" class="logoLoading" alt="Logo" src="../assets/logo.png" v-if="showLogo">
      <div class="loading-spinner" role="status">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
    </div>

    <canvas ref="canvas" class="particle-canvas" @mousemove="handleMouseMove"></canvas>
    <div class="logo-container">
      <transition name="fade">
        <img ref="logo" class="logo" alt="Logo" src="../assets/logo.png" v-if="showLogo">
      </transition>
      <a href="#loginAnch" :class="{ 'hover-effect': hover }" class="form-button">Login</a>
    </div>
  </div>

  <div class="loginBox">
    <div class="loginform"></div>
  </div>




  <!-- Login Form -->
  <div v-show="view === 'login'" class="form-wrapper" id="loginAnch">
    <div class="wrapperLogin">
      <div class="login-box">
        <form>
          <h2 class="form-title">Login</h2>
          <div class="user-box">
            <input type="text" id="username" v-model="username" :style="{ borderColor: usernameError ? 'red' : '' }"
              class="form-input" />
            <label for="username">Username:</label>
          </div>
          <div class="user-box">
            <input type="password" id="password" v-model="password" :style="{ borderColor: passwordError ? 'red' : '' }"
              class="form-input" />
            <label for="password">Password:</label>

          </div>
          <br />
          <label v-if="wrongData" style="color: red;">Wrong username or password</label>
          <label v-if="emptyDataError" style="color: red;">Please enter username and password </label>
          <button @click.prevent="login" :class="{ 'hover-effect': hover }" class="form-button">Login</button>
          <button @click.prevent="toggleView" :class="{ 'hover-effect': hover }" class="form-button">Register</button>
        </form>
      </div>
    </div>
  </div>

  <!-- Register Form -->
  <div v-show="view === 'register'" class="form-wrapper">
    <div class="wrapperRegister">
      <div class="login-box">
        <form>
          <h2 class="form-title">Register</h2>
          <div class="user-box">
            <input type="text" id="username" v-model="username" class="form-input" />
            <label for="username">Username</label>
          </div>
          <div class="user-box">
            <input type="password" id="password" v-model="password" @input="checkStrength" class="form-input" />
            <label for="password">Password:</label>
          </div>

          <div class="user-box">
            <input type="password" id="passwordConfirm" v-model="passwordConfirm" class="form-input" />
            <label for="passwordConfirm">Password Confirmation:</label>
            <div id="color-bar" :style="{ background: meterColor, width: meterWidth }"></div>
          </div>
          <label v-if="usernameError || passwordError" style="color: red;">Username already exists</label>
          <label v-if="emptyDataError" style="color: red;">Please enter username and password </label>
          <label v-if="notMatchingPassword" style="color: red;">Passwords are not matching</label>
          <button @click.prevent="register" :class="{ 'hover-effect': hover }" class="form-button">Register</button>
          <button @click.prevent="toggleView" :class="{ 'hover-effect': hover }" class="form-button">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      loading: true,
      meterColor: '#6B778D',
      meterWidth: '10%',
      meterText: 'Too short',
      wrongData: false,
      usernameError: false,
      passwordError: false,
      emptyDataError: false,
      notMatchingPassword: false,
      view: 'login',
      value1: false,
      particles: [],
      canvas: null,
      ctx: null,
      particleCount: 100,
      mouse: {
        x: 0,
        y: 0,
      },
      showLogo: false,
      username: '',
      password: '',
      passwordConfirm: '',
      hover: false,
      loginForm: false

    };
  },
  mounted() {
    this.initializeCanvas();
    this.createParticles();
    setTimeout(() => {
      this.showLogo = true;
      this.animate();
      this.loading = false; // Set loading to false after content is loaded
    }, 3000);

    setTimeout(() => {
      this.showLogo = true;
      this.animate();
    }, 1000);
  },
  methods: {
    initializeCanvas() {
      this.canvas = this.$refs.canvas;
      this.ctx = this.canvas.getContext('2d');
      this.resizeCanvas();
      window.addEventListener('resize', this.resizeCanvas);
    },
    resizeCanvas() {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.createParticles();
    },
    createParticles() {
      this.particles = [];
      for (let i = 0; i < this.particleCount; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          radius: Math.random() * 3 + 1,
          color: `rgba(165, 224, 218, ${Math.random()})`,
          speedX: Math.random() - 0.5,
          speedY: Math.random() - 0.5,
        });
      }
    },
    animate() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.particles.forEach((particle) => {
        this.drawParticle(particle);
        this.updateParticle(particle);
      });
      requestAnimationFrame(this.animate);
    },
    drawParticle(particle) {
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = particle.color;
      this.ctx.fill();
    },
    updateParticle(particle) {
      const dx = this.mouse.x - particle.x;
      const dy = this.mouse.y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 100) {
        const angle = Math.atan2(dy, dx);
        particle.speedX = Math.cos(angle) * 2;
        particle.speedY = Math.sin(angle) * 2;
      }

      particle.x += particle.speedX;
      particle.y += particle.speedY;

      if (
        particle.x + particle.radius > this.canvas.width ||
        particle.x - particle.radius < 0
      ) {
        particle.speedX = -particle.speedX;
      }

      if (
        particle.y + particle.radius > this.canvas.height ||
        particle.y - particle.radius < 0
      ) {
        particle.speedY = -particle.speedY;
      }
    },
    handleMouseMove(event) {
      this.mouse.x = event.clientX;
      this.mouse.y = event.clientY;
    },

    openPopup() {
      this.loginForm = true;
    },

    register() {
      this.usernameError = false;
      this.passwordError = false;
      this.wrongData = false;
      this.emptyDataError = false;
      this.notMatchingPassword = false;

      if (this.password !== this.passwordConfirm) {
        console.error('Password and password confirmation do not match');
        this.notMatchingPassword = true;
        return;
      }

      const apiUrl = 'http://localhost:8003/users/create';


      const requestData = {
        username: this.username,
        password: this.password,
        user_type: "admin"
      };

      alert(this.username.length);

      if (this.username.length === 0 || this.password.length === 0) {
        this.emptyDataError = true;
      } else {
        axios.post(apiUrl, requestData)
          .then(response => {
            if (response.data.status_code === 400) {
              this.usernameError = true;
              this.passwordError = true;
            } else {
              alert("Registration success")
              this.view = this.view === 'login' ? 'register' : 'login';
            }
          })
          .catch(error => {
            console.error('Registration failed!', error);
            this.usernameError = true;
            this.passwordError = true;


          });
      }


    },

    toggleView() {
      // Toggle between 'login' and 'register' views
      this.view = this.view === 'login' ? 'register' : 'login';
    },

    checkStrength() {
      let strength = 0;

      if (this.password.length < 6) {
        this.updateMeter('#6B778D', '10%', 'Too short');
        return;
      }

      if (this.password.length > 7) strength += 1;
      if (this.password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1;
      if (this.password.match(/([a-zA-Z])/) && this.password.match(/([0-9])/)) strength += 1;
      if (this.password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1;

      if (strength < 2) {
        this.updateMeter('#ff0000', '25%', 'Weak');
      } else if (strength === 2) {
        this.updateMeter('#00BCD4', '75%', 'Good');
      } else {
        this.updateMeter('#4CAF50', '100%', 'Strong');
      }
    },
    updateMeter(color, width, text) {
      this.meterColor = color;
      this.meterWidth = width;
      this.meterText = text;
    },

    login() {
      this.usernameError = false;
      this.passwordError = false;
      this.wrongData = false;
      this.emptyDataError = false;

      const username = this.username;
      const password = this.password;
      if (username.length === 0 && password.length === 0) {
        this.emptyDataError = true;

      } else {
        const apiUrl = `http://localhost:8003/users/get_by/userpass?username=${this.username}&password=${this.password}`;
        axios.get(apiUrl)
          .then(response => {
            const userData = response.data;
            console.log(userData.status_code);
            if (userData.status_code === 404) {

              this.wrongData = true;


            } else {

              localStorage.setItem('loggedInUserID', userData.id);
              localStorage.setItem('loggedInUser', userData.username);
              localStorage.setItem('loggedInUserType', userData.user_type);
              this.$router.push({ name: 'ticketsDashboard' });
            }
          })
      }
    },
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resizeCanvas);
  },
};
</script>

<style scoped>

#color-bar {
  height: 5px;
  margin-top: 5px;
  transition: width 0.5s ease, background-color 0.5s ease;
  background-color: #000000;
}

#meter {
  width: 100%;
  height: 10px;
  background-color: #ccc;
}

#meter-bar {
  height: 100%;
}

#meter-text {
  margin-top: 5px;
}


html {
  scroll-snap-type: x mandatory;
  overflow-y: hidden;
  scroll-behavior: smooth;
}

.loading-spinner-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: black;
  /* Set the background color */
  opacity: 1;
  /* Adjust the opacity if needed */
  z-index: 1000;
}

.wrapperLogin,
.wrapperRegister {
  height: 100vh;
  width: auto;
  overflow: hidden;
}

.login-container,
.register-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.user-box input:focus~label,
.user-box input:valid~label,
.user-box input:not(:placeholder-shown)~label {
  top: -20px;
  left: 0;
  color: #03e9f4;
  font-size: 12px;
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #03e9f4, #3273dc);
  z-index: 1;
  opacity: 0.8;
  animation: backgroundAnimation 5s infinite alternate;
}

@keyframes backgroundAnimation {
  0% {
    transform: translateX(-100%) translateY(-100%);
  }

  100% {
    transform: translateX(100%) translateY(100%);
  }
}

.wrapper {
  position: relative;
  z-index: 2;
}

.login-box,
.register-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid transparent;
  border-radius: 10px;
  overflow: hidden;
  z-index: 3;
  animation: borderAnimation 2s infinite alternate;
}

@keyframes borderAnimation {

  0%,
  100% {
    border-color: #03e9f4;
  }

  50% {
    border-color: transparent;
  }
}


.form-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #000000;
}

.login-box {
  position: relative;
  width: 400px;
  padding: 40px;
  background: rgba(0, 72, 101, 0);
  box-sizing: border-box;
  border-radius: 10px;
  z-index: 100;
  overflow: hidden;
}

.form-title {
  margin: 0 0 30px;
  padding: 0;
  color: #fff;
  text-align: center;
}

.user-box {
  position: relative;
}

.user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: transparent;
}

.user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.user-box input:focus~label,
.user-box input:valid~label {
  top: -20px;
  left: 0;
  color: #03e9f4;
  font-size: 12px;
}

.form-button {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: background 0.5s, color 0.5s, box-shadow 0.5s;
  margin-top: 40px;
  letter-spacing: 4px;
  border: 2px solid #03e9f4;
  background: transparent;
  border-radius: 5px;
}

.form-button:hover {
  background: #03e9f4;
  color: #fff;
  box-shadow: 0 0 10px rgba(3, 233, 244, 0.8), 0 0 20px rgba(3, 233, 244, 0.6),
    0 0 30px rgba(3, 233, 244, 0.4), 0 0 40px rgba(3, 233, 244, 0.2);
}

.form-button span {
  position: absolute;
  display: block;
}

.form-button span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 1s linear infinite;
}

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }

  50%,
  100% {
    left: 100%;
  }
}

.form-button span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #03e9f4);
  animation: btn-anim2 1s linear infinite;
  animation-delay: .25s;
}

@keyframes btn-anim2 {
  0% {
    top: -100%;
  }

  50%,
  100% {
    top: 100%;
  }
}

.form-button span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #03e9f4);
  animation: btn-anim3 1s linear infinite;
  animation-delay: .5s;
}

@keyframes btn-anim3 {
  0% {
    right: -100%;
  }

  50%,
  100% {
    right: 100%;
  }
}

.form-button span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #03e9f4);
  animation: btn-anim4 1s linear infinite;
  animation-delay: .75s;
}

@keyframes btn-anim4 {
  0% {
    bottom: -100%;
  }

  50%,
  100% {
    bottom: 100%;
  }
}

.particle-canvas {
  display: block;
  background: radial-gradient(closest-corner, #1d2020, #000000);
}

.logo-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  text-align: center;

}
#logo {
position: absolute;
top: 0;
left: 0;
width: 250px;
height: 100px;
overflow: hidden;
}
#logo img {
width: 100%;
}
#logo:before {
content: '';
position: absolute;
top: 0;
left: -100px;
width: 70px;
height: 100%;
background: rgba(255,255,255, 0.3);
transform: skewX(-30deg);
animation-name: slide;
animation-duration: 7s;
animation-timing-function: ease-in-out;
animation-delay: .3s;
animation-iteration-count: infinite;
animation-direction: alternate;
background: linear-gradient(
    to right, 
    rgba(255, 255, 255, 0.13) 0%,
    rgba(255, 255, 255, 0.13) 77%,
    rgba(255, 255, 255, 0.5) 92%,
    rgba(255, 255, 255, 0.0) 100%
  );
}
@keyframes slide {
  0% {
    left: -100;
    top: 0;
  }
  50% {
    left: 120px;
    top: 0px;
  }
  100% {
    left: 290px;
    top: 0;
  }
}
.login-shadow {
  width: 400px;
  height: 400px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 100%;
  z-index: 1;
  box-shadow: 10px -55px 30px 15px #823ca6, 24px -10px 47px 10px #aab3d2, -21px -25px 97px 10px #5acee3, 51px 5px 17px 10px #1b7d8f, 3px 2px 77px 10px #f30bf5;
  animation: shadow-rotate 1.5s linear infinite;
  transform-origin: center;
}

@keyframes circle-size {
  from {
    width: 250px;
    height: 250px;
  }

  to {
    width: 300px;
    height: 300px;
  }
}


@keyframes shadow-rotate {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

.logo {
  width: 100%;
  height: auto;
}

.logoLoading {
  width: 400px;
  /* Adjust the width to your preference */
  height: auto;
  margin-bottom: 300px;
  /* Adjust the bottom margin as needed */
  margin-top: 20px;
  /* Adjust the top margin as needed */
}

.loading-spinner-overlay {
  /* Existing styles */
  display: flex;
  flex-direction: column;
  align-items: center;
  /* Existing styles */
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}



.wrapper {
  position: relative;
  color: white;
  width: 750px;
  height: 450px;
}

.wrapper .form-box {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;

}

.wrapper .form-box.login {
  left: 0;
  padding: 0 40px;

}

.form-box .form-group {
  position: relative;
  width: 100%;
  height: 50px;
  margin: 25px 0;
}

.form-group input {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  border-bottom: 2px solid #fff;

}

.form-group label {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}


.form-group input:focus {
  color: #0ef;
}



body {
  margin: 0;
  background: radial-gradient(closest-corner, #1d2020, #000000);
  overflow: hidden;

}

.background {
  position: fixed;
  top: 0;
  left: 0;
  width: auto;
  height: 100vh;
  background: radial-gradient(closest-corner, #1d2020, #000000);
  z-index: -1;
}



.form-title {
  font-size: 28px;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  color: #70ced8;
  text-align: center;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.loading-spinner p {
  margin-top: 10px;
  /* Adjust the margin as needed */
  color: #03e9f4;
  /* Adjust the color as needed */
}


.form-label {
  display: block;
  font-size: 16px;
  margin-bottom: 8px;
  color: #ddd;
}

.form-input {
  width: 100%;
  padding: 12px;
  box-sizing: border-box;
  margin-bottom: 15px;
  border: 1px solid #444;
  border-radius: 5px;
  font-size: 16px;
  background-color: #333;
  color: white;
}

.form-button {
  position: relative;
  width: 100%;
  height: 45px;
  background: transparent;
  border: 2px solid #0ef;
  outline: none;
  font-size: 16px;
  color: #fff;
  font-weight: 	Copperplate;
}

.form-button:hover {
  background-color: #68d2df;
}

.hover-effect:hover {
  transform: scale(1.05);
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.spinner {
  border: 6px solid rgba(255, 255, 255, 0.3);
  border-top: 6px solid #68d2df;
  /* Change the color as needed */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
