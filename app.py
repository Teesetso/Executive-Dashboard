import os
from urllib.parse import urlparse

from dotenv import load_dotenv, set_key
from flask import Flask, jsonify, render_template, request

from data.dashboard_data import PERIODS, build_dashboard
from services.synchroteam import (
    SynchroteamError,
    get_customers,
    get_jobs,
    get_job,
    get_sites,
    normalize_customer,
    normalize_job,
    normalize_site,
)

load_dotenv()
app = Flask(__name__)
ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')
VIEWS = {'overview': 'Overview', 'jobs': 'Jobs', 'customers': 'Customers', 'sites': 'Sites', 'reports': 'Reports', 'settings': 'Settings', 'help': 'Help center'}


@app.get('/')
def dashboard():
    period = request.args.get('period', PERIODS[0])
    if period not in PERIODS:
        period = PERIODS[0]
    job_id = request.args.get('job_id') or os.getenv('SYNCHROTEAM_JOB_ID')
    view = request.args.get('view', 'overview')
    if view not in VIEWS:
        view = 'overview'
    jobs = []
    customers = []
    sites = []
    error = 'Enter a Synchroteam job ID to load live data.'
    if view == 'customers':
        try:
            customers = [normalize_customer(customer) for customer in get_customers()]
            error = None
        except SynchroteamError as exc:
            error = str(exc)
    elif view == 'sites':
        try:
            sites = [normalize_site(site) for site in get_sites()]
            error = None
        except SynchroteamError as exc:
            error = str(exc)
    elif os.getenv('SYNCHROTEAM_LIST_URL'):
        try:
            jobs = [normalize_job(job) for job in get_jobs()]
            if job_id:
                jobs = [job for job in jobs if job['id'] == job_id or str(job['number']) == job_id]
            error = None
        except SynchroteamError as exc:
            error = str(exc)
    elif job_id:
        try:
            jobs = [normalize_job(get_job(job_id))]
            error = None
        except SynchroteamError as exc:
            error = str(exc)
    config = {
        'job_endpoint': os.getenv('SYNCHROTEAM_JOB_URL', 'https://cvtitsolutions.synchroteam.com/api/v3/job/details'),
        'customer_endpoint': os.getenv('SYNCHROTEAM_CUSTOMER_LIST_URL', 'https://cvtitsolutions.synchroteam.com/api/v3/customer/list'),
        'site_endpoint': os.getenv('SYNCHROTEAM_SITE_LIST_URL', 'https://cvtitsolutions.synchroteam.com/api/v3/site/list'),
        'auth_status': 'Configured' if (os.getenv('SYNCHROTEAM_AUTHORIZATION') or (os.getenv('SYNCHROTEAM_USERNAME') and os.getenv('SYNCHROTEAM_PASSWORD'))) else 'Not configured',
    }
    return render_template('dashboard.html', job_id=job_id or '', view=view, views=VIEWS, customers=customers, sites=sites, config=config, **build_dashboard(period, jobs, error))


@app.post('/settings')
def save_settings():
    endpoint_keys = ('SYNCHROTEAM_JOB_URL', 'SYNCHROTEAM_CUSTOMER_LIST_URL', 'SYNCHROTEAM_SITE_LIST_URL')
    endpoint_values = {key: request.form.get(key, '').strip() for key in endpoint_keys}
    if any(urlparse(value).scheme not in ('http', 'https') or not urlparse(value).netloc for value in endpoint_values.values()):
        return render_template('dashboard.html', job_id='', view='settings', views=VIEWS, customers=[], sites=[], config={
            'job_endpoint': endpoint_values['SYNCHROTEAM_JOB_URL'],
            'customer_endpoint': endpoint_values['SYNCHROTEAM_CUSTOMER_LIST_URL'],
            'site_endpoint': endpoint_values['SYNCHROTEAM_SITE_LIST_URL'],
            'auth_status': 'Configured' if (os.getenv('SYNCHROTEAM_AUTHORIZATION') or (os.getenv('SYNCHROTEAM_USERNAME') and os.getenv('SYNCHROTEAM_PASSWORD'))) else 'Not configured',
        }, **build_dashboard(PERIODS[0], [], 'Enter valid http or https URLs for all endpoints.'))
    for key, value in endpoint_values.items():
        os.environ[key] = value
        set_key(ENV_FILE, key, value)
    return render_template('dashboard.html', job_id='', view='settings', views=VIEWS, customers=[], sites=[], config={
        'job_endpoint': endpoint_values['SYNCHROTEAM_JOB_URL'],
        'customer_endpoint': endpoint_values['SYNCHROTEAM_CUSTOMER_LIST_URL'],
        'site_endpoint': endpoint_values['SYNCHROTEAM_SITE_LIST_URL'],
        'auth_status': 'Configured',
    }, **build_dashboard(PERIODS[0], [], None))


@app.get('/api/jobs/<path:job_id>')
def job_details(job_id):
    try:
        return jsonify(get_job(job_id))
    except SynchroteamError as exc:
        return jsonify({'error': str(exc)}), 502


if __name__ == '__main__':
    app.run(debug=True, port=5000)
