# Google Calendar Clone - Full Stack Application

A high-fidelity full-stack clone of Google Calendar with smooth interactions, animations, and comprehensive event management features.

## Overview

This project implements a complete calendar application that replicates the core functionality and UI of Google Calendar. It includes monthly, weekly, and daily views, event creation/editing/deletion, recurring events, overlap detection, and a modern, responsive interface.

## Technology Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - RESTful API
- **SQLite** - Database
- **django-cors-headers** - CORS handling
- **python-dateutil** - Date manipulation and recurring event generation

### Frontend
- **Vue.js 3.3.4** - Frontend framework
- **date-fns 2.30.0** - Date utilities
- **Axios 1.6.0** - HTTP client
- **Vite** - Build tool

## Project Structure

```
.
├── backend/                 # Django backend
│   ├── calendar_app/       # Django project settings
│   ├── events/             # Events app
│   │   ├── models.py       # Event model with recurring support
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API views and recurring logic
│   │   └── urls.py         # URL routing
│   ├── manage.py
│   └── requirements.txt
├── frontend-vue/            # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   └── services/       # API service
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 16+ and npm
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create migrations for the events app:**
   ```bash
   python manage.py makemigrations events
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`
   - API endpoints: `http://localhost:8000/api/`
   - Admin panel: `http://localhost:8000/admin/`

### Frontend Setup

1. **Navigate to frontend-vue directory:**
   ```bash
   cd frontend-vue
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The Vue.js app will be available at `http://localhost:5173`

**Note:** Make sure the Django backend is running before starting the frontend.

## API Endpoints

### Events

- `GET /api/events/` - List all events (supports `start_date` and `end_date` query params)
- `GET /api/events/{id}/` - Get a specific event
- `POST /api/events/` - Create a new event
- `PUT /api/events/{id}/` - Update an event
- `DELETE /api/events/{id}/` - Delete an event
- `GET /api/events/by_date_range/` - Get events in date range with expanded recurring events
- `GET /api/events/check_overlap/` - Check if an event overlaps with existing events

### Event Data Model

