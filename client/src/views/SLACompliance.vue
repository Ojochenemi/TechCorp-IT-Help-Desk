<template>
  <div class="sla-compliance">
    <div class="page-header">
      <h1>{{ t('sla.title') }}</h1>
      <p>{{ t('sla.subtitle') }}</p>
    </div>

    <div v-if="loading" class="loading">Loading SLA data...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="charts-grid">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">SLA Rules</h2>
          </div>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Priority</th>
                  <th>Response Target</th>
                  <th>Resolution Target</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="rule in compliance" :key="rule.priority">
                  <td>
                    <span :class="['badge', priorityBadge(rule.priority)]">
                      {{ rule.priority }}
                    </span>
                  </td>
                  <td>{{ formatDuration(rule.response_target_minutes) }}</td>
                  <td>{{ formatDuration(rule.resolution_target_minutes) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Compliance Summary</h2>
          </div>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Priority</th>
                  <th>Total Tickets</th>
                  <th>Response Compliance</th>
                  <th>Resolution Compliance</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="rule in compliance" :key="rule.priority">
                  <td>
                    <span :class="['badge', priorityBadge(rule.priority)]">
                      {{ rule.priority }}
                    </span>
                  </td>
                  <td>{{ rule.total_tickets }}</td>
                  <td>
                    <span :class="['badge', complianceColor(rule.response_compliance_pct)]">
                      {{ rule.response_compliance_pct.toFixed(1) }}%
                    </span>
                  </td>
                  <td>
                    <span :class="['badge', complianceColor(rule.resolution_compliance_pct)]">
                      {{ rule.resolution_compliance_pct.toFixed(1) }}%
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2 class="card-title">SLA Breaches</h2>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Subject</th>
                <th>Priority</th>
                <th>Response</th>
                <th>Resolution</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ticket in breaches" :key="ticket.id">
                <td>#{{ ticket.id }}</td>
                <td>{{ ticket.subject }}</td>
                <td>
                  <span :class="['badge', priorityBadge(ticket.priority)]">
                    {{ ticket.priority }}
                  </span>
                </td>
                <td>
                  <span :class="['badge', ticket.sla_status?.response_met ? 'success' : 'danger']">
                    {{ ticket.sla_status?.response_met ? 'Met' : 'Breached' }}
                  </span>
                </td>
                <td>
                  <span :class="['badge', ticket.sla_status?.resolution_met ? 'success' : 'danger']">
                    {{ ticket.sla_status?.resolution_met ? 'Met' : 'Breached' }}
                  </span>
                </td>
              </tr>
              <tr v-if="breaches.length === 0">
                <td colspan="5" style="text-align: center;">No SLA breaches found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'
import { formatDuration } from '../utils/formatters'

const { t } = useI18n()

const compliance = ref([])
const breaches = ref([])
const loading = ref(true)
const error = ref(null)

function priorityBadge(priority) {
  const map = {
    Critical: 'danger',
    High: 'warning',
    Medium: 'info',
    Low: 'neutral'
  }
  return map[priority] || 'neutral'
}

function complianceColor(pct) {
  if (pct >= 90) return 'success'
  if (pct >= 75) return 'warning'
  return 'danger'
}

async function loadData() {
  loading.value = true
  error.value = null
  try {
    const [complianceData, breachData] = await Promise.all([
      api.getSLACompliance(),
      api.getSLABreaches()
    ])
    compliance.value = complianceData
    breaches.value = breachData
  } catch (err) {
    error.value = 'Failed to load SLA data: ' + err.message
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.sla-compliance {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
