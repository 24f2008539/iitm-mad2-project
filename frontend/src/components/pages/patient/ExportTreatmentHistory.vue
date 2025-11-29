<template>
  <patient-nav-bar></patient-nav-bar>
  <new-base-card>
    <div class="container mt-4">
      <h2>📊 Export Treatment History</h2>
      <hr />

      <!-- Export Section -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card border-primary">
            <div class="card-header bg-primary text-white">
              <h5>📥 Generate Export</h5>
            </div>
            <div class="card-body">
              <p>Download all your treatment history as a CSV file.</p>
              <p class="text-muted small">
                File will be available for 7 days after generation.
              </p>

              <button
                @click="triggerExport"
                :disabled="isExporting"
                class="btn btn-primary btn-block"
              >
                <span v-if="isExporting" class="spinner-border spinner-border-sm mr-2"></span>
                {{ isExporting ? "Generating..." : "Export as CSV" }}
              </button>

              <div v-if="exportError" class="alert alert-danger mt-3">
                {{ exportError }}
              </div>

              <div v-if="exportSuccess" class="alert alert-success mt-3">
                {{ exportSuccess }}
              </div>
            </div>
          </div>
        </div>

        <!-- Information Section -->
        <div class="col-md-6">
          <div class="card border-info">
            <div class="card-header bg-info text-white">
              <h5>ℹ️ What's Included</h5>
            </div>
            <div class="card-body">
              <ul>
                <li>Patient ID and Name</li>
                <li>Consulting Doctor Information</li>
                <li>Doctor's Specialization</li>
                <li>Appointment Dates</li>
                <li>Diagnosis Given</li>
                <li>Treatment/Prescription Details</li>
                <li>Follow-up Recommendations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Export History Section -->
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="card-header">
              <h5>📋 Your Exports</h5>
            </div>
            <div class="card-body">
              <div v-if="isLoadingExports" class="text-center">
                <the-loader></the-loader>
              </div>

              <div v-else-if="exports.length === 0" class="alert alert-info">
                No exports generated yet.
              </div>

              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-dark">
                    <tr>
                      <th>Created Date</th>
                      <th>Status</th>
                      <th>Type</th>
                      <th>Expires</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="exp in exports" :key="exp.id">
                      <td>{{ formatDate(exp.created_at) }}</td>
                      <td>
                        <span :class="getStatusBadgeClass(exp.status)">
                          {{ exp.status }}
                        </span>
                      </td>
                      <td>{{ exp.export_type.toUpperCase() }}</td>
                      <td>
                        <span v-if="exp.is_expired" class="badge badge-danger">
                          Expired
                        </span>
                        <span v-else class="badge badge-success">
                          {{ formatDate(exp.expires_at) }}
                        </span>
                      </td>
                      <td>
                        <button
                          v-if="exp.status === 'completed' && !exp.is_expired"
                          @click="downloadExport(exp.id)"
                          class="btn btn-sm btn-success"
                        >
                          ⬇️ Download
                        </button>
                        <button
                          v-else
                          disabled
                          class="btn btn-sm btn-secondary"
                        >
                          {{ getActionButtonText(exp) }}
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </new-base-card>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
import PatientNavBar from "../../ui/PatientNavBar.vue";
import NewBaseCard from "../../ui/NewBaseCard.vue";
import TheLoader from "../../ui/TheLoader.vue";

export default {
  components: {
    PatientNavBar,
    NewBaseCard,
    TheLoader,
  },
  data() {
    return {
      exports: [],
      isExporting: false,
      isLoadingExports: true,
      exportError: "",
      exportSuccess: "",
    };
  },
  computed: {
    ...mapState({
      showLoading: (state) => state.showLoading,
    }),
  },
  mounted() {
    this.loadExports();
    // Reload exports every 10 seconds to update status
    this.exportRefreshInterval = setInterval(() => {
      this.loadExports();
    }, 10000);
  },
  beforeUnmount() {
    if (this.exportRefreshInterval) {
      clearInterval(this.exportRefreshInterval);
    }
  },
  methods: {
    async triggerExport() {
      this.isExporting = true;
      this.exportError = "";
      this.exportSuccess = "";

      try {
        const token = localStorage.getItem("patient_access_token");
        const patientId = localStorage.getItem("patient_id");

        await axios.post(
          `http://localhost:5000/patient/${patientId}/export`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.exportSuccess = "✅ Export request received! Processing your data...";
        this.isExporting = false;

        // Reload exports after a short delay
        setTimeout(() => {
          this.loadExports();
        }, 2000);
      } catch (error) {
        this.isExporting = false;
        this.exportError =
          error.response?.data?.message || "Error creating export. Please try again.";
        console.error("Export error:", error);
      }
    },

    async loadExports() {
      this.isLoadingExports = true;
      try {
        const token = localStorage.getItem("patient_access_token");
        const patientId = localStorage.getItem("patient_id");

        const response = await axios.get(
          `http://localhost:5000/patient/${patientId}/exports`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.exports = response.data.exports || [];
        this.isLoadingExports = false;
      } catch (error) {
        this.isLoadingExports = false;
        console.error("Error loading exports:", error);
      }
    },

    async downloadExport(exportId) {
      try {
        const response = await axios.get(
          `http://localhost:5000/download/export/${exportId}`,
          {
            responseType: "blob",
          }
        );

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `treatment_history_${exportId}.csv`);
        document.body.appendChild(link);
        link.click();
        link.parentURL.removeChild(link);
      } catch (error) {
        console.error("Error downloading export:", error);
        alert("Error downloading file. Please try again.");
      }
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    getStatusBadgeClass(status) {
      const classes = "badge ";
      switch (status) {
        case "completed":
          return classes + "badge-success";
        case "processing":
          return classes + "badge-warning";
        case "pending":
          return classes + "badge-info";
        case "failed":
          return classes + "badge-danger";
        default:
          return classes + "badge-secondary";
      }
    },

    getActionButtonText(exp) {
      if (exp.is_expired) return "⏰ Expired";
      if (exp.status === "completed") return "⬇️ Download";
      if (exp.status === "processing") return "⏳ Processing...";
      return "⏱️ Pending...";
    },
  },
};
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: none;
  margin-bottom: 20px;
}

.card-header {
  border-bottom: 2px solid;
  font-weight: bold;
}

.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}

.btn-block {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  font-weight: bold;
}

.badge {
  padding: 8px 12px;
  font-size: 12px;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

ul li:before {
  content: "✓ ";
  color: #28a745;
  font-weight: bold;
  margin-right: 8px;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}
</style>
