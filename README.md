# MedX AI

MedX AI is a local research-workstation prototype for organizing medical-imaging research workflows and integrating researcher-owned models and analysis pipelines. Its current application includes a Flask web interface, a REST API, a SQLAlchemy-backed research-record layer, and integration points for future model and analysis components.

> **Research prototype only.** MedX AI is not a medical device and is not for clinical diagnosis, treatment decisions, or patient care. Its output must not be interpreted as medical advice or medical certainty.

## Project status

The web application and database layer are present, but the AI research pipeline is not connected by default. Inference, calibration, uncertainty estimation, explainability, quantification, severity assessment, and evaluation are integration points and return an unavailable or not-configured response until researcher-owned implementations are connected and validated. No model weights, benchmarks, accuracy claims, or research results are included.

The current source tree does not contain an OpenCV image-processing pipeline or YOLO model/training implementation. Those components are not added or represented as completed functionality here.

## Current capabilities

- Flask web interface served from `templates/` and `static/`.
- API endpoints for service health, system telemetry, database status, and model connection status.
- Local image upload handling for PNG, JPEG, WEBP, and TIFF files, subject to the configured upload-size limit.
- SQLAlchemy models and repositories for research records.
- Draft experiment-record submission and result storage hooks.
- Extension points for researcher-provided prediction, calibration, uncertainty, explainability, quantification, severity, and evaluation code.

The model connection endpoint registers metadata; it does not load or run a trained model. The analysis and downstream research stages are not implemented end-to-end.

## Technology

- Python and Flask
- SQLAlchemy and SQLite for local development
- PyTorch and TorchVision for the existing system/model integration surface
- HTML, CSS, and vanilla JavaScript
- pytest for the existing test suite

Additional packages listed in `requirements.txt` are retained from the project. OpenCV and Ultralytics are not present in the current source implementation.

## Repository layout

```text
.
├── app.py                  # Flask application entry point
├── backend/                # API, configuration, and research integration points
├── database/               # SQLAlchemy setup, models, and repositories
├── models/                 # Location for researcher-provided model artifacts
├── results/                # Runtime result output (not committed)
├── static/                 # CSS and JavaScript assets
├── templates/              # Flask HTML templates
├── tests/                  # Automated tests
├── uploads/                # Runtime uploads (not committed)
├── DATABASE_README.md      # Database-layer notes
└── requirements.txt        # Python dependencies
```

Datasets, notebooks, and trained weights are not included. Dataset and model-artifact paths are ignored by Git; add only appropriately licensed, de-identified research materials through a separately approved data workflow.

## Installation

Use a supported Python installation and a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows, activate the environment with `.venv\Scripts\activate` and copy the template with `copy .env.example .env`. PyTorch installation requirements vary by operating system and hardware; consult the official PyTorch installation selector if the default package install does not match your environment.

Before running, set a unique local `SECRET_KEY` in `.env`. Do not commit `.env` or put credentials in source files.

## Run locally

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000). The development server binds to all network interfaces; keep it on a trusted local network and do not expose it publicly. This Flask development server is not suitable for production.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///medx_ai.db` | SQLAlchemy database connection |
| `SECRET_KEY` | `medx-research-prototype` | Flask session/signing key; replace locally |
| `MODEL_PATH` | `models/best.pt` | Researcher-provided model artifact path |
| `DEVICE` | `auto` | Model/runtime device setting |
| `MAX_UPLOAD_MB` | `20` | Maximum accepted upload request size |
| `DEBUG` | `false` | Flask debug mode |

Local databases, uploaded files, generated results, model weights, and `.env` files are excluded from Git. Use only synthetic or properly de-identified data in this prototype: the application does not provide authentication, access controls, or a clinical-grade privacy/security boundary.

## API overview

| Method | Endpoint | Current behavior |
| --- | --- | --- |
| `GET` | `/api/health` | Service status |
| `GET` | `/api/system` | Host and PyTorch/CUDA telemetry |
| `GET` | `/api/database` | Database connectivity/status |
| `GET` | `/api/model` | Model connection metadata/status |
| `POST` | `/api/model/connect` | Register model metadata; does not load weights |
| `POST` | `/api/model/reload` | Model reload hook |
| `POST` | `/api/upload` | Store an allowed image in the local uploads directory |
| `POST` | `/api/analyze` | Inference entry point; unavailable until an adapter is connected |
| `POST` | `/api/calibrate`, `/api/uncertainty`, `/api/xai`, `/api/quantification`, `/api/severity`, `/api/degrade` | Research-stage hooks; not configured by default |
| `GET` | `/api/results` | Stored result records |
| `GET` / `POST` | `/api/experiments` | List or save experiment records; advanced lifecycle is not implemented |

## Tests

```bash
python -m pytest
```

## Safety and licensing

This repository is for research software development, not clinical use. Validate any connected model and analysis pipeline independently before research use, and do not submit patient-identifiable information.

No `LICENSE` file is included. All rights remain with their respective owners; obtain permission before redistributing or reusing this project.
