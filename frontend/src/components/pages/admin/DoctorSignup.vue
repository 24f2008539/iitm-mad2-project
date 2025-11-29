<template>
  <admin-nav-bar></admin-nav-bar>
  <the-loader v-if="showLoading"></the-loader>
  <base-card>
    <div class="alert alert-danger" v-if="error">{{ error }}</div>
    <div class="alert alert-success" v-if="isSuccess && error === '' ">
      You Signed up successfully
    </div>
    <form @submit.prevent="submitDoctor">
      <label class=" doctor">Sign Up as a doctor !</label>
      <div class="form-row">
        <div class="col">
          <label>First Name</label>
          <input
            type="text"
            class="form-control"
            placeholder="First name"
            v-model="first_name"
            required
          />
        </div>
        <div class="col">
          <label>Last Name</label>
          <input
            type="text"
            class="form-control"
            placeholder="Last name"
            v-model="last_name"
            required
          />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-6">
          <label for="inputEmail4">Email</label>
          <input
            type="email"
            class="form-control"
            id="inputEmail4"
            placeholder="xxx@email.com"
            v-model="email"
            required
          />
          <div class="error" v-if="errors.email">{{ errors.email }}</div>
        </div>
        <div class="form-group col-md-6">
          <label for="inputPassword4">Password</label>
          <input
            type="password"
            class="form-control"
            id="inputPassword4"
            v-model="password"
            required
          />
          <div class="error" v-if="errors.password">{{ errors.password }}</div>
        </div>
      </div>
      <div class="form-group">
        <label for="inputusername">User Name</label>
        <input
          type="text"
          class="form-control"
          id="inputusername"
          v-model="username"
          required
        />
      </div>
      <div class="form-group">
        <label for="inputAddress2">Mobile Number</label>
        <input
          type="text"
          class="form-control"
          id="inputmobile"
          placeholder="+20 01.."
          v-model="mobile"
          required
        />
      </div>
      <div class="form-group">
        <label for="inputAddress">Address</label>
        <input
          type="text"
          class="form-control"
          id="inputAddress"
          placeholder="1234 Main St"
          v-model="address"
          required
        />
      </div>
      <div class="form-check">
  <input class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios1" value="1"  v-model="gender">
  <label class="form-check-label" for="exampleRadios1">
    Female
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios2" value="0" v-model="gender">
  <label class="form-check-label" for="exampleRadios2">
    Male
  </label>
</div>
        <div class="form-group">
          <label for="inputSpecialization">Specialization</label>
          <input
            type="text"
            class="form-control"
            id="inputSpecialization"
            placeholder="e.g., Cardiology, Interventional Cardiology"
            v-model="specialization"
            required
          />
        </div>
        <div class="form-group">
          <label for="inputZip">Birth Date</label>
          <input
            type="date"
            class="form-control"
            id="inputZip"
            v-model="birthdate"
            required
          />
        </div>
      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  </base-card>
</template>
<script>
import axios from 'axios';
/* import SignupValidations from '../../../services/SignupValidations';
import {mapActions} from 'vuex'; */
import {mapState} from 'vuex';
//import {SIGNUP_ACTION} from '../../../store/storeconstants';
import TheLoader from '../../ui/TheLoader.vue';

export default {
  components: { TheLoader },
  computed: {
      ...mapState({
          showLoading: state => state.showLoading,
      })
  },
    data() {
        return {
            first_name: '',
            last_name: '',
            email: '',
            password: '',
            mobile: '',
            address: '',
            birthdate: '',
            gender: '' ,
            username: '',
            specialization: '',
            isSuccess: '',
            errors: [],
            error: '',

        };
    },
    methods: {
       /*  ...mapActions( 'auth', {
            signup: SIGNUP_ACTION
        }), */
        submitDoctor() {
           /*  let validtations = new SignupValidations(this.email, this.password);
      this.errors = validtations.checkValidations();
      if ('email' in this.errors || 'password' in this.errors) {
        return false; */
     // }
      /* this.signup({
        url: 'http://localhost:5000/doctor/register',
        body: {
          email: this.email,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
          birthdate: this.birthdate,
          username: this.username,
          gender: this.gender,
          mobile: this.mobile,
          address: this.address
        },
            headers: {
                    'Content-Type': 'application/json',
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
      })
        .then(() => {
          this.$router.push('/logindoctor');
        })
        .catch(error => {
          this.error = error;
        }); */
                axios
            .post(
                `http://localhost:5000/doctor/register`,
                {first_name: this.first_name, last_name: this.last_name, email: this.email, password: this.password, 
                mobile: this.mobile, address: this.address, birthdate: this.birthdate, gender: this.gender, username: this.username, specialization: this.specialization},
                {
                    headers: {
                        'Content_type': 'application/json',
                        Authorization: 'Bearer ' + localStorage.getItem('token')
                    }
                }
                )
            .then((response) => {
                console.log(response);
                this.$router.push('/adminhome')
            });
            /* let validtations = new SignupValidations(
                this.email,
                this.password,
            );
            this.errors = validtations.checkValidations();
            if ('email' in this.errors || 'password' in this.errors){
                return false;
            }
            this.signup({email: this.email, password: this.password
            }).catch((error) => {
                this.error = error;
            }); */
             this.isSuccess = true;
        },
    },
}
</script>
<style scoped>
.doctor{
    text-align: center;
    font-size: 30px;
    margin-left: 170px;
}
</style>