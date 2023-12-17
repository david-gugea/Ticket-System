<template>
  <section class="home-view">
    <div class="logo-container">
      <div class="d-flex justify-content-center">
        <img class="ticketSystemLogo" alt="TicketSystemLogo" src="../assets/logo.png">
      </div>
    </div>
    <span>
      <router-link to="/login" class="btn btn-outline-light btn-lg px-5" style="margin-top: 10px;">Login</router-link>
    </span>
  </section>
</template>

<script>
</script>

<style scoped>
.home-view {
  color: #ffffff;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease-in-out;
  background: radial-gradient(closest-corner,#1d2020, #000000);
}

.logo-container {
  margin-bottom: 50px; 
  cursor: pointer;
  transition: none; 
}

.ticketSystemLogo {
  width: 50em;
  height: auto;
  display: block;
  transition: transform 0.3s ease-in-out;
  image-rendering: crisp-edges;
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
</style>
