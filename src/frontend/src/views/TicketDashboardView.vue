<template>
   <div>
     <h1>Ticket Dashboard</h1>
 
     <!-- Display a form for creating tickets -->
     <form @submit.prevent="createTicket">
       <div class="mb-3">
         <label for="subject">Subject</label>
         <input type="text" class="form-control" id="subject" v-model="newTicket.subject" required />
       </div>
       <div class="mb-3">
         <label for="category">Category</label>
         <select class="form-select" id="category" v-model="newTicket.category" required>
           <option value="1">Support</option>
           <option value="2">Invoice</option>
           <option value="3">Cancellation</option>
         </select>
       </div>
       <div class="mb-3">
         <label for="description">Description</label>
         <textarea class="form-control" id="description" rows="3" v-model="newTicket.description" required></textarea>
       </div>
       <div class="mb-3">
         <label for="priority">Priority</label>
         <select class="form-select" id="priority" v-model="newTicket.priority" required>
           <option value="1">High</option>
           <option value="2">Medium</option>
           <option value="3">Low</option>
         </select>
       </div>
       <div class="mb-3">
         <label for="kind">Kind</label>
         <select class="form-select" id="kind" v-model="newTicket.kind" required>
           <option value="1">Bug</option>
           <option value="2">Task</option>
           <option value="3">Enhancement</option>
         </select>
       </div>
       <div class="mb-3">
         <label for="assignedTo">Assigned To</label>
         <select class="form-select" id="assignedTo" v-model="newTicket.assignedTo" required>
           <option value="1">John Doe</option>
           <option value="2">Jane Smith</option>
           <option value="3">Mary Johnson</option>
         </select>
       </div>
       <button type="submit" class="btn btn-primary">Create Ticket</button>
     </form>
 
     <!-- Display a table of all tickets -->
     <table class="table mt-4">
       <!-- Table headers -->
       <thead>
         <tr>
           <th>ID</th>
           <th>Subject</th>
           <th>Category</th>
           <th>Description</th>
           <th>Priority</th>
           <th>Kind</th>
           <th>Assigned To</th>
         </tr>
       </thead>
       <!-- Table body with tickets -->
       <tbody>
         <tr v-for="ticket in tickets" :key="ticket.id">
           <td>{{ ticket.id }}</td>
           <td>{{ ticket.subject }}</td>
           <td>{{ getCategoryLabel(ticket.category) }}</td>
           <td>{{ ticket.description }}</td>
           <td>{{ getPriorityLabel(ticket.priority) }}</td>
           <td>{{ getKindLabel(ticket.kind) }}</td>
           <td>{{ getAssignedToLabel(ticket.assignedTo) }}</td>
         </tr>
       </tbody>
     </table>
   </div>
 </template>
 
 <script>
 import axios from 'axios';
 
 export default {
   name: "TicketDashboardView",
   data() {
     return {
       newTicket: {
         subject: '',
         category: '',
         description: '',
         priority: '',
         kind: '',
         assignedTo: ''
       },
       tickets: []
     };
   },
   methods: {
     createTicket() {
       // Assuming an API endpoint for creating tickets
       const apiUrl = '/api/tickets';
 
       // Post the new ticket to the API
       axios.post(apiUrl, this.newTicket)
         .then(response => {
           console.log('Ticket created successfully', response.data);
           // Add the created ticket to the list
           this.tickets.push(response.data);
           // Reset the form
           this.newTicket = {
             subject: '',
             category: '',
             description: '',
             priority: '',
             kind: '',
             assignedTo: ''
           };
         })
         .catch(error => {
           console.error('Error creating ticket', error);
         });
     },
     getCategoryLabel(category) {
       // Map category values to labels
       const categoryMap = {
         1: 'Support',
         2: 'Invoice',
         3: 'Cancellation'
       };
       return categoryMap[category] || '';
     },
     getPriorityLabel(priority) {
       // Map priority values to labels
       const priorityMap = {
         1: 'High',
         2: 'Medium',
         3: 'Low'
       };
       return priorityMap[priority] || '';
     },
     getKindLabel(kind) {
       // Map kind values to labels
       const kindMap = {
         1: 'Bug',
         2: 'Task',
         3: 'Enhancement'
       };
       return kindMap[kind] || '';
     },
     getAssignedToLabel(assignedTo) {
       // Map assignedTo values to labels
       const assignedToMap = {
         1: 'John Doe',
         2: 'Jane Smith',
         3: 'Mary Johnson'
       };
       return assignedToMap[assignedTo] || '';
     }
   }
 };
 </script>
 
 <style scoped>
 /* Your styling here */
 </style>
 