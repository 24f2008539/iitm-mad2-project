<template>
    <patient-nav-bar></patient-nav-bar>
    <base-card>
        <div class="alert alert-success" v-if="isSuccess">✓ You Booked successfully</div>
        <div class="alert alert-danger" v-if="errorMessage">{{ errorMessage }}</div>
        <form @submit.prevent="addAppointment">
                    <div class="form-row">
                        <div class="col">
                            <label>First Name</label>
                            <input type="text" class="form-control" placeholder="First name" v-model="first_name" disabled>
                            </div>
                            <div class="col">
                                <label>Last Name</label>
                                <input type="text" class="form-control" placeholder="Last name" v-model="last_name" disabled>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="col">
                        <label for="inputEmail4">Email</label>
                        <input type="email" class="form-control" id="inputEmail4" placeholder="xxx@email.com" v-model="email" disabled>
                        </div>
                        <div class="col">
                        <label for="inputmobile">Mobile Number</label>
                        <input type="text" class="form-control" id="inputmobile" placeholder="+20 01.." v-model="mobile" disabled>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="col">
                            <label for="exampleFormControlSelect1">Doctor's Name</label>
                            <select class="form-control" id="exampleFormControlSelect1" v-model="doctor_id">
                                <option value="">-- Select Doctor --</option>
                                <option v-for="doctor in doctorDetails" :key="doctor._id" :value="doctor._id">{{ doctor.first_name}} {{ doctor.last_name}}</option>
                            </select>
                            </div>
                    </div>
                    <div class="form-group">
                        <label for="inputDate">Appointment Date <span style="color: red;">*</span></label>
                        <input type="date" class="form-control" id="inputDate" v-model="date" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group col-md-6">
                        <label for="description">Case Description</label>
                        <textarea id="description" rows="5" cols="45" v-model="description"></textarea>
                        </div>
                    
                    </div>         
                    <button type="submit" class="btn btn-primary">Book Appointment</button>
            </form>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            first_name: '',
            last_name: '',
            email: '',
            mobile: '',
            doctor_id: '',
            description: '',
            date: '',
            isSuccess: false,
            errorMessage: '',
            doctorDetails: [],
        };
    },
    mounted() {
        this.getDoctorDetails();
        this.loadPatientInfo();
    },
    methods: {
        loadPatientInfo() {
            // Get patient info from API
            axios.get(
                `http://localhost:5000/patients`,
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('token')
                    },
                }
            ).then((response) => {
                if (response.data && response.data.length > 0) {
                    const patient = response.data[0];
                    this.first_name = patient.first_name || '';
                    this.last_name = patient.last_name || '';
                    this.email = patient.email || '';
                    this.mobile = patient.mobile || '';
                }
            }).catch((error) => {
                console.error('Error loading patient info:', error);
            });
        },
        addAppointment() {
            this.errorMessage = '';
            
            // Validate form
            if (!this.doctor_id || !this.date) {
                this.errorMessage = 'Please select a doctor and date';
                return;
            }

            console.log('Booking appointment with:', {
                doctor_id: this.doctor_id,
                date: this.date,
                description: this.description
            });

            axios
            .post(
                `http://localhost:5000/appointments`,
                { 
                    doctor_id: this.doctor_id, 
                    date: this.date, 
                    description: this.description
                },
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem('patient_access_token'),
                        'Content-Type': 'application/json'
                    },
                }
                )
            .then((response) => {
                console.log('✓ Appointment booked successfully:', response.data);
                this.isSuccess = true;
                setTimeout(() => {
                    this.$router.push('/patienthome');
                }, 2000);
            })
            .catch((error) => {
                console.error('✗ Error booking appointment:', error);
                const errorMsg = error.response?.data?.message || error.response?.statusText || error.message;
                this.errorMessage = 'Error: ' + errorMsg;
            });
        },
        getDoctorDetails() {
            axios.get(
                `http://localhost:5000/doctors`, 
                {
                    headers: {
                        'Content-Type' : 'application/json',
                    }
                }
            ).then((response) => {
                this.formatDoctorDetails(response.data);
            }).catch((error) => {
                console.error('Error loading doctors:', error);
            });
        },
        formatDoctorDetails(doctors) {
            if (Array.isArray(doctors)) {
                this.doctorDetails = doctors;
            } else {
                for (let key in doctors) {
                    this.doctorDetails.push({...doctors[key], id:key});
                }
            }
            console.log('Doctors loaded:', this.doctorDetails);
        }
    }
}
</script>