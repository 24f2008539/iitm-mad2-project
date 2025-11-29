<template>
    <admin-nav-bar></admin-nav-bar>
    <base-card>
        <h2>Patients</h2>
        <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Age</th>
                    <th>Mobile Number</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="patients in patientDetails" :key="patients.id">
                    <td>{{ patients._id}}</td>
                    <td>{{ patients.first_name }}</td>
                    <td>{{ patients.last_name }}</td>
                    <td>{{ patients.age }}</td>
                    <td>{{ patients.mobile }}</td>
                </tr>
            </tbody>
        </table>
        </div>
        <form class="form-inline" @submit.prevent="deletePatient">
  <div class="form-group mx-sm-3 mb-2">
    <label for="inputPassword2" class="sr-only">Patient's Id</label>
    <input type="number" class="form-control" id="inputPassword2" placeholder="Patient's Id" v-model="id">
  </div>
  <button type="submit" class="btn btn-primary mb-2">Delete Patient</button>
</form>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
  data() {
      return {
          patientDetails: [],
          id: null,
      };
  },
  mounted() {
      this.getpatientDetails();
  },
  methods: {
      getpatientDetails() {
          axios.get(
              `http://localhost:5000/patients`, {
                   headers: {
                   Authorization: 'Bearer ' + localStorage.getItem('token')
              }
              }
          ).then((response) => {
              this.formatPatientDetails(response.data);
          });
      },
      formatPatientDetails(patients) {
          for (let key in patients) {
              this.patientDetails.push({...patients[key], id:key});
          }
          console.log(this.patientDetails);
      },
      async deletePatient() {
          await axios.delete(`http://localhost:5000/patient/${this.id}`, {
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