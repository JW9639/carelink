# CareLink - Testing Strategy & Documentation

**Version:** Jan 9, 2025 - MVP Demo Build  
**Status:** Development / Demo Phase  
**Last Updated:** Jan 9, 2025

---

## Overview

This document outlines the testing strategy for CareLink, including manual testing procedures for the Jan 9 demo, planned automated testing infrastructure, and quality assurance processes.

---

## Current Testing Status

### ✅ Manual Testing (Completed for Demo)

**Scope:** All 3 core demo workflows tested manually

**Test Environment:**
- Browser: Chrome 120+
- Python: 3.9+
- Streamlit: 1.29.0+
- OS: Windows 11

**Tests Performed:**
1. ✅ User authentication (patient, doctor, admin roles)
2. ✅ Lab results workflow (doctor review → share → patient view)
3. ✅ Appointment booking (patient request → doctor confirm)
4. ✅ Prescription refill (patient request → doctor approve)
5. ✅ Session state persistence across page navigation
6. ✅ UI rendering and responsiveness

### ❌ Automated Testing (Planned Post-Demo)

**Current Status:**
- pytest installed in requirements.txt
- No test files created yet
- No CI/CD pipeline
- **Code coverage: 0%**

**Target for Production:**
- Unit test coverage: 80%+
- Integration test coverage: 70%+
- E2E test coverage: 100% of critical workflows

---

## Manual Testing Procedures

### Pre-Demo Checklist

Run through this checklist **before the Jan 9 demo** to ensure all features work:

#### 1. Authentication & Navigation

- [ ] Login as patient (username: `john_doe`, password: `patient123`)
- [ ] Verify patient sidebar shows correct pages (Dashboard, Appointments, Lab Results, Prescriptions, Profile)
- [ ] Logout successfully
- [ ] Login as doctor (username: `dr_smith`, password: `doctor123`)
- [ ] Verify doctor sidebar shows correct pages
- [ ] Login as admin (username: `admin`, password: `admin123`)
- [ ] Verify admin sidebar shows correct pages

#### 2. Workflow 1: Lab Results

**Doctor Side:**
- [ ] Navigate to Doctor → Lab Results
- [ ] Find lab result with status "Pending Review"
- [ ] Click "Add Interpretation" and enter text
- [ ] Click "Save Interpretation" → status changes to "Reviewed"
- [ ] Click "Share with Patient" → status changes to "Shared with Patient"
- [ ] Verify success message appears

**Patient Side:**
- [ ] Logout, login as patient (`sarah_johnson`, `patient123`)
- [ ] Navigate to Patient → Lab Results
- [ ] Verify lab result appears with doctor's interpretation
- [ ] Verify color-coding (green for normal, red for abnormal)

#### 3. Workflow 2: Appointments

**Patient Side:**
- [ ] Navigate to Patient → Appointments
- [ ] Click "Book New Appointment"
- [ ] Fill form: Select doctor, date, time, type, reason
- [ ] Submit form
- [ ] Verify success message + balloons animation
- [ ] Verify new appointment appears with status "Pending"

**Doctor Side:**
- [ ] Logout, login as doctor (`dr_smith`, `doctor123`)
- [ ] Navigate to Doctor → Appointments
- [ ] Verify pending appointment appears in "Pending Requests" section
- [ ] Click "Confirm" → status changes to "Confirmed"
- [ ] Verify appointment moves to main calendar view

#### 4. Workflow 3: Prescription Refills

**Patient Side:**
- [ ] Navigate to Patient → Prescriptions
- [ ] Find prescription with refills remaining
- [ ] Click "Request Refill"
- [ ] Verify button changes to "Refill Pending" (orange badge)

**Doctor Side:**
- [ ] Logout, login as doctor (`dr_smith`, `doctor123`)
- [ ] Navigate to Doctor → Prescriptions
- [ ] Click "Refill Requests" tab
- [ ] Verify pending refill appears with 🔔 icon
- [ ] Click "✅ Approve"
- [ ] Verify success message + balloons animation
- [ ] Verify refill disappears from pending queue

**Patient Verification:**
- [ ] Logout, login as patient
- [ ] Navigate to Patient → Prescriptions
- [ ] Verify refill status shows "Approved" (green badge)

#### 5. Dashboard Views

**Patient Dashboard:**
- [ ] Verify statistics cards show correct counts
- [ ] Verify next appointment displays
- [ ] Verify recent messages display (3 max)
- [ ] Verify active prescriptions display (3 max)

**Doctor Dashboard:**
- [ ] Verify statistics cards (appointments, patients, pending labs)
- [ ] Verify upcoming appointments list

**Admin Dashboard:**
- [ ] Verify system statistics
- [ ] Verify "coming soon" messages for user management

#### 6. UI/UX Quality

- [ ] All buttons are clickable and responsive
- [ ] Color-coding is consistent (blue primary, green success, orange warning, red error)
- [ ] No broken layouts or overlapping text
- [ ] Custom CSS loads correctly
- [ ] No console errors in browser DevTools

