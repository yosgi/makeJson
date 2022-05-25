import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import data from './modules/data'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    data
  },
  getters
})

export default store
