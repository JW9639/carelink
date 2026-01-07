# CareLink - Project Requirements & Epic Documentation

## Project Overview

**Project Title:** CareLink: A Role-Based Patient Doctor Medical Dashboard for Integrated Patient Management and Hybrid Appointment Booking

**Project Status (as of January 7, 2026):**

- Patient Portal: 40% Complete (1/6 stories complete)
- Doctor Portal: 10% Complete (placeholders only)
- Admin Portal: 10% Complete (placeholders only)
- Testing: 35% Complete

## Technology Stack

| Technology              | Purpose             |
| ----------------------- | ------------------- |
| Python 3.11+            | Core language       |
| Streamlit               | Frontend framework  |
| PostgreSQL              | Database            |
| SQLAlchemy 2.0          | ORM                 |
| Pydantic v2             | Validation          |
| Alembic                 | Database migrations |
| Docker & Docker Compose | Containerization    |
| pytest                  | Testing             |
| bcrypt                  | Password hashing    |

---

## Design System

### Colour Palette

| Variable          | Hex Code | Usage                                    |
| ----------------- | -------- | ---------------------------------------- |
| --primary-color   | #0066CC  | NHS Blue - primary actions, links        |
| --secondary-color | #00A896  | Teal - success states, secondary actions |
| --success-color   | #06D6A0  | Green - confirmations, positive status   |
| --warning-color   | #FFB703  | Amber - warnings, pending states         |
| --error-color     | #EF476F  | Red/Pink - errors, critical alerts       |
| --dark-color      | #2B2D42  | Dark blue-grey - primary text            |
| --light-bg        | #F0F4F8  | Light grey-blue - page backgrounds       |
| --white           | #FFFFFF  | Cards, containers                        |
| --text-secondary  | #6B7280  | Secondary text, captions                 |
| --border-color    | #E2E8F0  | Borders, dividers                        |

### Typography

- Primary font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
- Minimum font size: 16px (accessibility requirement)
- Headers: Bold weights (600-700)

## Completed Work

### Sprint 1 - Infrastructure (COMPLETE)

- Project structure and configuration
- SQLAlchemy models for all 8 tables
- Pydantic schemas for validation
- Security utilities (auth, RBAC, session management, audit logging)
- Docker and Docker Compose setup
- Alembic migration configuration
- Initial unit tests (29 passing)
- CI/CD pipeline configuration

### Sprint 2 - Authentication & UI (COMPLETE)

- Login page (`Home.py`) - DESIGN COMPLETE, DO NOT MODIFY
- Patient Dashboard (`pages/patient_1_Dashboard.py`) - DESIGN COMPLETE, connected to real data
- Doctor Dashboard (`pages/doctor_1_Dashboard.py`) - placeholder content
- Admin Dashboard (`pages/admin_1_Dashboard.py`) - placeholder content
- CSS styling system (main.css, login.css, dashboard.css, sidebar.css)
- Sidebar navigation component (overlay mode, toggle button)
- Header component with role-based menu toggle
- Dashboard layout component
- User repository and auth service
- Patient repository and service (dashboard stats)
- Appointment repository (patient queries)
- Database seed script with demo users and sample data
- Initial Alembic migration

### Sprint 3 - Patient Features (IN PROGRESS) 🔄

- Appointments booking page (E3-S4) - COMPLETE
- Calendar interface with navigation
- Time slot selection system
- Modal confirmation dialog
- My Appointments view
- Appointment cancellation
- Full CSS styling matching design system

**In Progress:**

- 🔄 Bloodwork results viewer (E3-S2) - Not started
- 🔄 Prescriptions view (E3-S3) - Not started
- 🔄 Notifications view (E3-S5) - Partial

**Planned:**

- ⏳ Doctor dashboard data connection (E4-S1-T7)
- ⏳ Profile pages for all roles

---

## Epic Structure

### Epic E-1: Project Infrastructure - COMPLETE

All stories completed in Sprint 1.

### Epic E-2: Authentication & Security - COMPLETE

All stories completed in Sprint 1 and 2.

---

### Epic E-3: Patient Portal

#### E3-S1: Patient Dashboard - COMPLETE (DO NOT MODIFY DESIGN)

| Task     | Description                      | Status |
| -------- | -------------------------------- | ------ |
| E3-S1-T1 | Design dashboard wireframe       | DONE   |
| E3-S1-T2 | Implement dashboard layout       | DONE   |
| E3-S1-T3 | Create welcome/summary section   | DONE   |
| E3-S1-T4 | Add upcoming appointments widget | DONE   |
| E3-S1-T5 | Add notifications widget         | DONE   |
| E3-S1-T6 | Add quick actions section        | DONE   |
| E3-S1-T7 | Connect to real database data    | DONE   |

#### E3-S2: Bloodwork History View (Medichecks-Style) - PRIORITY 1

**Description:** Implement a 3-level hierarchical bloodwork viewer inspired by Medichecks.

##### User Flow

