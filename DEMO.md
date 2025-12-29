# CareLink - Jan 9 Interim Demo Guide

## Demo Accounts (Quick Login)

### Patient Account
- **Button**: "Login as Patient"
- **Mock User**: John Doe (ID: 1)
- **Access**: Patient dashboard, appointments, lab results, prescriptions, profile

### Doctor Account
- **Button**: "Login as Doctor"
- **Mock User**: Dr. Sarah Smith (ID: 2)
- **Specialty**: Cardiology
- **Access**: Doctor dashboard, appointments, lab results, prescriptions, profile

### Admin Account
- **Button**: "Login as Admin"
- **Mock User**: Admin User (ID: 3)
- **Access**: Admin dashboard, system-wide appointments, user management, analytics

---

## Demo Workflows (Part 2 of Video)

### Workflow 1: Doctor Lab Results Review & Publish (2-3 minutes)

**Purpose**: Demonstrate clinical workflow - doctor reviews results, adds interpretation, shares with patient

**Steps**:
1. **Login as Doctor** (Quick Login button)
2. Navigate to **"Lab Results"** from sidebar
3. Find pending result (status: "Pending Review")
4. Click to expand result details
5. Review lab values table (color-coded high/low/normal)
6. Add clinical interpretation in text area:
   - Example: "Glucose slightly elevated. Recommend dietary modifications and follow-up in 3 months."
7. Click **"Save Interpretation"** → Status changes to "Reviewed"
8. Click **"Share with Patient"** → Success message appears
9. **Logout**

10. **Login as Patient**
11. Navigate to **"Lab Results"**
12. Verify the shared result now appears in patient's view
13. Expand to see doctor's interpretation

**What This Proves**: Real workflow state management, role-based data visibility, clinical documentation

---

### Workflow 2: Patient Appointment Booking (2 minutes)

**Purpose**: Demonstrate patient self-service appointment scheduling

**Steps**:
1. **Login as Patient**
2. Navigate to **"My Appointments"** from sidebar
3. Click **"Schedule New Appointment"** button
4. Fill out appointment booking form:
   - **Doctor**: Select "Dr. Sarah Smith - Cardiology"
   - **Appointment Type**: "General Checkup"
   - **Date**: Tomorrow's date
   - **Time**: 10:00 AM
   - **Reason**: "Annual physical exam"
5. Click **"Submit Request"**
6. Success message: "Appointment request sent to Dr. Sarah Smith"
7. Verify new appointment appears in patient's appointment list
8. **Logout**

9. **Login as Doctor**
10. Navigate to **"Appointments"**
11. Verify patient's requested appointment appears in doctor's schedule

**What This Proves**: Form validation, data flow between roles, real-time updates (within session)

---

### Workflow 3: Prescription Refill Request & Approval (2-3 minutes)

**Purpose**: Demonstrate patient→doctor request workflow with approval cycle

**Steps**:
1. **Login as Patient**
2. Navigate to **"Prescriptions"** from sidebar
3. Find active prescription (e.g., "Lisinopril 10mg")
4. Click **"Request Refill"** button
5. Success message: "Refill request sent to Dr. Sarah Smith"
6. Verify prescription shows "Refill Pending" badge
7. **Logout**

8. **Login as Doctor**
9. Navigate to **"Prescriptions"**
10. Switch to **"Refill Requests"** tab
11. See patient's refill request listed
12. Click **"Approve"** button
13. Success message: "Refill approved and sent to pharmacy"
14. **Logout**

15. **Login as Patient**
16. Navigate to **"Prescriptions"**
17. Verify prescription now shows "Refill Approved" status

**What This Proves**: Bidirectional workflow, notification patterns, status state management

---

## Quick Navigation Reference

### Patient Portal
- 🏠 Dashboard - Overview stats, next appointment, quick actions
- 📅 My Appointments - View/filter appointments, schedule new
- 🧪 Lab Results - View shared results with doctor interpretations
- 💊 Prescriptions - View active prescriptions, request refills
- 👤 Profile - Personal info, security settings

### Doctor Portal
- 🏥 Dashboard - Today's schedule, pending tasks, patient summary
- 📅 Appointments - Manage schedule, book patient appointments
- 🧪 Lab Results - Review results, add interpretations, share with patients
- 💊 Prescriptions - View history, approve refill requests
- 👤 Profile - Professional info, credentials, availability

### Admin Portal
- 🎛️ Dashboard - System metrics, analytics charts, user management
- 📅 Appointments - System-wide view, bulk operations, analytics
- 👤 Profile - Admin settings, security

---

## Demo Tips

### What to Emphasize:
- ✅ **Professional UI/UX** - Healthcare-appropriate design, accessibility
- ✅ **Role-Based Access Control** - Different views for different roles
- ✅ **Real Workflows** - Not just static mockups, actual state changes
- ✅ **Form Validation** - Error prevention, user guidance
- ✅ **Consistent Design** - Reusable components, unified styling

### What to Avoid:
- ❌ Clicking "Export" or "View Calendar" buttons (still stubs)
- ❌ Trying to use traditional login form (use Quick Login only)
- ❌ Editing profile pages (save functionality not implemented)

### Talking Points:
- "This is a high-fidelity prototype demonstrating core clinical workflows"
- "Backend persistence is in progress - using comprehensive mock data for UX validation"
- "Focus of this demo is proving UI/UX design principles and role-based security"
- "Next sprint: SQLAlchemy ORM integration and real authentication"

---

## Technical Setup Before Demo

1. **Test all three workflows** at least twice
2. **Clear browser cache** to start fresh
3. **Have backup plan**: Local `streamlit run Home.py` if deployed app fails
4. **Screen recording ready**: OBS or Zoom configured
5. **Close unnecessary tabs/apps**: Clean screen for recording

---

## Timing Guide (20 minutes total)

- **Part 1 (5 min)**: GitLab repo, README, backlog, risks
- **Part 2 (10 min)**: System demo (3 workflows above)
- **Part 3 (5 min)**: Code structure, models, tests

Good luck! 🚀
