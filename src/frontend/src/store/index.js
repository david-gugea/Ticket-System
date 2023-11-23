import { createStore } from "vuex";

import tickets from './modules/tickets';
import users from './modules/users';

export default createStore({
  modules: {
    tickets,
    users,
  }
});