<template>
    <admin-nav-bar></admin-nav-bar>
    <new-base-card>
        <div class="row row-cols-1 row-cols-md-4">
    <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">View Doctors</h5>
      <img src="../../../images/doctor.jpg" class="card-img-top" alt="">
      <div class="card-body">
        <router-link to="viewdoctors" class="btn btn-primary">View Doctors</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">View Patients</h5>
      <img src="../../../images/patient.jpg" class="card-img-top" alt="">
      <div class="card-body">
         <router-link to="viewpatients" class="btn btn-primary">View Patients</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">View Appointments</h5>
      <img src="../../../images/image2.jpg" class="card-img-top" alt="">
      <div class="card-body">
       <router-link to="viewappointments" class="btn btn-primary">View Appointments</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">View Examinations</h5>
      <img src="../../../images/image.png" class="card-img-top" alt="">
      <div class="card-body">
         <router-link to="viewprescriptions" class="btn btn-primary">View Examinations</router-link>
      </div>
    </div>
  </div>
</div>
<div class="row row-cols-1 row-cols-md-4">
<div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Search For A Patient</h5>
      <img src="../../../images/search.png" class="card-img-top" alt="">
      <div class="card-body">
        <router-link to="searchpatient" class="btn btn-primary">Search Patients</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Statistical Analysis</h5>
      <img src="../../../images/analysis.png" class="card-img-top" alt="">
      <div class="card-body">
        <router-link to="analysis" class="btn btn-primary">See Analysis</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Doctor Signup</h5>
      <img src="../../../images/signup.png" class="card-img-top" alt="">
      <div class="card-body">
        <router-link to="doctorsignup" class="btn btn-primary">Add Doctor</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Patients Scans</h5>
      <img src="../../../images/scan.png" class="card-img-top" alt="">
      <div class="card-body">
        <router-link to="seescan" class="btn btn-primary">Search Scan</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Contact Us Forms</h5>
      <img src="../../../images/contactus.jpg" class="card-img-top" alt="">
      <div class="card-body">
         <router-link to="contactusforms" class="btn btn-primary">View Forms</router-link>
      </div>
    </div>
  </div>
</div>

    </new-base-card>
</template>
<style scoped>
.card-title{
    text-align: center;
    font-weight: bold;
    margin-top: 12px;
    font-family: Arial, Helvetica, sans-serif;
}
</style>