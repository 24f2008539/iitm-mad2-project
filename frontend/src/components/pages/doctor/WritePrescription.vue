<template>
    <doctor-nav-bar></doctor-nav-bar>
    <base-card>
        <h3>Write Examination/Prescription</h3>
        <div class="alert alert-success" v-if="isSuccess">✓ You wrote prescription successfully</div>
        <div class="alert alert-danger" v-if="errorMessage">{{ errorMessage }}</div>
        <form @submit.prevent="writePrescription">
                    <div class="form-group col-md-6">
                            <label for="appointmentSelect">Select Appointment <span style="color: red;">*</span></label>
                            <select class="form-control" id="appointmentSelect" v-model="appointment_id" @change="onAppointmentSelected">
                                <option value="">-- Select an Appointment --</option>
                                <option v-for="appt in appointmentDetails" :key="appt._id" :value="appt._id">
                                    Patient: {{ appt.patient_username }} | Date: {{ appt.date }} | Description: {{ appt.description || 'N/A' }}
                                </option>
                            </select>
                    </div>
                    <div class="form-group col-md-8" v-if="selectedAppointment">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h5 class="card-title">Appointment Details</h5>
                                <div class="row">
                                    <div class="col-md-6">
                                        <p><strong>Patient:</strong> {{ selectedAppointment.patient_username }}</p>
                                        <p><strong>Appointment Date:</strong> {{ selectedAppointment.date }}</p>
                                    </div>
                                    <div class="col-md-6">
                                        <p><strong>Doctor:</strong> {{ selectedAppointment.doctor_username }}</p>
                                        <p><strong>Description:</strong> {{ selectedAppointment.description || 'N/A' }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="form-row" style="max-width: 40rem">
                        <div class="form-group col-md-6">
                            <label for="diagnosis">Diagnosis <span style="color: red;">*</span></label>
                            <textarea id="diagnosis" class="form-control" rows="5" v-model="diagnosis" required></textarea>
                        </div>
                    </div>
                    <div class="form-row" style="max-width: 40rem">
                        <div class="form-group col-md-6">
                            <label for="prescription">Prescription <span style="color: red;">*</span></label>
                            <textarea id="prescription" class="form-control" rows="5" v-model="prescription" required style="max-width: 40rem;"></textarea>
                        </div>
                    </div>        
                    <button type="submit" class="btn btn-primary">Write Examination</button>
            </form>
    </base-card>
</template>
<script>
import axios from 'axios';
import BaseCard from '../../ui/BaseCard.vue';
export default {
  components: { BaseCard },
    data() {
        return {
            diagnosis: '',
            prescription: '',
            isSuccess: false,
            errorMessage: '',
            appointmentDetails: [],
            appointment_id: '',
            selectedAppointment: null,
        };
    },
    mounted() {
        this.getAppointments();
    },
    methods: {
        getAppointments() {
            axios.get(
                `http://localhost:5000/appointments`,
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('token')
                    }
                }
            ).then((response) => {
                console.log('Appointments:', response.data);
                this.appointmentDetails = Array.isArray(response.data) ? response.data : [];
            }).catch((error) => {
                console.error('Error fetching appointments:', error);
                this.errorMessage = 'Error loading appointments';
            });
        },
        onAppointmentSelected() {
            this.selectedAppointment = this.appointmentDetails.find(appt => appt._id === this.appointment_id);
            console.log('Selected appointment:', this.selectedAppointment);
        },
        writePrescription() {
            this.errorMessage = '';
            
            if (!this.appointment_id || !this.diagnosis || !this.prescription) {
                this.errorMessage = 'Please fill in all required fields';
                return;
            }

            console.log('Writing examination for appointment:', this.appointment_id);

            axios
            .post(
                `http://localhost:5000/appointments/${this.appointment_id}/examinations`,
                {
                    diagnosis: this.diagnosis,
                    prescription: this.prescription
                },
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('token'),
                        'Content-Type': 'application/json'
                    }
                }
            )
            .then((response) => {
                console.log('✓ Examination written successfully:', response.data);
                this.isSuccess = true;
                setTimeout(() => {
                    this.$router.push('/doctorhome');
                }, 1500);
            })
            .catch((error) => {
                console.error('✗ Error writing examination:', error);
                const errorMsg = error.response?.data?.message || error.response?.statusText || error.message;
                this.errorMessage = 'Error: ' + errorMsg;
            });
        }
    },
}
</script>