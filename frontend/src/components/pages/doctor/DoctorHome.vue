<template>
    <doctor-nav-bar></doctor-nav-bar>
    <new-base-card>
        <div class="row row-cols-1 row-cols-md-4">
    <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">My Patients</h5>
      <img src="../../../images/patient.jpg" class="card-img-top" alt="">
      <div class="card-body">
        <router-link to="doctorpatients" class="btn btn-primary">Search For Patient</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">View Appointments</h5>
      <img src="../../../images/image2.jpg" class="card-img-top" alt="">
      <div class="card-body">
         <router-link to="doctorappointments" class="btn btn-primary">View Your Appointments</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Write Examination</h5>
      <img src="../../../images/image.png" class="card-img-top" alt="">
      <div class="card-body">
       <router-link to="writeprescription" class="btn btn-primary">Write Examination</router-link>
      </div>
    </div>
  </div>
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">Upload Scan</h5>
      <img src="../../../images/upload.png" class="card-img-top" alt="">
      <div class="card-body">
         <router-link to="addscan" class="btn btn-primary">Upload Scan</router-link>
      </div>
    </div>
  </div>
</div>
<div class="row row-cols-1 row-cols-md-4">
  <div class="col mb-4">
    <div class="card">
        <h5 class="card-title">View Scans</h5>
      <img src="../../../images/search.png" class="card-img-top" alt="">
      <div class="card-body">
         <router-link to="searchscan" class="btn btn-primary">Search For Scans</router-link>
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
/* .btn{
    text-align: center;
    margin-left: 50px;
}
.box{
    margin-left: 100px;
} */
</style>