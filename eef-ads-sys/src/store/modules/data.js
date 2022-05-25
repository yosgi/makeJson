import { getData } from "@/api/data"
const state = {
  data: null
}

const mutations = {
  SET_DATA: (state, data) => {
    state.data = data;
  },
  UPDATE_CAMPAIGN: (state, data) => {
    state.data.campaigns[data.id] = data.data;
  },
  ADD_CAMPAIGN: (state, data) => {
    state.data.campaigns.unshift(data);
  },
  UPDATE_ZONE: (state, data) => {
    state.data.zones[data.id] = data.data;
  },
  ADD_ZONE: (state, data) => {
    state.data.zones.unshift(data);
  },
  UPDATE_BANNER: (state, data) => {
    state.data.banners[data.id] = data.data;
  },
  ADD_BANNER: (state, data) => {
    state.data.banners.unshift(data);
  },
}

const actions = {
  getData({ commit, state }) {
    return new Promise((resolve, reject) => {
      getData().then(response => {
        const data = response
        commit('SET_DATA', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateCampaign({commit, state}, data) {
    commit('UPDATE_CAMPAIGN', data)
  },
  addCampaign({commit, state}, data) {
    commit('ADD_CAMPAIGN', data)
  },
  updateZone({commit, state}, data) {
    commit('UPDATE_ZONE', data)
  },
  addZone({commit, state}, data) {
    commit('ADD_ZONE', data)
  },
  updateBanner({commit, state}, data) {
    commit('UPDATE_BANNER', data)
  },
  addBanner({commit, state}, data) {
    commit('ADD_BANNER', data)
  },
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