```
LEVEL 1: Blood Draw List
- Shows all blood test sessions for the patient
- Each card shows: date, test name, ordering doctor, status
- Only shows results with status "Shared with Patient"
- Click to drill down to Level 2

LEVEL 2: Categories within Blood Draw
- Back button to return to Level 1
- Header with test name and date
- Summary showing total markers and how many outside range
- List of category cards (CBC, Lipid Panel, Liver Function, etc.)
- Each category shows: name, marker count, status summary
- Click to drill down to Level 3

LEVEL 3: Individual Markers with Visual Range
- Back button to return to Level 2
- Header with category name
- For each marker:
  - Marker name and abbreviation
  - Large value display with unit
  - Status badge (Normal, High, Low, Critical)
  - Visual range indicator bar with coloured zones
  - Arrow marker showing patient's value position
  - Doctor's interpretation note (if any)
```

##### Visual Range Indicator Component

The range bar must show:

- Red zone: Below low threshold or above high threshold
- Yellow/amber zone: Borderline (between low/optimal and optimal/high)
- Green zone: Optimal range
- Arrow marker at patient's actual value position
- Colour of arrow matches status

##### Data Structure for Bloodwork Results

```json
{
  "test_name": "Full Blood Count & Metabolic Panel",
  "categories": [
    {
      "name": "Complete Blood Count (CBC)",
      "markers": [
        {
          "name": "White Blood Cell Count",
          "abbreviation": "WBC",
          "value": 7.2,
          "unit": "x10^9/L",
          "reference_range": {
            "low": 4.0,
            "optimal_low": 4.5,
            "optimal_high": 11.0,
            "high": 11.5
          },
          "status": "normal",
          "interpretation": null
        }
      ]
    }
  ]
}
```

##### Bloodwork Categories Reference

**Complete Blood Count (CBC)**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| White Blood Cell Count | WBC | x10^9/L | 4.0 - 11.0 |
| Red Blood Cell Count | RBC | x10^12/L | 4.5 - 6.5 (M) / 3.8 - 5.8 (F) |
| Hemoglobin | Hgb | g/L | 130 - 175 (M) / 115 - 165 (F) |
| Hematocrit | Hct | L/L | 0.40 - 0.54 (M) / 0.36 - 0.48 (F) |
| Mean Corpuscular Volume | MCV | fL | 80 - 100 |
| Mean Corpuscular Hemoglobin | MCH | pg | 27 - 33 |
| Mean Corpuscular Hemoglobin Concentration | MCHC | g/L | 320 - 360 |
| Red Cell Distribution Width | RDW | % | 11.5 - 14.5 |
| Platelet Count | PLT | x10^9/L | 150 - 400 |
| Mean Platelet Volume | MPV | fL | 7.5 - 12.0 |
| Neutrophils | Neut | x10^9/L | 2.0 - 7.5 |
| Lymphocytes | Lymph | x10^9/L | 1.0 - 4.0 |
| Monocytes | Mono | x10^9/L | 0.2 - 1.0 |
| Eosinophils | Eos | x10^9/L | 0.0 - 0.5 |
| Basophils | Baso | x10^9/L | 0.0 - 0.1 |

**Lipid Panel**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Total Cholesterol | TC | mmol/L | < 5.0 optimal |
| LDL Cholesterol | LDL-C | mmol/L | < 3.0 optimal |
| HDL Cholesterol | HDL-C | mmol/L | > 1.0 (M) / > 1.2 (F) |
| Triglycerides | TG | mmol/L | < 1.7 optimal |
| Non-HDL Cholesterol | Non-HDL | mmol/L | < 4.0 optimal |

**Liver Function**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Albumin | Alb | g/L | 35 - 50 |
| Alkaline Phosphatase | ALP | U/L | 30 - 130 |
| Alanine Aminotransferase | ALT | U/L | 7 - 56 |
| Aspartate Aminotransferase | AST | U/L | 10 - 40 |
| Total Bilirubin | T. Bil | umol/L | 3 - 21 |
| Total Protein | TP | g/L | 60 - 80 |
| Gamma-Glutamyl Transferase | GGT | U/L | 9 - 48 |

**Kidney Function**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Blood Urea Nitrogen | BUN | mmol/L | 2. 5 - 7.1 |
| Creatinine | Cr | umol/L | 59 - 104 (M) / 45 - 84 (F) |
| eGFR | eGFR | mL/min/1.73m2 | > 90 normal |

**Electrolytes**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Sodium | Na | mmol/L | 136 - 145 |
| Potassium | K | mmol/L | 3.5 - 5.1 |
| Chloride | Cl | mmol/L | 98 - 106 |
| Carbon Dioxide | CO2 | mmol/L | 22 - 29 |
| Calcium | Ca | mmol/L | 2.15 - 2.55 |

**Thyroid Function**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Thyroid Stimulating Hormone | TSH | mIU/L | 0.4 - 4.0 |
| Free T4 | FT4 | pmol/L | 12 - 22 |
| Free T3 | FT3 | pmol/L | 3.1 - 6.8 |

**Glucose Metabolism**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Fasting Glucose | Gluc | mmol/L | 3.9 - 5.5 |
| HbA1c | HbA1c | mmol/mol | < 42 normal |
| Fasting Insulin | Ins | pmol/L | 18 - 173 |

**Inflammation**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| C-Reactive Protein (High Sensitivity) | hsCRP | mg/L | < 1.0 low risk |
| Erythrocyte Sedimentation Rate | ESR | mm/hr | 0 - 15 (M) / 0 - 20 (F) |

