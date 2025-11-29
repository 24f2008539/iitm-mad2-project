import { createApp } from 'vue';

import router from './router.js';
import App from './App.vue';
import BaseCard from './components/ui/BaseCard.vue';
import NavBar from './components/ui/NavBar.vue';
import TheLoader from './components/ui/TheLoader.vue';
import PatientNavBar from './components/ui/PatientNavBar.vue';
import DoctorNavBar from './components/ui/DoctorNavBar.vue';
import NewBaseCard from './components/ui/NewBaseCard.vue';
import AdminNavBar from './components/ui/AdminNavBar.vue';
import store from './store/store.js';
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
const app = createApp(App)

app.use(router);
app.use(store);
app.component('base-card', BaseCard);
app.component('nav-bar', NavBar);
app.component('the-loader', TheLoader);
app.component('patient-nav-bar', PatientNavBar);
app.component('doctor-nav-bar', DoctorNavBar);
app.component('admin-nav-bar', AdminNavBar);
app.component('new-base-card', NewBaseCard);
app.mount('#app');
