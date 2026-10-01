# CVTS Dashboard

A simple Python and Flask dashboard.

CVTS Operations Dashboard

## Run locally

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open the local address shown in the Flask startup output.

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
$env:SYNCHROTEAM_LIST_URL = 'YOUR_PRIVATE_JOB_LIST_ENDPOINT'
$env:SYNCHROTEAM_USERNAME = 'cvtitsolutions'
$env:SYNCHROTEAM_PASSWORD = 'YOUR_PASSWORD'
python app.py
```

You can filter the list to one job by adding a `job_id` query parameter to the dashboard address. The raw response is available from the jobs API route.

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/16a90e03-e79c-48d7-b937-d9c0c3ae3915" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/4d6d6887-3786-4b6a-8c68-a558001af562" />


