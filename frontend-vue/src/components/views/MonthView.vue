<template>
  <div class="month-view">
    <div class="month-view-header">
      <div v-for="(dayName, index) in dayNames" :key="index" class="month-day-header">
        {{ dayName }}
      </div>
    </div>
    <div class="month-view-grid">
      <div
        v-for="(day, index) in days"
        :key="index"
        :class="[
          'month-day-cell',
          {
            'other-month': !isSameMonth(day, currentDate),
            today: isSameDay(day, new Date()),
          },
        ]"
        @click="$emit('date-click', day)"
      >
        <div class="month-day-number">{{ format(day, 'd') }}</div>
        <div class="month-day-events">
          <div
            v-for="(event, eventIndex) in getEventsForDay(day).slice(0, 3)"
            :key="eventIndex"
            class="month-event-item"
            :style="{ backgroundColor: event.color || '#4285f4' }"
            @click.stop="$emit('event-click', event)"
          >
            <span class="event-time">{{ format(parseISO(event.start_time), 'h:mm a') }}</span>
            <span class="event-title">{{ event.title }}</span>
          </div>
          <div
            v-if="getEventsForDay(day).length > 3"
            class="month-event-more"
          >
            +{{ getEventsForDay(day).length - 3 }} more
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { format, startOfMonth, endOfMonth, startOfWeek, endOfWeek, addDays, isSameMonth, isSameDay, parseISO } from 'date-fns'

export default {
  name: 'MonthView',
  props: {
    currentDate: {
      type: Date,
      required: true,
    },
    events: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['event-click', 'date-click'],
  setup(props) {
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    const days = computed(() => {
      const monthStart = startOfMonth(props.currentDate)
      const monthEnd = endOfMonth(props.currentDate)
      const startDate = startOfWeek(monthStart)
      const endDate = endOfWeek(monthEnd)

      const daysArray = []
      let day = startDate
      while (day <= endDate) {
        daysArray.push(day)
        day = addDays(day, 1)
      }
      return daysArray
    })

    const getEventsForDay = (day) => {
      return props.events.filter(event => {
        const eventStart = parseISO(event.start_time)
        return isSameDay(eventStart, day)
      })
    }

    return {
      dayNames,
      days,
      format,
      parseISO,
      isSameMonth,
      isSameDay,
      getEventsForDay,
    }
  },
}
</script>

<style scoped>
.month-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.month-view-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  border-bottom: 1px solid #dadce0;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.month-day-header {
  padding: 8px;
  text-align: center;
  font-size: 11px;
  font-weight: 500;
  color: #5f6368;
  text-transform: uppercase;
  border-right: 1px solid #dadce0;
}

.month-day-header:last-child {
  border-right: none;
}

.month-view-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: repeat(6, 1fr);
  flex: 1;
  border-right: 1px solid #dadce0;
  border-bottom: 1px solid #dadce0;
}

.month-day-cell {
  min-height: 120px;
  border-left: 1px solid #dadce0;
  border-top: 1px solid #dadce0;
  padding: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  flex-direction: column;
}

.month-day-cell:hover {
  background-color: #f8f9fa;
}

.month-day-cell.other-month {
  background-color: #f8f9fa;
  color: #9aa0a6;
}

.month-day-cell.today {
  background-color: #e8f0fe;
}

.month-day-number {
  font-size: 13px;
  font-weight: 400;
  color: #3c4043;
  margin-bottom: 4px;
  padding: 2px 4px;
  align-self: flex-start;
}

.month-day-cell.today .month-day-number {
  background-color: #1a73e8;
  color: #fff;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
}

.month-day-events {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow: hidden;
}

.month-event-item {
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 12px;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.month-event-item:hover {
  opacity: 0.9;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.event-time {
  font-weight: 500;
  font-size: 11px;
}

.event-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

.month-event-more {
  font-size: 11px;
  color: #5f6368;
  padding: 2px 4px;
  cursor: pointer;
}

.month-event-more:hover {
  background-color: #f1f3f4;
  border-radius: 3px;
}
</style>

