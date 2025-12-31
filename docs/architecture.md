# Architecture Overview

CareLink uses a Streamlit frontend backed by a PostgreSQL database. SQLAlchemy
2.0 models live in `app/models` with shared metadata in `app/db/base.py`.
Configuration comes from Pydantic settings in `app/config.py`, and Alembic
handles migrations from `migrations/`.

Security is layered through bcrypt hashing, session state management in
`app/security/session_manager.py`, RBAC in `app/security/rbac.py`, and audit
logging in `app/security/audit.py`.

## Authentication Flow

```
[Login Page: Home.py] -> [Auth Service] -> [Database]
        |                    |              |
        v                    v              v
    [Verify Hash]     [Update Login]     [User Data]
        |                                   |
        v                                   v
    [Session State] <-> [Role Router] -> [Dashboard by role]
```

### Session Management

- Sessions stored in Streamlit's `st.session_state`
- Timeout: 15 minutes of inactivity
- Tracked fields: `user`, `role`, `is_authenticated`, `last_activity`
