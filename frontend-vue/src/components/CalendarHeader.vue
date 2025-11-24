<template>
  <header class="calendar-header">
    <div class="header-left">
      <div class="logo-section">
        <svg class="calendar-icon" viewBox="0 0 24 24" width="40" height="40">
          <path fill="#4285f4" d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zm0-12H5V6h14v2z"/>
          <path fill="#34a853" d="M7 12h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2zm-8 4h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
        </svg>
        <span class="logo-text">Calendar</span>
      </div>
      <div class="date-navigation">
        <button class="nav-button" @click="handlePrevious" aria-label="Previous">
          <svg width="24" height="24" viewBox="0 0 24 24">
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
          </svg>
        </button>
        <button class="nav-button" @click="handleNext" aria-label="Next">
          <svg width="24" height="24" viewBox="0 0 24 24">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </button>
        <button class="today-button" @click="handleToday">Today</button>
        <div class="date-label">{{ dateLabel }}</div>
      </div>
    </div>
    <div class="header-right">
      <div class="view-selector">
        <button
          :class="['view-button', { active: view === 'month' }]"
          @click="$emit('view-change', 'month')"
        >
          Month
        </button>
        <button
          :class="['view-button', { active: view === 'week' }]"
          @click="$emit('view-change', 'week')"
        >
          Week
        </button>
        <button
          :class="['view-button', { active: view === 'day' }]"
          @click="$emit('view-change', 'day')"
        >
          Day
        </button>
      </div>
      <button class="create-event-button" @click="$emit('create-event')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
        </svg>
        <span>Create</span>
      </button>
    </div>
  </header>
</template>

<script>
import { computed } from 'vue'
import { format, addMonths, subMonths, addWeeks, subWeeks, addDays, subDays, startOfToday } from 'date-fns'

export default {
  name: 'CalendarHeader',
  props: {
    currentDate: {
      type: Date,
      required: true,
    },
    view: {
      type: String,
      required: true,
    },
  },
  emits: ['date-change', 'view-change', 'create-event'],
  setup(props, { emit }) {
    const handlePrevious = () => {
      let newDate
      switch (props.view) {
        case 'month':
          newDate = subMonths(props.currentDate, 1)
          break
        case 'week':
          newDate = subWeeks(props.currentDate, 1)
          break
        case 'day':
          newDate = subDays(props.currentDate, 1)
          break
        default:
          newDate = props.currentDate
      }
      emit('date-change', newDate)
    }

    const handleNext = () => {
      let newDate
      switch (props.view) {
        case 'month':
          newDate = addMonths(props.currentDate, 1)
          break
        case 'week':
          newDate = addWeeks(props.currentDate, 1)
          break
        case 'day':
          newDate = addDays(props.currentDate, 1)
          break
        default:
          newDate = props.currentDate
      }
      emit('date-change', newDate)
    }

    const handleToday = () => {
      emit('date-change', startOfToday())
    }

    const dateLabel = computed(() => {
      switch (props.view) {
        case 'month':
          return format(props.currentDate, 'MMMM yyyy')
        case 'week':
          return `Week of ${format(props.currentDate, 'MMM d, yyyy')}`
        case 'day':
          return format(props.currentDate, 'EEEE, MMMM d, yyyy')
        default:
          return format(props.currentDate, 'MMMM yyyy')
      }
    })

    return {
      handlePrevious,
      handleNext,
      handleToday,
      dateLabel,
    }
  },
}
</script>

<style scoped>
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  border-bottom: 1px solid #dadce0;
  background-color: #fff;
  min-height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-right: 16px;
  border-right: 1px solid #dadce0;
}

.calendar-icon {
  cursor: pointer;
}

.logo-text {
  font-size: 22px;
  font-weight: 400;
  color: #5f6368;
  cursor: pointer;
}

.date-navigation {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5f6368;
  transition: background-color 0.2s;
}

.nav-button:hover {
  background-color: #f1f3f4;
}

.today-button {
  background: none;
  border: 1px solid #dadce0;
  border-radius: 4px;
  padding: 6px 16px;
  cursor: pointer;
  font-size: 14px;
  color: #5f6368;
  margin-left: 8px;
  transition: background-color 0.2s;
}

.today-button:hover {
  background-color: #f8f9fa;
}

.date-label {
  font-size: 22px;
  font-weight: 400;
  color: #3c4043;
  margin-left: 16px;
  min-width: 200px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.view-selector {
  display: flex;
  background-color: #f1f3f4;
  border-radius: 4px;
  padding: 4px;
  gap: 4px;
}

.view-button {
  background: none;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #5f6368;
  transition: all 0.2s;
}

.view-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.view-button.active {
  background-color: #fff;
  color: #1a73e8;
  font-weight: 500;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.create-event-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #1a73e8;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 8px 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.create-event-button:hover {
  background-color: #1557b0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.create-event-button svg {
  width: 20px;
  height: 20px;
}
</style>

