<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Apartments</h1>
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
            <tr v-for="(apartment, index) in name" :key="index">
              <td>{{ apartment }}</td>
              <td>{{ address[index] }}</td>
              <td>{{ station1[index] }}</td>
              <td>{{ station2[index] }}</td>
              <td>{{ station3[index] }}</td>
              <td>{{ age[index] }}</td>
              <td>{{ total_floor[index] }}</td>
              <td>{{ floor[index] }}</td>
              <td>{{ rent[index] }}</td>
              <td>{{ admin[index] }}</td>
              <td>{{ other_cost[index] }}</td>
              <td>{{ plan[index] }}</td>
              <td>{{ m2[index] }}</td>
              <td>{{ url[index] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "List",
  data() {
    return {
      searchURL: "",
      books: [],
      apartments: [],
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
          this.apartments = JSON.parse(res.data.csv);
          this.name = this.apartments.Name;
          this.address = this.apartments.Address;
          this.station1 = this.apartments.Station1;
          this.station2 = this.apartments.Station2;
          this.station3 = this.apartments.Station3;
          this.age = this.apartments.age;
          this.total_floor = this.apartments["Total Floor"];
          this.floor = this.apartments.Floor;
          this.rent = this.apartments.Rent;
          this.admin = this.apartments.Admin;
          this.other_cost = this.apartments["Other Cost"];
          this.plan = this.apartments.Plan;
          this.m2 = this.apartments.m2;
          this.url = this.apartments.url;
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