<template>
   
    <doctor-nav-bar></doctor-nav-bar>
    <h1 id="sen">Have Any Questions?
        Contact us and we will be happy to help you!
    </h1>
   
<div class=container-fluid>
    <div class="column">
        <div class="row">
<img src="../../../images/contact.png">
 <div class="sen">
       <form @submit.prevent="sendMessage">
      <div class="form-row">
        <div class="col">
          <label>First Name</label>
          <input
            type="text"
            class="form-control"
            v-model="first_name"
            required
          />
        </div>
        <div class="col">
          <label>Last Name</label>
          <input
            type="text"
            class="form-control"
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
            v-model="email"
            required
          />
        </div>
        <div class="form-group col-md-6">
          <label for="inputPassword4">Mobile Number</label>
          <input
            type="text"
            class="form-control"
            id="inputPassword4"
            v-model="mobile"
            required
          />
        </div>
      </div>
      <div class="form-group">
        <label for="inputusername">Your Message</label>
        <textarea
          class="form-control"
          id="inputusername"
          v-model="text"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Contact Us</button>
</form>
        </div>
        </div>      
</div>
</div>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            first_name: '',
            last_name: '',
            mobile: '',
            email: '',
            text: '',
        };
    },
    methods: {
        sendMessage() {
            axios
            .post(
                `http://localhost:5000/contactus/form`,
                { first_name: this.first_name, last_name: this.last_name, email: this.email, mobile: this.mobile, text: this.text},
                {
                    headers: {
                       'Content-Type': 'application/json', 
                    },
                }
                )
            .then((response) => {
                this.isSuccess = true;
                this.$router.push('/home');
                console.log(response);
            });


        }
        }
}
</script>
<style scoped>

.fa {
  padding: 40px;
  font-size: 50px;
  text-align: center;
  text-decoration: none;
  border-radius: 50%;
}
.fa-facebook{
    color: mediumblue;
}
.fa-instagram{
    color: mediumvioletred;
}
.fa-whatsapp{
    color: green;
}
#sen{
    text-align: center;
    padding: 50px;
    color: #0366a8;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    
}
.border{
    background-color: rgb(255, 230, 230);
    text-align: center;
    
}
.call{
    text-align: center;

}
#img{
    width:40px;
}
.card{
    margin-left: 700px;
        margin-top: 10px;

    
    
}
.container-fluid{
    margin-top: 30px;
}
.row {
  display: flex;
  flex-wrap: wrap;
  padding: 0 4px;
      

}
.sen{
    font-family: cursive;
    color: #16A085;
    margin-left: 25px;
    margin-top: 40px;
}






</style>