"""Smoke tests to ensure modules import successfully."""


def test_module_imports():
    import app.main  # noqa: F401
    import app.config  # noqa: F401
    import app.db.session  # noqa: F401
    import app.db.base  # noqa: F401
    import app.security.auth  # noqa: F401
    import app.security.rbac  # noqa: F401
    import app.security.session_manager  # noqa: F401
    import app.security.audit  # noqa: F401
    import app.ui.theme  # noqa: F401
    import app.services.auth_service  # noqa: F401
    import app.services.patient_service  # noqa: F401
    import app.services.doctor_service  # noqa: F401
    import app.services.appointment_service  # noqa: F401
    import app.services.notification_service  # noqa: F401
    import app.services.admin_service  # noqa: F401
    import app.pages  # noqa: F401
    import app.pages.patient.Dashboard  # noqa: F401
    import app.pages.doctor.Dashboard  # noqa: F401
    import app.pages.admin.Dashboard  # noqa: F401


def test_apply_theme():
    from app.ui.theme import apply_theme

    apply_theme()
