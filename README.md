# CVTS Dashboard

A simple Python and Flask dashboard.

## Run locally

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## File guide

- `app.py`: Flask routes and application startup.
- `data/dashboard_data.py`: Dashboard data and calculations.
- `templates/dashboard.html`: Main page layout.
- `templates/partials/`: Small reusable template sections.
- `static/css/dashboard.css`: All dashboard styling.
- `static/js/dashboard.js`: Small browser interactions.

## Synchroteam connection

The dashboard loads jobs from the Synchroteam list endpoint. Copy `.env.example` to `.env` and set the credentials before starting Flask:

```powershell
$env:SYNCHROTEAM_LIST_URL = 'https://cvtitsolutions.synchroteam.com/api/v3/job/list'
$env:SYNCHROTEAM_USERNAME = 'cvtitsolutions'
$env:SYNCHROTEAM_PASSWORD = 'YOUR_PASSWORD'
python app.py
```

You can filter the list to one job with `http://127.0.0.1:5000/?job_id=YOUR_JOB_ID`.
The raw response is available at `/api/jobs/YOUR_JOB_ID`.

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
