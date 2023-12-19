<template>
  <section>
  <div class="fullSize">
    <div id="top-container">
      <div class="user-profile" @mouseover="showProfileDropdown = true" @mouseleave="showProfileDropdown = false">
        <button ref="userButton" @click="openUserPopup">Users</button>
        <img src="../assets/userAvatar.png" alt="User Profile Image" class="profile-image" />
        <p class="logged-in-user">User: <span>{{ loggedInUser }}</span></p>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">



        <!-- User Profile Dropdown -->
        <div v-if="showProfileDropdown" class="profile-dropdown">
          <!-- Add more user-related options as needed -->
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
      <!-- Search Bar Section -->
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Search..." @input="filterTable">
      </div>
    </div>

    <div id="table-container">
      <button id="wide-button" @click="openPopup" :class="{ 'hover-effect': hover }"></button>
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


    <div v-if="users" class="popupUser">
      <form @submit.prevent="createTicket">
        <div class="form-group">
          <div id="table-container">
            <table class="tablePopup">
              <thead>
                  <tr class="tablePopupTr">
                      <th>User ID</th>
                      <th>User Name</th>
                      <th>User Type</th>
                      <th></th>
                  </tr>
              </thead>
              <tbody>
                  <tr class="tablePopupTr">
                      <td>Data 1</td>
                      <td>Data 2</td>
                      <td>Data 3</td>
                  </tr>
                  <tr class="tablePopupTr">
                      <td>Data 4</td>
                      <td>Data 5</td>
                      <td>Data 6</td>
                  </tr>
                  <tr class="tablePopupTr">
                    <td>Data 4</td>
                    <td>Data 5</td>
                    <td>Data 6</td>
                </tr>
                <tr class="tablePopupTr">
                  <td>Data 4</td>
                  <td>Data 5</td>
                  <td>Data 6</td>
              </tr>
              <tr class="tablePopupTr">
                <td>Data 4</td>
                <td>Data 5</td>
                <td><button>Edit</button></td>
            </tr>
           
              </tbody>
          </table>
          </div>
        </div>
        <div class="button-group">
          <button type="submit" class="btn btn-success">Create Ticket</button>
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
      loading: false,
      isPopupVisible: false,
      hover: false,
      users:false,
      selectedTicket: null,
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

    openUserPopup(){
      this.users = true;
    },

    closeUserPopup(){
      this.users = false;
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
    },
  },
  mounted() {
    const newUserID = localStorage.getItem('loggedInUserID');
    this.loggedInUser = localStorage.getItem('loggedInUser');
    const username = localStorage.getItem('loggedInUserType');
    this.loading = true;
    if(username === "admin"){
     
     
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
      userButton.style.display= 'none'
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
*{
  margin: 0;
  padding: 0;
}
.fullSize{
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

#table-container {
  margin: 20px;

}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

#wide-button {
  width: 97%;
  padding: 15px;
  background-color: #68d2df;
  color: white;
  border: none;
  border-radius: 5px;
  margin-bottom: 10px; /* Adjust this value to control the space */
  transition: background-color 0.3s;
}


#wide-button:before {
  content: "+";
  position: absolute;
  top: 50%;
  left: 50%;
  
  /* Adjust the scale for a larger plus */
  opacity: 0.5;

}

#wide-button:hover {
  background-color: #57b0c9; /* Change this color to your desired hover color */
}




.box-menu {
  position: absolute;
  left: 50px;
  top: 50px;
  cursor: pointer;
  background: #eba440;
  width: 60px;
  height: 60px;
  box-shadow: 2px 3px 5px rgba(0, 0, 0, .3);
  border-radius: 60px;
  transition: height .4s;
}

.full-menu {
  height: 300px;
}

.wrapper {
  position: relative;
  width: 60px;
  height: 60px;
}

.hamburger {
  position: absolute;
  left: 22px;
  top: 22px;
  width: 16px;
  height: 16px;
}

.hamburger span {
  position: absolute;
  display: inline-block;
  height: 2px;
  width: 100%;
  background: #050d4b;
  border-radius: 10px;
  transition: all .3s;
}

.hamburger span:nth-child(1) {
  top: 3px;
}

.hamburger span:nth-child(2) {
  top: 8px;
}

.hamburger span:nth-child(3) {
  top: 8px;
}

.hamburger span:nth-child(4) {
  top: 13px;
}

.hamburger.active span:nth-child(1) {
  width: 0;
  margin-left: 8px;
}

.hamburger.active span:nth-child(2) {
  transform: rotate(45deg);
}

.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg);
}

.hamburger.active span:nth-child(4) {
  width: 0;
  margin-left: 8px;
}

.menu {
  position: relative;
  left: -9999px;
}

.menu a {
  white-space: nowrap;
  position: relative;
  display: inline-block;
  color: #333;
  text-decoration: none;
  width: 150px;
  height: 58px;
  line-height: 58px;
  font-family: Ubuntu;
}

.menu a::after {
  content: '';
  position: absolute;
  left: 50px;
  width: 15px;
  background: #e1a754;
  transition: height .3s, top .3s;
  transform: rotateZ(43deg);
}

.menu a.active::after {
  top: 19px;
  height: 20px;
}

.menu a span {
  opacity: 0;
  display: inline-block;
  font-size: 14px;
}

.menu a span.icon {
  transform: scale(.5);
  color: #050d4b;
  font-size: 18px;
  display: inline-block;
  width: 60px;
  text-align: center;
  transition: transform .3s;
}

.menu a span.text {
  text-shadow: 1px 1px 0px rgba(0, 0, 0, 0.3);
  opacity: 0;
  margin-left: 40px;
  color: #eba440;
  transition: margin .3s, opacity .3s, transform .3s;
}

.full-menu .menu {
  left: 0;
}

.full-menu .menu a:hover span {
  opacity: 1;
}

.full-menu .menu a span {
  opacity: .8;
}

.full-menu .menu a span.icon {
  transform: scale(1.1);
}

.full-menu .menu a span.text {
  margin-left: 25px;
}

.full-menu .menu a:hover span.text {
  transform: translateX(5px);
  transition-delay: 0s;
}

.menu a:nth-child(1) span {
  transition: all .5s .1s, opacity .5s 0s, transform .5s 0s;
}

.menu a:nth-child(2) span {
  transition: all .5s .15s, opacity .5s 0s, transform .5s 0s;
}

.menu a:nth-child(3) span {
  transition: all .5s .2s, opacity .5s 0s, transform .5s 0s;
}

.menu a:nth-child(4) span {
  transition: all .5s .25s, opacity .5s 0s, transform .5s 0s;
}

.round-luxury-button {
  position: absolute;
  display: flex;
  top: 1px;

  width: 96%;
  border-radius: 4px;
  height: 30px;
  font-size: 20px;
  font-weight: lighter;
  color: #fff;
  text-align: right;
  text-decoration: none;
  border: none;
  background-color: #68d2df;
  box-shadow: 0 3px 9px rgba(0, 0, 0, 0.2);
  transition: background-color 0.6s, transform 0.6s, box-shadow 0.6s;

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
  border-radius: 50%;
  margin-right: 10px;
}

.logged-in-user {
  font-size: 16px;
  color: #555;
  margin: 0;
}

.logged-in-user span {
  color: #68d2df;
  font-weight: bold;
}

.search-bar {
  display: flex;
  margin-top: 2%;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  width: 300px;
  /* Adjust width as needed */
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
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


.popupUser{
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

.tablePopup{
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.tablePopupTr{
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

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10%;
  overflow: auto;
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
  border-top: 6px solid #68d2df;
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
  background-color: #68d2df;
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
}</style>
 
 