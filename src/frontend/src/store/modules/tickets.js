import axios from 'axios';

const state = {
  tickets: null,
  ticket: null
};

const getters = {
  stateTickets: state => state.tickets,
  stateTicket: state => state.ticket,
};

const actions = {
  async createTicket({dispatch}, ticket) {
    await axios.post('ticket', ticket);
    await dispatch('getTickets');
  },
  async getTickets({commit}) {
    let {data} = await axios.get('tickets');
    commit('setTickets', data);
  },
  async viewTicket({commit}, id) {
    let {data} = await axios.get(`ticket/${id}`);
    commit('setTicket', data);
  },
  // eslint-disable-next-line no-empty-pattern
  async updateTicket({}, ticket) {
    await axios.patch(`ticket/${ticket.id}`, ticket.form);
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteTicket({}, id) {
    await axios.delete(`ticket/${id}`);
  }
};

const mutations = {
  setTickets(state, tickets){
    state.tickets = tickets;
  },
  setNote(state, ticket){
    state.ticket = ticket;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};