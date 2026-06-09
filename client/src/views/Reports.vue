<template>
  <div class="reports">
    <div class="page-header">
      <h1>{{ t('reports.title') }}</h1>
      <p>{{ t('reports.subtitle') }}</p>
    </div>

    <div v-if="loading" class="loading">Loading report data...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="charts-grid">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Monthly Ticket Trends</h2>
          </div>
          <div class="chart-container">
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-dot created"></span> Created</span>
              <span class="legend-item"><span class="legend-dot resolved"></span> Resolved</span>
              <span class="legend-item"><span class="legend-dot escalated"></span> Escalated</span>
            </div>
            <div class="chart-bars">
              <div v-for="item in trends" :key="item.month" class="bar-group">
                <div class="bars">
                  <div
                    class="bar created"
                    :style="{ height: (item.created_count / maxCount * 120) + 'px' }"
                    :title="'Created: ' + item.created_count"
                  ></div>
                  <div
                    class="bar resolved"
                    :style="{ height: (item.resolved_count / maxCount * 120) + 'px' }"
                    :title="'Resolved: ' + item.resolved_count"
                  ></div>
                  <div
                    class="bar escalated"
                    :style="{ height: (item.escalated_count / maxCount * 120) + 'px' }"
                    :title="'Escalated: ' + item.escalated_count"
                  ></div>
                </div>
                <span class="bar-label">{{ formatMonth(item.month) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Agent Performance</h2>
          </div>
          <div class="performance-summary" v-if="topPerformer">
            <div class="top-performer">
              <span class="performer-label">Top Performer</span>
              <span class="performer-name">{{ topPerformer.agent_name }}</span>
              <span class="performer-role">{{ topPerformer.role }}</span>
            </div>
            <div class="performance-stats">
              <div class="perf-stat">
                <span class="perf-stat-value">{{ topPerformer.avg_satisfaction.toFixed(1) }} &#9733;</span>
                <span class="perf-stat-label">Satisfaction</span>
              </div>
              <div class="perf-stat">
                <span class="perf-stat-value">{{ topPerformer.total_resolved }}</span>
                <span class="perf-stat-label">Resolved</span>
              </div>
              <div class="perf-stat">
                <span class="perf-stat-value">{{ topPerformer.sla_compliance_pct.toFixed(1) }}%</span>
                <span class="perf-stat-label">SLA Compliance</span>
              </div>
              <div class="perf-stat">
                <span class="perf-stat-value">{{ formatHours(topPerformer.avg_resolution_hours) }}</span>
                <span class="perf-stat-label">Avg Resolution</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Agent Performance Comparison</h2>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Agent</th>
                <th>Role</th>
                <th>Assigned</th>
                <th>Resolved</th>
                <th>Open</th>
                <th>Avg Resolution</th>
                <th>Satisfaction</th>
                <th>SLA Compliance</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="agent in agents" :key="agent.agent_id">
                <td>{{ agent.agent_name }}</td>
                <td>{{ agent.role }}</td>
                <td>{{ agent.total_assigned }}</td>
                <td>{{ agent.total_resolved }}</td>
                <td>{{ agent.open_tickets }}</td>
                <td>{{ formatHours(agent.avg_resolution_hours) }}</td>
                <td>{{ agent.avg_satisfaction.toFixed(1) }} &#9733;</td>
                <td>
                  <span :class="['badge', complianceColor(agent.sla_compliance_pct)]">
                    {{ agent.sla_compliance_pct.toFixed(1) }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'
import { formatHours } from '../utils/formatters'

const { t } = useI18n()

const trends = ref([])
const agents = ref([])
const loading = ref(true)
const error = ref(null)

const maxCount = computed(() => {
  if (trends.value.length === 0) return 1
  return Math.max(
    ...trends.value.flatMap(t => [t.created_count, t.resolved_count, t.escalated_count]),
    1
  )
})

const topPerformer = computed(() => {
  if (agents.value.length === 0) return null
  return [...agents.value].sort((a, b) => b.avg_satisfaction - a.avg_satisfaction)[0]
})

function complianceColor(pct) {
  if (pct >= 90) return 'success'
  if (pct >= 75) return 'warning'
  return 'danger'
}

function formatMonth(monthStr) {
  if (!monthStr) return ''
  const [year, month] = monthStr.split('-')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return months[parseInt(month, 10) - 1] || monthStr
}

async function loadData() {
  loading.value = true
  error.value = null
  try {
    const [trendsData, agentData] = await Promise.all([
      api.getMonthlyTrends(),
      api.getAgentPerformance()
    ])
    trends.value = trendsData
    agents.value = agentData
  } catch (err) {
    error.value = 'Failed to load report data: ' + err.message
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.reports {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chart-container {
  padding: 1rem;
}

.chart-legend {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  display: inline-block;
}

.legend-dot.created {
  background-color: #3b82f6;
}

.legend-dot.resolved {
  background-color: #10b981;
}

.legend-dot.escalated {
  background-color: #ef4444;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  padding: 0.5rem 0;
  overflow-x: auto;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}

.bars {
  display: flex;
  align-items: flex-end;
  gap: 3px;
}

.bar {
  min-width: 12px;
  border-radius: 3px 3px 0 0;
  transition: height 0.3s ease;
  cursor: default;
}

.bar.created {
  background-color: #3b82f6;
}

.bar.resolved {
  background-color: #10b981;
}

.bar.escalated {
  background-color: #ef4444;
}

.bar-label {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
}

.performance-summary {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.top-performer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.performer-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
}

.performer-name {
  font-size: 1.25rem;
  font-weight: 600;
}

.performer-role {
  font-size: 0.85rem;
  color: #6b7280;
}

.performance-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.perf-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
}

.perf-stat-value {
  font-size: 1.1rem;
  font-weight: 600;
}

.perf-stat-label {
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
