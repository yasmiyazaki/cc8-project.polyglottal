<script>
import { Bar } from "vue-chartjs";

export default {
  extends: Bar,
  created() {
    this.$store.commit("createBarChart");
  },
  mounted() {
    const list = this.$store.state.locationList;
    const sortedLocations = Object.keys(list).sort((a, b) => list[b] - list[a]);
    const sortedLocationsNum = Object.values(list).sort((a, b) => b - a);

    this.renderChart(
      {
        labels: sortedLocations,
        datasets: [
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: sortedLocationsNum
          }
        ]
      },
      {
        responsive: true,
        maintainAspectRatio: false
      }
    );
  }
};
</script>