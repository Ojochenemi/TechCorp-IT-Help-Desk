<template>
  <div class="app">
    <SidebarNav
      :collapsed="sidebarCollapsed"
      @toggle-collapse="sidebarCollapsed = !sidebarCollapsed"
      @show-profile-details="showProfileDetails = true"
      @show-tasks="showTasks = true"
    />
    <div class="main-area" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <TopBar
        @show-profile-details="showProfileDetails = true"
        @show-tasks="showTasks = true"
      />
      <FilterBar />
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuth } from './composables/useAuth'
import SidebarNav from './components/SidebarNav.vue'
import TopBar from './components/TopBar.vue'
import FilterBar from './components/FilterBar.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'

export default {
  name: 'App',
  components: {
    SidebarNav,
    TopBar,
    FilterBar,
    ProfileDetailsModal,
    TasksModal
  },
  setup() {
    const { currentUser } = useAuth()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const sidebarCollapsed = ref(false)

    const mediaQuery = window.matchMedia('(max-width: 1024px)')
    const handleMediaChange = (e) => {
      sidebarCollapsed.value = e.matches
    }
    sidebarCollapsed.value = mediaQuery.matches
    mediaQuery.addEventListener('change', handleMediaChange)

    onUnmounted(() => {
      mediaQuery.removeEventListener('change', handleMediaChange)
    })

    const tasks = computed(() => currentUser.value.tasks)

    const deleteTask = (taskId) => {
      const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
      if (index !== -1) currentUser.value.tasks.splice(index, 1)
    }

    const toggleTask = (taskId) => {
      const task = currentUser.value.tasks.find(t => t.id === taskId)
      if (task) task.status = task.status === 'pending' ? 'completed' : 'pending'
    }

    return {
      showProfileDetails,
      showTasks,
      tasks,
      deleteTask,
      toggleTask,
      sidebarCollapsed
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f8fafc;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  display: flex;
  min-height: 100vh;
}

.main-area {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f8fafc;
  transition: margin-left 0.2s ease;
}

.main-area.sidebar-collapsed {
  margin-left: 64px;
}

.main-content {
  flex: 1;
  padding: 1.5rem;
  max-width: 1400px;
  width: 100%;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: #64748b;
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.stat-label {
  color: #64748b;
  font-size: 0.8125rem;
  font-weight: 500;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value { color: #ea580c; }
.stat-card.success .stat-value { color: #059669; }
.stat-card.danger .stat-value { color: #dc2626; }
.stat-card.info .stat-value { color: #2563eb; }

.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: #64748b;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

td {
  padding: 0.75rem 1rem;
  border-top: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: #f8fafc;
}

tbody tr.clickable {
  cursor: pointer;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.025em;
}

.badge.success { background: #d1fae5; color: #065f46; }
.badge.warning { background: #fed7aa; color: #92400e; }
.badge.danger { background: #fecaca; color: #991b1b; }
.badge.info { background: #dbeafe; color: #1e40af; }
.badge.neutral { background: #e2e8f0; color: #475569; }

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.938rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
</style>
