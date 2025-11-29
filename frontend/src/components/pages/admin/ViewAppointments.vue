<template>
    <admin-nav-bar></admin-nav-bar>
    <new-base-card>
        <h2 class="header">Appointments</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Appointment Id</th>
                        <th>Date</th>
                        <th>Patient Username </th>
                        <th>Doctor Username</th>
                        <th>Description </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="appointments in appointmentDetails" :key="appointments.id">
                        <td>{{ appointments._id }}</td>
                        <td>{{ appointments.date }}</td>
                        <td>{{ appointments.patient_id }}- {{ appointments.patient_username }}</td>
                        <td>{{ appointments.doctor_id }}- {{ appointments.doctor_username }}</td>
                        <td>{{ appointments.description }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
         <form class="form-inline" @submit.prevent="deleteappointment">
        <div class="form-group mx-sm-3 mb-2">
            <label for="inputPassword2" class="sr-only" >Appointment's ID</label>
            <input type="number" class="form-control" id="inputPassword2" placeholder="Appointment's ID" v-model="id">
        </div>
        <button type="submit" class="btn btn-primary mb-2">Delete Appointment</button>
        </form>
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
          for (let key in appointments) {
              this.appointmentDetails.push({...appointments[key], id:key});
          }
          console.log(this.appointmentDetails);
      },
      async deleteappointment (){
           await axios.delete(`http://localhost:5000/appointments/${this.id}`, {
                headers: {
                    Authorization : 'Bearer ' + localStorage.getItem('token')
                }
                }).then((response) => {
                console.log(response);
                if (response.status === 200) {
                    this.$router.push('/adminhome');
                }
            });
        }
  }

}
</script>
<style scoped>
.header{
    text-align: center;
}
</style>