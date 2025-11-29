<template>
    <admin-nav-bar></admin-nav-bar>
    <new-base-card>
        <h2>Doctors</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Form Id</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Mobile Number</th>
                        <th>Email</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="forms in formDetails" :key="forms.id">
                        <td>{{ forms._id }}</td>
                        <td>{{ forms.first_name }}</td>
                        <td>{{ forms.last_name }}</td>
                        <td>{{ forms.mobile }}</td>
                        <td>{{ forms.email }}</td>
                        <td>{{ forms.text }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
<form class="form-inline" @submit.prevent="deleteForm">
  <div class="form-group mx-sm-3 mb-2">
    <label for="inputPassword2" class="sr-only">Form's Id</label>
    <input type="number" class="form-control" id="inputPassword2" placeholder="Form Id" v-model="id">
  </div>
  <button type="submit" class="btn btn-primary mb-2">Delete Form</button>
</form>
    </new-base-card>
</template>
<script>
import axios from 'axios';
export default {
  data() {
      return {
          formDetails: [],
          id: null,
      };
  },
  mounted() {
      this.getFormDetails();
  },
  methods: {
      getFormDetails() {
          axios.get(
              `http://localhost:5000/contactus/forms`, {
                  headers: {
                    Authorization : 'Bearer ' + localStorage.getItem('token')
                }
              }
          ).then((response) => {
              this.formatFormDetails(response.data);
          });
      },
      formatFormDetails(forms) {
          for (let key in forms) {
              this.formDetails.push({...forms[key], id:key});
          }
          console.log(this.formDetails);
      },
      async deleteForm() {
          await axios.delete(`http://localhost:5000/contactus/${this.id}`, {
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