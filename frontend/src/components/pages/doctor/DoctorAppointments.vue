<template>
    <doctor-nav-bar></doctor-nav-bar>
    <new-base-card>
        <h2 class="header">Appointments</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Appointment Id</th>
                        <th>Date</th>
                        <th>Patient Id</th>
                        <th>Patient Username </th>
                        <th>Doctor Username</th>
                        <th>Description </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="appointments in appointmentDetails" :key="appointments.id">
                        <td>{{ appointments._id }}</td>
                        <td>{{ appointments.date }}</td>
                        <td>{{ appointments.patient_id }}</td>
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
                    Authorization : 'Bearer ' + localStorage.getItem('token')
                }
          }).then((response) => {
              this.formatAppointmentDetails(response.data);
          });
      },
      formatAppointmentDetails(appointments) {
          // Handle both array and object formats
          let appointmentsArray = Array.isArray(appointments) ? appointments : Object.values(appointments);
          
          for (let i = 0; i < appointmentsArray.length; i++) {
              this.appointmentDetails.push({...appointmentsArray[i], id: i});
          }
          console.log('Doctor appointments (pending only):', this.appointmentDetails);
      },
  }

}
</script>
<style scoped>
.header{
    text-align: center;
}
</style>