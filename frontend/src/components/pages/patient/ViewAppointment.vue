<template>
    <patient-nav-bar></patient-nav-bar>
    <new-base-card>
        <h2 class="header">Appointments</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Appointment Id</th>
                        <th>Date</th>
                        <th>Patient Name </th>
                        <th>Doctor Name</th>
                        <th>Description </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="appointments in appointmentDetails" :key="appointments.id">
                        <td>{{ appointments._id }}</td>
                        <td>{{ appointments.date }}</td>
                        <td>{{ appointments.patient_username }}</td>
                        <td>{{ appointments.doctor_username }}</td>
                        <td>{{ appointments.description }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </new-base-card>
</template>
<script>
import axios from 'axios';
export default {
  data() {
      return {
          appointmentDetails: [],
          id:null,
      };
  },
  mounted() {
      this.getAppointmentDetails();
  },
  methods: {
      getAppointmentDetails() {
          axios.get(
              `http://localhost:5000/appointments`,  {
                headers: {
                    Authorization : 'Bearer ' + localStorage.getItem('patient_access_token')
                }
          }).then((response) => {
              this.formatAppointmentDetails(response.data);
          });
      },
      formatAppointmentDetails(appointments) {
          for (let key in appointments) {
              this.appointmentDetails.push({...appointments[key], id:key});
          }
          console.log(this.appointmentDetails);
      },
  }

}
</script>
<style scoped>
.header{
    text-align: center;
}
</style>