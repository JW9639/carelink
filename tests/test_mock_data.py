"""Test mock data structure and integrity.

These tests verify that mock data has the correct structure and required fields
for all workflows (lab results, appointments, prescriptions, messages).

NOTE: These tests are written for the CURRENT mock_data.py structure.
MOCK_USERS is a dict (not list), lab results use "ordered_by" (not "doctor_name"), etc.
"""

import pytest
from database.mock_data import (
    MOCK_USERS,
    MOCK_APPOINTMENTS,
    MOCK_LAB_RESULTS,
    MOCK_PRESCRIPTIONS,
    MOCK_MESSAGES,
    MOCK_MEDICAL_RECORDS,
    MOCK_STATS
)


class TestMockUsers:
    """Test MOCK_USERS data structure."""
    
    def test_users_exist(self):
        """Verify mock users dictionary is defined."""
        assert len(MOCK_USERS) > 0, "MOCK_USERS should not be empty"
    
    def test_user_roles_present(self):
        """Verify all required roles exist in MOCK_USERS."""
        required_roles = ["patient", "doctor", "admin"]
        
        for role in required_roles:
            assert role in MOCK_USERS, f"Missing role: {role}"
    
    def test_user_required_fields(self):
        """Verify each user has required fields."""
        required_fields = ["id", "name", "role", "email"]
        
        for role, user in MOCK_USERS.items():
            for field in required_fields:
                assert field in user, f"{role} user missing field: {field}"


class TestMockAppointments:
    """Test MOCK_APPOINTMENTS data structure."""
    
    def test_appointments_exist(self):
        """Verify appointments are defined."""
        assert len(MOCK_APPOINTMENTS) > 0, "MOCK_APPOINTMENTS should not be empty"
    
    def test_appointment_required_fields(self):
        """Verify all appointments have required fields."""
        required_fields = ["id", "patient_name", "doctor_name", "date", "time", "type", "status"]
        
        for appointment in MOCK_APPOINTMENTS:
            for field in required_fields:
                assert field in appointment, f"Appointment missing field: {field}"
    
    def test_appointment_status_valid(self):
        """Verify appointment statuses are valid."""
        valid_statuses = ["Pending", "Confirmed", "Cancelled", "Completed"]
        
        for appointment in MOCK_APPOINTMENTS:
            assert appointment["status"] in valid_statuses, f"Invalid status: {appointment['status']}"


class TestMockLabResults:
    """Test MOCK_LAB_RESULTS data structure."""
    
    def test_lab_results_exist(self):
        """Verify lab results are defined."""
        assert len(MOCK_LAB_RESULTS) > 0, "MOCK_LAB_RESULTS should not be empty"
    
    def test_lab_result_required_fields(self):
        """Verify all lab results have required fields."""
        required_fields = ["id", "patient_name", "date", "review_status"]
        
        for lab in MOCK_LAB_RESULTS:
            for field in required_fields:
                assert field in lab, f"Lab result missing field: {field}"
    
    def test_lab_result_status_valid(self):
        """Verify lab result statuses are valid."""
        valid_statuses = ["Pending Review", "Reviewed", "Shared with Patient"]
        
        for lab in MOCK_LAB_RESULTS:
            assert lab["review_status"] in valid_statuses, f"Invalid review_status: {lab['review_status']}"
    
    def test_lab_result_values_have_status(self):
        """Verify lab result values have status indicators."""
        for lab in MOCK_LAB_RESULTS:
            if "values" in lab:
                for value in lab["values"]:
                    assert "status" in value, "Lab value missing status field"
                    assert value["status"] in ["Normal", "Low", "High"], f"Invalid value status: {value['status']}"
    
    def test_reviewed_labs_have_interpretation(self):
        """Verify reviewed/shared labs have interpretation field."""
        for lab in MOCK_LAB_RESULTS:
            if lab["review_status"] in ["Reviewed", "Shared with Patient"]:
                assert "interpretation" in lab, f"Reviewed lab {lab['id']} missing interpretation"


