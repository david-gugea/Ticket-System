<template>
   <div class="ticketDasboard-container">
      <div class="background"></div>
      <div class="ticket-dashboard" @mouseover="hover = true" @mouseleave="hover = false">
        <!-- Button to open the pop-up form -->
        <button @click="openPopup" :class="{ 'hover-effect': hover }" class="btn btn-primary add-ticket-btn">Add Ticket</button>  
     
         <!-- Pop-up form -->
         <div v-if="isPopupVisible" class="popup">
           <form @submit.prevent="createTicket">
             <div class="form-group">
               <label for="description">Description</label>
               <textarea class="form-control" id="description" v-model="newTicket.description" required></textarea>
             </div>
             <div class="form-group">
               <label for="closed_by">Closed By</label>
               <input type="text" class="form-control" id="closed_by" v-model="newTicket.closed_by">
             </div>
             <div class="form-group">
               <label for="user_id">User ID</label>
               <input type="number" class="form-control" id="user_id" v-model="newTicket.user_id" required>
             </div>
             <div class="button-group">
               <button type="submit" class="btn btn-success">Create Ticket</button>
               <button @click.prevent="closePopup" class="btn btn-secondary">Cancel</button>
             </div>
           </form>
         </div>
     
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
               <th>Action</th>
             </tr>
           </thead>
           <!-- Table body with tickets -->
           <tbody>
             <tr v-for="ticket in tickets" :key="ticket.id">
               <td>{{ ticket.id }}</td>
               <td>{{ ticket.description }}</td>
               <td>{{ formatDate(ticket.date_created) }}</td>
               <td>{{ formatDate(ticket.date_closed) }}</td>
               <td>{{ ticket.done ? 'Yes' : 'No' }}</td>
               <td>{{ ticket.closed_by || '-' }}</td>
               <td>{{ ticket.user_id }}</td>
               <td>
                 <button @click="closeTicket(ticket)" :disabled="ticket.done" class="btn btn-sm btn-primary">Close</button>
               </td>
             </tr>
           </tbody>
         </table>
     
         <!-- Loading spinner -->
         <div v-if="loading" class="spinner-border text-primary" role="status">
           <span class="sr-only">Loading...</span>
         </div>
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
      loading: false,
      isPopupVisible: false,
      hover: false,
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
           this.saveDataToLocalStorage();
           this.closePopup();
         })
         .catch(error => {
           console.error('Failed to create ticket', error);
         })
         .finally(() => {
           this.loading = false;
         });
     },
     closeTicket(ticket) {
       if (!ticket.done) {
         this.loading = true;
         ticket.done = true;
         ticket.date_closed = new Date().toISOString().split('T')[0];
         ticket.closed_by = "System";
         axios.put(`http://localhost:8003/tickets/${ticket.id}`, ticket)
           .then(() => {
             this.saveDataToLocalStorage();
           })
           .catch(error => {
             console.error('Failed to update ticket', error);
           })
           .finally(() => {
             this.loading = false;
           });
       }
     },
     saveDataToLocalStorage() {
       localStorage.setItem('tickets', JSON.stringify(this.tickets));
     },
     loadDataFromLocalStorage() {
       const storedTickets = localStorage.getItem('tickets');
       if (storedTickets) {
         this.tickets = JSON.parse(storedTickets);
       }
     },
     formatDate(dateString) {
       if (dateString) {
         const date = new Date(dateString);
         return date.toLocaleDateString();
       }
       return '-';
     },
     openPopup() {
       this.isPopupVisible = true;
     },
     closePopup() {
       this.isPopupVisible = false;
     },
   },
   mounted() {
     this.loading = true;
     this.loadDataFromLocalStorage();
     axios.get('http://localhost:8003/tickets/get_all')
       .then(response => {
         this.tickets = response.data;
         this.saveDataToLocalStorage();
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
 .popup {
   display: block;
   position: fixed;
   top: 50%;
   left: 50%;
   transform: translate(-50%, -50%);
   background: #292b2c; /* Adjusted background color to match the ticket dashboard */
   padding: 20px;
   border: 1px solid #333; /* Adjusted border color */
   z-index: 1000;
   max-width: 400px;
   width: 100%;
   border-radius: 10px; /* Adjusted border radius to match the ticket dashboard */
   box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
 }
 
 .form-group {
   margin-bottom: 20px;
 }
 
 .btn-primary {
   width: 100%;
   padding: 15px;
   background-color: #68d2df;
   color: white;
   border: none;
   border-radius: 5px;
   cursor: pointer;
   transition: background-color 0.3s;
 }

 .btn-secondary {
   background-color: #7f8c8d;
   color: #ecf0f1;
 }
 
 .btn-success {
   background-color: #27ae60;
   color: #ecf0f1;
 }
 
 .table {
   width: 100%;
   border-collapse: collapse;
   margin-top: 20px;
   overflow: hidden;
   box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
   font-size: 16px;
 }
 
 th, td {
   border: 1px solid #333;
   padding: 15px;
   text-align: left;
   background-color: #292b2c;
   color: white;
 }
 
 th {
   background-color: #68d2df;
   color: white;
 }
 
 .spinner-border {
   display: block;
   margin: 20px auto;
 }

.ticketDasboard-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.ticket-dashboard {
  max-width: 1200px;
  padding: 20px;
  border-radius: 10px;
  color: white;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
  width: 100%; /* Set width to 100% */
  box-sizing: border-box;
}

/* Add these styles to center the add-ticket-btn */
.add-ticket-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  margin-left: 85%;
  width: 200px;
  padding: 15px;
  background-color: #68d2df;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}
/* Responsive styles */
@media (max-width: 768px) {
   .ticket-dashboard {
     padding: 10px; /* Adjust padding for smaller screens */
   }
 
   .add-ticket-btn {
     top: 10px;
     right: 10px;
     font-size: 14px; /* Adjust font size for smaller screens */
     padding: 10px; /* Adjust padding for smaller screens */
   }
 }
.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(closest-corner, #1d2020, #000000);
  z-index: -1;
}
 </style>
 
 