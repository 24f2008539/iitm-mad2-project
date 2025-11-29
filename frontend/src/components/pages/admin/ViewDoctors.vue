<template>
    <admin-nav-bar></admin-nav-bar>
    <base-card>
        <h2>Doctors</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Age</th>
                        <th>Mobile Number</th>
                        <th>Specialization</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="doctors in doctorDetails" :key="doctors.id">
                        <td>{{ doctors._id }}</td>
                        <td>{{ doctors.first_name }}</td>
                        <td>{{ doctors.last_name }}</td>
                        <td>{{ doctors.age }}</td>
                        <td>{{ doctors.mobile }}</td>
                        <td><span class="badge badge-info">{{ doctors.specialization }}</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
<form class="form-inline" @submit.prevent="deleteDoctor">
  <div class="form-group mx-sm-3 mb-2">
    <label for="inputPassword2" class="sr-only">Doctor's Id</label>
    <input type="number" class="form-control" id="inputPassword2" placeholder="Doctor's Id" v-model="id">
  </div>
  <button type="submit" class="btn btn-primary mb-2">Delete Doctor</button>
</form>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
  data() {
      return {
          doctorDetails: [],
          id: null,
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
      },
      async deleteDoctor() {
          await axios.delete(`http://localhost:5000/doctor/${this.id}`, {
              headers: {
                   Authorization: 'Bearer ' + localStorage.getItem('token')
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