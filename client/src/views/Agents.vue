<template>
  <div class="agents">
    <div class="page-header">
      <h1>{{ t('agents.title', 'Agents') }}</h1>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading', 'Loading...') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="agents-grid">
        <div
          v-for="agent in agents"
          :key="agent.id"
          class="card agent-card"
        >
          <div class="agent-header">
            <div class="avatar" :style="{ backgroundColor: roleColor(agent.role) }">
              {{ initials(agent.name) }}
            </div>
            <div class="agent-info">
              <h3 class="agent-name">{{ agent.name }}</h3>
              <div class="agent-meta">
                <span class="badge info">{{ agent.role }}</span>
                <span class="status-indicator" :class="statusClass(agent.status)">
                  <span class="status-dot"></span>
                  {{ agent.status }}
                </span>
              </div>
            </div>
          </div>

          <div class="agent-stats">
            <div class="agent-stat">
              <span class="agent-stat-value">{{ agent.assigned_tickets ?? '-' }}</span>
              <span class="agent-stat-label">{{ t('agents.assigned', 'Assigned') }}</span>
            </div>
            <div class="agent-stat">
              <span class="agent-stat-value">{{ agent.resolved_tickets ?? '-' }}</span>
              <span class="agent-stat-label">{{ t('agents.resolved', 'Resolved') }}</span>
            </div>
            <div class="agent-stat">
              <span class="agent-stat-value">{{ agent.avg_resolution_hours != null ? formatHours(agent.avg_resolution_hours) : '-' }}</span>
              <span class="agent-stat-label">{{ t('agents.avgResolution', 'Avg Resolution') }}</span>
            </div>
            <div class="agent-stat">
              <span class="agent-stat-value">
                <template v-if="agent.avg_satisfaction != null">
                  {{ agent.avg_satisfaction.toFixed(1) }} ★
                </template>
                <template v-else>-</template>
              </span>
              <span class="agent-stat-label">{{ t('agents.satisfaction', 'Satisfaction') }}</span>
            </div>
          </div>

          <div v-if="agent.skills && agent.skills.length" class="agent-skills">
            <span v-for="skill in agent.skills" :key="skill" class="skill-tag">{{ skill }}</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { formatHours } from '../utils/formatters'

const { t } = useI18n()
const { getCurrentFilters, selectedStatus, selectedPriority, selectedCategory, selectedAgent, selectedPeriod } = useFilters()

const agents = ref([])
const loading = ref(false)
const error = ref(null)

const roleColors = {
  'L1': '#3b82f6',
  'L2': '#8b5cf6',
  'L3': '#f59e0b'
}

function roleColor(role) {
  return roleColors[role] || '#6b7280'
}

function initials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

function statusClass(status) {
  const map = {
    'Available': 'available',
    'Busy': 'busy',
    'Away': 'away'
  }
  return map[status] || 'away'
}

async function loadData() {
  loading.value = true
  error.value = null
  try {
    const list = await api.getAgents()
    const detailed = await Promise.all(
      list.map(async (agent) => {
        try {
          const detail = await api.getAgent(agent.id)
          return { ...agent, ...detail }
        } catch {
          return agent
        }
      })
    )
    agents.value = detailed
  } catch (e) {
    error.value = e.message || 'Failed to load agents'
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
.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.25rem;
}

.agent-card {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  cursor: default;
}

.agent-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.agent-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  flex-shrink: 0;
}

.agent-info {
  flex: 1;
  min-width: 0;
}

.agent-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.agent-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;
  color: var(--color-text-secondary, #6b7280);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.available .status-dot {
  background-color: #10b981;
}

.busy .status-dot {
  background-color: #f59e0b;
}

.away .status-dot {
  background-color: #9ca3af;
}

.agent-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--color-border, #e5e7eb);
}

.agent-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.agent-stat-value {
  font-size: 0.95rem;
  font-weight: 700;
}

.agent-stat-label {
  font-size: 0.7rem;
  color: var(--color-text-secondary, #6b7280);
  margin-top: 0.15rem;
}

.agent-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  padding: 0.5rem 1rem 1rem;
  border-top: 1px solid var(--color-border, #e5e7eb);
}

.skill-tag {
  font-size: 0.7rem;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  background-color: var(--color-bg-secondary, #f3f4f6);
  color: var(--color-text-secondary, #6b7280);
}
</style>
