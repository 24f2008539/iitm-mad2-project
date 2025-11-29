<template>
<div class="navigation">
        <nav class="navbar navbar-expand flex-column flex-md-row bg-light">
    <div class="container-fluid">
        <router-link to="/contactus" class="navbar-brand" style="color: #0366A8">WELCOME</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
            <li class="nav-item">
            <router-link to="/home" class="nav-link active box" aria-current="page" style="color: #0366A8">Home</router-link>
            </li>
            <li class="nav-item">
            <router-link to="/aboutus" class="nav-link box" style="color: #0366A8">About Us</router-link>
            </li>
            <li class="nav-item">
            <router-link to="/doctors" class="nav-link box" style="color: #0366A8">Doctors</router-link>
            </li>
            <li class="nav-item">
            <router-link to="/contactus" class="nav-link box" style="color: #0366A8">Contact Us</router-link>
            </li>
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Login
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <router-link to="/loginpatient" class="dropdown-item">Patient</router-link>
                    <router-link to="/logindoctor" class="dropdown-item">Doctor</router-link>
                    <router-link to="/loginadmin" class="dropdown-item">Admin</router-link>
                </div>
            </div>
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Signup
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <router-link to="/patientsignup" class="dropdown-item">Patient</router-link>
                </div>
            </div>
        </ul>
        </div>
    </div>
    </nav>
</div>
</template>
<style scoped>
.navigation{
    width: 100%;
}
.dropdown {
    padding: 5px;
 
}
.container-fluid{
    background-color: transparent;
     color:#2980B9;
}
#dropdownMenuButton{
    background-color: #D6EAF8;
    color:#2980B9;
    font-weight: bold;
}
.nav-item{
    color:#083f64;
    font-weight: bold;
    font-size: large;
}
.navbar-brand{
     color:#D6EAF8;
    font-weight: bold;
    font-size: large;

}
.box{
    color: #D6EAF8;
}


</style>