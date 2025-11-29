<template>
  <admin-nav-bar></admin-nav-bar>
  <new-base-card>
    <form
      class="form-inline my-2 my-lg-0"
      @submit.prevent="getDataAndFillChart"
    >
      <input
        class="form-control mr-sm-2"
        type="date"
        placeholder="search by patient Id"
        aria-label="Search"
        v-model="date"
      />
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">
        See Analytics
      </button>
    </form>
    <div class="alert alert-danger mt-3" v-if="error">{{ error }}</div>
    <canvas id="planet-chart"></canvas>
  </new-base-card>
</template>
<script>
import Chart from 'chart.js';
import axios from 'axios';
//import planetChartData from '../../../services/chart-data.js';
export default {
  data() {
    return {
      date: '2026-11-26',
      time: [],
      doctors: [],
      patients: [],
      appointments: [],
      planetChartData: null,
      chartInstance: null,
      error: ''
    };
  },
  mounted() {
    if (this.date) {
      this.getDataAndFillChart();
    }
  },
  methods: {
    getDataAndFillChart() {
      this.error = '';
      this.getData()
        .then(() => {
          this.fillData();
          this.createChart('planet-chart', this.planetChartData);
        })
        .catch(err => {
          this.error = err?.response?.data?.message || 'Unable to load analytics';
        });
    },
    fillData() {
      this.planetChartData = {
        type: 'line',
        data: {
          labels: this.time,
          datasets: [
            {
              // one line graph
              label: 'Number of Doctors',
              data: this.doctors,
              backgroundColor: 'rgba(255, 255, 0, 0.2)',
              borderColor: 'yellow',
              pointBackgroundColor: 'orange',
              borderWidth: 1,
              pointBorderColor: 'orange'
            },
            {
              // another line graph
              label: 'Number of Patients',
              data: this.patients,
              backgroundColor: 'rgba(255, 0, 0, 0.2)',
              borderColor: 'lightpink',
              pointBackgroundColor: 'red',
              borderWidth: 1,
              pointBorderColor: 'red'
            },
            {
              // another line graph
              label: 'Number of Appointments',
              data: this.appointments,
              backgroundColor: 'rgba(0, 0, 255, 0.2)',
              borderColor: 'lightblue',
              pointBackgroundColor: 'blue',
              borderWidth: 1,
              pointBorderColor: 'blue'
            }
          ]
        },
        options: {
          responsive: true,
          lineTension: 1,
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                  padding: 25
                }
              }
            ]
          }
        }
      };
    },
    async getData() {
      const response = await axios.get(`http://localhost:5000/analytics`, {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('token')
        },
        params: {
          date: this.date
        }
      });

      const doc = [];
      const pat = [];
      const appo = [];
      const time = [];

      for (let i = response.data.length - 1; i >= 0; i--) {
        const entry = response.data[i];
        doc.push(Number(entry.doctors));
        pat.push(Number(entry.patients));
        appo.push(Number(entry.appointments));
        time.push(entry.date);
      }

      this.doctors = doc;
      this.patients = pat;
      this.appointments = appo;
      this.time = time;
    },

    createChart(chartId, chartData) {
      const ctx = document.getElementById(chartId);
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }
      this.chartInstance = new Chart(ctx, {
        type: chartData.type,
        data: chartData.data,
        options: chartData.options
      });
    }
  }
};
</script>
