<template>
    <admin-nav-bar></admin-nav-bar>
    <new-base-card>
        <h2 class="header">Examination</h2>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Examination Id</th>
                        <th>Date</th>
                        <th>Patient Name </th>
                        <th>Doctor Name</th>
                        <th>Diagnosis </th>
                        <th>Prescription</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="examinations in examinationDetails" :key="examinations.id">
                        <td>{{ examinations._id }}</td>
                        <td>{{ examinations.appointment.date }}</td>
                        <td>{{ examinations.appointment.patient_username }}</td>
                        <td>{{ examinations.appointment.doctor_username }}</td>
                        <td>{{ examinations.diagnosis }}</td>
                        <td>{{ examinations.prescription }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
         <form class="form-inline" @submit.prevent="deleteExamination">
        <div class="form-group mx-sm-3 mb-2">
            <label for="inputPassword2" class="sr-only" >Examination's ID</label>
            <input type="number" class="form-control" id="inputPassword2" placeholder="Examination's ID" v-model="id">
        </div>
        <button type="submit" class="btn btn-primary mb-2">Delete Examination</button>
        </form>
    </new-base-card>
</template>
<script>
import axios from 'axios';
export default {
  data() {
      return {
          examinationDetails: [],
          id:null,
      };
  },
  mounted() {
      this.getExaminationDetails();
  },
  methods: {
      getExaminationDetails() {
          axios.get(
              `http://localhost:5000/examinations`,  {
                headers: {
                    Authorization : 'Bearer ' + localStorage.getItem('token')
                }
          }).then((response) => {
              this.formatExaminationDetails(response.data);
          });
      },
      formatExaminationDetails(examinations) {
          for (let key in examinations) {
              this.examinationDetails.push({...examinations[key], id:key});
          }
          console.log(this.examinationDetails);
      },
      async deleteExamination (){
           await axios.delete(`http://localhost:5000/examination/${this.id}`, {
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