<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Area Finder</h1>
        <hr>
        <div>https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&ta=13&bs=040&ekInput=41560&tj=10&nk=-1&ct=15.0&cb=10.0&kz=1&kz=2&et=15&mt=9999999&mb=35&cn=25&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&pc=30</div>
        <br>
        <br>
        <div>
          <form>
            <input @change="setURL" type="text" value="URL">
            <button @click="searchThisURL($event)">Search</button>
          </form>
        </div>
        <br>
        <br>
        <Chart v-if="Object.entries(this.$store.state.locationList).length !== 0"/>
        <PieChart v-if="Object.entries(this.$store.state.locationList).length !== 0"/>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Address</th>
              <th scope="col">Station1</th>
              <th scope="col">Station2</th>
              <th scope="col">Station3</th>
              <th scope="col">age</th>
              <th scope="col">total floor</th>
              <th scope="col">floor</th>
              <th scope="col">rent</th>
              <th scope="col">admin</th>
              <th scope="col">other cost</th>
              <th scope="col">plan</th>
              <th scope="col">m2</th>
              <th scope="col">url</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(name, index) in this.$store.state.apartments.name" :key="index">
              <td>{{ name }}</td>
              <td>{{ $store.state.apartments.address[index] }}</td>
              <td>{{ $store.state.apartments.station1[index] }}</td>
              <td>{{ $store.state.apartments.station2[index] }}</td>
              <td>{{ $store.state.apartments.station3[index] }}</td>
              <td>{{ $store.state.apartments.age[index] }}</td>
              <td>{{ $store.state.apartments.total_floor[index] }}</td>
              <td>{{ $store.state.apartments.floor[index] }}</td>
              <td>{{ $store.state.apartments.rent[index] }}</td>
              <td>{{ $store.state.apartments.admin[index] }}</td>
              <td>{{ $store.state.apartments.other_cost[index] }}</td>
              <td>{{ $store.state.apartments.plan[index] }}</td>
              <td>{{ $store.state.apartments.m2[index] }}</td>
              <td>{{ $store.state.apartments.url[index] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "./Chart";
import PieChart from "./PieChart";

export default {
  name: "List",
  components: {
    Chart,
    PieChart
  },
  data() {
    return {
      searchURL: ""
    };
  },
  methods: {
    getApartList(searchUrl) {
      const path = "http://localhost:5000/list";
      axios
        .get(path, {
          params: {
            URL: searchUrl
          }
        })
        .then(res => {
          // eslint-disable-next-line
          const apartments = JSON.parse(res.data.csv);
          this.$store.commit("setApartments", apartments);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    setURL(e) {
      this.searchURL = e.target.value;
    },
    searchThisURL(e) {
      e.preventDefault();
      this.getApartList(this.searchURL);
    }
  }
};
</script>