<template>
  <section id="main">

    <!-- Main container -->
    <div class="fullSize">

      <!-- Top container with navigation -->
      <div id="top-container">
        <nav>

          <!-- Logo -->
          <div class="logo">
            <img ref="logo" class="logo" alt="Logo" src="../assets/logo_title.png">
          </div>

          <!-- Navigation menu -->
          <ul class="menu">

            <!-- User profile dropdown -->
            <li>
              <div class="dropdown">
                <button class="dropbtn" @click="openUserPopup">
                  <div class="profile-container">
                    <img src="../assets/userAvatar.png" alt="User Profile Image" class="profile-image" />
                    <div class="user-info">
                      <p class="logged-in-user">User: <span id="usernamePlaceholder">{{ loggedInUser }}</span></p>
                      <p class="logged-in-user-type">User type: <span id="userTypePlaceholder">{{ loggedInUserType
                      }}</span></p>
                    </div>
                  </div>
                </button>

                <!-- Dropdown content -->
                <div class="dropdown-content animated-btn">
                  <a ref="userButton" @click="openUserPopup">Users</a>
                  <a @click="logout">Logout</a>
                </div>
              </div>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Search Bar -->
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Description..." @input="filterTable">
        <div class="search"></div>
      </div>

      <!-- Button and Table Box -->
      <div class="btnTableBox">
        <button id="wide-button" @click="openPopup" :class="{ 'hover-effect': hover }">+</button>

        <!-- Table Container -->
        <div class="table-container">
          <div class="tbl-header">
            <table cellpadding="0" cellspacing="0" border="0">
              <thead>
                <!-- Table Rows -->
                <tr>
                  <!-- Table Columns -->
                  <th>ID</th>
                  <th>Description</th>
                  <th>Date Created</th>
                  <th>Date Closed</th>
                  <th>Created By</th>
                  <th>Closed By</th>
                  <th>User ID</th>
                  <th>Done</th>
                  <th></th>
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
                  <td>
                    <button @click="closeTicket(ticket)" :disabled="ticket.done"
                      class="closeTicketBtn animated-btn">Close</button>
                  </td>
                  <td>
                    <button @click="editTicket(ticket)" class="edit" type="button"><span
                        class="edit-icon"></span><span></span></button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Pop-up form for creating a ticket -->
    <div v-if="isPopupVisible" class="popup">
      <form @submit.prevent="createTicket">
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" id="description" v-model="newTicket.description"
            oninvalid="this.setCustomValidity('Please fill out this field.')" required></textarea>
        </div>

        <!-- Button group for Create Ticket and Close -->
        <div class="button-group">
          <button type="submit" class="createTicketBtn animated-btn">Create Ticket</button>
          <button @click.prevent="closePopup" type="button" class="btn-close" data-dismiss="modal" aria-label="Close">
          </button>
        </div>
      </form>
    </div>

    <!-- Pop-up form for managing user data -->
    <div class="popup" v-if="userDataPopup">
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
                      <select v-model="user.updatedUserType" class="dark-background-select">
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

        <!-- Button group for closing the user data popup -->
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
        <!-- Button group for Update Ticket, Delete Ticket, and Close -->
        <div class="button-group">
          <button @click.prevent="closePopup" type="button" class="btn-close" data-dismiss="modal"
            aria-label="Close"></button>
          <button type="submit" class="updatebtn">
            <span class="text">Update</span>
            <span class="icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M20 6.7l-9.3 9.3-4-4L2 12l7 7 13-13z" />
              </svg>
            </span>
          </button>
          <br>
          <button @click.prevent="deleteTicket" class="deletebtn"><span class="text">Delete</span><span class="icon"><svg
                xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path
                  d="M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206 8.313 3.666 3.666 8.237-8.318 8.285 8.203z">
                </path>
              </svg></span></button>
        </div>
      </form>
    </div>

    <!-- Loading Spinner -->
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
      // Data properties for managing tickets and user data
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
    // Method to handle user logout
    logout() {
      localStorage.removeItem('loggedInUser');
      localStorage.removeItem('loggedInUserID');
      localStorage.removeItem('loggedInUserType');
      this.$router.push('/');
    },
    // Method to create a new ticket
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
    // Method to filter tickets based on search query
    filterTable() {
      // Filter the table based on the searchQuery
      this.filteredTickets = this.tickets.filter(ticket =>
        ticket.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    // Method to open user data popup
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
    // Method to close user data popup
    closeUserPopup() {
      this.userDataPopup = false;
    },
    // Method to update user information
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
    // Method to close a ticket
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
    // Method to edit a ticket
    editTicket(ticket) {
      this.selectedTicket = { ...ticket };
      this.openPopup();
    },
    // Method to update ticket information
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
    // Method to delete a ticket
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
    // Method to save data to local storage
    saveDataToLocalStorage() {
      localStorage.setItem('tickets', JSON.stringify(this.tickets));
    },
    // Method to load data from local storage
    loadDataFromLocalStorage() {
      const storedTickets = localStorage.getItem('tickets');
      if (storedTickets) {
        this.tickets = JSON.parse(storedTickets);
      }
    },
    // Method to format date for display
    formatDate(dateString) {
      if (dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
      }
      return '-';
    },
    // Method to open the ticket popup
    openPopup() {
      this.isPopupVisible = true;
    },
    // Method to close the ticket popup
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
  margin: 0px;
  padding: 0px;
  font-family: "Asap", sans-serif;
}

* {
  box-sizing: border-box;
  scroll-behavior: smooth;
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

.btnTableBox {
  padding-top: 3em;
}

#top-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

ul {
  list-style: none;
}

a {
  text-decoration: none;
}

/*Navigation*/
nav {
  padding-bottom: 9em;
  padding-right: 17em;
  left: 0;
  display: inline-flex;
  justify-content: space-around;
  align-items: center;
  height: 80px;
  width: 100%;
  position: fixed;
  z-index: 1;
  background: #000000;
  box-shadow: 0px 1px 2px rgba(3, 233, 244, 0.6),
    0px 2px 4px rgba(3, 233, 244, 0.6),
    0px 4px 8px rgba(3, 233, 244, 0.6),
    0px 8px 16px rgba(3, 233, 244, 0.6);
}

.logo {
  position: fixed;
  display: flex;
  height: 50px;
  width: auto;
  display: flex;
  padding-right: 82em;
  margin-top: 4.25em;

}

.dark-background-select {
  background-color: #333;
  color: white;
  border: solid #528388;
  box-shadow: 0 0 10px #69d2dd;

  &:hover {
    background-color: #555;
    /* Replace with the hover background color */
  }
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropbtn {
  background-color: #333;
  color: #fff;
  padding: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.dropdown-content {
  display: none;
  position: absolute;
  margin-top: 9.1em;
  margin-left: 43em;
  border: 1px solid;
  background-color: #528388;
  min-width: 200px;
  cursor: pointer;
  box-shadow: 0 0 10px #69d2dd;
  z-index: 1;
}

.animated {
  transition: transform 0.3s ease-in-out;
}

.animated:hover {
  transform: scale(1.1);
}

.dropdown-content a {
  color: #ffffff;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.profile-container {
  position: fixed;
  display: flex;
  align-items: center;
  max-width: 600px;
  margin: 20px;
  margin-right: 1em;
  margin-top: 0.3em;
  padding: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 3;
  background-color: rgba(0, 0, 0, 0.2);
  position: fixed;
  top: 10px;
  right: 10px;
}

.profile-image {
  max-width: 40px;
  margin-right: 20px;
  margin-bottom: 1em;
}

.user-info {
  text-align: left;
  margin-bottom: 1em;
  display: flex;
  flex-direction: column;
}

.logged-in-user,
.logged-in-user-type {
  font-size: 14px;
  font-weight: bold;
  color: #fff;
  margin: 0;
}

#left-placeholder,
#center-placeholder,
#right-placeholder {
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
  margin-top: 80px;
  margin-bottom: 10px;
  letter-spacing: 4px;
  border: 2px solid #69d2dd;
  background: transparent;
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

.table-container {
  margin-top: 1em;
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

.search-bar {
  position: absolute;
  display: flex;
  margin: auto;
  margin-left: 60.5em;
  margin-top: 1.5em;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 600px;
  height: 30px;
}

.search-bar input {
  width: 100%;
  max-width: 300px;
}

.search-bar .search {
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 40px;
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
  max-width: 1000px;
  width: 100%;
  color: #69d2dd;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  opacity: 0;
  animation: fadeIn 0.3s ease-in-out forwards;
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background: radial-gradient(closest-corner, #1d2020, #000000);
  border: solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}


.tablePopupTr {
  padding: 8px;
  text-align: left;
  overflow: hidden;
  z-index: 3;
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

.edit {
  background: #00000000;
  color: #fff;
  cursor: pointer;
  font-size: 25px;
  height: 40px;
  line-height: 40px;
  outline: none;
  padding: 0;
  padding-right: 10px;
  position: relative;
  -webkit-transition: background .4s;
  transition: background .4s;
}

.edit span {
  display: inline-block;
  float: left;
}

.edit .edit-icon {
  height: 40px;
  position: relative;
  width: 40px;
}

.edit .edit-icon:before {
  border: 3px solid #fff;
  content: "";
  display: inline-block;
  height: 50%;
  left: 50%;
  position: absolute;
  top: 50%;
  width: 50%;
  transform: translate(-50%, -50%);
}

.edit .edit-icon:after {
  background: #69d2dd;
  border: 2px #fff solid;
  border-bottom-left-radius: 5px 15px;
  border-bottom-right-radius: 5px 15px;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  box-shadow: 0 0 0 2px #69d2dd;
  content: "";
  display: inline-block;
  height: 55%;
  position: absolute;
  top: 7%;
  left: 45%;
  width: 6px;
  transform: translate(0, 0) rotate(45deg);
  transform-origin: 50% 75%;
  transition: background .4s, box-shadow .4s;
}

.edit:hover span:after {
  background: #69d2dd;
  box-shadow: 0 0 0 2px #69d2dd;
  animation: wiggle .25s 3 linear;
}

@keyframes wiggle {
  0% {
    transform: translate(0, 0) rotate(45deg);
  }

  25% {
    transform: translate(0, 0) rotate(25deg);
  }

  50% {
    transform: translate(0, 0) rotate(45deg);
  }

  75% {
    transform: translate(0, 0) rotate(65deg);
  }

  100% {
    transform: translate(0, 0) rotate(45deg);
  }
}

.updatebtn {
  width: 165px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  background: rgba(255, 0, 0, 0);
  border: solid #36ff65;
  box-shadow: 0 0 5px #69d2dd;
  background: #e6222200;
}

.updatebtn,
.updatebtn span {
  transition: 200ms;
}

.updatebtn .text {
  transform: translateX(35px);
  color: white;
  font-weight: bold;
}

.updatebtn .icon {
  position: absolute;
  border-left: 1px solid #36ff6565;
  transform: translateX(110px);
  height: 40px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.updatebtn svg {
  width: 50px;
  fill: #eee;
}

.updatebtn:hover {
  background: #36ff65a6;
}

.updatebtn:hover .text {
  color: transparent;
}

.updatebtn:hover .icon {
  width: 150px;
  border-left: none;
  transform: translateX(0);
}

.updatebtn:focus {
  outline: none;
}

.updatebtn:active .icon svg {
  transform: scale(0.8);
}

.deletebtn:active .icon svg {
  transform: scale(0.8);
}

.deletebtn {
  width: 165px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  background: rgba(255, 0, 0, 0);
  border: solid red;
  box-shadow: 0 0 5px red;
  background: #e6222200;
}

.deletebtn,
.deletebtn span {
  transition: 200ms;
}

.deletebtn .text {
  transform: translateX(35px);
  color: white;
  font-weight: bold;
}

.deletebtn .icon {
  position: absolute;
  border-left: 1px solid #c41b1b71;
  transform: translateX(110px);
  height: 40px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.deletebtn svg {
  width: 15px;
  fill: #eee;
}

.deletebtn:hover {
  background: #ff3636;
}

.deletebtn:hover .text {
  color: transparent;
}

.deletebtn:hover .icon {
  width: 150px;
  border-left: none;
  transform: translateX(0);
}

.deletebtn:focus {
  outline: none;
}

.deletebtn:active .icon svg {
  transform: scale(0.8);
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.createTicketBtn {
  display: inline-block;
  margin-bottom: 0.3em;
  padding: 5px 10px;
  font-size: 15px;
  text-align: center;
  text-decoration: none;
  outline: none;
  border: 1px solid;
  background-color: #69d1dd00;
  color: #69d2dd;
  cursor: pointer;
  box-shadow: 0 0 10px #69d2dd;
}

.closeTicketBtn {
  display: inline-block;
  margin-bottom: 0.3em;
  padding: 5px 10px;
  font-size: 15px;
  text-align: center;
  text-decoration: none;
  outline: none;
  border: 1px solid;
  background-color: #69d1dd00;
  color: #69d2dd;
  cursor: pointer;
  box-shadow: 0 0 10px #69d2dd;
}

.animated-btn {
  transition: transform 0.3s ease-in-out;
}

.animated-btn:hover {
  transform: scale(1.1);
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
.btn-close {
  position: absolute;
  background-color: hsla(186, 63%, 64%, 0.73);
  top: 10px;
  right: 10px;
  transition: transform 0.3s ease-in-out;
  color: #ecf0f1;
}

.btn-close:hover {
  transform: scale(1.2);

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
  margin-top: 1em;
  border: 1px solid transparent;
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
}

th {
  padding: 20px 15px;
  text-align: center;
  font-weight: 500;
  font-size: 13px;
  color: #fff;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}


td {
  padding: 15px;
  text-align: center;
  vertical-align: middle;
  font-weight: 300;
  font-size: 13px;
  color: #fff;
  border-bottom: solid 1px rgba(255, 255, 255, 0.1);
}

tr {
  transition: background-color 0.3s ease;
}

tr:hover {
  background-color: #5283882e;
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
 
 