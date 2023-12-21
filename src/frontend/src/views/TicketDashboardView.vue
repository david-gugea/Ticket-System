<template>
  <section>
    <div class="fullSize">
      <div id="top-container">

        <nav role="navigation">
          <div id="menuToggle">
            <input type="checkbox" />
            <span></span>
            <span></span>
            <span></span>
            <ul id="menu">
              <a>
                <li ref="userButton" @click="openUserPopup">Users</li>
              </a>
              <a @click="logout">
                <li>Logout</li>
              </a>
            </ul>
          </div>
        </nav>

        <!-- User Profile -->
        <div class="profile-container">
          <img src="../assets/userAvatar.png" alt="User Profile Image" class="profile-image" />
          <div class="user-info">
            <p class="logged-in-user">User: <span id="usernamePlaceholder">{{ loggedInUser }}</span></p>
            <p class="logged-in-user-type">User type: <span id="userTypePlaceholder">{{ loggedInUserType }}</span></p>
          </div>
        </div>

        <!-- Search Bar Section -->
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="Search... Description" @input="filterTable">
          <div class="search"></div>
        </div>
      </div>

      <button id="wide-button" @click="openPopup" :class="{ 'hover-effect': hover }">+</button>

      <div class="table-container">
        <div class="tbl-header">
          <table cellpadding="0" cellspacing="0" border="0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Description</th>
                <th>Date Created</th>
                <th>Date Closed</th>
                <th>Created By</th>
                <th>Closed By</th>
                <th>User ID</th>
                <th>Done</th>
                <th>Close</th>
                <th></th>
              </tr>
            </thead>
          </table>
        </div>
        <div class="tbl-content">
          <table cellpadding="0" cellspacing="0" border="0">
            <tbody>
              <tr v-for="ticket in filteredTickets" :key="ticket.id">
                <td>{{ ticket.id }}</td>
                <td>{{ ticket.description }}</td>
                <td>{{ formatDate(ticket.date_created) }}</td>
                <td>{{ formatDate(ticket.date_closed) }}</td>
                <td><span>{{ loggedInUser }}</span></td>
                <td>{{ ticket.closed_by || '-' }}</td>
                <td>{{ ticket.user_id }}</td>
                <td>{{ ticket.done ? 'Yes' : 'No' }}</td>
                <td><button @click="closeTicket(ticket)" :disabled="ticket.done"
                    class="btn btn-sm btn-primary">Close</button>
                </td>
                <td>
                  <button @click="editTicket(ticket)" class="btn btn-sm btn-primary">Edit</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <!-- Pop-up form -->
    <div v-if="isPopupVisible" class="popup">
      <form @submit.prevent="createTicket">
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" id="description" v-model="newTicket.description" 
            oninvalid="this.setCustomValidity('Please fill out this field.')" required></textarea>
        </div>
        <div class="button-group">
          <button type="submit" class="btn btn-success">Create Ticket</button>
          <button @click.prevent="closePopup" type="button" class="btn-close" data-dismiss="modal" aria-label="Close">
          </button>
        </div>
      </form>
    </div>


    <div class="popupUser" v-if="userDataPopup">
      <form>
        <div class="form-group">
          <div id="table-container">
            <div class="tbl-header">
              <table cellpadding="0" cellspacing="0" border="0">
                <thead>
                  <tr class="tablePopupTr">
                    <th>User ID</th>
                    <th>User Name</th>
                    <th>User Type</th>
                    <th>New Role</th>
                  </tr>
                </thead>
              </table>
            </div>
            <div class="tbl-content">
              <table ellpadding="0" cellspacing="0" border="0">
                <tbody>
                  <tr v-for="user in usersData" class="tablePopupTr" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.user_type }}</td>
                    <td v-if="selectedUser" @change="updateUser(user)">
                      <select v-model="user.updatedUserType">
                        <option value="admin">Admin</option>
                        <option value="developer">Developer</option>
                        <option value="customer">Customer</option>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="button-group">
          <button @click="closeUserPopup" type="button" class="btn-close" data-dismiss="modal" aria-label="Close">
          </button>
        </div>
      </form>
    </div>


    <!-- Edit Ticket Popup -->
    <div v-if="selectedTicket" class="popup">
      <form @submit.prevent="updateTicket(ticket)">
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" id="description" v-model="selectedTicket.description" required
            title="Please fill out this field."
            oninvalid="this.setCustomValidity('Please fill out this field.')"></textarea>
        </div>

        <div class="button-group">
          <button @click.prevent="closePopup" type="button" class="btn-close" data-dismiss="modal"
            aria-label="Close"></button>
          <button type="submit" class="btn btn-sm btn-primary">Update Ticket</button>
          <br>
          <button @click.prevent="deleteTicket" class="btn btn-sm btn-danger">Delete Ticket</button>
        </div>
      </form>
    </div>

    <div v-if="loading" class="loading-spinner" role="status">
      <div class="spinner"></div>
    </div>
  </section>
