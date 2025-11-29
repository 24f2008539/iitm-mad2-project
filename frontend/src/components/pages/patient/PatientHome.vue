<template>

    <patient-nav-bar></patient-nav-bar>
    <new-base-card>
        <div class="card-deck">
            <div class="card">
                <h5 class="card-title">Book Appointment</h5>
                <img src="../../../images/images.png" class="card-img-top" alt="">
                <div class="card-body">
                 <router-link to="/bookappointment" class="btn btn-primary box">Book Now</router-link>  
                </div>
            </div>
            <div class="card">
                <h5 class="card-title">Your Appointments</h5>
                <img src="../../../images/image2.jpg" class="card-img-top" alt="">
                <div class="card-body">
                <router-link to="/viewappointment" class="btn btn-primary">View Your Appointments</router-link>
                </div>
            </div>
            <div class="card">
                <h5 class="card-title">Your Doctor's Examination</h5>
                <img src="../../../images/image.png" class="card-img-top" alt="">
                <div class="card-body">
                 <router-link to="/doctorprescription" class="btn btn-primary">View Your Examination</router-link>
                </div>
            </div>
            <div class="card">
                <h5 class="card-title">Export Treatment History</h5>
                <div style="background-color: #f0f0f0; height: 200px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 48px;">📊</span>
                </div>
                <div class="card-body">
                 <router-link to="/exporthistory" class="btn btn-primary">Export as CSV</router-link>
                </div>
            </div>
    </div>
    </new-base-card>
</template>

<style scoped>
.container{
    width: 100%,
}
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