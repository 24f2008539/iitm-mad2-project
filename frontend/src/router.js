import { createRouter, createWebHistory } from 'vue-router';

import HomePage from './components/pages/HomePage.vue';
import AboutUs from './components/pages/AboutUs.vue';
import DoctorsList from './components/doctors/DoctorsList.vue';
import ContactUs from './components/pages/ContactUs.vue';
import NotFound from './components/pages/NotFound.vue';
import PatientLogin from './components/login/PatientLogin.vue';
import DoctorLogin from './components/login/DoctorLogin.vue';
import AdminLogin from './components/login/AdminLogin.vue';
import PatientSignup from './components/signup/PatientSignup.vue';
import DoctorSignup from './components/pages/admin/DoctorSignup.vue';
import PatientHome from './components/pages/patient/PatientHome.vue';
import BookAppointment from './components/pages/patient/BookAppointment.vue';
import ViewAppointment from './components/pages/patient/ViewAppointment.vue';
import DoctorPrescription from './components/pages/patient/DoctorPrescription.vue';
import DoctorHome from './components/pages/doctor/DoctorHome.vue';
import DoctorAppointments from './components/pages/doctor/DoctorAppointments.vue';
import WritePrescription from './components/pages/doctor/WritePrescription.vue';
import AdminHome from './components/pages/admin/AdminHome.vue';
import ViewPatients from './components/pages/admin/ViewPatients.vue';
import ViewDoctors from './components/pages/admin/ViewDoctors.vue';
import ViewAppointments from './components/pages/admin/ViewAppointments.vue';
import ViewPrescriptions from './components/pages/admin/ViewPrescriptions.vue';
import DoctorPatients from './components/pages/doctor/DoctorPatients.vue';
import ContactUsForms from './components/pages/admin/ContactUsForms.vue';
import PatientContactUs from './components/pages/patient/PatientContactUs.vue';
import PatientAboutUs from './components/pages/patient/PatientAboutUs.vue';
import PatientDoctors from './components/pages/patient/PatientDoctors.vue';
import DoctorAboutUs from './components/pages/doctor/DoctorAboutUs.vue';
import DoctorContactUs from './components/pages/doctor/DoctorContactUs.vue';
import DoctorDoctors from './components/pages/doctor/DoctorDoctors.vue';
import AdminAboutUs from './components/pages/admin/AdminAboutUs.vue';
import AdminContactUs from './components/pages/admin/AdminContactUs.vue';
import AdminDoctors from './components/pages/admin/AdminDoctors.vue';
import SearchPatient from './components/pages/admin/SearchPatient.vue';
import StatisticalAnalysis from './components/pages/admin/StatisticalAnalysis.vue';
import AddScan from './components/pages/doctor/AddScan.vue';
import SearchScan from './components/pages/doctor/SearchScan.vue';
import SeeScan from './components/pages/admin/SeeScan.vue';
import ExportTreatmentHistory from './components/pages/patient/ExportTreatmentHistory.vue';


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/home' },
    { path: '/home', component: HomePage },
    { path: '/aboutus', component: AboutUs },
    { path: '/doctors', component: DoctorsList },
    { path: '/contactus', component: ContactUs},
    { path: '/loginpatient', component: PatientLogin},
    { path: '/logindoctor', component: DoctorLogin},
    { path: '/loginadmin', component: AdminLogin},
    { path: '/patientsignup', component: PatientSignup},
    { path: '/doctorsignup', component: DoctorSignup},
    { path: '/patienthome', component: PatientHome},
    { path: '/bookappointment', component: BookAppointment},
    { path: '/viewappointment', component: ViewAppointment},
    { path: '/doctorprescription', component: DoctorPrescription},
    { path:'/doctorhome', component: DoctorHome},
    { path: '/doctorpatients', component: DoctorPatients},
    { path: '/doctorappointments', component: DoctorAppointments},
    { path: '/writeprescription', component: WritePrescription},
    { path: '/adminhome', component: AdminHome},
    { path: '/viewpatients', component: ViewPatients},
    { path: '/viewdoctors', component: ViewDoctors},
    { path: '/viewappointments', component: ViewAppointments},
    { path: '/viewprescriptions', component: ViewPrescriptions},
    { path: '/contactusforms', component: ContactUsForms},
    { path: '/patientcontactus', component: PatientContactUs},
    { path: '/patientaboutus', component: PatientAboutUs},
    { path: '/patientdoctors', component: PatientDoctors},
    { path: '/doctoraboutus', component: DoctorAboutUs},
    { path: '/doctorcontactus', component: DoctorContactUs},
    { path: '/doctordoctors', component: DoctorDoctors},
    { path: '/adminaboutus', component: AdminAboutUs},
    { path: '/admincontactus', component: AdminContactUs},
    { path: '/admindoctors', component: AdminDoctors},
    { path: '/searchpatient', component: SearchPatient},
    { path: '/analysis', component: StatisticalAnalysis},
    { path: '/addscan', component: AddScan},
    { path: '/searchscan', component: SearchScan},
    { path: '/seescan', component: SeeScan},
    { path: '/exporthistory', component: ExportTreatmentHistory},
    { path: '/:notFound(.*)', component: NotFound },
  ]
});

export default router;
