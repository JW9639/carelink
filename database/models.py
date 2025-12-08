"""Database models and schemas."""

class User:
    """User model for patients, doctors, and admins."""
    def __init__(self, user_id, name, role, email, phone):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.email = email
        self.phone = phone

class Patient(User):
    """Patient model extending User."""
    def __init__(self, user_id, name, email, phone, dob, address):
        super().__init__(user_id, name, "patient", email, phone)
        self.dob = dob
        self.address = address

class Doctor(User):
    """Doctor model extending User."""
    def __init__(self, user_id, name, email, phone, specialty, license):
        super().__init__(user_id, name, "doctor", email, phone)
        self.specialty = specialty
        self.license = license

class Appointment:
    """Appointment model."""
    def __init__(self, appointment_id, patient_id, doctor_id, date, time, type, status):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.type = type
        self.status = status

class MedicalRecord:
    """Medical record model."""
    def __init__(self, record_id, patient_id, date, diagnosis, doctor, notes):
        self.record_id = record_id
        self.patient_id = patient_id
        self.date = date
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.notes = notes