**Nutritional**
| Marker | Abbreviation | Unit | Reference Range |
|--------|--------------|------|-----------------|
| Vitamin D | VitD | nmol/L | 50 - 175 |
| Vitamin B12 | B12 | pmol/L | 145 - 569 |
| Folate | Folate | nmol/L | > 10 |
| Ferritin | Ferr | ug/L | 30 - 400 (M) / 13 - 150 (F) |
| Iron | Fe | umol/L | 10 - 30 |

##### Tasks

| Task     | Description                                 | Status |
| -------- | ------------------------------------------- | ------ |
| E3-S2-T1 | Create bloodwork repository                 | TODO   |
| E3-S2-T2 | Create bloodwork service                    | TODO   |
| E3-S2-T3 | Create range indicator UI component         | TODO   |
| E3-S2-T4 | Implement Level 1 - Blood draw list         | TODO   |
| E3-S2-T5 | Implement Level 2 - Categories view         | TODO   |
| E3-S2-T6 | Implement Level 3 - Markers with range bars | TODO   |
| E3-S2-T7 | Update seed data with realistic bloodwork   | TODO   |
| E3-S2-T8 | Write unit tests                            | TODO   |

#### E3-S3: Prescriptions View

| Task     | Description                         | Status |
| -------- | ----------------------------------- | ------ |
| E3-S3-T1 | Create prescription repository      | TODO   |
| E3-S3-T2 | Create prescription service         | TODO   |
| E3-S3-T3 | Implement active prescriptions list | TODO   |
| E3-S3-T4 | Implement prescription history tab  | TODO   |
| E3-S3-T5 | Add refill request placeholder      | TODO   |
| E3-S3-T6 | Write unit tests                    | TODO   |

#### E3-S4: Appointments View & Booking - COMPLETE

**Completion Date:** January 7, 2026

**Description:** Full appointment booking interface with calendar, time selection, and confirmation modal.

**Design Decisions:**

- Tabbed interface: "My Appointments" and "Book Appointment"
- Calendar with Previous/Next month navigation
- Green visual indicator (✓) for selected dates
- Duration selector (30/60 min) with teal selection indicators
- Time slots organized by AM/PM with availability status
- Modal dialog for appointment confirmation
- White card design matching system aesthetics
- All form inputs styled consistently with light backgrounds

**Implementation Details:**

- Custom calendar grid with day-of-week headers
- Disabled past dates and weekends
- Selected date displays with green button style
- Time slots show as teal buttons when selected, gray outline when unselected
- Checkmarks on selected options (date, time, duration)
- Appointment confirmation modal with:
  - White background, dark text
  - Summary of selected date/time/duration
  - Patient name pre-filled (disabled)
  - Reason for visit textarea with red asterisk
  - Blue gradient "Confirm Booking" button
  - Gray outline "Back" button
- Success message after booking with green checkmark
- Automatic redirect to "My Appointments" tab after confirmation

**CSS Enhancements:**

