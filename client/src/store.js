import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    apartments: {
      name: [],
      address: [],
      station1: [],
      station2: [],
      station3: [],
      age: [],
      total_floor: [],
      floor: [],
      rent: [],
      admin: [],
      other_cost: [],
      plan: [],
      m2: [],
      url: []
    },
    locations: [],
    locationList: {}
  },
  mutations: {
    setApartments(state, apartments) {
      state.apartments.name = apartments.Name;
      state.apartments.address = apartments.Address;
      state.apartments.station1 = apartments.Station1;
      state.apartments.station2 = apartments.Station2;
      state.apartments.station3 = apartments.Station3;
      state.apartments.age = apartments.age;
      state.apartments.total_floor = apartments["Total Floor"];
      state.apartments.floor = apartments.Floor;
      state.apartments.rent = apartments.Rent;
      state.apartments.admin = apartments.Admin;
      state.apartments.other_cost = apartments["Other Cost"];
      state.apartments.plan = apartments.Plan;
      state.apartments.m2 = apartments.m2;
      state.apartments.url = apartments.url;
      this.commit("getLocations");
      this.commit("createBarChart");
    },
    getLocations(state) {
      for (let index in state.apartments.address) {
        let addressWithoutNum = state.apartments.address[index].replace(
          /[０-９]/g,
          ""
        );
        state.locations.push(addressWithoutNum);
      }
    },
    createBarChart(state) {
      for (let location of state.locations) {
        if (state.locationList[location]) {
          state.locationList[location] += 1;
        } else {
          state.locationList[location] = 1;
        }
      }
    }
  }
});
