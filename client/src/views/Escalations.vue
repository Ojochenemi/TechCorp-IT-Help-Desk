<template>
  <div class="escalations">
    <div class="page-header">
      <h1>{{ t('escalations.title') }}</h1>
      <p>{{ t('escalations.subtitle') }}</p>
    </div>

    <div v-if="loading" class="loading">Loading escalation data...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-label">Total Escalations</span>
          <span class="stat-value">{{ escalations.length }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Active</span>
          <span class="stat-value" style="color: var(--color-danger, #ef4444);">{{ activeCount }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Resolved</span>
          <span class="stat-value" style="color: var(--color-success, #10b981);">{{ resolvedCount }}</span>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Escalation Records</h2>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Ticket ID</th>
                <th>Reason</th>
                <th>From</th>
                <th>To</th>
                <th>Escalated At</th>
                <th>Status</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="esc in filteredEscalations" :key="esc.id">
                <td>#{{ esc.ticket_id }}</td>
                <td>{{ esc.reason }}</td>
                <td>{{ agentMap[esc.escalated_from] || 'Unknown' }}</td>
                <td>{{ agentMap[esc.escalated_to] || 'Unknown' }}</td>
                <td>{{ formatDate(esc.escalated_at) }}</td>
                <td>
                  <span :class="['badge', statusBadge(esc.status)]">
                    {{ esc.status }}
                  </span>
                </td>
                <td>{{ esc.notes || '—' }}</td>
              </tr>
              <tr v-if="filteredEscalations.length === 0">
                <td colspan="7" style="text-align: center;">No escalations found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'
import { useFilters } from '../composables/useFilters'
import { formatDate } from '../utils/formatters'

const { t } = useI18n()
const { selectedStatus, selectedPriority } = useFilters()

const escalations = ref([])
const agentMap = ref({})
const loading = ref(true)
const error = ref(null)

const activeCount = computed(() =>
  escalations.value.filter(e => e.status === 'Active').length
)

const resolvedCount = computed(() =>
  escalations.value.filter(e => e.status === 'Resolved').length
)

const filteredEscalations = computed(() => {
  let result = escalations.value
  if (selectedStatus.value) {
    result = result.filter(e => e.status === selectedStatus.value)
  }
  return result
})

function statusBadge(status) {
  const map = {
    Active: 'danger',
    Resolved: 'success',
    Reassigned: 'warning'
  }
  return map[status] || 'neutral'
}

async function loadData() {
  loading.value = true
  error.value = null
  try {
    const [escalationData, agents] = await Promise.all([
      api.getEscalations({ status: selectedStatus.value, priority: selectedPriority.value }),
      api.getAgents()
    ])
    escalations.value = escalationData
    agentMap.value = Object.fromEntries(agents.map(a => [a.id, a.name]))
  } catch (err) {
    error.value = 'Failed to load escalation data: ' + err.message
  } finally {
    loading.value = false
  }
}

watch([selectedStatus, selectedPriority], () => {
  loadData()
})

onMounted(loadData)
</script>

<style scoped>
.escalations {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
