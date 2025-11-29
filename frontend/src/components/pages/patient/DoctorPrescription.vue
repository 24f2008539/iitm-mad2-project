<template>
<patient-nav-bar></patient-nav-bar>
    <base-card>
        <h3>Your Examinations and Prescriptions</h3>
        <div v-if="prescriptionDetails.length === 0" class="alert alert-info">
            No examinations found yet.
        </div>
        <div class="table-responsive" v-if="prescriptionDetails.length > 0">
            <table class="table table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>Exam ID</th>
                        <th>Doctor</th>
                        <th>Specialization</th>
                        <th>Appointment Date</th>
                        <th>Diagnosis</th>
                        <th>Prescription</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="prescription in prescriptionDetails" :key="prescription._id">
                        <td><strong>{{ prescription._id }}</strong></td>
                        <td>{{ prescription.doctor_name }}</td>
                        <td><span class="badge badge-info">{{ prescription.doctor_specialization }}</span></td>
                        <td>{{ prescription.appointment_date }}</td>
                        <td>{{ prescription.diagnosis }}</td>
                        <td>{{ prescription.prescription }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
    data() {
      return {
          prescriptionDetails: [],
      };
  },
  mounted() {
      this.getPrescriptionDetails();
  },
  methods: {
      getPrescriptionDetails() {
          axios.get(
              `http://localhost:5000/examinations`, {
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem('patient_access_token')
            }
                }).then((response) => {
              this.formatPrescriptionDetails(response.data);
          });
      },
      formatPrescriptionDetails(Prescriptions) {
          for (let key in Prescriptions) {
              this.prescriptionDetails.push({...Prescriptions[key], id:key});
          }
          console.log(this.prescriptionDetails);
      }
  }
}
</script>