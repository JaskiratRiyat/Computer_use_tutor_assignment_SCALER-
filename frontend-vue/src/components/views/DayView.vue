<template>
  <div class="day-view">
    <div class="day-view-header">
      <div class="day-time-column"></div>
      <div :class="['day-day-header', { today: isSameDay(currentDate, new Date()) }]">
        <div class="day-day-name">{{ format(currentDate, 'EEEE') }}</div>
        <div class="day-day-number">{{ format(currentDate, 'd') }}</div>
      </div>
    </div>
    <div class="day-view-content">
      <div class="day-time-column">
        <div v-for="hour in hours" :key="hour" class="day-hour-cell">
          {{ format(new Date().setHours(hour, 0, 0, 0), 'h a') }}
        </div>
      </div>
      <div class="day-day-column">
        <div v-for="hour in hours" :key="hour" class="day-hour-slot"></div>
        <div
          v-for="(event, eventIndex) in dayEvents"
          :key="eventIndex"
          class="day-event-item"
          :style="{
            backgroundColor: event.color || '#4285f4',
            top: getEventPosition(event).top,
            height: getEventPosition(event).height,
          }"
          @click.stop="$emit('event-click', event)"
        >
          <div class="day-event-time">
            {{ format(parseISO(event.start_time), 'h:mm a') }} - {{ format(parseISO(event.end_time), 'h:mm a') }}
          </div>
          <div class="day-event-title">{{ event.title }}</div>
          <div v-if="event.description" class="day-event-description">{{ event.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { format, isSameDay, parseISO, getHours, getMinutes } from 'date-fns'

export default {
  name: 'DayView',
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
    const hours = Array.from({ length: 24 }, (_, i) => i)

    const dayEvents = computed(() => {
      return props.events.filter(event => {
        const eventStart = parseISO(event.start_time)
        return isSameDay(eventStart, props.currentDate)
      })
    })

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
      hours,
      dayEvents,
      format,
      parseISO,
      isSameDay,
      getEventPosition,
    }
  },
}
</script>

<style scoped>
.day-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.day-view-header {
  display: grid;
  grid-template-columns: 60px 1fr;
  border-bottom: 1px solid #dadce0;
  background-color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.day-time-column {
  width: 60px;
  border-right: 1px solid #dadce0;
  background-color: #fff;
}

.day-day-header {
  padding: 16px;
  text-align: center;
  background-color: #fff;
}

.day-day-header.today {
  background-color: #e8f0fe;
}

.day-day-name {
  font-size: 14px;
  font-weight: 500;
  color: #5f6368;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.day-day-number {
  font-size: 36px;
  font-weight: 400;
  color: #3c4043;
}

.day-day-header.today .day-day-number {
  background-color: #1a73e8;
  color: #fff;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
}

.day-view-content {
  display: flex;
  flex: 1;
  overflow-y: auto;
}

.day-time-column {
  width: 60px;
  border-right: 1px solid #dadce0;
  background-color: #fff;
  position: sticky;
  left: 0;
  z-index: 5;
}

.day-hour-cell {
  height: 60px;
  padding: 4px 8px;
  font-size: 12px;
  color: #5f6368;
  border-bottom: 1px solid #e8eaed;
  display: flex;
  align-items: flex-start;
}

.day-day-column {
  flex: 1;
  position: relative;
  cursor: pointer;
}

.day-hour-slot {
  height: 60px;
  border-bottom: 1px solid #e8eaed;
  transition: background-color 0.2s;
}

.day-hour-slot:hover {
  background-color: #f1f3f4;
}

.day-event-item {
  position: absolute;
  left: 8px;
  right: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  font-size: 14px;
  z-index: 10;
  transition: box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.day-event-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 20;
}

.day-event-time {
  font-weight: 500;
  font-size: 12px;
}

.day-event-title {
  font-weight: 500;
  font-size: 14px;
}

.day-event-description {
  font-size: 12px;
  opacity: 0.9;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>

