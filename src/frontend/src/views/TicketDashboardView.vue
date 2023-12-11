<template>
   <div class="ticket-dashboard">
     <!-- Create ticket form -->
     <form @submit.prevent="createTicket">
       <div class="form-group">
         <label for="description">Description</label>
         <textarea class="form-control" id="description" v-model="newTicket.description" required></textarea>
       </div>
       <div class="form-group">
         <label for="date_created">Date Created</label>
         <input type="date" class="form-control" id="date_created" v-model="newTicket.date_created" required>
       </div>
       <div class="form-group">
         <label for="date_closed">Date Closed</label>
         <input type="date" class="form-control" id="date_closed" v-model="newTicket.date_closed">
       </div>
       <div class="form-group">
         <label for="done">Done</label>
         <input type="checkbox" id="done" v-model="newTicket.done">
       </div>
       <div class="form-group">
         <label for="closed_by">Closed By</label>
         <input type="text" class="form-control" id="closed_by" v-model="newTicket.closed_by">
       </div>
       <div class="form-group">
         <label for="user_id">User ID</label>
         <input type="number" class="form-control" id="user_id" v-model="newTicket.user_id" required>
       </div>
       <button type="submit" class="btn btn-primary">Create Ticket</button>
     </form>
 
     <!-- Display a table of all tickets -->
     <table class="table mt-4">
       <!-- Table headers -->
       <thead>
         <tr>
           <th>ID</th>
           <th>Description</th>
           <th>Date Created</th>
           <th>Date Closed</th>
           <th>Done</th>
           <th>Closed By</th>
           <th>User ID</th>
         </tr>
       </thead>
       <!-- Table body with tickets -->
       <tbody>
         <tr v-for="ticket in tickets" :key="ticket.id">
           <td>{{ ticket.id }}</td>
           <td>{{ ticket.subject }}</td>
           <td>{{ ticket.description }}</td>
           <td>{{ ticket.date_created }}</td>
           <td>{{ ticket.date_closed }}</td>
           <td>{{ ticket.done }}</td>
           <td>{{ ticket.closed_by }}</td>
           <td>{{ ticket.user_id }}</td>
         </tr>
       </tbody>
     </table>
 
     <!-- Loading spinner -->
     <div v-if="loading" class="spinner-border text-primary" role="status">
       <span class="sr-only">Loading...</span>
     </div>
   </div>
 </template>
 
 <script>
 import axios from 'axios';
 
 export default {
   name: "TicketDashboardView",
   data() {
     return {
       newTicket: {
         description: '',
         date_created: '',
         date_closed: '',
         done: false,
         closed_by: '',
         user_id: ''
       },
       tickets: [],
       loading: false
     };
   },
   methods: {
     createTicket() {
       this.loading = true;
       axios.post('http://localhost:8003/tickets/create', this.newTicket)
         .then(response => {
           this.tickets.push(response.data);
           this.newTicket = {
             description: '',
             date_created: '',
             date_closed: '',
             done: false,
             closed_by: '',
             user_id: ''
           };
         })
         .catch(error => {
           console.error('Failed to create ticket', error);
         })
         .finally(() => {
           this.loading = false;
         });
     }
   },
   mounted() {
     this.loading = true;
     axios.get('/api/tickets')
       .then(response => {
         this.tickets = response.data;
       })
       .catch(error => {
         console.error('Failed to fetch tickets', error);
       })
       .finally(() => {
         this.loading = false;
       });
   }
 };
 </script>
 
 <style scoped>
 .ticket-dashboard {
   max-width: 1200px;
   margin: 0 auto;
   padding: 20px;
   background-color: #f8f9fa;
   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
 }
 
 .form-group {
   margin-bottom: 20px;
 }
 
 .btn-primary {
   background-color: #007bff;
   color: #fff;
 }
 
 table {
   width: 100%;
   border-collapse: collapse;
   margin-top: 20px;
 }
 
 th, td {
   border: 1px solid #dee2e6;
   padding: 8px;
   text-align: left;
 }
 
 th {
   background-color: #007bff;
   color: #fff;
 }
 
 /* Add other styles as needed */
 </style>
 