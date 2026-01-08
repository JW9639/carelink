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
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E1-S1 | Sidebar and role navigation | Done: custom sidebar toggle + nav buttons | DONE |
| E1-S2 | App header and global theme | Done: fixed header, typography, color tokens | DONE |
| E1-S3 | Reusable cards + stat tiles | Done: shared card/stats patterns across pages | DONE |

## Epic E2: Authentication and Security
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E2-S1 | Login and session management | Done: auth flow + session state | DONE |
| E2-S2 | RBAC and role routing | Done: role-based page access | DONE |
| E2-S3 | Audit logging for actions | To-do: log critical user and admin actions | TODO |
| E2-S4 | Account recovery and lockout | To-do: reset flow + brute-force protection | TODO |

## Epic E3: Patient Portal
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E3-S1 | Patient dashboard | Done: live stats + upcoming appointment | DONE |
| E3-S2 | Bloodwork results viewer | Done: panels, results, range markers | DONE |
| E3-S3 | Prescriptions view | To-do: active + history with refills | TODO |
| E3-S4 | Appointments booking and list | Done: booking flow + confirmations | DONE |
| E3-S5 | Notifications center | To-do: list, read state, filters | TODO |
| E3-S6 | Patient profile | To-do: demographics, contacts, settings | TODO |

## Epic E4: Doctor Portal
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E4-S1 | Doctor dashboard (live stats) | To-do: caseload, pending reviews, alerts | TODO |
| E4-S2 | Patient list and detail view | To-do: roster + patient overview | TODO |
| E4-S3 | Results entry, review, publish | Done: data entry + review + publish flow | DONE |
| E4-S4 | Doctor appointments view | To-do: upcoming, history, filters | TODO |
| E4-S5 | Prescription management | To-do: create, renew, discontinue | TODO |
| E4-S6 | Doctor profile | To-do: availability, specialties, settings | TODO |

## Epic E5: Admin Portal
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E5-S1 | Admin dashboard | To-do: system stats and alerts | TODO |
| E5-S2 | User management | To-do: create/edit roles + deactivate | TODO |
| E5-S3 | Appointment assignment workflow | To-do: assign/triage pending bookings | TODO |
| E5-S4 | Audit log viewer | To-do: filterable audit timeline | TODO |
| E5-S5 | Admin profile | To-do: profile + permissions view | TODO |

## Epic E6: Scheduling and Availability
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E6-S1 | Available slot calculation | Done: slot generation from schedules | DONE |
| E6-S2 | Conflict detection | Done: block overlapping bookings | DONE |
| E6-S3 | Doctor availability management | To-do: clinic hours + time off | TODO |
| E6-S4 | Reschedule workflow | To-do: patient/doctor reschedule flow | TODO |

## Epic E7: Notifications System
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E7-S1 | Notification storage and read state | Done: model + repository + read flags | DONE |
| E7-S2 | Patient notification UI | To-do: inbox list + mark read | TODO |
| E7-S3 | Auto notification rules | To-do: appointment/bloodwork triggers | TODO |

## Epic E8: Infrastructure and Data
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E8-S1 | Database models and migrations | Done: schema + Alembic versions | DONE |
| E8-S2 | Repository + service layers | Done: data access patterns | DONE |
| E8-S3 | Docker and env setup | Done: container + env config | DONE |
| E8-S4 | Seed data for dev/demo | Done: initial dataset scripts | DONE |
| E8-S5 | CI pipeline for tests/lint | To-do: GitLab CI with pytest/flake8 | TODO |
| E8-S6 | Logging and error handling | To-do: consistent app logging | TODO |
| E8-S7 | Data retention and backups | To-do: backup strategy + retention notes | TODO |

## Epic E9: Testing and QA
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E9-S1 | Unit tests for core services | To-do: expand coverage beyond auth | TODO |
| E9-S2 | Appointment service unit tests | Done: overlap + booking logic | DONE |
| E9-S3 | Integration tests (login, booking) | Done: basic flow coverage | DONE |
| E9-S4 | E2E patient journey | To-do: full patient workflow path | TODO |
| E9-S5 | Bloodwork/prescription/notification tests | To-do: service + UI coverage | TODO |
| E9-S6 | QA checklist and bug tracking | To-do: test plan + known issues log | TODO |

## Epic E10: Documentation
| Story | Title | Desc | Status |
| --- | --- | --- | --- |
| E10-S1 | README and setup docs | Done: install + run instructions | DONE |
| E10-S2 | Database schema doc | To-do: finalize schema tables | TODO |
| E10-S3 | Architecture overview | To-do: services + repo flow | TODO |
| E10-S4 | Data flow docs | To-do: request/response paths | TODO |

---

## Remaining Work (By Priority)
1) Doctor portal data: dashboard stats, patient list, appointments view (E4-S1, E4-S2, E4-S4)
2) Admin portal: user management, assignment workflow, audit viewer (E5-S2, E5-S3, E5-S4)
3) Patient profile + doctor/admin profiles (E3-S6, E4-S6, E5-S5)
4) Notifications: patient UI + auto rules (E7-S2, E7-S3)
5) Scheduling: availability management + reschedule flow (E6-S3, E6-S4)
6) QA + CI: expand tests and add pipeline (E9-S1, E9-S4, E9-S5, E8-S5)
7) Docs and guides: schema, architecture, user guide (E10-S2, E10-S3, E10-S5)