---

## Demo Day Testing Protocol

### 30 Minutes Before Demo

1. **Fresh Start:**
   ```powershell
   # Stop any running Streamlit instances
   Get-Process | Where-Object {$_.Name -eq "streamlit"} | Stop-Process
   
   # Clear browser cache
   # Chrome: Ctrl+Shift+Delete → Clear last hour
   
   # Restart Streamlit
   cd "c:\Users\Jwill\Desktop\School\Full Year Project\carelink"
   streamlit run Home.py
   ```

2. **Smoke Test:**
   - Open http://localhost:8501
   - Login as patient → Verify dashboard loads
   - Login as doctor → Verify dashboard loads
   - Don't execute workflows (save for demo)

3. **Have Backup Ready:**
   - Streamlit Cloud URL: https://carelink-demo.streamlit.app (if deployed)
   - Backup laptop with same code
   - Screenshots of working workflows (plan B)

### During Demo

**Error Recovery:**
- If page crashes: Hit "Refresh" button, session state should persist
- If data disappears: Restart app, apologize, move to next section
- If browser freezes: Have backup browser tab open

---

## Automated Testing Plan (Post-Demo)

### Phase 1: Unit Tests (Week of Jan 16)

**Objective:** Test individual functions and data structures

#### Test Files to Create:

**`tests/test_mock_data.py`**
```python
"""Test mock data structure and integrity."""
import pytest
from database.mock_data import (
    MOCK_USERS, MOCK_APPOINTMENTS, MOCK_LAB_RESULTS, 
    MOCK_PRESCRIPTIONS, MOCK_MESSAGES
)

def test_mock_users_structure():
    """Verify all users have required fields."""
    required_fields = ["id", "username", "role", "name"]
    for user in MOCK_USERS:
        for field in required_fields:
            assert field in user, f"Missing {field} in user"

def test_lab_results_have_status():
    """Verify all lab results have review_status field."""
    for lab in MOCK_LAB_RESULTS:
        assert "review_status" in lab
        assert lab["review_status"] in ["Pending Review", "Reviewed", "Shared with Patient"]

def test_prescriptions_have_refill_status():
    """Verify all prescriptions have refill tracking."""
    for rx in MOCK_PRESCRIPTIONS:
        assert "refill_status" in rx
        assert "refills_remaining" in rx
```

**`tests/test_session_manager.py`**
```python
"""Test session management logic."""
import pytest
import streamlit as st
from services.session_manager import SessionManager

def test_init_session():
    """Verify session initialization creates required keys."""
    SessionManager.init_session()
    assert "authenticated" in st.session_state
    assert st.session_state.authenticated == False

def test_login_sets_state():
    """Verify login updates session state correctly."""
    SessionManager.login(
        user_id=1, 
        username="test_user", 
        role="patient", 
        name="Test Patient"
    )
    assert st.session_state.authenticated == True
    assert st.session_state.user_role == "patient"

def test_logout_clears_state():
    """Verify logout clears authentication."""
    SessionManager.login(1, "test", "patient", "Test")
    SessionManager.logout()
    assert st.session_state.authenticated == False
```

**`tests/test_workflows.py`**
```python
"""Test core workflow logic."""
import pytest
from database.mock_data import MOCK_LAB_RESULTS, MOCK_PRESCRIPTIONS

def test_lab_result_status_progression():
    """Verify lab result status can progress correctly."""
    lab = MOCK_LAB_RESULTS[0].copy()
    assert lab["review_status"] == "Pending Review"
    
    # Doctor adds interpretation
    lab["interpretation"] = "Results normal"
    lab["review_status"] = "Reviewed"
    assert lab["review_status"] == "Reviewed"
    
    # Doctor shares with patient
    lab["review_status"] = "Shared with Patient"
    assert lab["review_status"] == "Shared with Patient"

def test_prescription_refill_workflow():
    """Verify prescription refill status changes."""
    rx = MOCK_PRESCRIPTIONS[0].copy()
    assert rx["refill_status"] == "None"
    
    # Patient requests refill
    rx["refill_status"] = "Pending"
    rx["refill_requested"] = "2025-01-09"
    assert rx["refill_status"] == "Pending"
    
    # Doctor approves
    rx["refill_status"] = "Approved"
    rx["refills_remaining"] -= 1
    assert rx["refill_status"] == "Approved"
    assert rx["refills_remaining"] == 2
```

### Phase 2: Integration Tests (Week of Jan 23)

**Objective:** Test interactions between components

**Tools:**
- pytest-streamlit (if available)
- Selenium for UI testing

**Example Tests:**
- Navigate from login → dashboard → appointments
- Submit appointment booking form → verify data persists
- Login as different roles → verify correct pages visible

### Phase 3: End-to-End Tests (Week of Jan 30)

