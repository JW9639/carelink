# CareLink - Epics and Progress

Last updated: January 08, 2026

## Project Overview
CareLink is a role-based patient, doctor, and admin portal for appointment booking, results review, prescriptions, and notifications. The app is built with Streamlit, PostgreSQL, SQLAlchemy, and Docker. Core patterns are repository + service layers with audit logging.

Delivery approach: UI-first, then functionality, then database integration.

Design constraints (do not redesign):
- Login page: app/pages/Home.py
- Patient dashboard: app/pages/patient_1_Dashboard.py
- Patient appointments: app/pages/patient_4_Appointments.py


---

## Epic E1: UI and Layout System
| Story | Description | Status |
| --- | --- | --- |
| E1-S1 | Sidebar/navigation system | DONE |
| E1-S2 | Header + global styles | DONE |
| E1-S3 | Card/stats styling patterns | DONE |

## Epic E2: Authentication and Security
| Story | Description | Status |
| --- | --- | --- |
| E2-S1 | Login + session management | DONE |
| E2-S2 | RBAC and role routing | DONE |
| E2-S3 | Audit logging for actions | TODO |

## Epic E3: Patient Portal
| Story | Description | Status |
| --- | --- | --- |
| E3-S1 | Patient dashboard | DONE |
| E3-S2 | Bloodwork results viewer | DONE |
| E3-S3 | Prescriptions view (active/history) | TODO |
| E3-S4 | Appointment booking and my appointments | DONE |
| E3-S5 | Notifications center | TODO |
| E3-S6 | Patient profile | TODO |

## Epic E4: Doctor Portal
| Story | Description | Status |
| --- | --- | --- |
| E4-S1 | Doctor dashboard (live stats) | TODO |
| E4-S2 | Patient list and detail view | TODO |
| E4-S3 | Results entry, review, publish | DONE |
| E4-S4 | Doctor appointments view | TODO |
| E4-S5 | Prescription management | TODO |
| E4-S6 | Doctor profile | TODO |

## Epic E5: Admin Portal
| Story | Description | Status |
| --- | --- | --- |
| E5-S1 | Admin dashboard | TODO |
| E5-S2 | User management | TODO |
| E5-S3 | Assign doctors to pending appointments | TODO |
| E5-S4 | Audit log viewer | TODO |
| E5-S5 | Admin profile | TODO |

## Epic E6: Scheduling and Availability
| Story | Description | Status |
| --- | --- | --- |
| E6-S1 | Available slot calculation | DONE |
| E6-S2 | Conflict detection | DONE |
| E6-S3 | Doctor availability management | TODO |
| E6-S4 | Reschedule workflow | TODO |

## Epic E7: Notifications System
| Story | Description | Status |
| --- | --- | --- |
| E7-S1 | Notification storage + read state | DONE |
| E7-S2 | Patient notification UI | TODO |
| E7-S3 | Automatic notification generation | TODO |

## Epic E8: Infrastructure and Data
| Story | Description | Status |
| --- | --- | --- |
| E8-S1 | Database models and migrations | DONE |
| E8-S2 | Repository + service layers | DONE |
| E8-S3 | Docker and env setup | DONE |
| E8-S4 | Seed data for dev/demo | DONE |

## Epic E9: Testing and QA
| Story | Description | Status |
| --- | --- | --- |
| E9-S1 | Unit tests (auth, validators, repos) | PARTIAL |
| E9-S2 | Appointment service unit tests | DONE |
| E9-S3 | Integration tests (login, booking) | DONE |
| E9-S4 | E2E patient journey | PARTIAL |
| E9-S5 | Bloodwork/prescription/notification tests | TODO |

## Epic E10: Documentation
| Story | Description | Status |
| --- | --- | --- |
| E10-S1 | README and setup docs | DONE |
| E10-S2 | Database schema doc | TODO |
| E10-S3 | Architecture overview | TODO |
| E10-S4 | Data flow docs | TODO |

---

## Remaining Work (By Priority)
1) Doctor portal data: dashboard stats, appointments list, patient list (E4-S1, E4-S2, E4-S4)
2) Admin portal: user management, audit log, full appointments list (E5-S2, E5-S4)
3) Patient profile and doctor/admin profiles (E3-S6, E4-S6, E5-S5)
4) Notification generation rules (E7-S3)
5) Availability + reschedule workflow (E6-S3, E6-S4)
6) Update epic for full testing requirements
