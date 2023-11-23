<template>
<section class="vh-100 gradient-custom">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card bg-dark text-white" style="border-radius: 1rem;">
          <div class="card-body p-2 text-center">
            <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
            <p class="text-white-50 mb-5">Please enter your login and password!</p>

            <div class="form-outline form-white mb-4">
              <input type="email" id="typeEmailX" class="form-control form-control-lg" />
              <label class="form-label" for="typeEmailX">Email</label>
            </div>

            <div class="form-outline form-white mb-2">
              <input type="password" id="typePasswordX" class="form-control form-control-lg" />
              <label class="form-label" for="typePasswordX">Password</label>
            </div>

            <p class="small pb-lg-2"><a class="text-white-50" href="#!">Forgot password?</a></p>

            <button class="btn btn-outline-light btn-lg px-5" type="submit">Login</button>

            <div>
              <p class="pd-2 mb-2">Don't have an account? <a href="#!" class="text-white-50 fw-bold">Sign Up</a></p>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'LoginForm',
  data() {
    return {
      form: {
        username: '',
        password:'',
      }
    };
  },
  methods: {
    ...mapActions(['logIn']),
    async submit() {
      const User = new FormData();
      User.append('username', this.form.username);
      User.append('password', this.form.password);
      await this.logIn(User);
      this.$router.push('/dashboard');
    }
  }
});
</script>


<style>

.ticketSystemLogo {
  width: 80%; 
  height: auto; 
  display: block;
}

.btn-outline-light {
  color: #6ad1d9;
  border-color: #6ad1d9;
}

.btn-outline-light:hover {
  background-color: #6ad1d9;
  color: #ffffff;
}
</style>