class TestMockPrescriptions:
    """Test MOCK_PRESCRIPTIONS data structure."""
    
    def test_prescriptions_exist(self):
        """Verify prescriptions are defined."""
        assert len(MOCK_PRESCRIPTIONS) > 0, "MOCK_PRESCRIPTIONS should not be empty"
    
    def test_prescription_required_fields(self):
        """Verify all prescriptions have required fields."""
        required_fields = ["id", "patient_name", "medication", "dosage", "status"]
        
        for rx in MOCK_PRESCRIPTIONS:
            for field in required_fields:
                assert field in rx, f"Prescription missing field: {field}"
    
    def test_prescription_status_valid(self):
        """Verify prescription statuses are valid."""
        valid_statuses = ["Active", "Completed", "Cancelled"]
        
        for rx in MOCK_PRESCRIPTIONS:
            assert rx["status"] in valid_statuses, f"Invalid status: {rx['status']}"
    
    def test_prescription_refill_fields(self):
        """Verify prescriptions have refill tracking fields."""
        required_refill_fields = ["refill_status", "refills_remaining"]
        
        for rx in MOCK_PRESCRIPTIONS:
            for field in required_refill_fields:
                assert field in rx, f"Prescription missing refill field: {field}"
    
    def test_prescription_refill_status_valid(self):
        """Verify refill statuses are valid."""
        valid_refill_statuses = ["None", "Pending", "Approved", "Denied"]
        
        for rx in MOCK_PRESCRIPTIONS:
            assert rx["refill_status"] in valid_refill_statuses, f"Invalid refill_status: {rx['refill_status']}"
    
    def test_refills_remaining_valid(self):
        """Verify refills_remaining is a non-negative integer."""
        for rx in MOCK_PRESCRIPTIONS:
            assert isinstance(rx["refills_remaining"], int), "refills_remaining must be integer"
            assert rx["refills_remaining"] >= 0, "refills_remaining cannot be negative"


class TestMockMessages:
    """Test MOCK_MESSAGES data structure."""
    
    def test_messages_exist(self):
        """Verify messages are defined."""
        assert len(MOCK_MESSAGES) > 0, "MOCK_MESSAGES should not be empty"
    
    def test_message_required_fields(self):
        """Verify all messages have required fields."""
        required_fields = ["id", "subject", "date", "read"]
        
        for msg in MOCK_MESSAGES:
            for field in required_fields:
                assert field in msg, f"Message missing field: {field}"
    
    def test_message_read_status_boolean(self):
        """Verify message read status is boolean."""
        for msg in MOCK_MESSAGES:
            assert isinstance(msg["read"], bool), "Message 'read' field must be boolean"


class TestMockMedicalRecords:
    """Test MOCK_MEDICAL_RECORDS data structure."""
    
    def test_medical_records_exist(self):
        """Verify medical records are defined."""
        assert len(MOCK_MEDICAL_RECORDS) > 0, "MOCK_MEDICAL_RECORDS should not be empty"
    
    def test_medical_record_required_fields(self):
        """Verify all medical records have required fields."""
        required_fields = ["id", "date", "diagnosis"]
        
        for record in MOCK_MEDICAL_RECORDS:
            for field in required_fields:
                assert field in record, f"Medical record missing field: {field}"


class TestMockStats:
    """Test MOCK_STATS data structure."""
    
    def test_stats_roles_exist(self):
        """Verify stats exist for all roles."""
        required_roles = ["patient", "doctor", "admin"]
        
        for role in required_roles:
            assert role in MOCK_STATS, f"MOCK_STATS missing role: {role}"
    
    def test_patient_stats_fields(self):
        """Verify patient stats have required fields."""
        required_fields = ["upcoming_appointments", "active_prescriptions", "unread_messages"]
        
        for field in required_fields:
            assert field in MOCK_STATS["patient"], f"Patient stats missing field: {field}"
    
    def test_doctor_stats_fields(self):
        """Verify doctor stats have required fields."""
        required_fields = ["patients_total", "pending_reviews"]
        
        for field in required_fields:
            assert field in MOCK_STATS["doctor"], f"Doctor stats missing field: {field}"
    
    def test_admin_stats_fields(self):
        """Verify admin stats have required fields."""
        required_fields = ["pending_approvals", "today_appointments"]
        
        for field in required_fields:
            assert field in MOCK_STATS["admin"], f"Admin stats missing field: {field}"


class TestWorkflowIntegrity:
    """Test workflow data integrity for demo scenarios."""
    
    def test_pending_labs_exist(self):
        """Verify at least one lab result is pending review (for demo)."""
        pending_labs = [lab for lab in MOCK_LAB_RESULTS if lab["review_status"] == "Pending Review"]
        assert len(pending_labs) > 0, "At least one lab result should be pending for demo"
    
    def test_shared_labs_exist(self):
        """Verify at least one lab result is shared with patient (for demo)."""
        shared_labs = [lab for lab in MOCK_LAB_RESULTS if lab["review_status"] == "Shared with Patient"]
        assert len(shared_labs) > 0, "At least one lab result should be shared for demo"
    
    def test_prescriptions_have_refillable_items(self):
        """Verify at least one prescription has refills remaining (for demo)."""
        refillable = [rx for rx in MOCK_PRESCRIPTIONS if rx["refills_remaining"] > 0 and rx["status"] == "Active"]
        assert len(refillable) > 0, "At least one prescription should have refills remaining for demo"
    
    def test_confirmed_appointments_exist(self):
        """Verify at least one confirmed appointment exists."""
        confirmed = [apt for apt in MOCK_APPOINTMENTS if apt["status"] == "Confirmed"]
        assert len(confirmed) > 0, "At least one confirmed appointment should exist"


# Run tests with: pytest tests/test_mock_data.py -v

