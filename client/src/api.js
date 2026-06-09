import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001/api'

export const api = {
  // Tickets
  async getTickets(filters = {}) {
    const params = new URLSearchParams()
    if (filters.status && filters.status !== 'all') params.append('status', filters.status)
    if (filters.priority && filters.priority !== 'all') params.append('priority', filters.priority)
    if (filters.category && filters.category !== 'all') params.append('category', filters.category)
    if (filters.agent_id && filters.agent_id !== 'all') params.append('agent_id', filters.agent_id)
    if (filters.month && filters.month !== 'all') params.append('month', filters.month)
    const response = await axios.get(`${API_BASE_URL}/tickets?${params.toString()}`)
    return response.data
  },

  async getTicket(id) {
    const response = await axios.get(`${API_BASE_URL}/tickets/${id}`)
    return response.data
  },

  async createTicket(data) {
    const response = await axios.post(`${API_BASE_URL}/tickets`, data)
    return response.data
  },

  // Agents
  async getAgents(filters = {}) {
    const params = new URLSearchParams()
    if (filters.status && filters.status !== 'all') params.append('status', filters.status)
    if (filters.role && filters.role !== 'all') params.append('role', filters.role)
    const response = await axios.get(`${API_BASE_URL}/agents?${params.toString()}`)
    return response.data
  },

  async getAgent(id) {
    const response = await axios.get(`${API_BASE_URL}/agents/${id}`)
    return response.data
  },

  // Escalations
  async getEscalations(filters = {}) {
    const params = new URLSearchParams()
    if (filters.status && filters.status !== 'all') params.append('status', filters.status)
    if (filters.priority && filters.priority !== 'all') params.append('priority', filters.priority)
    const response = await axios.get(`${API_BASE_URL}/escalations?${params.toString()}`)
    return response.data
  },

  // SLA
  async getSLACompliance() {
    const response = await axios.get(`${API_BASE_URL}/sla/compliance`)
    return response.data
  },

  async getSLABreaches() {
    const response = await axios.get(`${API_BASE_URL}/sla/breaches`)
    return response.data
  },

  // Dashboard
  async getDashboardSummary(filters = {}) {
    const params = new URLSearchParams()
    if (filters.status && filters.status !== 'all') params.append('status', filters.status)
    if (filters.priority && filters.priority !== 'all') params.append('priority', filters.priority)
    if (filters.category && filters.category !== 'all') params.append('category', filters.category)
    if (filters.agent_id && filters.agent_id !== 'all') params.append('agent_id', filters.agent_id)
    if (filters.month && filters.month !== 'all') params.append('month', filters.month)
    const response = await axios.get(`${API_BASE_URL}/dashboard/summary?${params.toString()}`)
    return response.data
  },

  // Reports
  async getMonthlyTrends() {
    const response = await axios.get(`${API_BASE_URL}/reports/monthly-trends`)
    return response.data
  },

  async getAgentPerformance() {
    const response = await axios.get(`${API_BASE_URL}/reports/agent-performance`)
    return response.data
  },

  // Satisfaction
  async getSatisfactionSummary() {
    const response = await axios.get(`${API_BASE_URL}/satisfaction/summary`)
    return response.data
  },

  // Categories
  async getCategories() {
    const response = await axios.get(`${API_BASE_URL}/categories`)
    return response.data
  }
}
