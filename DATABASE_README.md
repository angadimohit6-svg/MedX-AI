# MedX AI Database Layer

This project now includes a dedicated database layer for persistent storage of medical research records and externally generated outputs.

## Database technology

- SQLAlchemy ORM
- SQLite for local development
- PostgreSQL-compatible schema design for future migration
- Environment-driven configuration

## Local configuration

Copy the example environment file and update it if needed:

```bash
cp .env.example .env
```

Example:

```env
DATABASE_URL=sqlite:///medx_ai.db
SECRET_KEY=medx-research-prototype
```

## Initialization

```python
from database import init_db

init_db()
```

## Demo data

```python
from database.seed import seed_demo_data

seed_demo_data()
```

## Main entities

- Patient
- PatientHistory
- Examination
- MedicalImage
- Prediction
- AnalysisResult
- Report
- Experiment
- ExperimentMetric
- ModelRegistry
- AuditLog

## Notes

This database layer stores results generated elsewhere and does not implement AI or medical inference logic.

## Backup and restore

SQLite:

```bash
cp medx_ai.db medx_ai_backup.db
```

Restore:

```bash
cp medx_ai_backup.db medx_ai.db
```

For PostgreSQL, use native dump/restore tooling such as `pg_dump` and `pg_restore`.

Remember that image/report files stored outside the database also need to be backed up separately.