```json
{
  "id": 1,
  "title": "Meeting",
  "description": "Team meeting",
  "start_time": "2024-01-15T10:00:00Z",
  "end_time": "2024-01-15T11:00:00Z",
  "location": "Conference Room A",
  "color": "#4285f4",
  "is_recurring": true,
  "recurrence_type": "weekly",
  "recurrence_end_date": "2024-12-31T23:59:59Z",
  "recurrence_interval": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Architecture and Technology Choices

### Backend Architecture

**Django REST Framework** was chosen for:
- Rapid API development with built-in serialization
- Automatic API documentation capabilities
- Strong ORM for database operations
- Built-in authentication and permissions (extensible for future features)

**SQLite** was chosen for:
- Zero configuration required
- Perfect for development and small-to-medium deployments
- Easy to migrate to PostgreSQL/MySQL if needed
- File-based, easy to backup and version

**Event Model Design:**
- Supports both one-time and recurring events
- Recurring events use a parent-child relationship
- Recurring instances are generated on-the-fly for display
- Efficient date range queries with database indexes

### Frontend Architecture

**Vue.js Implementation:**
- Composition API for better code organization
- Reactive data binding
- Component-based architecture for reusability
- Vite for fast development and building
- Service layer for API communication
- Scoped CSS for component styling

## Business Logic and Edge Cases

### Recurring Events

**Implementation:**
- Parent event stores recurrence configuration
- Recurring instances are generated dynamically when viewing date ranges
- Uses `python-dateutil`'s `rrule` for accurate recurrence calculation
- Supports daily, weekly, monthly, and yearly recurrence
- Configurable interval (e.g., every 2 weeks, every 3 months)

**Edge Cases Handled:**
1. **Recurrence End Date:** Events stop recurring at the specified end date
2. **Time Zone:** All times stored in UTC, converted in frontend for display
3. **Leap Years:** Handled automatically by dateutil
4. **Month End Variations:** Monthly events on day 31 adjust to last day of shorter months
5. **Daylight Saving Time:** UTC storage prevents DST issues

### Event Overlap Detection

**Implementation:**
- Overlap check API endpoint validates new/updated events
- Frontend displays warnings when overlaps are detected
- Users can still save overlapping events (flexibility)
- Overlap calculation: `start1 < end2 && end1 > start2`

**Edge Cases Handled:**
1. **Exact Boundary:** Events ending exactly when another starts are not considered overlapping
2. **Nested Events:** Events completely contained within another are detected
3. **Multiple Overlaps:** All overlapping events are reported
4. **Recurring Event Overlaps:** Each instance checked individually

### Date Range Queries

**Optimization:**
- Database indexes on `start_time` and `end_time`
- Efficient query: `start_time <= end_date AND end_time >= start_date`
- Recurring events expanded only for requested date range
- Pagination support for large event sets

### Validation

**Backend Validation:**
- End time must be after start time
- Required fields enforced
- Recurrence settings validated when `is_recurring` is true
- Date format validation

**Frontend Validation:**
- Real-time overlap checking
- Form validation before submission
- User-friendly error messages
- Prevents invalid date selections

## Animations and Interactions

### Smooth Transitions

**Modal Animations:**
- Fade-in overlay (0.2s ease-out)
- Slide-up modal content (0.3s ease-out)
- CSS transitions for all interactive elements

**View Switching:**
- Instant view changes with smooth data loading
- Calendar grid animations via CSS transitions
- Hover effects on all interactive elements

**Event Interactions:**
- Hover effects on event items (opacity, shadow)
- Click feedback with visual states
- Smooth color transitions
- Loading states during API calls

**Calendar Navigation:**
- Smooth date transitions
- Today button highlights current date
- Mini calendar in sidebar for quick navigation
- Responsive touch interactions

### CSS Animation Techniques

1. **Transitions:** Used for hover states, color changes, and state updates
2. **Keyframe Animations:** Modal appearance, fade effects
3. **Transform:** Scale effects on color picker, button interactions
4. **Opacity:** Smooth fade-in/fade-out effects

### Performance Optimizations

- Event rendering optimized for large date ranges
- Virtual scrolling considered for very large event lists
- Debounced overlap checking
- Efficient date calculations with date-fns

## Features Implemented

✅ **Core Features:**
- Monthly, Weekly, and Daily calendar views
- Create, Edit, and Delete events
- Event details modal with full form
- Color-coded events
- Location and description fields

✅ **Advanced Features:**
- Recurring events (daily, weekly, monthly, yearly)
- Recurrence interval configuration
- Overlap detection and warnings
- Date range filtering
- Responsive design

✅ **UI/UX Features:**
- Google Calendar-like interface
- Smooth animations and transitions
- Interactive mini calendar
- Today button and quick navigation
- Event color picker
- Loading states

## Future Enhancements

### Short-term Improvements

1. **User Authentication:**
   - User registration and login
   - Personal calendars per user
   - Shared calendars

2. **Event Reminders:**
   - Email notifications
   - Push notifications
   - In-app reminders

3. **Event Invitations:**
   - Invite other users
   - RSVP functionality
   - Attendee management

4. **Calendar Sharing:**
   - Share calendars with others
   - Public calendar links
   - Permission levels (view/edit)

### Medium-term Enhancements

1. **Advanced Recurrence:**
   - Custom recurrence patterns
   - Exception dates
   - Edit single occurrence vs. entire series

2. **Search and Filter:**
   - Full-text search
   - Filter by color, location, date range
   - Saved filters

3. **Import/Export:**
   - iCal (.ics) import/export
   - Google Calendar sync
   - CSV export

4. **Mobile App:**
   - React Native or Flutter app
   - Offline support
   - Push notifications

### Long-term Vision

1. **Collaboration Features:**
   - Comments on events
   - File attachments
   - Meeting notes

2. **Analytics:**
   - Calendar usage statistics
   - Time tracking
   - Productivity insights

3. **Integration:**
   - Google Calendar API integration
   - Outlook Calendar sync
   - Zoom/Meet integration

4. **AI Features:**
   - Smart scheduling suggestions
   - Conflict resolution recommendations
   - Natural language event creation

## Development Notes

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend-vue
npm run test
```

### Building for Production

```bash
cd frontend-vue
npm run build
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django admin
# Navigate to http://localhost:8000/admin/
```

## Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Ensure `django-cors-headers` is installed
   - Check `CORS_ALLOWED_ORIGINS` in settings.py
   - Verify frontend URL matches allowed origins

2. **Port Already in Use:**
   - Change port in `package.json` (React) or `vite.config.js` (Vue)
   - Or stop the process using the port

3. **Database Errors:**
   - Run migrations: `python manage.py migrate`
   - Delete `db.sqlite3` and re-run migrations if needed

4. **Module Not Found:**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt` or `npm install`

## Contributing

This is an assignment project. For production use, consider:
- Adding comprehensive test coverage
- Implementing proper authentication
- Adding rate limiting
- Setting up CI/CD pipeline
- Using environment variables for configuration
- Implementing proper error logging

## License

See LICENSE file for details.

## Acknowledgments

- Google Calendar for design inspiration
- Django and React/Vue.js communities
- date-fns for excellent date utilities

---

**Note:** This project was built as a high-fidelity clone of Google Calendar for educational purposes. All design elements are inspired by Google Calendar's interface. Credits - Jaskirat Singh, made for the take-home assignment for Scaler.
