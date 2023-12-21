<template>
  <section>
    <div class="fullSize">
      <div id="top-container">

        <nav role="navigation">
          <div id="menuToggle">
            <!--
            A fake / hidden checkbox is used as click reciever,
            so you can use the :checked selector on it.
            -->
            <input type="checkbox" />
            
            <!--
            Some spans to act as a hamburger.
            
            They are acting like a real hamburger,
            not that McDonalds stuff.
            -->
            <span></span>
            <span></span>
            <span></span>
            
            <!--
            Too bad the menu has to be inside of the button
            but hey, it's pure CSS magic.
            -->
            <ul id="menu">
              <img src="../assets/userAvatar.png" alt="User Profile Image" class="profile-image" />
              <p class="logged-in-user">{{ loggedInUser }}</p>
              <a><li>Users</li></a>
              <a @click="logout"><li>Logout</li></a>
            </ul>
          </div>
        </nav>

        <div class="user-profile" @mouseover="showProfileDropdown = true" @mouseleave="showProfileDropdown = false">
          <button ref="userButton" @click="openUserPopup">Users</button>
          <img src="../assets/userAvatar.png" alt="User Profile Image" class="profile-image" />
          <p class="logged-in-user">User: <span>{{ loggedInUser }}</span></p>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">

          <!-- Search Bar Section -->
          <div class="search-bar">
            <input type="text" v-model="searchQuery" placeholder="Search..." @input="filterTable">
            <div class="search"></div>
          </div>
        </div>

        

        <!-- User Profile Dropdown -->
        <div v-if="showProfileDropdown" class="profile-dropdown">
          <!-- Add more user-related options as needed -->
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    
    <button id="wide-button" @click="openPopup" :class="{ 'hover-effect': hover }">+</button>

    <div id="table-container" class="table-container">
      <table>
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
            <td><button @click="closeTicket(ticket)" :disabled="ticket.done" class="btn btn-sm btn-primary">Close</button>
            </td>
            <td>
              <button @click="editTicket(ticket)" class="btn btn-sm btn-primary">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
    <!-- Pop-up form -->
    <div v-if="isPopupVisible" class="popup">
      <form @submit.prevent="createTicket">
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" id="description" v-model="newTicket.description" required></textarea>
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
            <table class="tablePopup">
              <thead>
                <tr class="tablePopupTr">
                  <th>User ID</th>
                  <th>User Name</th>
                  <th>User Type</th>
                  <th>New Role</th>
                  <th>Edit</th>
                </tr>
              </thead>
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

                  <td>
                    <button @click="updateUser(user)" class="btn btn-sm btn-primary">User</button>
                  </td>
                </tr>


              </tbody>
            </table>
          </div>
        </div>
        <div class="button-group">
          <button @click="updateUser" class="btn btn-success">Create Ticket</button>
          <button @click="closeUserPopup" type="button" class="btn-close" data-dismiss="modal" aria-label="Close">
          </button>
        </div>
      </form>
    </div>


    <!-- Edit Ticket Popup -->
    <div v-if="selectedTicket" class="popup">
      <form>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" v-model="selectedTicket.description" required></textarea>
        </div>

        <div class="button-group">
          <button @click.prevent="updateTicket(ticket)" class="btn btn-sm btn-primary">Update Ticket</button>
          <button @click.prevent="closePopup" class="btn btn-sm btn-secondary">Cancel</button>
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
      searchQuery: '',
      filteredTickets: [],
      showProfileDropdown: false,
    };
  },


  methods: {
    logout() {
      localStorage.removeItem('loggedInUser');
      localStorage.removeItem('loggedInUserID');
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

    } else if(userType === "developer"){

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
* {
  margin: 0;
  padding: 0;
}

.fullSize {
  min-height: 100vh;
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
  width: 90%;
  max-width: 800px;
  padding: 5px;
  background-color: #03e9f4;
  color: white;
  border: none;
  border-radius: 5px;
  margin-top: 100px;
  margin-bottom: 1em;
  transition: background-color 0.3s;
  position: relative;
  overflow: hidden;
}

#wide-button:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #fff;
  opacity: 0.5;
  transform: translate(-50%, -50%) rotate(45deg);
  transition: opacity 0.3s;
}

#wide-button:hover:before {
  opacity: 0;
}



#wide-button:hover {
  background: #03e9f4;
  color: #fff;
  box-shadow: 0 0 10px rgba(3, 233, 244, 0.8), 0 0 20px rgba(3, 233, 244, 0.6),
    0 0 30px rgba(3, 233, 244, 0.4), 0 0 40px rgba(3, 233, 244, 0.2);
}

.profile-dropdown {
  position: absolute;
  top: 70px;
  right: 0;
  margin-left: 10%;
  background-color: #292b2c;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  position: absolute;
  z-index: 1000;
}

