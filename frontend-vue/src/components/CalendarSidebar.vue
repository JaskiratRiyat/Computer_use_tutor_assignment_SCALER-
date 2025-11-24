<template>
  <aside class="calendar-sidebar">
    <div class="sidebar-content">
      <div class="mini-calendar">
        <div class="mini-calendar-header">{{ monthLabel }}</div>
        <div class="mini-calendar-days-header">
          <div v-for="(day, index) in dayNames" :key="index" class="mini-calendar-day-name">
            {{ day }}
          </div>
        </div>
        <div class="mini-calendar-grid">
          <div
            v-for="(date, index) in miniCalendarDays"
            :key="index"
            :class="[
              'mini-calendar-day',
              {
                empty: !date,
                selected: date && isSameDayHelper(date, currentDate),
                today: date && isSameDayHelper(date, today),
                'other-month': date && date.getMonth() !== currentDate.getMonth(),
              },
            ]"
            @click="date && handleMiniCalendarClick(date)"
          >
            {{ date ? date.getDate() : '' }}
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
import { computed } from 'vue'
import { format, startOfToday } from 'date-fns'

export default {
  name: 'CalendarSidebar',
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
  emits: ['date-change', 'view-change'],
  setup(props, { emit }) {
    const today = startOfToday()
    const isSameDayHelper = (date1, date2) => {
      return date1.getDate() === date2.getDate() &&
             date1.getMonth() === date2.getMonth() &&
             date1.getFullYear() === date2.getFullYear()
    }

    const monthLabel = computed(() => {
      return format(props.currentDate, 'MMMM yyyy')
    })

    const dayNames = ['S', 'M', 'T', 'W', 'T', 'F', 'S']

    const miniCalendarDays = computed(() => {
      const days = []
      const startOfCurrentMonth = new Date(props.currentDate.getFullYear(), props.currentDate.getMonth(), 1)
      const endOfCurrentMonth = new Date(props.currentDate.getFullYear(), props.currentDate.getMonth() + 1, 0)
      const startDay = startOfCurrentMonth.getDay()
      
      for (let i = 0; i < startDay; i++) {
        days.push(null)
      }
      
      for (let day = 1; day <= endOfCurrentMonth.getDate(); day++) {
        days.push(new Date(props.currentDate.getFullYear(), props.currentDate.getMonth(), day))
      }
      
      return days
    })

    const handleMiniCalendarClick = (date) => {
      emit('date-change', date)
      if (props.view !== 'month') {
        emit('view-change', 'month')
      }
    }

    return {
      today,
      isSameDayHelper,
      currentDate: props.currentDate,
      monthLabel,
      dayNames,
      miniCalendarDays,
      handleMiniCalendarClick,
    }
  },
}
</script>

<style scoped>
.calendar-sidebar {
  width: 256px;
  border-right: 1px solid #dadce0;
  background-color: #fff;
  overflow-y: auto;
  flex-shrink: 0;
}

.sidebar-content {
  padding: 16px;
}

.mini-calendar {
  background-color: #fff;
}

.mini-calendar-header {
  font-size: 18px;
  font-weight: 400;
  color: #3c4043;
  margin-bottom: 12px;
  text-align: center;
}

.mini-calendar-days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.mini-calendar-day-name {
  text-align: center;
  font-size: 11px;
  font-weight: 500;
  color: #5f6368;
  padding: 4px 0;
}

.mini-calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.mini-calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #3c4043;
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.2s, color 0.2s;
}

.mini-calendar-day:hover {
  background-color: #f1f3f4;
}

.mini-calendar-day.selected {
  background-color: #1a73e8;
  color: #fff;
  font-weight: 500;
}

.mini-calendar-day.today {
  background-color: #ea4335;
  color: #fff;
  font-weight: 500;
}

.mini-calendar-day.today.selected {
  background-color: #1a73e8;
}

.mini-calendar-day.other-month {
  color: #9aa0a6;
}

.mini-calendar-day.empty {
  cursor: default;
}
</style>

