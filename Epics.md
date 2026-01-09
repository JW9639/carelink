# CareLink - Epics and Progress

Last updated: January 09, 2026

---

# EPIC 0 - Setup & Runtime Foundations

**E0-S1 [DONE] Create Repo**  
Description: Initialise GitLab repo.

**E0-S2 [DONE] Repo Structure Skeleton**  
Description: Create skeleton folders:  
app/pages, app/services, app/db/repositories, app/models, app/security, app/ui, app/styles, app/utils, app/schemas, scripts, tests/*, migrations/*.

---

## EPIC 1 - Configuration, Secrets, Logging & Safe Errors

**E1-S1 [DONE] Config Loader + .env.example**  
Description: Implement app/config.py (env vars), include .env.example.  
Acceptance: App boots via env vars; no secrets committed.

**E1-S2 [TODO] Logging + Redaction**  
Description: Add app-wide logging; redact secrets; log exceptions with safe messages.  
Acceptance: Logs consistent; user never sees raw stack traces.

**E1-S3 [TODO] Error Handling Pattern**  
Description: Standardize service exceptions -> UI-safe error messages.  
Acceptance: Common failures show friendly UI feedback.

---

## EPIC 2 - Docker & Local Dev Experience

**E2-S1 [DONE] Dockerfile for Streamlit App**  
Description: Build Dockerfile for Streamlit.  
Acceptance: Image builds and runs.

**E2-S2 [DONE] docker-compose (App + Postgres)**  
Description: Compose file with Postgres volume + healthcheck + Streamlit on 8501.  
Acceptance: docker-compose up --build works.

**E2-S3 [STARTED] Reset/Seed Scripts**  
Description: Add scripts to reset DB + seed demo users/patients/doctors/results/appointments.  
Acceptance: Repeatable demo environment.

---

# EPIC 3 - Patient MVP (Build the Patient Experience First)

**E3-S1 [DONE] Patient Dashboard**  
Description: Show upcoming appointment + recent results + active prescriptions + unread notifications.  
Acceptance: Handles empty states; fast.

**E3-S2 [DONE] Bloodwork Viewer (Published Only)**  
Description: History + detail view; show only published results.  
Acceptance: Drafts never visible to patient.

**E3-S3 [STARTED] Prescriptions Viewer**  
Description: Active + history prescriptions with notes/instructions.  
Acceptance: Accurate grouping.

**E3-S4 [STARTED] Notifications Inbox (Read-only)**  
Description: List notification cards; click "View" to read full message.  
Acceptance:
- Preview card -> detail view
- No replying
- Read/unread optional but recommended

**E3-S5 [DONE] Patient Online Booking**  
Description: Patient books slot -> stored in DB -> confirmation.  
Acceptance: Booking persists; appointment shows in lists.

**E3-S6 [TODO] Patient Profile (Including Low-Priority Requests)**  
Description: Demographic/contact info view (editable fields as allowed).  
Also include 2 low-priority actions:
- Button: "Request Medical Records" -> popup collects brief details -> submits request to Admin Requests tab.
- Button: "Request Private Referral" -> popup collects details -> submits request to Admin Requests tab for triage/assignment.
Acceptance:
- Validations + audit log on profile edits
- Requests create DB records and appear in admin queue (see E5-S8)

**E3-S7 [TODO] Appointment Cancellation Policy**  
Description: Patient cancellation up to cutoff (e.g. 1 hour before).  
Acceptance: Rule enforced; audit logged.

**E3-S8 [TODO] Reschedule (Patient-facing where allowed)**  
Description: Reschedule workflow with full conflict checks + audit.  
Acceptance: Safe rescheduling; history preserved.

**E3-S9 [TODO] Appointment Detail View (Past + Upcoming)**  
Description: On patient appointment history (upcoming + past), allow user to click an appointment row/card to open a detail view (modal or detail section) showing:
- date/time, doctor (if set), status, duration, booking_source, notes (if any)
- cancellation reason (if cancelled)
Acceptance:
- Works for past and upcoming appointments
- Does not expose internal-only/admin-only fields

---

# EPIC 4 - Doctor MVP (After Patient Works)

**E4-S1 [STARTED] Doctor Dashboard**  
Description: Show today's appointments, pending tasks, quick links to roster.  
Acceptance: DB-backed; handles empty.

**E4-S2 [TODO] Doctor Patient List + Patient Detail**  
Description: Doctor sees linked patients only, with search by name and pagination (X per page). Each row has a View button that opens a patient chart with actions: Prescribe, Order Lab, Send Message.  
Acceptance:
- Cannot view unlinked patients
- Search filters the list
- Pagination works with real data
- View opens the chart and shows the action buttons

**E4-S3 [DONE] Bloodwork Draft + Review**  
Description: Doctor creates draft results; review step before publish.  
Acceptance: Stored as unpublished.

**E4-S4 [DONE] Publish Bloodwork**  
Description: Publish sets flags/timestamps and makes visible to patient.  
Acceptance: Patient sees immediately; audit logged.

**E4-S5 [TODO] Prescription Management**  
Description: Doctor creates/renews/discontinues prescriptions.  
Acceptance: Patient view updates; audit logged.

**E4-S6 [TODO] Doctor Appointments View**  
Description: Upcoming/history with filters + pagination.  
Acceptance: Works with real data.

**E4-S7 [TODO] Doctor Notification Composer**  
Description: Implement doctor-side "send notification" modal on patient detail page:
- Button "Send Notification"
- Popup/modal: subject + message body (and optional category)
- Submit creates notification for that patient (one-way)  
Acceptance:
- Notification appears in patient notifications inbox as a card preview
- Patient can open and read, cannot respond
- Audit log entry for send action

**E4-S8 [TODO] Doctor Approves/Declines Private Referral Requests (Assigned by Admin)**  
Description: Doctor can view referral requests assigned to them (from Admin Requests tab), review details, and set outcome:
- Approve / Decline
- Optional note
Acceptance:
- Outcome saved to request record
- Audit log entry created
- Patient can see updated status (can be minimal: status string visible in profile request history or notification)

**E4-S9 [STARTED] Doctor Message Center (GP Admin Messages)**  
Description: Doctor receives messages from GP Admin in a Message Center (similar to patient notifications), labeled by an admin-selected category:
- Medication refill request for patient (to be added)
- Bloodwork results (admin message that prompts doctor action)
- Private referral requests  
Acceptance:
- Messages are stored and shown in a doctor inbox
- Category label is visible on each message
- Unread/read state is supported
- Admin selects a category when sending

---

# EPIC 5 - Admin MVP (Provisioning + Operational Control)

**E5-S1 [STARTED] Admin Dashboard**  
Description: Operational overview: pending items, quick links.  
Acceptance: DB-backed.

**E5-S2 [TODO] Admin Creates Patient Account (In-person Registration Flow)**  
Description: Admin creates patient user credentials:
- Admin enters patient details + email
- System generates/sets a temporary password (admin can copy)
- User created with must_change_password=True
- Patient record created and linked to user  
Acceptance:
- Patient can login with temp creds
- Forced password change occurs on first login
- Account creation audited

**E5-S3 [TODO] Admin Creates Doctor Account (Same Provisioning Flow)**  
Description: Admin creates doctor credentials using same pattern:
- email + temp password
- must_change_password=True
- doctor profile created  
Acceptance: Doctor forced to change password on first login; audited.

**E5-S4 [TODO] User Management (Activate/Deactivate, Role Updates)**  
Description: Admin can disable accounts, reset temp password (sets must_change_password True), change roles where appropriate.  
Acceptance: Changes audited; RBAC enforced.

**E5-S5 [TODO] Patient-Doctor Linking**  
Description: Admin assigns patients to doctors.  
Acceptance: Doctor roster updates; audited.

**E5-S6 [TODO] Admin Phone Booking (Hybrid Booking)**  
Description: Admin can record phone bookings into the canonical appointment model.  
Acceptance: booking_source=PHONE; conflict checks; audited.

**E5-S7 [TODO] Admin Audit Viewer**  
Description: Admin filters and views audit timeline.  
Acceptance: Works + safe display.

**E5-S8 [TODO] Admin Requests Tab (Medical Records + Private Referral)**  
Description: Create an Admin page/tab to manage incoming patient requests submitted from Patient Profile:
- **Medical Records Requests**
  - view request details
  - set status: NEW / IN_REVIEW / COMPLETED / REJECTED (minimal)
- **Private Referral Requests**
  - view details
  - assign to a doctor
  - set status: NEW / ASSIGNED / APPROVED / DECLINED / COMPLETED
Acceptance:
- Requests are stored in DB and visible here
- Referral requests can be assigned to a doctor (doctor sees them in E4-S8)
- Status changes audited

**E5-S9 [OPTIONAL] Repeat Prescription Requests Triage**  
Description: Add a request workflow for repeat prescriptions:
- Patient submits request (simple form)
- Admin triages (approve/decline/assign to doctor)
- Doctor finalises prescription action
Acceptance:
- Status tracked and audited
- (Optional) Notification to patient on outcome

---

# EPIC 6 - Core Platform Hardening (Security + Data Integrity)

**E6-S1 [DONE] Password Hashing + Verification**  
Description: Implement secure hashing (bcrypt via passlib/bcrypt) and login verification.  
Acceptance: Passwords never stored in plain text.

**E6-S2 [DONE] Session Management + Logout**  
Description: Implement session keys (user_id, role, last_activity, etc.), and logout clears all.  
Acceptance: Session persists across navigation; logout resets state.

**E6-S3 [STARTED] Inactivity Timeout**  
Description: Enforce timeout based on last_activity.  
Acceptance: Idle session expires and requires re-login.

**E6-S4 [STARTED] RBAC Enforcement (Deny-by-default)**  
Description: Add require_role() guards in every protected page + sensitive services.  
Acceptance: Direct URL/page access cannot bypass role restrictions.

**E6-S5 [TODO] Forced Password Change on First Login**  
Description: If must_change_password=True, user is forced into password change flow before accessing portal.  
Acceptance:
- User cannot access dashboards until password updated
- Updates DB: new hash, must_change_password=False, timestamps

**E6-S6 [STARTED] Core Model Design**  
Description: Implement models:
- Users (role-based)
- Patients, Doctors
- Appointments (canonical)
- Bloodwork (draft/review/publish)
- Prescriptions
- Notifications
- AuditLogs  
Acceptance: Relationships exist; minimal required fields defined.

**E6-S7 [DONE] Alembic Setup + Initial Migration**  
Description: Configure Alembic and generate initial schema migration.  
Acceptance: Upgrade works from empty DB.

**E6-S8 [STARTED] Reliability Constraints + Indexes**  
Description: Add indexes for list pages + constraints for appointment reliability.  
Acceptance: Queries fast; integrity improved.

**E6-S9 [DONE] Repository Layer CRUD**  
Description: Repositories per entity: create/get/list/update; no business logic.  
Acceptance: Services can access DB cleanly.

**E6-S10 [STARTED] Service Layer Business Rules**  
Description: Services implement workflows (booking, publish, notifications, admin create accounts, etc.).  
Acceptance: Pages call services only.

**E6-S11 [TODO] Transaction Ownership in Services**  
Description: Services own transactions; repos do not auto-commit.  
Acceptance: multi-step actions are atomic (e.g., create appointment + audit).

---

# EPIC 7 - Audit Logging (Security & Accountability)

**E7-S1 [DONE] Audit Log Model**  
Description: AuditLog records actor, role, action, entity, timestamp, metadata JSON.  
Acceptance: Table exists + migration.

**E7-S2 [DONE] Audit Logging Service**  
Description: audit_service.log_action() used for: login events, account creation, bookings, cancellations, result publish, prescription changes.  
Acceptance: Consistent audit records written.

**E7-S3 [TODO] Admin Audit Viewer**  
Description: Admin UI to filter and view audit logs.  
Acceptance: Filters by date/action/user/entity.

---

# EPIC 8 - Testing & QA (After Features Exist)

**E8-S1 [DONE] Unit Test Foundations**  
Description: Add factories/helpers and baseline test setup.  
Acceptance: Easy to create test users/patients/doctors.

**E8-S2 [STARTED] Unit Tests: Auth + Password Change**  
Description: Test login, lockout, must_change_password flow, password update.  
Acceptance: Coverage for auth-critical logic.

**E8-S3 [STARTED] Unit Tests: Booking + Cancellation + Reschedule**  
Description: Test conflict checks and policy cutoffs.  
Acceptance: Reliability rules covered.

**E8-S4 [TODO] Unit Tests: Publish Results + Notification Send**  
Description: Test publish makes results visible; notification send creates correct record.  
Acceptance: Correctness + audit logging.

**E8-S5 [STARTED] Integration Tests (DB-backed)**  
Description: Test end-to-end flows against Postgres: login -> forced change -> booking -> doctor publish -> patient view.  
Acceptance: Runs locally + in CI.

---

# EPIC 9 - GitLab CI/CD Quality Gates

**E9-S1 [DONE] Choose Tooling (Lint/Format/Security)**  
Description: Standardise: formatter + linter + security scanner (one stack).  
Acceptance: Documented in README; consistent locally + CI.

**E9-S2 [DONE] CI Pipeline: Lint + Tests**  
Description: .gitlab-ci.yml stages:
- lint/format check
- pytest (unit + integration where feasible)  
Acceptance: pipeline blocks merge on failures.

**E9-S3 [DONE] CI Reports (Coverage)**  
Description: Add coverage report output and (optional) badge.  
Acceptance: Coverage visible per pipeline.

---

# EPIC 10 - Documentation + Non-Functional Requirements

**E10-S1 [TODO] README (Run, Seed, Demo Accounts)**  
Description: Docker run steps, env vars, seed scripts, demo accounts, troubleshooting.  
Acceptance: New dev can run in <10 mins.

**E10-S2 [TODO] Architecture Doc**  
Description: Explain layers, RBAC points, transactions, provisioning flow.  
Acceptance: Clear and consistent with code.

**E10-S3 [STARTED] Usability/Performance Pass**  
Description: Pagination on long lists; accessibility basics; consistent empty states.  
Acceptance: Feels like a real product; typical actions fast.

**E10-S4 [TODO] WCAG: Keyboard-operable Key Workflows**  
Description: Ensure key workflows can be completed with keyboard only (tabbing, enter/space activation, logical focus order):
- Login
- Booking flow
- Viewing results
- Viewing notifications
- Admin create account
Acceptance:
- Verified via manual checklist
- Any accessibility improvements documented

**E10-S5 [TODO] Performance Target: <3s Typical Actions + Pagination Definition**  
Description:
- Define "typical actions" and enforce pagination where needed (appointments list, audit logs, bloodwork history, notifications list).
- Add lightweight timing measurement (logs or in-app timing) for these actions.
Acceptance:
- Typical actions consistently under ~3 seconds in local docker environment with seeded demo data
- Pagination enabled on large lists

---

# EPIC 11 - Deployment, Observability & Operations (Optional / Final Hardening)

**E11-S1 [TODO] Deployment Target + Runbook**  
Description: Document hosting target, health checks, and rollback steps.  
Acceptance: Clear runbook for deploy and rollback.

**E11-S2 [TODO] Observability Basics**  
Description: Centralized logs + basic metrics (errors, response time).  
Acceptance: Logs and metrics visible in one place.

**E11-S3 [TODO] Data Privacy + Retention Notes**  
Description: Define retention policy, access logging, and privacy assumptions.  
Acceptance: DPIA-lite notes documented.

**E11-S4 [TODO] Backup + Restore Plan**  
Description: Postgres backup schedule and a tested restore procedure.  
Acceptance: Backup and restore steps documented and verified.

**E11-S5 [TODO] Release + Versioning**  
Description: Version tags and changelog update routine.  
Acceptance: Release process documented and repeatable.