.profile-dropdown button {
  padding: 10px;
  width: 100%;
  text-align: left;
  border: none;
  background-color: transparent;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.profile-dropdown button:hover {
  background-color: #333;
}


#menuToggle
{
  display: block;
  position: relative;
  top: 20px;
  left: 30px;
  
  z-index: 1;
  
  -webkit-user-select: none;
  user-select: none;
}

#menuToggle a
{
  text-decoration: none;
  color: #fff;
  
  transition: color 0.3s ease;
}

#menuToggle a:hover
{
  color: #03e9f4;
}


#menuToggle input
{
  display: block;
  width: 40px;
  height: 32px;
  position: absolute;
  top: -7px;
  left: -5px;
  
  cursor: pointer;
  
  opacity: 0; /* hide this */
  z-index: 2; /* and place it over the hamburger */
  
  -webkit-touch-callout: none;
}

/*
 * Just a quick hamburger
 */
#menuToggle span
{
  display: block;
  width: 33px;
  height: 4px;
  margin-bottom: 5px;
  position: relative;
  
  background: #cdcdcd;
  border-radius: 3px;
  
  z-index: 1;
  
  transform-origin: 4px 0px;
  
  transition: transform 0.5s cubic-bezier(0.77,0.2,0.05,1.0),
              background 0.5s cubic-bezier(0.77,0.2,0.05,1.0),
              opacity 0.55s ease;
}

#menuToggle span:first-child
{
  transform-origin: 0% 0%;
}

#menuToggle span:nth-last-child(2)
{
  transform-origin: 0% 100%;
}

/* 
 * Transform all the slices of hamburger
 * into a crossmark.
 */
#menuToggle input:checked ~ span
{
  opacity: 1;
  transform: rotate(45deg) translate(-2px, -1px);
  background: #03e9f4;
}

/*
 * But let's hide the middle one.
 */
#menuToggle input:checked ~ span:nth-last-child(3)
{
  opacity: 0;
  transform: rotate(0deg) scale(0.2, 0.2);
}

/*
 * Ohyeah and the last one should go the other direction
 */
#menuToggle input:checked ~ span:nth-last-child(2)
{
  transform: rotate(-45deg) translate(0, -1px);
}

/*
 * Make this absolute positioned
 * at the top left of the screen
 */
#menu
{
  position: absolute;
  width: 300px;
  margin: -100px 0 0 -60px;
  padding: 50px;
  padding-top: 60px;
  
  background: #1d2020,;
  list-style-type: none;
  -webkit-font-smoothing: antialiased;
  /* to stop flickering of text in safari */
  
  transform-origin: 0% 0%;
  transform: translate(-100%, 0);
  
  transition: transform 0.5s cubic-bezier(0.77,0.2,0.05,1.0);
}

#menu li
{
  padding: 10px 0;
  font-size: 22px;
}

/*
 * And let's slide it in from the left
 */
#menuToggle input:checked ~ ul
{
  transform: none;
}

.user-profile {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  background-color: #292b2c;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.profile-image {
  width: 40px;
  height: 40px;
  right: 10px;
  border-radius: 50%;
  margin-right: 10px;
}

.logged-in-user {
  font-size: 16px;
  color: #555;
  margin: 0;
}

.logged-in-user span {
  color: #03e9f4;
  font-weight: bold;
}

.search-bar {
  position: absolute;
  margin: auto;
  margin-right: 15em;
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
  background:#03e9f4;
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
  background:#03e9f4;
  color: white;
  text-shadow: 0 0 10px#03e9f4;
  padding: 0 80px 0 20px;
  box-shadow: 0 0 25px 0 #03e9f4, 0 20px 25px 0 rgba(0, 0, 0, 0.2);
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
  right:250px;
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

.table-container {
  display: flex;
  justify-content: center;
  align-items: center;

}

table {
  width: 80%;
  /* Adjust this to control the width of the table */
}

.popupUser {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.tablePopup {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.tablePopupTr {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
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
  background-color: #68d2df;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
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
    margin-top: 10px;
    width: 100%;
    border-collapse: collapse;

  }

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  #table-container {
    margin: 20px;
    justify-content: center;
    align-items: center;
  }

  .user-profile {
    top: 10px;
    right: 10px;
  }

  .search-bar input {
    width: 100%;
    max-width: 300px;
  }
}

.btn-secondary {
  background-color: #7f8c8d;
  color: #ecf0f1;
}

.btn-success {
  background-color: #68d2df;
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



th,
td {
  border: 1px solid #333;
  padding: 15px;
  text-align: left;
  background-color: #292b2c;
  color: white;
}

th {
  position: sticky;
  top: 0;
  background-color: #292b2c;
  color: white;
  z-index: 1;

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
  border: 6px solid rgba(255, 255, 255, 0.3);
  border-top: 6px solid #03e9f4;
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
  background-color: #03e9f4;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

@media screen and (max-width: 600px) {
  table {
    width: 100%;
  }

  th,
  td {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }
}

body {
  margin: 0;
  background-color: black;
  overflow: hidden;
}

.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(closest-corner, #1d2020, #000000);
  z-index: -1;
}
</style>
 
 