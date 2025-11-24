<template>
  <div class="week-view">
    <div class="week-view-header">
      <div class="week-time-column"></div>
      <div
        v-for="(day, index) in days"
        :key="index"
        :class="['week-day-header', { today: isSameDay(day, new Date()) }]"
      >
        <div class="week-day-name">{{ dayNames[index] }}</div>
        <div class="week-day-number">{{ format(day, 'd') }}</div>
      </div>
    </div>
    <div class="week-view-content">
      <div class="week-time-column">
        <div v-for="hour in hours" :key="hour" class="week-hour-cell">
          {{ format(new Date().setHours(hour, 0, 0, 0), 'h a') }}
        </div>
      </div>
      <div class="week-days-grid">
        <div
          v-for="(day, dayIndex) in days"
          :key="dayIndex"
          :class="['week-day-column', { today: isSameDay(day, new Date()) }]"
          @click="$emit('date-change', day)"
        >
          <div v-for="hour in hours" :key="hour" class="week-hour-slot"></div>
          <div
            v-for="(event, eventIndex) in getEventsForDay(day)"
            :key="eventIndex"
            class="week-event-item"
            :style="{
              backgroundColor: event.color || '#4285f4',
              top: getEventPosition(event).top,
              height: getEventPosition(event).height,
            }"
            @click.stop="$emit('event-click', event)"
          >
            <div class="week-event-time">{{ format(parseISO(event.start_time), 'h:mm a') }}</div>
            <div class="week-event-title">{{ event.title }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { format, startOfWeek, addDays, isSameDay, parseISO, getHours, getMinutes } from 'date-fns'

export default {
  name: 'WeekView',
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
  emits: ['event-click', 'date-change'],
  setup(props) {
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const hours = Array.from({ length: 24 }, (_, i) => i)

    const days = computed(() => {
      const weekStart = startOfWeek(props.currentDate)
      const daysArray = []
      for (let i = 0; i < 7; i++) {
        daysArray.push(addDays(weekStart, i))
      }
      return daysArray
    })

    const getEventsForDay = (day) => {
      return props.events.filter(event => {
        const eventStart = parseISO(event.start_time)
        return isSameDay(eventStart, day)
      })
    }

    const getEventPosition = (event) => {
      const start = parseISO(event.start_time)
      const end = parseISO(event.end_time)
      const startMinutes = getHours(start) * 60 + getMinutes(start)
      const endMinutes = getHours(end) * 60 + getMinutes(end)
      const top = (startMinutes / 60) * 100
      const height = ((endMinutes - startMinutes) / 60) * 100
      return { top: `${top}%`, height: `${height}%` }
    }

    return {
      dayNames,
      hours,
      days,
      format,
      parseISO,
      isSameDay,
      getEventsForDay,
      getEventPosition,
    }
  },
}
</script>

<style scoped>
.week-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.week-view-header {
  display: grid;
  grid-template-columns: 60px repeat(7, 1fr);
  border-bottom: 1px solid #dadce0;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.week-time-column {
  width: 60px;
  border-right: 1px solid #dadce0;
  background-color: #fff;
}

.week-day-header {
  padding: 8px;
  text-align: center;
  border-right: 1px solid #dadce0;
  background-color: #fff;
}

.week-day-header.today {
  background-color: #e8f0fe;
}

.week-day-name {
  font-size: 11px;
  font-weight: 500;
  color: #5f6368;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.week-day-number {
  font-size: 22px;
  font-weight: 400;
  color: #3c4043;
}

.week-day-header.today .week-day-number {
  background-color: #1a73e8;
  color: #fff;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
}

.week-view-content {
  display: flex;
  flex: 1;
  overflow-y: auto;
}

.week-time-column {
  width: 60px;
  border-right: 1px solid #dadce0;
  background-color: #fff;
  position: sticky;
  left: 0;
  z-index: 5;
}

.week-hour-cell {
  height: 60px;
  padding: 4px 8px;
  font-size: 12px;
  color: #5f6368;
  border-bottom: 1px solid #e8eaed;
  display: flex;
  align-items: flex-start;
}

.week-days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  flex: 1;
  position: relative;
}

.week-day-column {
  border-right: 1px solid #dadce0;
  position: relative;
  cursor: pointer;
}

.week-day-column.today {
  background-color: #f8f9fa;
}

.week-hour-slot {
  height: 60px;
  border-bottom: 1px solid #e8eaed;
  transition: background-color 0.2s;
}

.week-hour-slot:hover {
  background-color: #f1f3f4;
}

.week-event-item {
  position: absolute;
  left: 2px;
  right: 2px;
  padding: 4px 6px;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  font-size: 12px;
  z-index: 10;
  transition: box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.week-event-item:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  z-index: 20;
}

.week-event-time {
  font-weight: 500;
  font-size: 11px;
}

.week-event-title {
  font-weight: 400;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>

