"""Mock data for development and testing."""

# Mock users for login testing
MOCK_USERS = {
    "patient": {
        "id": "P001",
        "name": "John Smith",
        "role": "patient",
        "email": "john.smith@email.com",
        "phone": "(555) 123-4567",
        "dob": "1985-03-15",
        "address": "123 Main St, City, State 12345"
    },
    "doctor": {
        "id": "D001",
        "name": "Dr. Sarah Johnson",
        "role": "doctor",
        "email": "dr.johnson@medicare.com",
        "phone": "(555) 987-6543",
        "specialty": "Cardiology",
        "license": "MD-12345"
    },
    "admin": {
        "id": "A001",
        "name": "Admin User",
        "role": "admin",
        "email": "admin@medicare.com",
        "phone": "(555) 000-0000",
        "department": "System Administration"
    }
}

# Mock appointments
MOCK_APPOINTMENTS = [
    {
        "id": "APT001",
        "patient_id": "P001",
        "patient_name": "John Smith",
        "doctor_id": "D001",
        "doctor_name": "Dr. Sarah Johnson",
        "date": "2025-12-10",
        "time": "10:00 AM",
        "type": "Check-up",
        "status": "Confirmed",
        "notes": "Annual physical examination"
    },
    {
        "id": "APT002",
        "patient_id": "P002",
        "patient_name": "Jane Doe",
        "doctor_id": "D001",
        "doctor_name": "Dr. Sarah Johnson",
        "date": "2025-12-10",
        "time": "11:00 AM",
        "type": "Follow-up",
        "status": "Confirmed",
        "notes": "Follow-up for blood pressure"
    },
    {
        "id": "APT003",
        "patient_id": "P001",
        "patient_name": "John Smith",
        "doctor_id": "D002",
        "doctor_name": "Dr. Michael Chen",
        "date": "2025-12-15",
        "time": "2:00 PM",
        "type": "Consultation",
        "status": "Pending",
        "notes": "Initial consultation"
    }
]

# Mock medical records
MOCK_MEDICAL_RECORDS = [
    {
        "id": "MR001",
        "patient_id": "P001",
        "date": "2025-11-20",
        "diagnosis": "Annual Physical Examination",
        "doctor": "Dr. Sarah Johnson",
        "notes": "Patient in good health. Blood pressure: 120/80. Weight: 175 lbs. No concerns noted.",
        "prescriptions": ["Multivitamin daily"],
        "follow_up": "1 year"
    },
    {
        "id": "MR002",
        "patient_id": "P001",
        "date": "2025-10-05",
        "diagnosis": "Common Cold",
        "doctor": "Dr. Michael Chen",
        "notes": "Patient presented with mild cold symptoms. Prescribed rest and fluids. Temperature: 99.2°F.",
        "prescriptions": ["Acetaminophen as needed"],
        "follow_up": "As needed"
    },
    {
        "id": "MR003",
        "patient_id": "P001",
        "date": "2025-08-15",
        "diagnosis": "Routine Blood Work",
        "doctor": "Dr. Sarah Johnson",
        "notes": "All blood work results normal. Cholesterol levels within healthy range.",
        "prescriptions": [],
        "follow_up": "6 months"
    }
]

# Mock prescriptions
MOCK_PRESCRIPTIONS = [
    {
        "id": "RX001",
        "patient_id": "P001",
        "medication": "Lisinopril 10mg",
        "dosage": "Once daily",
        "prescribed_by": "Dr. Sarah Johnson",
        "date": "2025-11-20",
        "refills": 3,
        "instructions": "Take with water in the morning"
    },
    {
        "id": "RX002",
        "patient_id": "P001",
        "medication": "Multivitamin",
        "dosage": "Once daily",
        "prescribed_by": "Dr. Sarah Johnson",
        "date": "2025-11-20",
        "refills": 6,
        "instructions": "Take with food"
    }
]

# Mock lab results
MOCK_LAB_RESULTS = [
    {
        "id": "LAB001",
        "patient_id": "P001",
        "date": "2025-11-19",
        "test_type": "Complete Blood Count",
        "results": {
            "White Blood Cells": "7.5 K/uL (Normal)",
            "Red Blood Cells": "5.0 M/uL (Normal)",
            "Hemoglobin": "15.2 g/dL (Normal)",
            "Platelets": "250 K/uL (Normal)"
        },
        "status": "Completed",
        "ordered_by": "Dr. Sarah Johnson"
    },
    {
        "id": "LAB002",
        "patient_id": "P001",
        "date": "2025-11-19",
        "test_type": "Lipid Panel",
        "results": {
            "Total Cholesterol": "185 mg/dL (Normal)",
            "LDL": "110 mg/dL (Normal)",
            "HDL": "55 mg/dL (Normal)",
            "Triglycerides": "100 mg/dL (Normal)"
        },
        "status": "Completed",
        "ordered_by": "Dr. Sarah Johnson"
    }
]

# Mock statistics for dashboards
MOCK_STATS = {
    "patient": {
        "upcoming_appointments": 2,
        "active_prescriptions": 2,
        "unread_messages": 3,
        "pending_bills": 1,
        "last_visit": "2025-11-20",
        "next_appointment": "2025-12-10"
    },
    "doctor": {
        "today_appointments": 8,
        "pending_reviews": 5,
        "new_messages": 12,
        "patients_total": 145,
        "completed_today": 3,
        "upcoming_today": 5
    },
    "admin": {
        "total_patients": 1250,
        "total_doctors": 45,
        "total_staff": 120,
        "today_appointments": 87,
        "pending_approvals": 12,
        "active_prescriptions": 3450,
        "system_uptime": "99.9%"
    }
}

# Mock patient list for doctors
MOCK_PATIENTS = [
    {
        "id": "P001",
        "name": "John Smith",
        "age": 39,
        "gender": "Male",
        "last_visit": "2025-11-20",
        "status": "Active",
        "primary_doctor": "Dr. Sarah Johnson"
    },
    {
        "id": "P002",
        "name": "Jane Doe",
        "age": 45,
        "gender": "Female",
        "last_visit": "2025-11-18",
        "status": "Active",
        "primary_doctor": "Dr. Sarah Johnson"
    },
    {
        "id": "P003",
        "name": "Robert Johnson",
        "age": 52,
        "gender": "Male",
        "last_visit": "2025-11-15",
        "status": "Follow-up",
        "primary_doctor": "Dr. Sarah Johnson"
    },
    {
        "id": "P004",
        "name": "Mary Williams",
        "age": 38,
        "gender": "Female",
        "last_visit": "2025-11-10",
        "status": "Active",
        "primary_doctor": "Dr. Sarah Johnson"
    }
]

# Mock messages
MOCK_MESSAGES = [
    {
        "id": "MSG001",
        "from": "Dr. Sarah Johnson",
        "to": "John Smith",
        "subject": "Lab Results Available",
        "message": "Your recent lab results are available. All values are within normal range.",
        "date": "2025-12-07",
        "read": False
    },
    {
        "id": "MSG002",
        "from": "Billing Department",
        "to": "John Smith",
        "subject": "Payment Reminder",
        "message": "You have a pending balance of $150 from your last visit.",
        "date": "2025-12-05",
        "read": False
    },
    {
        "id": "MSG003",
        "from": "MediCare System",
        "to": "John Smith",
        "subject": "Appointment Confirmation",
        "message": "Your appointment on Dec 10, 2025 at 10:00 AM has been confirmed.",
        "date": "2025-12-03",
        "read": True
    }
]
