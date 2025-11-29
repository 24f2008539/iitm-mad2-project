<template>
    <nav-bar></nav-bar>
    <the-loader v-if="showLoading"></the-loader>
    <div class="scale-up-tl">
    <base-card>
        <div class="alert alert-danger" v-if="error">{{ error }}</div>
        <form @submit.prevent="onLogin">
            <div class="form-group">
                <label for="exampleInputEmail1">Doctor Username</label>
                <input type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model.trim="username" required>
                <div class="error" v-if="errors.email">{{ errors.email }}</div>
            </div>
            <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input type="password" class="form-control" id="exampleInputPassword1" v-model.trim="password" required>
                 <div class="error" v-if="errors.password">{{ errors.password }}</div>

            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </base-card>
    <img src="../../images/doc.jpg" id="img" class="mx-auto d-block">
    </div>
</template>
<script>
//import { mapActions } from 'vuex';
import axios from 'axios';
import {mapState} from 'vuex';
//import SignupValidations from '../../services/SignupValidations';
//import { LOGIN_ACTION } from '../../store/storeconstants';
import TheLoader from '../ui/TheLoader.vue';
export default {
  components: { TheLoader },
  computed: {
      ...mapState({
          showLoading: state => state.showLoading,
      })
  },
    data() {
        return {
            username: '',
            password: '',
            errors: [],
            error: '',
        };
    },
    methods: {
       /*  ...mapActions('auth', {
            login: LOGIN_ACTION,
        }), */
        async onLogin() {
             axios
            .post(
                `http://localhost:5000/doctor/login`,
                {password: this.password, username: this.username},
                )
            .then((response) => {
                console.log(response);
                if (response.status === 200) {
                    localStorage.setItem('token', response.data.access_token);
                    console.log(localStorage.getItem('token'));
                    this.$router.push('/doctorhome');
                }
            });

          /* let validtations = new SignupValidations(
              this.email,
              this.password,
          );
          this.errors = validtations.checkValidations();
          if (this.errors.length) {
              return false;
          }
          this.error = '';
          //Login check
        try {
            await this.login({
                email: this.email,
                password: this.password
            });
             this.$router.push('/patienthome');
        } catch (e) {
            this.error = e;
        }
             */
        },
    },
};
</script>
<style scoped>
#img{
    width:300px;
    border-radius: 50%;

}
.scale-up-tl {
	-webkit-animation: scale-up-tl 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
	animation: scale-up-tl 0.4s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
}
@-webkit-keyframes scale-up-tl {
  0% {
    -webkit-transform: scale(0.5);
     transform: scale(0.5);
    -webkit-transform-origin: 0% 0%;
     transform-origin: 0% 0%;
  }
  100% {
    -webkit-transform: scale(1);
    transform: scale(1);
    -webkit-transform-origin: 0% 0%;
    transform-origin: 0% 0%;
  }
}
@keyframes scale-up-tl {
  0% {
    -webkit-transform: scale(0.5);
    transform: scale(0.5);
    -webkit-transform-origin: 0% 0%;
    transform-origin: 0% 0%;
  }
  100% {
    -webkit-transform: scale(1);
    transform: scale(1);
    -webkit-transform-origin: 0% 0%;
    transform-origin: 0% 0%;
  }
}
</style>