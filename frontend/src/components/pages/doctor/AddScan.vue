<template>
    <doctor-nav-bar></doctor-nav-bar>
    <base-card>
        <form @submit.prevent="onUpload">
         <div class="form-row">
                <div class="col">
                    <label for="inputdoctorid">patient's Id</label>
                    <input type="number" class="form-control" id="inputdoctorid" v-model="patient_id">
                </div> 
         </div>  
        <div class="form-group">
            <label for="exampleFormControlFile1">Upload Your Scan</label>
            <input @change="onFileChanged" type="file" class="form-control-file" id="exampleFormControlFile1">  
        </div>
        <button type="submit" class="btn btn-primary mb-2">Upload</button>
        </form>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
    data (){
        return{
            selectedFile: null,
            patient_id:null,
        }
    },
    methods:{
        onFileChanged (event) {
            this.selectedFile = event.target.files[0]
        },
        onUpload() {
            const formData = new FormData()
            formData.append('image', this.selectedFile, this.selectedFile.name)
            axios.post(`http://localhost:5000/upload/image/${this.patient_id}`, formData, {
                 headers: {
                     'Content_Type' : 'multipart/formdata',
                     Authorization: 'Bearer ' + localStorage.getItem('token')
                 }
             }).then(() => {
                 this.$router.push('/doctorhome');
             })
        },
    }
}
</script>