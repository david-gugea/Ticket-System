<template>
    <div class="register-container">
      <div class="background"></div>
      <div class="register-form" @mouseover="hover = true" @mouseleave="hover = false">
        <form>
          <h2 class="form-title">Register</h2>
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input type="text" id="username" v-model="username" class="form-input" />
          </div>
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input type="text" id="email" v-model="email" class="form-input" />
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Password:</label>
            <input type="password" id="password" v-model="password" class="form-input" />
          </div>
          <button @click.prevent="login" :class="{ 'hover-effect': hover }" class="form-button">Login</button>
          <span>
            <router-link to="/login"  style="margin-top: 20px;">Already have an account? Login</router-link>
          </span>
          <p></p>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        email:'',
        password: '',
        hover: false,
      };
    },
    methods: {
      register() {
        console.log('Register clicked!');
      },
    },
  };
  </script>
  
  <style scoped>
  .register-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
  }
  
  .background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(closest-corner,#1d2020, #000000);
    z-index: -1;
  }
  
  .register-form {
    background-color: #292b2c;
    padding: 40px;
    border-radius: 10px;
    color: white;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
    width: 400px;
  }
  
  .form-title {
    font-size: 28px;
    color: #68d2df;
    margin-bottom: 30px;
  }
  
  .form-group {
    margin-bottom: 20px;
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
    width: 100%;
    padding: 15px;
    background-color: #68d2df;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .form-button:hover {
    background-color: #68d2df;
  }
  
  .hover-effect:hover {
    transform: scale(1.05);
  }
  </style>
  