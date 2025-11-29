<template>
    <nav-bar></nav-bar>
   <div class="fluid-container">  
    <h1 id="sen">Hospital Management System</h1>
<div class=container-fluid>
    <div class="column">
        <div class="row">
<img src="../../images/yy.png" id="img" class="d-block m-auto">
 <div class="sen">
        <h1 >WELCOME TO OUR WEBSITE !</h1> 
       

  
 
        </div>

        </div>
        
       
</div>


    </div>
         
             
   </div>

</template>
<script>
import NavBar from '../../components/ui/NavBar.vue';
export default {
    components: {
        NavBar,
    }
}
</script>

<style scoped>

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
    width:600px;  
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
    margin-top: 140px;
}







</style>