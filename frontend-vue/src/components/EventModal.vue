<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ event ? 'Edit Event' : 'Create Event' }}</h2>
        <button class="modal-close" @click="$emit('close')">
          <svg width="24" height="24" viewBox="0 0 24 24">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="event-form">
        <div class="form-group">
          <label>Title *</label>
          <input
            type="text"
            v-model="formData.title"
            placeholder="Add title"
            required
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Start</label>
            <input
              type="datetime-local"
              v-model="formData.start_time"
              required
            />
          </div>
          <div class="form-group">
            <label>End</label>
            <input
              type="datetime-local"
              v-model="formData.end_time"
              required
            />
          </div>
        </div>

        <div v-if="overlapWarning && overlapWarning.hasOverlap" class="overlap-warning">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="#ea4335">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
          </svg>
          <span>This event overlaps with {{ overlapWarning.events.length }} other event(s)</span>
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea
            v-model="formData.description"
            placeholder="Add description"
            rows="3"
          />
        </div>

        <div class="form-group">
          <label>Location</label>
          <input
            type="text"
            v-model="formData.location"
            placeholder="Add location"
          />
        </div>

        <div class="form-group">
          <label>Color</label>
          <div class="color-picker">
            <button
              v-for="color in colors"
              :key="color"
              type="button"
              :class="['color-option', { selected: formData.color === color }]"
              :style="{ backgroundColor: color }"
              @click="formData.color = color"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="formData.is_recurring"
            />
            <span>Repeat</span>
          </label>
        </div>

        <div v-if="formData.is_recurring" class="recurrence-options">
          <div class="form-group">
            <label>Repeat</label>
            <select v-model="formData.recurrence_type">
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>

          <div class="form-group">
            <label>Every</label>
            <input
              type="number"
              v-model.number="formData.recurrence_interval"
              min="1"
              max="365"
            />
            <span class="interval-label">
              {{ intervalLabel }}
            </span>
          </div>

          <div class="form-group">
            <label>Ends</label>
            <input
              type="datetime-local"
              v-model="formData.recurrence_end_date"
              :required="formData.is_recurring"
            />
          </div>
        </div>

        <div class="modal-actions">
          <button
            v-if="$attrs.onDelete"
            type="button"
            class="delete-button"
            @click="$emit('delete')"
          >
            Delete
          </button>
          <div class="action-buttons">
            <button
              type="button"
              class="cancel-button"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button type="submit" class="save-button">
              {{ event ? 'Update' : 'Save' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue'
import { format, parseISO } from 'date-fns'
import { eventService } from '../services/api'

export default {
  name: 'EventModal',
  props: {
    event: {
      type: Object,
      default: null,
    },
  },
  emits: ['save', 'close', 'delete'],
  setup(props, { emit }) {
    const colors = [
      '#4285f4', '#ea4335', '#fbbc04', '#34a853',
      '#ff6d01', '#9334e6', '#e67c73', '#f83a22',
    ]

    const formData = ref({
      title: '',
      description: '',
      start_time: '',
      end_time: '',
      location: '',
      color: '#4285f4',
      is_recurring: false,
      recurrence_type: 'none',
      recurrence_end_date: '',
      recurrence_interval: 1,
    })

    const overlapWarning = ref(null)
    const isCheckingOverlap = ref(false)

    const intervalLabel = computed(() => {
      const labels = {
        daily: 'day(s)',
        weekly: 'week(s)',
        monthly: 'month(s)',
        yearly: 'year(s)',
      }
      return labels[formData.value.recurrence_type] || ''
    })

    watch(() => props.event, (newEvent) => {
      if (newEvent) {
        formData.value = {
          title: newEvent.title || '',
          description: newEvent.description || '',
          start_time: newEvent.start_time ? format(parseISO(newEvent.start_time), "yyyy-MM-dd'T'HH:mm") : '',
          end_time: newEvent.end_time ? format(parseISO(newEvent.end_time), "yyyy-MM-dd'T'HH:mm") : '',
          location: newEvent.location || '',
          color: newEvent.color || '#4285f4',
          is_recurring: newEvent.is_recurring || false,
          recurrence_type: newEvent.recurrence_type || 'none',
          recurrence_end_date: newEvent.recurrence_end_date ? format(parseISO(newEvent.recurrence_end_date), "yyyy-MM-dd'T'HH:mm") : '',
          recurrence_interval: newEvent.recurrence_interval || 1,
        }
      } else {
        const now = new Date()
        const oneHourLater = new Date(now.getTime() + 60 * 60 * 1000)
        formData.value = {
          ...formData.value,
          start_time: format(now, "yyyy-MM-dd'T'HH:mm"),
          end_time: format(oneHourLater, "yyyy-MM-dd'T'HH:mm"),
        }
      }
    }, { immediate: true })

    watch([() => formData.value.start_time, () => formData.value.end_time], () => {
      if (formData.value.start_time && formData.value.end_time) {
        const startTime = new Date(formData.value.start_time)
        const endTime = new Date(formData.value.end_time)
        
        if (endTime > startTime) {
          checkOverlap(startTime, endTime)
        }
      }
    })

    const checkOverlap = async (startTime, endTime) => {
      isCheckingOverlap.value = true
      try {
        const result = await eventService.checkOverlap(
          startTime,
          endTime,
          props.event?.id
        )
        
        if (result.has_overlap && result.overlapping_events.length > 0) {
          overlapWarning.value = {
            hasOverlap: true,
            events: result.overlapping_events,
          }
        } else {
          overlapWarning.value = null
        }
      } catch (error) {
        console.error('Error checking overlap:', error)
      } finally {
        isCheckingOverlap.value = false
      }
    }

    const handleSubmit = async () => {
      if (!formData.value.title.trim()) {
        alert('Please enter a title for the event')
        return
      }

      const startTime = new Date(formData.value.start_time)
      const endTime = new Date(formData.value.end_time)

      if (endTime <= startTime) {
        alert('End time must be after start time')
        return
      }

      const eventData = {
        title: formData.value.title.trim(),
        description: formData.value.description.trim(),
        start_time: startTime.toISOString(),
        end_time: endTime.toISOString(),
        location: formData.value.location.trim(),
        color: formData.value.color,
        is_recurring: formData.value.is_recurring,
        recurrence_type: formData.value.is_recurring ? formData.value.recurrence_type : 'none',
        recurrence_end_date: formData.value.is_recurring && formData.value.recurrence_end_date
          ? new Date(formData.value.recurrence_end_date).toISOString()
          : null,
        recurrence_interval: formData.value.is_recurring ? parseInt(formData.value.recurrence_interval) : 1,
      }

      emit('save', eventData)
    }

    return {
      formData,
      colors,
      overlapWarning,
      intervalLabel,
      handleSubmit,
    }
  },
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #dadce0;
}

.modal-header h2 {
  font-size: 22px;
  font-weight: 400;
  color: #3c4043;
  margin: 0;
}

.modal-close {
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

.modal-close:hover {
  background-color: #f1f3f4;
}

.event-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #5f6368;
  margin-bottom: 8px;
}

.form-group input[type="text"],
.form-group input[type="datetime-local"],
.form-group textarea,
.form-group select,
.form-group input[type="number"] {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dadce0;
  border-radius: 4px;
  font-size: 14px;
  color: #3c4043;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #1a73e8;
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
}

.color-picker {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.selected {
  border-color: #3c4043;
  box-shadow: 0 0 0 2px rgba(60, 64, 67, 0.2);
}

.overlap-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background-color: #fce8e6;
  border-radius: 4px;
  margin-bottom: 16px;
  color: #c5221f;
  font-size: 14px;
}

.recurrence-options {
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
  margin-top: 8px;
}

.recurrence-options .form-group {
  margin-bottom: 16px;
}

.recurrence-options .form-group:last-child {
  margin-bottom: 0;
}

.interval-label {
  margin-left: 8px;
  font-size: 14px;
  color: #5f6368;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 24px;
  border-top: 1px solid #dadce0;
  margin-top: 24px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.delete-button {
  background: none;
  border: none;
  color: #ea4335;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.delete-button:hover {
  background-color: #fce8e6;
}

.cancel-button,
.save-button {
  padding: 8px 24px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-button {
  background: none;
  border: 1px solid #dadce0;
  color: #5f6368;
}

.cancel-button:hover {
  background-color: #f8f9fa;
}

.save-button {
  background-color: #1a73e8;
  color: #fff;
  border: none;
}

.save-button:hover {
  background-color: #1557b0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #dadce0;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #bdc1c6;
}
</style>