</template>
 
<script>
import axios from 'axios';
const userID = localStorage.getItem("loggedInUserID");
const user = localStorage.getItem("loggedInUser");

export default {


  name: "TicketDashboardView",
  data() {
    return {
      newTicket: {
        description: '',
        date_created: '',
        date_closed: '',
        done: false,
        created_by: user,
        closed_by: '',
        user_id: userID
      },
      tickets: [],
      usersData: [],
      loading: false,
      isPopupVisible: false,
      hover: false,
      userDataPopup: false,
      selectedTicket: null,
      selectedUser: null,
      loggedInUser: '',
      loggedInUserType: '',
      searchQuery: '',
      filteredTickets: [],
      showProfileDropdown: false,
    };
  },


  methods: {
    logout() {
      localStorage.removeItem('loggedInUser');
      localStorage.removeItem('loggedInUserID');
      localStorage.removeItem('loggedInUserType');
      this.$router.push('/');
    },
    createTicket() {
      const user = localStorage.getItem("loggedInUser");
      this.loading = true;
      axios.post('http://localhost:8003/tickets/create', this.newTicket)
        .then(response => {
          this.tickets.push(response.data);
          this.newTicket = {
            description: '',
            date_created: '',
            date_closed: '',
            done: false,
            created_by: user,
            closed_by: '',
            user_id: '',
            selectedTicket: null
          };
          this.saveDataToLocalStorage();
          this.closePopup();
          window.location.reload();
        })
        .catch(error => {
          console.error('Failed to create ticket', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    filterTable() {
      // Filter the table based on the searchQuery
      this.filteredTickets = this.tickets.filter(ticket =>
        ticket.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },

    openUserPopup() {
      this.userDataPopup = true;
      axios.get(`http://localhost:8003/users/get_all`)
        .then(response => {
          this.usersData = response.data;
          if (this.usersData.length > 0) {
            this.selectedUser = { ...this.usersData[0] };
          }
          console.log(this.usersData);
        })
        .catch(error => {
          console.error('Failed to fetch tickets', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    closeUserPopup() {
      this.userDataPopup = false;
    },

    updateUser(user) {
      this.loading = true;

      const requestBody = {
        "id": user.id,
        "user_type": user.updatedUserType, // Use user.updatedUserType
      };

      axios.put(`http://localhost:8003/users/update_user_type`, requestBody)
        .then(() => {
          this.saveDataToLocalStorage();
          window.location.reload();
        })
        .catch(error => {
          console.error('Failed to update user', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    closeTicket(ticket) {
      const userID = localStorage.getItem("loggedInUserID");

      if (!ticket.done) {
        this.loading = true;
        ticket.done = true;
        ticket.date_closed = Date.now();
        ticket.closed_by = this.loggedInUser;
        const requestBody = {
          "id": ticket.id,
          "closed_by": userID,
        }
        axios.put(`http://localhost:8003/tickets/close`, requestBody)
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

      const requestBody = {
        "id": this.selectedTicket.id,
        "description": this.selectedTicket.description
      }
      axios.put(`http://localhost:8003/tickets/update`, requestBody)
        .then(() => {
          this.saveDataToLocalStorage();
          window.location.reload();
        })
        .catch(error => {
          console.error('Failed to update ticket', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    deleteTicket() {
      const requestBody = {
        "id": this.selectedTicket.id
      }
      axios.delete(`http://localhost:8003/tickets/delete`, {
        data: requestBody
      })
        .then(() => {
          this.saveDataToLocalStorage();
          window.location.reload();
        })
        .catch(error => {
          console.error('Failed to delete ticket', error);
        })
        .finally(() => {
          this.loading = false;
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
      this.popupUser
    },
  },
  mounted() {
    const newUserID = localStorage.getItem('loggedInUserID');
    this.loggedInUser = localStorage.getItem('loggedInUser');
    this.loggedInUserType = localStorage.getItem('loggedInUserType')

    if (this.loggedInUserType === "developer") {
      this.loggedInUserType == "Developer"
    } else {
      this.loggedInUserType = localStorage.getItem('loggedInUserType')
    }
    const userType = localStorage.getItem('loggedInUserType');
    this.loading = true;
    if (userType === "admin") {
      axios.get(`http://localhost:8003/tickets/get_all`)
        .then(response => {
          this.tickets = response.data;
          this.filteredTickets = [...this.tickets];
          this.saveDataToLocalStorage();
        })
        .catch(error => {
          console.error('Failed to fetch tickets', error);
        })
        .finally(() => {
          this.loading = false;
        });

    } else if (userType === "developer") {

      const userButton = this.$refs.userButton

      userButton.style.display = 'none'
      axios.get(`http://localhost:8003/tickets/get_all`)
        .then(response => {
          this.tickets = response.data;
          this.filteredTickets = [...this.tickets];
          this.saveDataToLocalStorage();
        })
        .catch(error => {
          console.error('Failed to fetch tickets', error);
        })
        .finally(() => {
          this.loading = false;
        });
    } else {
      const userButton = this.$refs.userButton
      userButton.style.display = 'none'
      //Get by UserID 
      this.loadDataFromLocalStorage();
      axios.get(`http://localhost:8003/tickets/get_by_user_id`, {
        params: {
          user_id: newUserID,
        }
      })
        .then(response => {
          this.tickets = response.data;
          this.filteredTickets = [...this.tickets];
          this.saveDataToLocalStorage();
        })
        .catch(error => {
          console.error('Failed to fetch tickets', error);
        })
        .finally(() => {
          this.loading = false;
        });
    }

  }
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
}


.fullSize {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: radial-gradient(closest-corner, #1d2020, #000000);

}

#top-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

#left-placeholder,
#center-placeholder,
#right-placeholder {
  width: 50px;
  height: 20px;
  background-color: #ccc;
}

.top {
  width: 50px;
  height: 20px;
  background-color: #ccc;
}

#wide-button {
  position: relative;
  display: inline-block;
  width: 65em;
  padding: 10px 20px;
  color: #69d2dd;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: background 0.5s, color 0.5s, box-shadow 0.5s;
  margin-top: 60px;
  margin-bottom: 30px;
  letter-spacing: 4px;
  border: 2px solid #69d2dd;
  background: transparent;
  border-radius: 5px;
}

#wide-button:hover {
  background: #69d2dd;
  color: #fff;
  box-shadow: 0 0 10px #69d2dd, 0 0 20px rgba(3, 233, 244, 0.6),
    0 0 30px rgba(3, 233, 244, 0.4), 0 0 40px rgba(3, 233, 244, 0.2);
}

#wide-button span {
  position: absolute;
  display: block;
}

#wide-button span:nth-child(1) {
  top: 0;
  left: -100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #69d2dd);
  animation: wide-button 1s linear infinite;
}

@keyframes wide-button {
  0% {
    left: -100%;
  }

  50%,
  100% {
    left: 100%;
  }
}

nav {
  margin-top: 15px;
  padding: 10px;
}

#menuToggle {
  display: block;
  position: relative;
  user-select: none;
  cursor: pointer;
}

#menuToggle input {
  display: block;
  width: 40px;
  height: 32px;
  position: absolute;
  top: -7px;
  left: -5px;
  cursor: pointer;
  text-align: left;
  opacity: 0;
  /* hide the checkbox */
  z-index: 2;
  /* ensure the checkbox is above the span elements */
}

#menuToggle span {
  display: block;
  width: 30px;
  height: 3px;
  margin-bottom: 5px;
  position: relative;
  background: #69d2dd;
  border-radius: 3px;
  z-index: 1;
  transform-origin: 4px 0;
  transition: transform 0.5s cubic-bezier(0.77, 0.2, 0.05, 1), background 0.5s cubic-bezier(0.77, 0.2, 0.05, 1),
    opacity 0.55s ease;
}

#menuToggle span:first-child {
  transform-origin: 0% 0%;
}

#menuToggle span:nth-last-child(2) {
  transform-origin: 0% 100%;
}

#menuToggle input:checked~span {
  opacity: 1;
  transform: rotate(-45deg) translate(-5px, -6px);
  background: #69d2dd;
}

#menuToggle input:checked~span:nth-last-child(3) {
  opacity: 0;
  transform: rotate(0deg) scale(0.2, 0.2);
}

#menuToggle input:checked~span:nth-last-child(2) {
  transform: rotate(45deg) translate(-5px, 6px);
}

#menu {
  position: absolute;
  width: 200px;
  margin-top: -33.5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  list-style-type: none;
  padding: 0;
  visibility: hidden;
  transition: opacity 0.2s ease, visibility 0.2s ease;
}

#menuToggle input:checked~ul {
  opacity: 1;
  visibility: visible;
}

#menu a {
  text-decoration: none;
  color: #69d2dd;
  text-align: left;
}

#menu li {
  padding: 15px;
  text-align: center;
}

.search-bar {
  position: absolute;
  margin: auto;
  margin-right: -1.7em;
  margin-top: 1em;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 600px;
  height: 100px;
}

.search-bar .search {
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 50px;
  background: #69d2dd;
  transition: all 1s;
  z-index: 4;
  box-shadow: 0 0 25px 0 rgba(0, 0, 0, 0.4);
}

.search-bar .search:hover {
  cursor: pointer;
}

.search-bar .search::before {
  content: "";
  position: absolute;
  margin: auto;
  top: 22px;
  right: 0;
  bottom: 0;
  left: 22px;
  width: 12px;
  height: 2px;
  background: white;
  transform: rotate(45deg);
  transition: all .5s;
}

.search-bar .search::after {
  content: "";
  position: absolute;
  margin: auto;
  top: -5px;
  right: 0;
  bottom: 0;
  left: -5px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  border: 2px solid white;
  transition: all .5s;
}

.search-bar input {
  font-family: 'Inconsolata', monospace;
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 35px;
  height: 35px;
  outline: none;
  border: none;
  background: #69d2dd;
  color: white;
  text-shadow: 0 0 10px #69d2dd;
  padding: 0 80px 0 20px;
  box-shadow: 0 0 25px 0 #69d2dd, 0 20px 25px 0 rgba(0, 0, 0, 0.2);
  transition: all 1s;
  opacity: 0;
  z-index: 5;
  font-weight: bolder;
  letter-spacing: 0.1em;
}

.search-bar input:hover {
  cursor: pointer;
}

.search-bar input:focus {
  width: 250px;
  right: 250px;
  opacity: 1;
  cursor: text;
}

.search-bar input:focus~.search {
  right: 0px;
  background: #151515;
  z-index: 6;
}

.search-bar input:focus~.search::before {
  top: 0;
  left: 0;
  width: 25px;
}

.search-bar input:focus~.search::after {
  top: 0;
  left: 0;
  width: 25px;
  height: 2px;
  border: none;
  background: white;
  border-radius: 0%;
  transform: rotate(-45deg);
}

.search-bar input::placeholder {
  color: rgb(0, 0, 0);
  opacity: 0.5;
  font-weight: bolder;
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 20px;
  border: 1px solid #ddd;
  z-index: 1000;
  max-width: 400px;
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  opacity: 0;
  animation: fadeIn 0.3s ease-in-out forwards;
}

.popupUser {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background: radial-gradient(closest-corner, #1d2020, #000000);
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.tablePopup {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  border: 2px solid transparent;
  overflow: hidden;
  z-index: 3;
  animation: borderAnimation 10s infinite alternate;
}

.tablePopupTr {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  border: 2px solid transparent;
  overflow: hidden;
  z-index: 3;
  animation: borderAnimation 10s infinite alternate;
}

.popup form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.btn {
  background-color: #5cb85c;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-close {
  background-color: #d9534f;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.form-group {
  margin-bottom: 20px;
}

.btn-primary {
  width: 100%;
  padding: 15px;
  background-color: #69d2dd;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.profile-container {
  display: flex;
  align-items: center;
  max-width: 600px;
  margin: 20px;
  margin-right: 1em;
  padding: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  overflow: hidden;
  z-index: 3;
  background-color: rgba(0, 0, 0, 0.2);
  animation: borderAnimation 10s infinite alternate;
  position: fixed;
  top: 10px;
  right: 10px;
}

.profile-image {
  max-width: 40px;
  margin-right: 20px;
}

.user-info {
  text-align: left;
}

.logged-in-user {
  font-size: 15px;
  font-weight: bold;
  color: #333;
}

.logged-in-user-type {
  font-size: 15px;
  font-weight: bold;
  color: #333;
}

.search-bar input {
  width: 100%;
  max-width: 300px;
}


.btn-secondary {
  background-color: #7f8c8d;
  color: #ecf0f1;
}

.btn-success {
  background-color: #69d2dd;
  color: #ecf0f1;
}

.btn-close {
  position: absolute;
  top: 10px;
  right: 10px;
  transition: transform 0.3s ease-in-out;
  background-color: #7f8c8d;
  color: #ecf0f1;
}

.btn-close:hover {
  transform: scale(1.2);
  /* Adjust the scale factor as needed */
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.spinner {
  border: 6px solid #528388;
  border-top: 6px solid #69d2dd;
  /* Change the color as needed */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
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
  background-color: #69d2dd;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

table {
  width: 100%;
  table-layout: fixed;
}

@keyframes borderAnimation {

  0%,
  100% {
    box-shadow: 0 0 5px rgba(3, 233, 244, 0.8);
  }

  50% {
    box-shadow: 0 0 10px rgba(3, 233, 244, 1);
  }
}

.tbl-header {
  max-width: 1038px;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  border: 2px solid transparent;
  overflow: hidden;
  z-index: 3;
  background-color: #528388;
  animation: borderAnimation 10s infinite alternate;
}

.tbl-content {
  height: 400px;
  overflow-x: auto;
  margin-top: 0px;
  max-width: 1038px;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  border: 2px solid transparent;
  animation: borderAnimation 10s infinite alternate;
}

th {
  padding: 20px 15px;
  text-align: center;
  font-weight: 500;
  font-size: 12px;
  color: #fff;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}


td {
  padding: 15px;
  text-align: center;
  vertical-align: middle;
  font-weight: 300;
  font-size: 12px;
  color: #fff;
  border-bottom: solid 1px rgba(255, 255, 255, 0.1);
}

/* Animated hover effect */
tr {
  transition: background-color 0.3s ease;
}

tr:hover {
  background-color: #5283882e;
  /* Lighter neon light turquoise on hover */
  transition: background-color 0.3s ease;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
}

::-webkit-scrollbar-thumb {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
}
</style>
 
 