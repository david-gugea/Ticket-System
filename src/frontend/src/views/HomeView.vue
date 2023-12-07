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
  margin-bottom: 50px; /* Adjust as needed */
  cursor: pointer;
  transition: none; /* Disable the toggle animation */
}

.ticketSystemLogo {
  width: 50em;
  height: auto;
  display: block;
  transition: transform 0.3s ease-in-out;
  image-rendering: crisp-edges;
}

</style>
