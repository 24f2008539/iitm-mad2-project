<template>
    <nav-bar></nav-bar>
    <base-card>
        <h2>Doctors</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Age</th>
                        <th>Mobile Number</th>
                        <th>Specialization</th>
                        <!-- <th>Id</th> -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="doctors in doctorDetails" :key="doctors.id">
                        <td>{{ doctors.first_name }}</td>
                        <td>{{ doctors.last_name }}</td>
                        <td>{{ doctors.age }}</td>
                        <td>{{ doctors.mobile }}</td>
                        <td><span class="badge badge-info">{{ doctors.specialization }}</span></td>
                        <!-- <td>{{ doctors._id}}</td> -->
                    </tr>
                </tbody>
            </table>
        </div>
    </base-card>
</template>
<script>
import BaseCard from '../ui/BaseCard.vue';
import NavBar from '../ui/NavBar.vue';
import axios from 'axios';
export default {
  components: { BaseCard, NavBar },
  data() {
      return {
          doctorDetails: [],
      };
  },
  mounted() {
      this.getDoctorDetails();
  },
  methods: {
      getDoctorDetails() {
          axios.get(
              `http://localhost:5000/doctors`, {
                  headers: {
                      'Content-Type' : 'application/json',
                  }
              }
          ).then((response) => {
              this.formatDoctorDetails(response.data);
          });
      },
      formatDoctorDetails(doctors) {
          for (let key in doctors) {
              this.doctorDetails.push({...doctors[key], id:key});
          }
          console.log(this.doctorDetails);
      }
  }

}
</script>