- Tab slider: black, 4px thick
- Month title: 28px, bold, centered
- Section headers: underlined with 8px offset
- Divider line: 3px solid black between sections
- Input fields: white background (#f9fafb), dark text (#111827)
- Modal backdrop: rgba(0,0,0,0.5) overlay
- Primary buttons: teal (#0d9488) with hover effects
- Secondary buttons: white with gray outline
- Blue Continue button maintained system gradient

| Task      | Description                              | Status | Completion Date |
| --------- | ---------------------------------------- | ------ | --------------- |
| E3-S4-T1  | Create appointment repository            | DONE   | Dec 2025        |
| E3-S4-T2  | Create appointment service               | DONE   | Jan 6, 2026     |
| E3-S4-T3  | Implement My Appointments tab            | DONE   | Jan 6, 2026     |
| E3-S4-T4  | Design calendar interface                | DONE   | Jan 6, 2026     |
| E3-S4-T5  | Implement calendar navigation            | DONE   | Jan 6, 2026     |
| E3-S4-T6  | Implement date selection with visuals    | DONE   | Jan 7, 2026     |
| E3-S4-T7  | Implement duration selector              | DONE   | Jan 6, 2026     |
| E3-S4-T8  | Implement time slot selection            | DONE   | Jan 6, 2026     |
| E3-S4-T9  | Style buttons with teal/gray theme       | DONE   | Jan 6, 2026     |
| E3-S4-T10 | Create appointment confirmation modal    | DONE   | Jan 7, 2026     |
| E3-S4-T11 | Style modal to match system design       | DONE   | Jan 7, 2026     |
| E3-S4-T12 | Implement booking submission logic       | DONE   | Jan 6, 2026     |
| E3-S4-T13 | Add success/error handling               | DONE   | Jan 6, 2026     |
| E3-S4-T14 | Add appointment cancellation feature     | DONE   | Jan 6, 2026     |
| E3-S4-T15 | Test booking flow end-to-end             | DONE   | Jan 6, 2026     |
| E3-S4-T16 | Write unit tests for appointment service | DONE   | Jan 5, 2026     |

#### E3-S5: Notification Centre - PARTIAL ⏳

**Status:** Basic structure exists, needs completion

| Task     | Description                                | Status      | Notes                              |
| -------- | ------------------------------------------ | ----------- | ---------------------------------- |
| E3-S5-T1 | Create notification repository             | TODO        | Service exists, repo layer needed  |
| E3-S5-T2 | Create notification service                | DONE        | Basic service implemented          |
| E3-S5-T3 | Implement notification list with filtering | IN PROGRESS | Page exists, needs data connection |
| E3-S5-T4 | Implement mark as read functionality       | TODO        |                                    |
| E3-S5-T5 | Implement mark all read                    | TODO        |                                    |
| E3-S5-T6 | Write unit tests                           | TODO        |                                    |

#### E3-S6: Patient Profile Page

| Task     | Description                                    | Status |
| -------- | ---------------------------------------------- | ------ |
| E3-S6-T1 | Create patient repository                      | DONE   |
| E3-S6-T2 | Create patient service                         | DONE   |
| E3-S6-T3 | Display read-only fields (NHS Number, DOB, GP) | TODO   |
| E3-S6-T4 | Implement editable contact details             | TODO   |
| E3-S6-T5 | Implement emergency contact section            | TODO   |
| E3-S6-T6 | Implement communication preferences            | TODO   |
| E3-S6-T7 | Implement password change                      | TODO   |
| E3-S6-T8 | Add audit logging for profile updates          | TODO   |
| E3-S6-T8 | Write unit tests                               | TODO   |

---

### Epic E-4: Doctor Portal

#### E4-S1: Doctor Dashboard

| Task     | Description                             | Status             |
| -------- | --------------------------------------- | ------------------ |
| E4-S1-T1 | Design doctor dashboard layout          | DONE (placeholder) |
| E4-S1-T2 | Show today's appointments from database | TODO               |
| E4-S1-T3 | Show pending results to review count    | TODO               |
| E4-S1-T4 | Show patient count                      | TODO               |
| E4-S1-T5 | Add priority actions section            | DONE (placeholder) |
| E4-S1-T6 | Add quick actions buttons               | DONE (placeholder) |
| E4-S1-T7 | Connect to real database data           | TODO               |

#### E4-S2: Patient List View

| Task     | Description                        | Status |
| -------- | ---------------------------------- | ------ |
| E4-S2-T1 | Create doctor repository           | DONE   |
| E4-S2-T2 | Implement patient list with search | TODO   |
| E4-S2-T3 | Implement patient detail view      | TODO   |
| E4-S2-T4 | Show patient medical history       | TODO   |
| E4-S2-T5 | Write unit tests                   | TODO   |

#### E4-S3: Results Review & Publishing

| Task     | Description                                | Status |
| -------- | ------------------------------------------ | ------ |
| E4-S3-T1 | Implement pending results list             | TODO   |
| E4-S3-T2 | Implement result review interface          | TODO   |
| E4-S3-T3 | Add interpretation text input              | TODO   |
| E4-S3-T4 | Implement publish to patient functionality | TODO   |
| E4-S3-T5 | Add audit logging for publish actions      | TODO   |
| E4-S3-T6 | Write unit tests                           | TODO   |

#### E4-S4: Doctor Appointments

| Task     | Description                              | Status |
| -------- | ---------------------------------------- | ------ |
| E4-S4-T1 | Show doctor's appointments from database | TODO   |
| E4-S4-T2 | Implement appointment confirmation       | TODO   |
| E4-S4-T3 | Implement reschedule functionality       | TODO   |
| E4-S4-T4 | Write unit tests                         | TODO   |

#### E4-S5: Prescription Management

| Task     | Description                            | Status |
| -------- | -------------------------------------- | ------ |
| E4-S5-T1 | Implement new prescription form        | TODO   |
| E4-S5-T2 | Implement refill approval workflow     | TODO   |
| E4-S5-T3 | Implement prescription discontinuation | TODO   |
| E4-S5-T4 | Add audit logging                      | TODO   |
| E4-S5-T5 | Write unit tests                       | TODO   |

#### E4-S6: Doctor Profile Page

| Task     | Description                                     | Status |
| -------- | ----------------------------------------------- | ------ |
| E4-S6-T1 | Display read-only fields (GMC, approval status) | TODO   |
| E4-S6-T2 | Implement editable contact details              | TODO   |
| E4-S6-T3 | Implement availability settings                 | TODO   |
| E4-S6-T4 | Implement password change                       | TODO   |
| E4-S6-T5 | Write unit tests                                | TODO   |

---

### Epic E-5: Admin Portal

#### E5-S1: Admin Dashboard

| Task     | Description                          | Status             |
| -------- | ------------------------------------ | ------------------ |
| E5-S1-T1 | Design admin dashboard layout        | DONE (placeholder) |
| E5-S1-T2 | Show system statistics from database | TODO               |
| E5-S1-T3 | Show pending doctor approvals        | TODO               |
| E5-S1-T4 | Show recent activity summary         | TODO               |
| E5-S1-T5 | Connect to real database data        | TODO               |

#### E5-S2: User Management

| Task     | Description                        | Status |
| -------- | ---------------------------------- | ------ |
| E5-S2-T1 | Implement user list with filtering | TODO   |
| E5-S2-T2 | Implement user creation form       | TODO   |
| E5-S2-T3 | Implement user deactivation        | TODO   |
| E5-S2-T4 | Implement doctor approval workflow | TODO   |
| E5-S2-T5 | Implement patient-doctor linking   | TODO   |
| E5-S2-T6 | Write unit tests                   | TODO   |

#### E5-S3: Appointment Management

| Task     | Description                        | Status |
| -------- | ---------------------------------- | ------ |
| E5-S3-T1 | Show all appointments system-wide  | TODO   |
| E5-S3-T2 | Implement phone booking entry      | TODO   |
| E5-S3-T3 | Implement appointment modification | TODO   |
| E5-S3-T4 | Write unit tests                   | TODO   |

#### E5-S4: Audit Log Viewer

| Task     | Description                              | Status |
| -------- | ---------------------------------------- | ------ |
| E5-S4-T1 | Implement audit log list with pagination | TODO   |
| E5-S4-T2 | Add filtering by user, action, date      | TODO   |
| E5-S4-T3 | Show audit log details                   | TODO   |
| E5-S4-T4 | Write unit tests                         | TODO   |

#### E5-S5: Admin Profile Page

| Task     | Description                       | Status |
| -------- | --------------------------------- | ------ |
| E5-S5-T1 | Display admin account information | TODO   |
| E5-S5-T2 | Implement password change         | TODO   |
| E5-S5-T3 | Show account activity summary     | TODO   |
| E5-S5-T4 | Write unit tests                  | TODO   |

---

### Epic E-6: Appointment System

#### E6-S1: Appointment Booking Logic

| Task     | Description                            | Status |
| -------- | -------------------------------------- | ------ |
| E6-S1-T1 | Implement available slot calculation   | TODO   |
| E6-S1-T2 | Implement conflict checking            | TODO   |
| E6-S1-T3 | Implement transactional booking writes | TODO   |
| E6-S1-T4 | Write unit tests                       | TODO   |

#### E6-S2: Hybrid Booking Support

| Task     | Description                                  | Status |
| -------- | -------------------------------------------- | ------ |
| E6-S2-T1 | Support online bookings                      | TODO   |
| E6-S2-T2 | Support phone call-in bookings (admin entry) | TODO   |
| E6-S2-T3 | Unified calendar view                        | TODO   |
| E6-S2-T4 | Write unit tests                             | TODO   |

---

### Epic E-7: Notifications System

#### E7-S1: Notification Generation

| Task     | Description                                 | Status |
| -------- | ------------------------------------------- | ------ |
| E7-S1-T1 | Generate appointment reminder notifications | TODO   |
| E7-S1-T2 | Generate results ready notifications        | TODO   |
| E7-S1-T3 | Generate prescription update notifications  | TODO   |
| E7-S1-T4 | Write unit tests                            | TODO   |

---

### Epic E-8: Testing & QA

#### E8-S1: Unit Testing

| Task     | Description                   | Status |
| -------- | ----------------------------- | ------ |
| E8-S1-T1 | Test validators               | DONE   |
| E8-S1-T2 | Test authentication functions | DONE   |
| E8-S1-T3 | Test RBAC functions           | DONE   |
| E8-S1-T4 | Test session management       | DONE   |
| E8-S1-T5 | Test user repository          | DONE   |
| E8-S1-T6 | Test auth service             | DONE   |

#### E8-S2: Integration Testing

| Task     | Description                   | Status       |
| -------- | ----------------------------- | ------------ |
| E8-S2-T1 | Test login flow               | DONE (basic) |
| E8-S2-T2 | Test appointment booking flow | TODO         |
| E8-S2-T3 | Test results publishing flow  | TODO         |

---

### Epic E-9: Documentation

#### E9-S1: Technical Documentation

| Task     | Description                    | Status |
| -------- | ------------------------------ | ------ |
| E9-S1-T1 | README with setup instructions | DONE   |
| E9-S1-T2 | Database schema documentation  | DONE   |
| E9-S1-T3 | Architecture overview          | DONE   |
| E9-S1-T4 | Authentication flow diagram    | DONE   |

---

### Epic E-10: UI Components & Layout

#### E10-S1: Sidebar Navigation - COMPLETE

| Task      | Description                                        | Status |
| --------- | -------------------------------------------------- | ------ |
| E10-S1-T1 | Create sidebar component structure                 | DONE   |
| E10-S1-T2 | Implement role-based navigation links              | DONE   |
| E10-S1-T3 | Style sidebar with CSS (sidebar.css)               | DONE   |
| E10-S1-T4 | Implement sidebar as overlay (not pushing content) | DONE   |
| E10-S1-T5 | Add JavaScript toggle functionality                | DONE   |
| E10-S1-T6 | Hide menu toggle on login page                     | DONE   |
| E10-S1-T7 | Add logout button in sidebar                       | DONE   |
| E10-S1-T8 | Highlight active page in navigation                | DONE   |

#### E10-S2: Header Component - COMPLETE

| Task      | Description                                  | Status |
| --------- | -------------------------------------------- | ------ |
| E10-S2-T1 | Create header component with logo            | DONE   |
| E10-S2-T2 | Add menu toggle button (hamburger icon)      | DONE   |
| E10-S2-T3 | Conditional menu toggle (hide on login)      | DONE   |
| E10-S2-T4 | Style header with gradient background        | DONE   |
| E10-S2-T5 | Fix HTML rendering issues (single-line HTML) | DONE   |

#### E10-S3: Dashboard Layout Component - COMPLETE

| Task      | Description                            | Status |
| --------- | -------------------------------------- | ------ |
| E10-S3-T1 | Create reusable dashboard_layout.py    | DONE   |
| E10-S3-T2 | Integrate header, sidebar, CSS loading | DONE   |
| E10-S3-T3 | Add role-based access control          | DONE   |
| E10-S3-T4 | Remove empty container divs            | DONE   |

#### E10-S4: CSS Styling System - COMPLETE

| Task      | Description                                   | Status |
| --------- | --------------------------------------------- | ------ |
| E10-S4-T1 | Create main.css with base styles              | DONE   |
| E10-S4-T2 | Create login.css for authentication pages     | DONE   |
| E10-S4-T3 | Create dashboard.css for dashboard components | DONE   |
| E10-S4-T4 | Create sidebar.css for navigation styling     | DONE   |
| E10-S4-T5 | Hide Streamlit default elements               | DONE   |
| E10-S4-T6 | Implement stat cards styling                  | DONE   |
| E10-S4-T7 | Implement appointment card styling            | DONE   |

---

## Test Credentials

| Role    | Email                      | Password    |
| ------- | -------------------------- | ----------- |
| Admin   | admin@carelink.nhs.uk      | Admin123!   |
| Doctor  | dr.johnson@carelink.nhs.uk | Doctor123!  |
| Patient | patient@carelink.nhs.uk    | Patient123! |

---

## Database Tables

1. `users` - Authentication and role data
2. `patients` - Patient demographics and contact details
3. `doctors` - Clinician data and approval status
4. `appointments` - Bookings between patients and doctors
5. `prescriptions` - Medication orders and lifecycle
6. `bloodwork` - Lab results with JSON payloads (structured as categories/markers)
7. `notifications` - Patient-facing notifications
8. `audit_logs` - Immutable audit trail

---

## Functional Requirements Mapping

| Requirement | Description                                                | Related Stories     |
| ----------- | ---------------------------------------------------------- | ------------------- |
| FR1         | Patient portal for bloodwork, prescriptions, notifications | E3-S2, E3-S3, E3-S5 |
| FR2         | Hybrid appointment booking (online + phone)                | E3-S4, E6-S1, E6-S2 |
| FR3         | Doctor portal for reviewing/publishing results             | E4-S2, E4-S3        |
| FR4         | Admin portal for user management and phone bookings        | E5-S2, E5-S3        |

## Non-Functional Requirements Mapping

| Requirement        | Description                                    | Implementation              |
| ------------------ | ---------------------------------------------- | --------------------------- |
| NFR1 (Security)    | RBAC, TLS, encryption, audit logging           | Sprint 1 complete           |
| NFR2 (Performance) | Page actions < 3s, pagination                  | Use ITEMS_PER_PAGE = 7      |
| NFR3 (Reliability) | Consistent booking state, transactional writes | E6-S1                       |
| NFR4 (Usability)   | WCAG 2.1 AA, clear layouts                     | 16px min font, keyboard nav |

---

## Sprint 3 Progress (January 5-7, 2026)

### Completed Items ✅

1. **Patient Appointments Page (E3-S4)** - COMPLETE

   - Full booking calendar with month navigation
   - Time slot selection with AM/PM organization
   - Duration selector (30/60 minutes)
   - Appointment confirmation modal dialog
   - My Appointments list view with cancellation
   - Visual indicators (green for dates, teal for times)
   - Responsive design matching system aesthetics
   - Form validation and error handling

2. **UI/UX Refinements**

   - Modal dialog system for confirmations
   - Consistent button styling (teal primary, gray secondary, blue actions)
   - White card backgrounds throughout
   - Dark text on light backgrounds for readability
   - Red asterisks for required fields
   - Checkmarks on selected options
   - Professional calendar interface

3. **DevOps & Deployment**
   - Docker Compose configuration verified
   - .env.example template created
   - Database migrations working
   - Development environment stable

### In Progress 🔄

1. **Bloodwork Viewer (E3-S2)** - Priority for demo

   - Repository layer: Not started
   - 3-level hierarchical UI: Not started
   - Visual range indicators: Not started

2. **Prescriptions View (E3-S3)** - Secondary priority

   - Repository layer: Not started
   - Active/history tabs: Not started

3. **Notifications View (E3-S5)** - Secondary priority
   - List view: Partially done
   - Mark as read: Not implemented

### Blockers & Issues

- None currently

### Next Sprint Priorities

1. **Bloodwork Viewer** (High Priority - Demo Impact)

   - Build repository and service layers
   - Implement Level 1: Blood draw list
   - Implement Level 2: Categories view
   - Implement Level 3: Marker details with range bars
   - Add seed data with realistic bloodwork results

2. **Prescriptions View** (Medium Priority)

   - Create repository
   - Build simple list view
   - Add active/history filtering

3. **Notifications View** (Medium Priority)

   - Complete list rendering
   - Add mark as read functionality

4. **Doctor Dashboard** (Medium Priority)
   - Connect to real appointment data
   - Show today's schedule
   - Display statistics from database

---

## Interim Demo Preparation (Target: January 9, 2026)

### Demo Flow Script

**1. Login & Authentication (30 seconds)**

- Show login page design
- Demonstrate role-based access control
- Login as patient

**2. Patient Dashboard (45 seconds)**

- Overview of dashboard layout
- Real data: upcoming appointments, recent notifications
- Quick actions buttons

**3. Appointment Booking (2 minutes)** ✅ READY

- Navigate to Appointments page
- Show "My Appointments" tab with existing bookings
- Switch to "Book Appointment" tab
- Select date from calendar (demonstrate month navigation)
- Choose duration (30/60 min)
- Select time slot from AM/PM sections
- Click "Continue to Confirm"
- Show modal confirmation dialog
- Enter reason for visit
- Confirm booking
- Show success message

**4. Bloodwork Results (1.5 minutes)** - TODO

- Navigate to Bloodwork page
- Show list of blood test results
- Drill into specific test
- Show categories (CBC, Lipid Panel, etc.)
- Drill into category
- Show individual markers with visual range bars
- Highlight interpretation notes

**5. Prescriptions (30 seconds)** - TODO

- Navigate to Prescriptions page
- Show active prescriptions
- Show prescription history

**6. Role Switching (30 seconds)**

- Logout
- Login as doctor
- Show doctor dashboard
- Demonstrate different navigation options

**Total Demo Time:** ~5-6 minutes

### Demo Readiness Status

| Feature             | Status   | Notes                        |
| ------------------- | -------- | ---------------------------- |
| Authentication      | ✅ READY | Working with seed data       |
| Patient Dashboard   | ✅ READY | Connected to database        |
| Appointment Booking | ✅ READY | Full flow working with modal |
| Bloodwork Viewer    | ⏳ TODO  | Critical for demo            |
| Prescriptions List  | ⏳ TODO  | Simple view sufficient       |
| Notifications List  | ⏳ TODO  | Basic list sufficient        |
| Doctor Dashboard    | ⏳ TODO  | Connect to real data         |
| UI/UX Polish        | ✅ READY | Consistent design system     |
| Docker Deployment   | ✅ READY | One-command setup            |

---

## Sprint 3 Priority (Updated January 7, 2026)

For the Interim Demo (January 9, 2026), focus on:

1. ~~**Fix CSS loading issues**~~ - COMPLETE ✓
2. ~~**Connect Patient Dashboard to real data**~~ - COMPLETE ✓ (E3-S1-T7)
3. ~~**UI Components (Sidebar, Header)**~~ - COMPLETE ✓ (E10)
4. ~~**Appointments page with booking flow**~~ - COMPLETE ✓ (E3-S4)
5. **Bloodwork viewer** (E3-S2) - CRITICAL for demo - IN PROGRESS
6. **Prescriptions view** (E3-S3) - Simple list view (1-2 hours)
7. **Notifications view** (E3-S5) - Simple list view (1 hour)
8. **Connect Doctor Dashboard to real data** (E4-S1-T7) - (2 hours)

**Estimated Time to Demo-Ready:** 8-12 hours of focused development

---

## Sprint Retrospectives

### Sprint 3 Retrospective (January 5-7, 2026)

**Sprint Goal:** Build patient-facing features for interim demo

**Completed:**

- ✅ Patient appointment booking system (E3-S4) - EXCEEDED EXPECTATIONS
  - Full calendar interface
  - Time slot selection
  - Modal confirmation
  - Responsive design
  - Professional UI/UX

**Challenges Faced:**

1. **CSS Overriding Issues**
   - Problem: Streamlit's default styles overriding custom button colors
   - Solution: Used `!important` rules and specific selectors
   - Time Impact: +3 hours
2. **Modal Dialog Styling**

   - Problem: Default dark theme not matching system design
   - Solution: Comprehensive CSS targeting `div[role="dialog"]`
   - Time Impact: +2 hours

3. **Input Text Color in Disabled Fields**
   - Problem: Disabled inputs showing white/light text
   - Solution: Added `-webkit-text-fill-color` and opacity overrides
   - Time Impact: +1 hour

**What Went Well:**

- st.dialog() API simplified modal implementation
- Reusable CSS patterns from previous pages sped up styling
- Clear design system made decisions straightforward
- Docker environment remained stable throughout

**What Could Improve:**

- Better upfront understanding of Streamlit CSS specificity
- Could have planned modal styling earlier in design phase
- Need to timebox CSS tweaking (perfectionism risk)

**Velocity:**

- Estimated: 5 story points
- Actual: 8 story points (appointment booking was larger than estimated)
- Velocity improving as familiarity with stack increases

**Action Items for Next Sprint:**

- Document CSS override patterns for reuse
- Create component library for common UI elements
- Set 2-hour timebox for styling iterations

### Sprint 2 Retrospective (December 2025)

**Sprint Goal:** Authentication and core dashboard UI

**Completed:**

- ✅ Login page with full authentication
- ✅ Patient dashboard with real data
- ✅ Sidebar navigation system
- ✅ CSS styling foundation

**Challenges:**

- Learning Streamlit's component model
- Understanding session state management
- CSS loading and caching issues

**Outcomes:**

- Strong foundation for all future pages
- Reusable component patterns established
- Clear design system in place

---

## Technical Debt & Known Issues

### Technical Debt Log

| ID   | Description                          | Impact | Priority | Created    | Status |
| ---- | ------------------------------------ | ------ | -------- | ---------- | ------ |
| TD-1 | CSS uses many !important rules       | Low    | P3       | Jan 7 2026 | OPEN   |
| TD-2 | No automated integration tests yet   | Medium | P2       | Jan 7 2026 | OPEN   |
| TD-3 | Hardcoded time slots in appointments | Low    | P3       | Jan 6 2026 | OPEN   |
| TD-4 | No pagination on My Appointments     | Medium | P2       | Jan 6 2026 | OPEN   |
| TD-5 | Doctor availability not implemented  | High   | P1       | Jan 6 2026 | OPEN   |

**Technical Debt Repayment Plan:**

- TD-5 (Doctor availability): Required before production
- TD-2 (Integration tests): Add during Sprint 4
- TD-4 (Pagination): Add when > 7 appointments exist
- TD-1, TD-3: Low priority, address in refactoring sprint

### Known Issues

| ID    | Description                             | Severity | Reported   | Status        |
| ----- | --------------------------------------- | -------- | ---------- | ------------- |
| BUG-1 | Modal backdrop click doesn't close      | Minor    | Jan 7 2026 | OPEN          |
| BUG-2 | Calendar doesn't prevent double-booking | Critical | Jan 6 2026 | INVESTIGATING |

### Browser Compatibility

**Tested:**

- ✅ Chrome 120+ (macOS)
- ✅ Safari 17+ (macOS)
- ⏳ Firefox (not tested)
- ⏳ Chrome (Windows)
- ⏳ Edge (Windows)

**Note:** Full cross-browser testing scheduled for Sprint 4

---

## Risk Register

| Risk ID | Description                               | Probability | Impact | Mitigation Strategy                   | Status  |
| ------- | ----------------------------------------- | ----------- | ------ | ------------------------------------- | ------- |
| R-1     | Bloodwork viewer too complex for deadline | High        | High   | Simplify to 2-level view if needed    | MONITOR |
| R-2     | Docker deployment issues on Windows       | Medium      | Medium | Test on Windows machine before demo   | OPEN    |
| R-3     | Database migration conflicts              | Low         | High   | Use version control, test migrations  | CLOSED  |
| R-4     | Insufficient test coverage                | Medium      | Medium | Prioritize critical path testing      | OPEN    |
| R-5     | Demo video technical difficulties         | Medium      | High   | Record multiple takes, test equipment | OPEN    |

**Risk Mitigation Actions:**

- R-1: Have backup plan for simplified bloodwork view
- R-2: Set up Windows test environment by Jan 8
- R-5: Practice demo walkthrough Jan 8

---

## Development Metrics

### Code Statistics (as of January 7, 2026)

**Lines of Code:**

- Python: ~8,500 lines
- CSS: ~1,200 lines
- SQL/Migrations: ~400 lines
- Tests: ~1,800 lines
- **Total:** ~11,900 lines

**File Count:**

- Models: 8 files
- Repositories: 5 files
- Services: 6 files
- Pages: 17 files (6 patient, 5 doctor, 5 admin, 1 login)
- Tests: 10 test files
- CSS: 4 stylesheets

**Test Coverage:**

- Unit Tests: 29 passing
- Integration Tests: 3 passing
- E2E Tests: 1 passing
- **Total:** 33 tests
- Coverage: ~45% (estimated)

### Velocity Tracking

**Sprint 1 (Infrastructure):**

- Story Points Completed: 21
- Stories: 15
- Duration: 2 weeks

**Sprint 2 (Auth & UI):**

- Story Points Completed: 18
- Stories: 12
- Duration: 2 weeks

**Sprint 3 (Patient Features):**

- Story Points Planned: 25
- Story Points Completed: 8 (as of Jan 7)
- Stories Completed: 1/6
- Duration: 1 week (in progress)
- Projected Completion: 60% (if focus on demo priorities)

**Average Velocity:** ~6-7 story points per week

### Time Tracking

**Development Hours (Sprint 3):**

- Appointment Booking: 12 hours
- CSS/Styling: 6 hours
- Bug Fixes: 2 hours
- Testing: 1 hour
- **Total:** 21 hours

**Estimated Remaining (to Demo):**

- Bloodwork Viewer: 8 hours
- Prescriptions: 2 hours
- Notifications: 1 hour
- Doctor Dashboard: 2 hours
- Demo Preparation: 2 hours
- **Total:** 15 hours

### Repository Activity

**Commits (January 2026):**

- Jan 5: 3 commits (appointment booking start)
- Jan 6: 8 commits (calendar implementation, time slots)
- Jan 7: 12 commits (modal, styling refinements)
- **Total:** 23 commits in 3 days

**Key Milestones:**

- ✅ Dec 15, 2025: Infrastructure complete
- ✅ Dec 28, 2025: Authentication working
- ✅ Jan 3, 2026: Patient dashboard live
- ✅ Jan 7, 2026: Appointment booking complete
- ⏳ Jan 9, 2026: Interim demo (TARGET)

---

## Important Notes for Development

1. **DO NOT modify** `Home.py` or `pages/patient_1_Dashboard.py` design - these are complete
2. **Minimal emoji usage** - only for visual indicators where appropriate
3. **NO static/hardcoded values** - all data must come from database
4. **All pages must load CSS** before rendering content
5. **Minimum 16px font size** for accessibility
6. **Use repository pattern** for all database access
7. **Use service layer** for business logic
8. **Audit log** all sensitive operations
