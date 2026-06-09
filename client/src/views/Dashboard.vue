<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>{{ t('dashboard.title', 'Dashboard') }}</h1>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading', 'Loading...') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else-if="data">
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-label">{{ t('dashboard.openTickets', 'Open Tickets') }}</span>
          <span class="stat-value info">{{ data.open_tickets }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">{{ t('dashboard.avgResolution', 'Avg Resolution') }}</span>
          <span class="stat-value warning">{{ formatHours(data.avg_resolution_hours) }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">{{ t('dashboard.slaCompliance', 'SLA Compliance') }}</span>
          <span class="stat-value" :class="data.sla_compliance_pct >= 90 ? 'success' : 'danger'">
            {{ data.sla_compliance_pct.toFixed(1) }}%
          </span>
        </div>
        <div class="stat-card">
          <span class="stat-label">{{ t('dashboard.agentUtilization', 'Agent Utilization') }}</span>
          <span class="stat-value neutral">{{ data.agent_utilization.toFixed(1) }}%</span>
        </div>
      </div>

      <div class="charts-grid">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">{{ t('dashboard.statusDistribution', 'Status Distribution') }}</h2>
          </div>
          <div class="chart-container donut-container">
            <svg viewBox="0 0 180 180" class="donut-chart">
              <circle
                v-for="(segment, idx) in statusSegments"
                :key="idx"
                cx="90"
                cy="90"
                r="65"
                fill="none"
                :stroke="segment.color"
                stroke-width="28"
                :stroke-dasharray="`${segment.dash} ${circumference - segment.dash}`"
                :stroke-dashoffset="-segment.offset"
                :transform="`rotate(-90 90 90)`"
              />
              <text x="90" y="85" text-anchor="middle" class="donut-total">{{ data.total_tickets }}</text>
              <text x="90" y="102" text-anchor="middle" class="donut-label">{{ t('dashboard.total', 'Total') }}</text>
            </svg>
            <div class="chart-legend">
              <div v-for="(segment, idx) in statusSegments" :key="idx" class="legend-item">
                <span class="legend-dot" :style="{ backgroundColor: segment.color }"></span>
                <span class="legend-text">{{ segment.label }} ({{ segment.count }})</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h2 class="card-title">{{ t('dashboard.priorityBreakdown', 'Priority Breakdown') }}</h2>
          </div>
          <div class="chart-container bar-container">
            <div v-for="(bar, idx) in priorityBars" :key="idx" class="bar-row">
              <span class="bar-label">{{ bar.label }}</span>
              <div class="bar-track">
                <div
                  class="bar-fill"
                  :style="{ width: bar.pct + '%', backgroundColor: bar.color }"
                ></div>
              </div>
              <span class="bar-value">{{ bar.count }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2 class="card-title">{{ t('dashboard.recentTickets', 'Recent Tickets') }}</h2>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('tickets.id', 'ID') }}</th>
                <th>{{ t('tickets.subject', 'Subject') }}</th>
                <th>{{ t('tickets.status', 'Status') }}</th>
                <th>{{ t('tickets.priority', 'Priority') }}</th>
                <th>{{ t('tickets.created', 'Created') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ticket in data.recent_tickets" :key="ticket.id">
                <td>{{ ticket.id }}</td>
                <td>{{ ticket.subject }}</td>
                <td><span class="badge" :class="statusBadge(ticket.status)">{{ ticket.status }}</span></td>
                <td><span class="badge" :class="priorityBadge(ticket.priority)">{{ ticket.priority }}</span></td>
                <td>{{ formatDate(ticket.created_at) }}</td>
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
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { formatDate, formatHours } from '../utils/formatters'

const { t } = useI18n()
const { getCurrentFilters, selectedStatus, selectedPriority, selectedCategory, selectedAgent, selectedPeriod } = useFilters()

const data = ref(null)
const loading = ref(false)
const error = ref(null)

const circumference = 2 * Math.PI * 65 // ~408.4

const statusColors = {
  'Open': '#3b82f6',
  'In Progress': '#f59e0b',
  'Waiting': '#8b5cf6',
  'Escalated': '#ef4444',
  'Resolved': '#10b981',
  'Closed': '#6b7280'
}

const priorityColors = {
  'Critical': '#ef4444',
  'High': '#f59e0b',
  'Medium': '#3b82f6',
  'Low': '#6b7280'
}

const statusSegments = computed(() => {
  if (!data.value?.status_distribution) return []
  const dist = data.value.status_distribution
  const total = Object.values(dist).reduce((sum, v) => sum + v, 0)
  if (total === 0) return []

  const segments = []
  let offset = 0
  for (const [label, count] of Object.entries(dist)) {
    const dash = (count / total) * circumference
    segments.push({
      label,
      count,
      color: statusColors[label] || '#6b7280',
      dash,
      offset
    })
    offset += dash
  }
  return segments
})

const priorityBars = computed(() => {
  if (!data.value?.priority_distribution) return []
  const dist = data.value.priority_distribution
  const max = Math.max(...Object.values(dist), 1)

  return Object.entries(dist).map(([label, count]) => ({
    label,
    count,
    pct: (count / max) * 100,
    color: priorityColors[label] || '#6b7280'
  }))
})

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

async function loadData() {
  loading.value = true
  error.value = null
  try {
    data.value = await api.getDashboardSummary(getCurrentFilters())
  } catch (e) {
    error.value = e.message || 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

watch([selectedStatus, selectedPriority, selectedCategory, selectedAgent, selectedPeriod], () => {
  loadData()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.donut-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
}

.donut-chart {
  width: 180px;
  height: 180px;
  flex-shrink: 0;
}

.donut-total {
  font-size: 1.5rem;
  font-weight: 700;
  fill: var(--color-text, #1f2937);
}

.donut-label {
  font-size: 0.75rem;
  fill: var(--color-text-secondary, #6b7280);
}

.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.bar-container {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bar-label {
  width: 70px;
  font-size: 0.85rem;
  font-weight: 500;
  text-align: right;
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  height: 22px;
  background: var(--color-bg-secondary, #f3f4f6);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.bar-value {
  width: 32px;
  font-size: 0.85rem;
  font-weight: 600;
  text-align: right;
}
</style>
