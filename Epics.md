# CareLink - Project Requirements & Epic Documentation

## Project Overview

**Project Title:** CareLink: A Role-Based Patient Doctor Medical Dashboard for Integrated Patient Management and Hybrid Appointment Booking

**Student:** Jack Williamson (40365072)

**Key Deadline:** Interim Demo Video - January 9, 2026

---

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

### Components

- Border radius: 12px for cards, 8px for buttons/inputs
- Box shadow: `0 2px 8px rgba(0, 0, 0, 0.08)` standard
- Card padding: 20-24px

### Important Design Rules

1. MINIMAL emoji usage - only for visual indicators where appropriate (e.g., status icons)
2. NO hardcoded/static values - all data must come from database
3. Minimum 16px font size for accessibility
4. All pages must load CSS before rendering content

---

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
- Database seed script
- Initial Alembic migration

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

#### E3-S4: Appointments View & Booking

| Task     | Description                          | Status      |
| -------- | ------------------------------------ | ----------- |
| E3-S4-T1 | Create appointment repository        | DONE        |
| E3-S4-T2 | Create appointment service           | IN PROGRESS |
| E3-S4-T3 | Implement upcoming appointments list | TODO        |
| E3-S4-T4 | Implement appointment booking form   | TODO        |
| E3-S4-T5 | Implement appointment cancellation   | TODO        |
| E3-S4-T6 | Add conflict checking for bookings   | TODO        |
| E3-S4-T7 | Write unit tests                     | TODO        |

#### E3-S5: Notification Centre

| Task     | Description                                | Status |
| -------- | ------------------------------------------ | ------ |
| E3-S5-T1 | Create notification repository             | TODO   |
| E3-S5-T2 | Create notification service                | DONE   |
| E3-S5-T3 | Implement notification list with filtering | TODO   |
| E3-S5-T4 | Implement mark as read functionality       | TODO   |
| E3-S5-T5 | Implement mark all read                    | TODO   |
| E3-S5-T6 | Write unit tests                           | TODO   |

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

## Sprint 3 Priority

For the Interim Demo (January 9, 2026), focus on:

1. ~~**Fix CSS loading issues**~~ - COMPLETE ✓
2. ~~**Connect Patient Dashboard to real data**~~ - COMPLETE ✓ (E3-S1-T7)
3. ~~**UI Components (Sidebar, Header)**~~ - COMPLETE ✓ (E10)
4. **Bloodwork viewer** (E3-S2) - HIGH IMPACT demo feature - IN PROGRESS
5. **Appointments page** (E3-S4) - Shows hybrid booking concept
6. **Prescriptions view** (E3-S3) - Simple list is sufficient
7. **Notifications view** (E3-S5) - Simple list is sufficient
8. **Connect Doctor Dashboard to real data** (E4-S1-T7)

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
