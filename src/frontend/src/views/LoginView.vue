<template> 
  <div class="login-container">
    <div class="background"></div>
    <div class="login-form" @mouseover="hover = true" @mouseleave="hover = false">
      <form>
        <h2 class="form-title">Login</h2>
        <div class="form-group">
          <label for="username" class="form-label">Username:</label>
          <input type="text" id="username" v-model="username" class="form-input" />
        </div>
        <div class="form-group">
          <label for="password" class="form-label">Password:</label>
          <input type="password" id="password" v-model="password" class="form-input" />
        </div>
        <button @click.prevent="login" :class="{ 'hover-effect': hover }" class="form-button">Login</button>
        <span>
          <router-link to="/register" style="margin-top: 20px;">Don't have an account? Register</router-link>
        </span>
        <p></p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      hover: false,
    };
  },
  methods: {
    login() {
      const username = this.username;
      const password = this.password;
      if(username.length === 0 && password.length === 0){
        alert('Please enter your username and password!')
      }else{
        const apiUrl = `http://localhost:8003/users/get_by/userpass?username=${this.username}&password=${this.password}`;
        axios.get(apiUrl)
          .then(response => {
            const userData = response.data;
            console.log(userData.status_code);
            if (userData.status_code === 404) {
              alert('Invalid username or password');
            } else {

              localStorage.setItem('loggedInUserID', userData.id);
              localStorage.setItem('loggedInUser', userData.username);
              this.$router.push({ name: 'ticketsDashboard' });
            }
          })
      }
    },
  },
};
</script>
  
  <style scoped>
  .login-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
  }
  
  body {
    margin: 0;
    background-color: black;
    overflow: hidden;
  }
  
  .background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(closest-corner, #1d2020, #000000);
    z-index: -1;
  }
  
  .login-form {
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
  