**Objective:** Test complete user journeys

**Tools:**
- Playwright or Cypress
- Automated browser testing

**Test Scenarios:**
1. **Full Lab Results Workflow:**
   - Login as doctor
   - Navigate to lab results
   - Add interpretation
   - Share with patient
   - Logout
   - Login as patient
   - Navigate to lab results
   - Verify interpretation visible

2. **Full Appointment Booking:**
   - Login as patient
   - Book appointment
   - Logout
   - Login as doctor
   - Confirm appointment
   - Logout
   - Login as patient
   - Verify confirmed status

3. **Full Prescription Refill:**
   - Login as patient
   - Request refill
   - Logout
   - Login as doctor
   - Approve refill
   - Logout
   - Login as patient
   - Verify approved status

### Phase 4: CI/CD Pipeline (Feb 2025)

**GitHub Actions Workflow:**
```yaml
name: CareLink Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/ --cov=. --cov-report=html
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Quality Gates:**
- All tests must pass before merge
- Code coverage must be 80%+
- No high-severity linting errors

---

## Test Data Management

### Mock Data for Testing

**Current Approach:**
- `database/mock_data.py` contains all test data
- Data includes various scenarios (pending, confirmed, denied, etc.)
- Session state used for workflow testing

**Future Approach (With Database):**
- Create `database/seed_test_data.py` for test database
- Use database transactions for test isolation
- Reset database after each test run

**Test Accounts:**
| Username | Password | Role | Purpose |
|----------|----------|------|---------|
| john_doe | patient123 | patient | General patient testing |
| sarah_johnson | patient123 | patient | Secondary patient (has shared labs) |
| dr_smith | doctor123 | doctor | General doctor testing |
| admin | admin123 | admin | Admin testing |

---

## Bug Tracking

### Known Issues (Jan 9, 2025)

| ID | Severity | Description | Status | Workaround |
|----|----------|-------------|--------|------------|
| BUG-001 | Low | Page refresh loses session state | Known | Don't refresh during demo |
| BUG-002 | Low | "Coming soon" buttons on dashboards | By Design | Clearly communicate in demo |
| BUG-003 | Medium | No input validation on appointment dates | Accepted | Use valid dates in demo |

### Future Testing

**When to Add Tests:**
- Before every new feature (TDD approach)
- After every bug fix (regression prevention)
- Before every release (quality gate)

**Test Coverage Goals:**
| Component | Current | Target | Timeline |
|-----------|---------|--------|----------|
| database/mock_data.py | 0% | 90% | Week 1 |
| services/session_manager.py | 0% | 95% | Week 1 |
| services/auth_service.py | 0% | 90% | Week 2 |
| components/*.py | 0% | 80% | Week 3 |
| pages/*.py | 0% | 70% | Week 4 |

---

## Performance Testing

### Load Testing (Future)

**Not Required for Demo, Critical for Production:**

**Tools:** Locust, JMeter

**Scenarios:**
- 100 concurrent users browsing dashboards
- 50 concurrent appointment bookings
- Database query performance with 10,000+ records

**Targets:**
- Page load time: < 2 seconds
- Form submission: < 1 second
- Database query: < 500ms

---

## Accessibility Testing

### WCAG 2.1 Compliance (Future)

**Tools:**
- axe DevTools
- WAVE browser extension
- Screen reader testing (NVDA, JAWS)

**Requirements for Production:**
- All interactive elements keyboard accessible
- Proper ARIA labels
- Color contrast ratio 4.5:1 minimum
- Focus indicators visible

---

## Security Testing

### Penetration Testing (Future)

**Not Required for Demo, Critical for Production:**

**Tests:**
- SQL injection attempts
- XSS (cross-site scripting) vulnerabilities
- CSRF (cross-site request forgery) protection
- Session hijacking prevention
- Password strength enforcement

---

## Testing Checklist Summary

### ✅ Jan 9 Demo (Completed)
- [x] Manual testing of 3 core workflows
- [x] Browser compatibility check (Chrome)
- [x] UI/UX visual inspection
- [x] Session state persistence verification

### ⏳ Week of Jan 16 (Post-Demo)
- [ ] Create tests/ directory
- [ ] Write unit tests (mock_data, session_manager)
- [ ] Run pytest successfully
- [ ] Set up code coverage reporting

### ⏳ Week of Jan 23
- [ ] Integration tests for workflows
- [ ] UI testing with Selenium
- [ ] Test database integration (once connected)

### ⏳ February 2025
- [ ] End-to-end test suite
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Achieve 80%+ code coverage

### ⏳ March 2025 (Pre-Production)
- [ ] Security testing
- [ ] Performance testing
- [ ] Accessibility audit
- [ ] HIPAA compliance verification

---

## Contact

For questions about testing procedures:
- **Technical Lead:** [Your Name]
- **Last Updated:** Jan 9, 2025
- **Next Review:** Jan 16, 2025 (post-demo)
