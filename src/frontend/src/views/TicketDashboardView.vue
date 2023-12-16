<template>
  <div class="logged-in-user">
    <p>Logged in as: {{ loggedInUser }}</p>
  </div>
  <div>
    <input type="text" v-model="searchQuery" placeholder="Search...">
    <ul>

    </ul>
  </div>
  <div class="ticketDasboard-container">

    <div class="background"></div>
    <div class="ticket-dashboard" @mouseover="hover = true" @mouseleave="hover = false">
      <!-- Button to open the pop-up form -->
      <button @click="openPopup" :class="{ 'hover-effect': hover }" class="btn btn-primary add-ticket-btn">Add
        Ticket</button>

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
            <th>Closed By</th>
            <th>User ID</th>
            <th>Done</th>
            <th>Close</th>
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
            <td>{{ ticket.closed_by || '-' }}</td>
            <td>{{ ticket.user_id }}</td>
            <td>{{ ticket.done ? 'Yes' : 'No' }}</td>
            <td><button @click="closeTicket(ticket)" :disabled="ticket.done" class="btn btn-sm btn-primary">Close</button>
            </td>
            <td>
              <button @click="editTicket(ticket)" class="btn btn-sm btn-primary">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Edit Ticket Popup -->
      <div v-if="selectedTicket" class="popup">
        <form>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" v-model="selectedTicket.description" required></textarea>
          </div>
          <div class="form-group">
            <label for="closed_by">Closed By</label>
            <input type="text" class="form-control" v-model="selectedTicket.closed_by">
          </div>
          <div class="form-group">
            <label for="user_id">User ID</label>
            <input type="number" class="form-control" v-model="selectedTicket.user_id" required>
          </div>
          <div class="button-group">
            <button @click.prevent="updateTicket(ticket)" class="btn btn-sm btn-primary">Update Ticket</button>
            <button @click.prevent="closePopup" class="btn btn-sm btn-secondary">Cancel</button>
            <button @click.prevent="deleteTicket" class="btn btn-sm btn-danger">Delete Ticket</button>
          </div>
        </form>
      </div>


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
      selectedTicket: null,
      loggedInUser: '',
      searchQuery: ''
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
            user_id: '',
            selectedTicket: null
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

    filteredItems() {
      return this.filteredItems.filter(item =>
        item.name.toLowerCase().includes(this.searchQuery.toLowerCase))
    },

    closeTicket(ticket) {
      if (!ticket.done) {
        this.loading = true;
        ticket.done = true;
        ticket.date_closed = new Date().toISOString().split('T')[0];
        ticket.closed_by = "System";
        axios.put(`http://localhost:8003/tickets/close/${ticket.id}`, this.newTicket)
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

    editTicket(ticket) {
      this.selectedTicket = { ...ticket };
      this.openPopup();
    },

    updateTicket() {
      this.loading = true;
      const id = this.selectedTicket.id;
      axios.put(`http://localhost:8003/tickets/update/${id}`, {
        "id": id,
        "description": "testPut"
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      })
        .then(res => {
          console.log(res.data);
          alert(res.data.message);
          this.errorlist = '';
        })
        .catch(error => {
          console.error("Error updating ticket:", error);
          if (error.response) {
            console.error("Response data:", error.response.data);
            console.error("Response status:", error.response.status);
            console.error("Response headers:", error.response.headers);
          } else if (error.request) {
            console.error("No response received. Request details:", error.request);
          } else {
            console.error("Error setting up the request:", error.message);
          }
        })
    },

    deleteTicket() {
      if (!this.selectedTicket) {
        console.error("No ticket selected for deletion");
        return;
      }

      const id = this.selectedTicket.id;

      axios.delete(`http://localhost:8003/tickets/delete/${id}`)
        .then(res => {
          console.log(res.data);
          alert(res.data.message);

          this.selectedTicket = null;
        })
        .catch(error => {
          console.error("Error deleting ticket:", error);
          if (error.response) {
            console.error("Response data:", error.response.data);
            console.error("Response status:", error.response.status);
            console.error("Response headers:", error.response.headers);
          } else if (error.request) {
            console.error("No response received. Request details:", error.request);
          } else {
            console.error("Error setting up the request:", error.message);
          }
        });
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
      this.selectedTicket = null;
    },
  },
  mounted() {
    this.loggedInUser = localStorage.getItem('loggedInUser');
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
.logged-in-user {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
  position: absolute;
  top: 20px;
  right: 20px;
}

.logged-in-user span {
  color: #68d2df;
  font-weight: bold;
}

.popup {
  display: block;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #292b2c;

  padding: 20px;
  border: 1px solid #333;

  z-index: 1000;
  max-width: 400px;
  width: 100%;
  border-radius: 10px;

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

th,
td {
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
  max-width: 100%;
  margin: 20px;
  padding: 20px;
  border-radius: 10px;
  color: white;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
  position: relative;
}

.add-ticket-btn {
  position: absolute;
  top: 1px;
  right: 20px;
  width: 100px;
  padding: 5px;
  background-color: #68d2df;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}


@media (max-width: 768px) {
  .ticket-dashboard {
    padding: 10px;
  }

  .add-ticket-btn {
    top: 1px;
    right: 10px;
    font-size: 14px;
    padding: 5px;
  }

  .table {
    margin-top: 10px;
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
 
 