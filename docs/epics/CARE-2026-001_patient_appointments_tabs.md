# Epic: Patient Appointments Tabbed Interface

## Epic ID: CARE-2026-001

## Status: Completed

## Date: January 1, 2026

---

## Overview

This epic restructures the Patient Appointments page to provide a clearer separation between viewing existing appointments and booking new ones. The page now uses a tabbed interface with improved navigation from the patient dashboard.

---

## User Stories

### US-001: View Appointments Tab

**As a** patient  
**I want to** see my upcoming and past appointments in one place  
**So that** I can easily track my appointment history and upcoming visits

#### Acceptance Criteria

- [x] Tab displays up to 2 upcoming appointments
- [x] Tab displays appointment history with max 3 items per page
- [x] History section has pagination (Previous/Next buttons)
- [x] Each appointment shows date, time, duration, doctor, and status
- [x] Clear visual distinction between upcoming (white bg) and past (gray bg) appointments
- [x] Status badges show: Pending Review, Confirmed, Completed, Cancelled, No Show

### US-002: Book Appointment Tab

**As a** patient  
**I want to** have a dedicated space for booking appointments  
**So that** I can focus on the booking process without distraction

#### Acceptance Criteria

- [x] Tab contains the calendar date picker
- [x] Weekends and past dates are disabled
- [x] Time slot selection appears after date selection
- [x] Duration selector (30 or 60 minutes)
- [x] Booking confirmation modal with patient details
- [x] Success message after booking redirects to appointments tab

### US-003: Dashboard Navigation

**As a** patient  
**I want to** navigate directly to specific appointment functions from the dashboard  
**So that** I can quickly access what I need

#### Acceptance Criteria

- [x] "View All Appointments" button navigates to My Appointments tab
- [x] "Book New Appointment" button navigates to Book Appointment tab
- [x] Book button has primary styling for emphasis

---

## Technical Implementation

### Files Modified

1. **`app/pages/patient_4_Appointments.py`**

   - Complete rewrite with tabbed interface
   - Added session state for tab selection and history pagination
   - Query parameter support (`?tab=book` or `?tab=history`)

2. **`app/pages/patient_1_Dashboard.py`**

   - Updated navigation buttons to include tab query parameters
   - Added primary styling to "Book New Appointment" button

3. **`app/services/appointment_service.py`**

   - Added `get_patient_past_appointments()` method with pagination
   - Added `count_patient_past_appointments()` method

4. **`app/db/repositories/appointment_repository.py`**
   - Added `get_patient_past_appointments()` with limit/offset
   - Added `count_patient_past_appointments()` for pagination

### Data Flow

```
Patient Dashboard
    │
    ├── "View All Appointments" ──→ /patient_4_Appointments.py?tab=history
    │                                    │
    │                                    └── Tab 1: My Appointments
    │                                         ├── Upcoming (max 2)
    │                                         └── History (paginated, 3/page)
    │
    └── "Book New Appointment" ──→ /patient_4_Appointments.py?tab=book
                                         │
                                         └── Tab 2: Book Appointment
                                              ├── Calendar picker
                                              ├── Time slot selection
                                              └── Booking modal
```

### Session State Variables

| Variable             | Type | Purpose                            |
| -------------------- | ---- | ---------------------------------- |
| `appointments_tab`   | str  | Tracks active tab                  |
| `history_page`       | int  | Current page in history pagination |
| `selected_date`      | date | Selected booking date              |
| `selected_time`      | time | Selected booking time              |
| `selected_duration`  | int  | Appointment duration (30/60 min)   |
| `show_booking_modal` | bool | Modal visibility                   |
| `booking_success`    | bool | Success message flag               |
| `calendar_month`     | int  | Current calendar month view        |
| `calendar_year`      | int  | Current calendar year view         |

---

## UI Components

### Tab 1: My Appointments

```
┌─────────────────────────────────────────────────────┐
│ 📋 My Appointments  |  ➕ Book Appointment          │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Upcoming Appointments                               │
│ ┌─────────────────────────────────────────────────┐│
│ │ ▌Friday, January 3, 2026          [Confirmed]   ││
│ │  11:24 PM • 15 min • Dr. Johnson                ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
│ ─────────────────────────────────────────────────  │
│                                                     │
│ Appointment History                                 │
│ ┌─────────────────────────────────────────────────┐│
│ │ ▌Monday, December 15, 2025        [Completed]   ││
│ │  2:00 PM • 30 min • Dr. Smith                   ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
│ [◀ Previous]      Page 1 of 3      [Next ▶]        │
└─────────────────────────────────────────────────────┘
```

### Tab 2: Book Appointment

```
┌─────────────────────────────────────────────────────┐
│ 📋 My Appointments  |  ➕ Book Appointment          │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Select a Date                                       │
│ [◀ Prev]        January 2026         [Next ▶]      │
│                                                     │
│  Sun  Mon  Tue  Wed  Thu  Fri  Sat                 │
│        [ 5] [ 6] [ 7] [ 8] [ 9]  10                │
│   11  [12] [13] [14] [15] [16]  17                 │
│   ...                                              │
│                                                     │
│ ─────────────────────────────────────────────────  │
│                                                     │
│ Select a Time for Monday, January 6, 2026          │
│ Duration: [30 minutes ▼]                           │
│                                                     │
│   Morning          Afternoon                       │
│   [9:00 AM]        [12:00 PM]                      │
│   [9:30 AM]        [12:30 PM]                      │
│   ...              ...                             │
│                                                     │
│ [          Continue to Book →          ]           │
└─────────────────────────────────────────────────────┘
```

---

## Testing Notes

- Verify pagination works correctly with varying numbers of past appointments
- Test tab navigation via query parameters
- Ensure booking flow redirects to correct tab after success
- Verify dashboard buttons navigate to correct tabs

---

## Future Enhancements

- [ ] Add appointment cancellation from history view
- [ ] Add appointment rescheduling capability
- [ ] Add filtering by date range in history
- [ ] Add search functionality for past appointments
- [ ] Add appointment reminders/notifications integration
