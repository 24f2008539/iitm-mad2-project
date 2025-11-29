<template>
    <admin-nav-bar></admin-nav-bar>
    <new-base-card>
        <form class="form-inline my-2 my-lg-0" @submit.prevent="getpatientDetails">
      <input class="form-control mr-sm-2" type="search" placeholder="search by patient Id" aria-label="Search" v-model="id">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
    <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Age</th>
                        <th>Mobile</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="patients in patientDetails" :key="patients.id">
                        <td>{{ patients.first_name }}</td>
                        <td>{{ patients.last_name }}</td>
                        <td>{{ patients.age }}</td>
                        <td>{{ patients.mobile }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Appointment Date</th>
                        <th>Patient Username</th>
                        <th>Doctor Username</th>
                        <th>Case Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="appointments in appointmentDetails" :key="appointments.id">
                        <td>{{appointments.date}}</td>
                        <td>{{appointments.patient_username }}</td>
                        <td>{{appointments.doctor_username }}</td>
                        <td>{{ appointments.description }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Examination Id</th>
                        <th>Diagnosis</th>
                        <th>Prescription</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="examinations in examinationDetails" :key="examinations.id">
                        <td>{{ examinations._id }}</td>
                        <td>{{ examinations.diagnosis }}</td>
                        <td>{{ examinations.prescription }}</td>
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
            first_name: '',
            last_name: '',
            age: '',
            diagnosis: '',
            prescription: '',
            description: '',
            date_of_reservation: '',
            id: null,
            patientDetails: [],
            appointmentDetails: [],
            examinationDetails: [],
        };
    },
    mounted() {
      this.getpatientDetails();

  },
    methods: {
        getpatientDetails() {
               axios.get(
              `http://localhost:5000/patient/${this.id}`, {
                   headers: {
                   Authorization: 'Bearer ' + localStorage.getItem('token')
              }
              }
          ).then((response) => {
              this.patientDetails.push(response.data);
              console.log(response);
              this.formatAppointmentDetails(response.data.appointments);
              this.formatExaminationDetails(response.data.examinations);
          });
      },
      formatAppointmentDetails(appointments) {
          for (let key in appointments) {
              this.appointmentDetails.push({...appointments[key], id:key});
          }
          console.log(this.appointmentDetails);
      },
      formatExaminationDetails(examinations) {
          for (let key in examinations) {
              this.examinationDetails.push({...examinations[key], id:key});
          }
          console.log(this.examinationDetails);
      },

        }
    
}
</script>