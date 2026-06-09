<template>
  <div class="tickets">
    <div class="page-header">
      <h1>{{ t('tickets.title', 'Tickets') }}</h1>
      <p>{{ t('tickets.subtitle', 'Browse and manage all support tickets') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading', 'Loading...') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">{{ t('tickets.allTickets', 'All Tickets') }} ({{ tickets.length }})</h2>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('tickets.id', 'ID') }}</th>
                <th>{{ t('tickets.subject', 'Subject') }}</th>
                <th>{{ t('tickets.status', 'Status') }}</th>
                <th>{{ t('tickets.priority', 'Priority') }}</th>
                <th>{{ t('tickets.category', 'Category') }}</th>
                <th>{{ t('tickets.assignedTo', 'Assigned To') }}</th>
                <th>{{ t('tickets.created', 'Created') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="ticket in tickets"
                :key="ticket.id"
                class="ticket-row"
                @click="openTicket(ticket.id)"
              >
                <td>{{ ticket.id }}</td>
                <td>{{ ticket.subject }}</td>
                <td><span class="badge" :class="statusBadge(ticket.status)">{{ ticket.status }}</span></td>
                <td><span class="badge" :class="priorityBadge(ticket.priority)">{{ ticket.priority }}</span></td>
                <td>{{ ticket.category }}</td>
                <td>{{ agentName(ticket.assigned_to) }}</td>
                <td>{{ formatDate(ticket.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <TicketDetailModal
      v-if="selectedTicket"
      :ticket="selectedTicket"
      @close="selectedTicket = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { formatDate } from '../utils/formatters'
import TicketDetailModal from '../components/TicketDetailModal.vue'

const { t } = useI18n()
const { getCurrentFilters, selectedStatus, selectedPriority, selectedCategory, selectedAgent, selectedPeriod } = useFilters()

const tickets = ref([])
const agents = ref({})
const loading = ref(false)
const error = ref(null)
const selectedTicket = ref(null)

function statusBadge(status) {
  const map = {
    'Open': 'info',
    'In Progress': 'warning',
    'Waiting on Customer': 'warning',
    'Escalated': 'danger',
    'Resolved': 'success',
    'Closed': 'neutral'
  }
  return map[status] || 'neutral'
}

function priorityBadge(priority) {
  const map = { 'Critical': 'danger', 'High': 'warning', 'Medium': 'info', 'Low': 'neutral' }
  return map[priority] || 'neutral'
}

function agentName(agentId) {
  if (!agentId) return '-'
  const agent = agents.value[agentId]
  return agent ? agent.name : agentId
}

async function loadAgents() {
  try {
    const list = await api.getAgents()
    const lookup = {}
    for (const agent of list) {
      lookup[agent.id] = agent
    }
    agents.value = lookup
  } catch {
    // Agent lookup is non-critical; rows will fall back to IDs
  }
}

async function loadTickets() {
  loading.value = true
  error.value = null
  try {
    tickets.value = await api.getTickets(getCurrentFilters())
  } catch (e) {
    error.value = e.message || 'Failed to load tickets'
  } finally {
    loading.value = false
  }
}

async function openTicket(id) {
  try {
    selectedTicket.value = await api.getTicket(id)
  } catch (e) {
    error.value = e.message || 'Failed to load ticket details'
  }
}

watch([selectedStatus, selectedPriority, selectedCategory, selectedAgent, selectedPeriod], () => {
  loadTickets()
})

onMounted(() => {
  loadAgents()
  loadTickets()
})
</script>

<style scoped>
.ticket-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.ticket-row:hover {
  background-color: var(--color-bg-hover, #f9fafb);
}
</style>
