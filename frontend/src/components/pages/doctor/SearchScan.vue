<template>
    <doctor-nav-bar></doctor-nav-bar>
    <base-card>
        <form class="form-inline my-2 my-lg-0" @submit.prevent="getScanDetails">
      <input class="form-control mr-sm-2" type="search" placeholder="search by patient Id" aria-label="Search" v-model="id">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
    <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Scan URL</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="scans in scanDetails" :key="scans.id">
                          <td> <a v-bind:href=" `${scans.image}` "> {{ scans.image }} </a> </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </base-card>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            scanDetails: [],
            id: null,
        };
    },
    mounted() {
        this.getScanDetails();
    },
    methods: {
        getScanDetails() {
               axios.get(
              `http://localhost:5000/images/${this.id}`, {
                   headers: {
                   Authorization: 'Bearer ' + localStorage.getItem('token')
              }
              }
          ).then((response) => {
              this.formatScanDetails(response.data);
              console.log(response);
          });
      },
      formatScanDetails(scans) {
          for (let key in scans) {
              this.scanDetails.push({...scans[key], id:key});
          }
          console.log(this.scanDetails);
      },
}
}
</script>