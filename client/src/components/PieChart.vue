<script>
import { Pie } from "vue-chartjs";

export default {
  extends: Pie,
  created() {
    this.$store.commit("createBarChart");
  },
  mounted() {
    const list = this.$store.state.locationList;
    const sortedLocations = Object.keys(list).sort((a, b) => list[b] - list[a]);
    const sortedLocationsNum = Object.values(list).sort((a, b) => b - a);
    const backcolors = sortedLocationsNum.map(() => {
      function getRandomColor() {
        const letters = "0123456789ABCDEF";
        let colorPick = "#";
        for (let i = 0; i < 6; i++) {
          colorPick += letters[Math.floor(Math.random() * 16)];
        }
        return colorPick;
      }
      return getRandomColor();
    });
    // eslint-disable-next-line
    console.log(backcolors);

    this.renderChart(
      {
        labels: sortedLocations,
        datasets: [
          {
            label: "Data One",
            backgroundColor: backcolors,
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