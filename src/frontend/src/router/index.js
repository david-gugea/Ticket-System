// Import necessary functions from vue-router
import { createRouter, createWebHistory } from 'vue-router'

// Importing views to be used in the router
import HomeView from '../views/HomeView.vue'
import TicketDashboardView from '../views/TicketDashboardView.vue'

// Defining the routes for the application
const routes = [
  {
    // Route for the home page
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    // Route for the ticket dashboard page
    path: '/ticketsDashboard',
    name: 'ticketsDashboard',
    component: TicketDashboardView
  }
]

// Creating the router instance with history mode and the defined routes
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Exporting the router instance to be used in the application
export default router
