<template>
  <div class="calendar-container">
    <CalendarHeader
      :current-date="currentDate"
      :view="view"
      @date-change="handleDateChange"
      @view-change="handleViewChange"
      @create-event="handleCreateEvent"
    />
    <div class="calendar-content">
      <CalendarSidebar
        :current-date="currentDate"
        :view="view"
        @date-change="handleDateChange"
        @view-change="handleViewChange"
      />
      <div class="calendar-main">
        <div v-if="loading" class="loading">Loading events...</div>
        <MonthView
          v-else-if="view === 'month'"
          :current-date="currentDate"
          :events="events"
          @event-click="handleEditEvent"
          @date-click="handleDateChange"
        />
        <WeekView
          v-else-if="view === 'week'"
          :current-date="currentDate"
          :events="events"
          @event-click="handleEditEvent"
          @date-change="handleDateChange"
        />
        <DayView
          v-else-if="view === 'day'"
          :current-date="currentDate"
          :events="events"
          @event-click="handleEditEvent"
          @date-change="handleDateChange"
        />
      </div>
    </div>
    <EventModal
      v-if="isModalOpen"
      :event="selectedEvent"
      @save="handleSaveEvent"
      @close="handleCloseModal"
      @delete="selectedEvent ? () => handleDeleteEvent(selectedEvent.id) : null"
    />
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { startOfMonth, endOfMonth, startOfWeek, endOfWeek, startOfDay, endOfDay } from 'date-fns'
import CalendarHeader from './CalendarHeader.vue'
import CalendarSidebar from './CalendarSidebar.vue'
import MonthView from './views/MonthView.vue'
import WeekView from './views/WeekView.vue'
import DayView from './views/DayView.vue'
import EventModal from './EventModal.vue'
import { eventService } from '../services/api'

export default {
  name: 'Calendar',
  components: {
    CalendarHeader,
    CalendarSidebar,
    MonthView,
    WeekView,
    DayView,
    EventModal,
  },
  setup() {
    const currentDate = ref(new Date())
    const view = ref('month')
    const events = ref([])
    const selectedEvent = ref(null)
    const isModalOpen = ref(false)
    const loading = ref(false)

    const getDateRange = () => {
      switch (view.value) {
        case 'month':
          return {
            start: startOfWeek(startOfMonth(currentDate.value)),
            end: endOfWeek(endOfMonth(currentDate.value)),
          }
        case 'week':
          return {
            start: startOfWeek(currentDate.value),
            end: endOfWeek(currentDate.value),
          }
        case 'day':
          return {
            start: startOfDay(currentDate.value),
            end: endOfDay(currentDate.value),
          }
        default:
          return {
            start: startOfMonth(currentDate.value),
            end: endOfMonth(currentDate.value),
          }
      }
    }

    const fetchEvents = async () => {
      loading.value = true
      try {
        const { start, end } = getDateRange()
        const data = await eventService.getEventsByDateRange(start, end)
        events.value = data
      } catch (error) {
        console.error('Error fetching events:', error)
      } finally {
        loading.value = false
      }
    }

    watch([currentDate, view], () => {
      fetchEvents()
    }, { immediate: true })

    const handleDateChange = (newDate) => {
      currentDate.value = newDate
    }

    const handleViewChange = (newView) => {
      view.value = newView
    }

    const handleCreateEvent = () => {
      selectedEvent.value = null
      isModalOpen.value = true
    }

    const handleEditEvent = (event) => {
      selectedEvent.value = event
      isModalOpen.value = true
    }

    const handleDeleteEvent = async (eventId) => {
      if (window.confirm('Are you sure you want to delete this event?')) {
        try {
          await eventService.deleteEvent(eventId)
          await fetchEvents()
        } catch (error) {
          console.error('Error deleting event:', error)
          alert('Failed to delete event')
        }
      }
    }

    const handleSaveEvent = async (eventData) => {
      try {
        if (selectedEvent.value && selectedEvent.value.id) {
          await eventService.updateEvent(selectedEvent.value.id, eventData)
        } else {
          await eventService.createEvent(eventData)
        }
        
        await fetchEvents()
        isModalOpen.value = false
        selectedEvent.value = null
      } catch (error) {
        console.error('Error saving event:', error)
        alert('Failed to save event')
      }
    }

    const handleCloseModal = () => {
      isModalOpen.value = false
      selectedEvent.value = null
    }

    return {
      currentDate,
      view,
      events,
      selectedEvent,
      isModalOpen,
      loading,
      handleDateChange,
      handleViewChange,
      handleCreateEvent,
      handleEditEvent,
      handleDeleteEvent,
      handleSaveEvent,
      handleCloseModal,
    }
  },
}
</script>

<style scoped>
.calendar-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #fff;
  font-family: 'Google Sans', Roboto, Arial, sans-serif;
}

.calendar-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.calendar-main {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background-color: #fff;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 14px;
  color: #5f6368;
}

.calendar-main::-webkit-scrollbar {
  width: 8px;
}

.calendar-main::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.calendar-main::-webkit-scrollbar-thumb {
  background: #dadce0;
  border-radius: 4px;
}

.calendar-main::-webkit-scrollbar-thumb:hover {
  background: #bdc1c6;
}
</style>

