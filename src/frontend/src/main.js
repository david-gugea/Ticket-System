// Importing Bootstrap CSS to apply styling to the application
import 'bootstrap/dist/css/bootstrap.css';

// Importing createApp function from Vue to create the main application instance
import { createApp } from "vue";

// Importing the root component of the application
import App from './App.vue';

// Importing the router instance created in the router.js file
import router from './router';

// Creating the main application instance
const app = createApp(App);



// Using the router instance in the application
app.use(router);

// Mounting the application to the HTML element with the ID 'app'
app.mount("#app");