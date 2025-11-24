import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const eventService = {
  getEvents: async (startDate, endDate) => {
    const params = {}
    if (startDate) params.start_date = startDate.toISOString()
    if (endDate) params.end_date = endDate.toISOString()
    
    const response = await api.get('/events/', { params })
    return response.data
  },

  getEventsByDateRange: async (startDate, endDate) => {
    const response = await api.get('/events/by_date_range/', {
      params: {
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
      },
    })
    return response.data
  },

  getEvent: async (id) => {
    const response = await api.get(`/events/${id}/`)
    return response.data
  },

  createEvent: async (eventData) => {
    const response = await api.post('/events/', eventData)
    return response.data
  },

  updateEvent: async (id, eventData) => {
    const response = await api.put(`/events/${id}/`, eventData)
    return response.data
  },

  deleteEvent: async (id) => {
    await api.delete(`/events/${id}/`)
  },

  checkOverlap: async (startTime, endTime, excludeId = null) => {
    const params = {
      start_time: startTime.toISOString(),
      end_time: endTime.toISOString(),
    }
    if (excludeId) params.exclude_id = excludeId
    
    const response = await api.get('/events/check_overlap/', { params })
    return response.data
  },
}

export default api

