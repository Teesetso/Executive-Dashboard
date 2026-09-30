import json
import os
from base64 import b64encode
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_URL = 'https://cvtitsolutions.synchroteam.com/api/v3/job/details'
DEFAULT_LIST_URL = 'https://cvtitsolutions.synchroteam.com/api/v3/job/list'
DEFAULT_CUSTOMER_LIST_URL = 'https://cvtitsolutions.synchroteam.com/api/v3/customer/list'
DEFAULT_SITE_LIST_URL = 'https://cvtitsolutions.synchroteam.com/api/v3/site/list'


class SynchroteamError(Exception):
    """Raised when Synchroteam cannot return a job."""


def _authorization_header():
    value = os.getenv('SYNCHROTEAM_AUTHORIZATION')
    if value:
        return value if value.lower().startswith('basic ') else f'Basic {value}'

    username = os.getenv('SYNCHROTEAM_USERNAME')
    password = os.getenv('SYNCHROTEAM_PASSWORD')
    if username and password:
        credentials = b64encode(f'{username}:{password}'.encode()).decode()
        return f'Basic {credentials}'
    raise SynchroteamError('Set SYNCHROTEAM_AUTHORIZATION or SYNCHROTEAM_USERNAME and SYNCHROTEAM_PASSWORD.')


def get_job(job_id):
    url = os.getenv('SYNCHROTEAM_JOB_URL', DEFAULT_URL)
    return _request_json(f'{url}?{urlencode({"id": job_id})}')


def get_jobs():
    url = os.getenv('SYNCHROTEAM_LIST_URL', DEFAULT_LIST_URL)
    jobs = _list_data(_request_json(url))
    if not isinstance(jobs, list):
        raise SynchroteamError('Synchroteam returned an invalid job list.')
    return jobs


def get_customers():
    url = os.getenv('SYNCHROTEAM_CUSTOMER_LIST_URL', DEFAULT_CUSTOMER_LIST_URL)
    customers = _list_data(_request_json(url))
    if not isinstance(customers, list):
        raise SynchroteamError('Synchroteam returned an invalid customer list.')
    return customers


def get_sites():
    url = os.getenv('SYNCHROTEAM_SITE_LIST_URL', DEFAULT_SITE_LIST_URL)
    sites = _list_data(_request_json(url))
    if not isinstance(sites, list):
        raise SynchroteamError('Synchroteam returned an invalid site list.')
    return sites


def _list_data(response):
    return response.get('data') if isinstance(response, dict) else response


def normalize_customer(customer):
    position = customer.get('Position') or customer.get('position') or {}
    first_name = customer.get('contactFirstName') or ''
    last_name = customer.get('contactLastName') or ''
    return {
        'id': customer.get('myId') or customer.get('id', ''),
        'name': customer.get('name') or 'Unnamed customer',
        'address': customer.get('address') or '',
        'city': customer.get('addressCity') or '',
        'province': customer.get('addressProvince') or '',
        'zip': customer.get('addressZIP') or '',
        'country': customer.get('addressCountry') or '',
        'contact': ' '.join(part for part in (first_name, last_name) if part),
        'email': customer.get('contactEmail') or '',
        'phone': customer.get('contactPhone') or customer.get('contactMobile') or '',
        'active': bool(customer.get('active')),
        'latitude': position.get('latitude') or '',
        'longitude': position.get('longitude') or '',
        'date_modified': customer.get('dateModified') or '',
    }


def normalize_site(site):
    customer = site.get('customer') or {}
    return {
        'id': site.get('myId') or site.get('id', ''),
        'name': site.get('name') or 'Unnamed site',
        'address': site.get('address') or '',
        'city': site.get('addressCity') or '',
        'province': site.get('addressProvince') or '',
        'zip': site.get('addressZIP') or '',
        'country': site.get('addressCountry') or '',
        'customer': customer.get('name') or 'Unassigned',
        'contact': ' '.join(part for part in (site.get('contactFirstName') or '', site.get('contactLastName') or '') if part),
        'email': site.get('contactEmail') or '',
        'phone': site.get('contactPhone') or site.get('contactMobile') or '',
        'active': bool(site.get('active')),
        'date_modified': site.get('dateModified') or '',
    }


def _request_json(request_url):
    request = Request(request_url, headers={
        'Accept': 'text/json',
        'Authorization': _authorization_header(),
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    })

    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        raise SynchroteamError(f'Synchroteam returned HTTP {error.code}.') from error
    except URLError as error:
        raise SynchroteamError(f'Could not connect to Synchroteam: {error.reason}.') from error
    except json.JSONDecodeError as error:
        raise SynchroteamError('Synchroteam returned invalid JSON.') from error


def normalize_job(job):
    technician = job.get('technician') or {}
    customer = job.get('customer') or {}
    site = job.get('site') or {}
    job_type = job.get('type') or {}
    actual_start = job.get('actualStart') or ''
    actual_end = job.get('actualEnd') or ''
    scheduled_start = job.get('scheduledStart') or ''
    scheduled_end = job.get('scheduledEnd') or ''
    duration = _hours_between(actual_start, actual_end)

    return {
        'id': job.get('myId') or job.get('id') or str(job.get('num', '')),
        'number': job.get('num', ''),
        'description': (job.get('description') or '').strip(),
        'priority': job.get('priority', ''),
        'customer': customer.get('name', 'Unknown customer'),
        'site': site.get('name', 'Unknown site'),
        'type': job_type.get('name', 'Job'),
        'status': _status_label(job.get('status', 'created')),
        'technician': technician.get('name', 'Unassigned'),
        'address': job.get('address') or '',
        'scheduled_start': scheduled_start,
        'scheduled_end': scheduled_end,
        'actual_start': actual_start,
        'actual_end': actual_end,
        'duration': duration,
        'scheduled': _scheduled_hours(scheduled_start, scheduled_end),
        'overdue': bool(job.get('actualEnd') and scheduled_end and job.get('actualEnd') > scheduled_end),
    }


def _scheduled_hours(start, end):
    return _hours_between(start, end)


def _status_label(status):
    labels = {'started': 'In progress', 'in_progress': 'In progress'}
    return labels.get(status, str(status).replace('_', ' ').title())


def _hours_between(start, end):
    if not start or not end:
        return 0
    try:
        from datetime import datetime
        start_time = datetime.strptime(start, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end, '%Y-%m-%d %H:%M')
        return round((end_time - start_time).total_seconds() / 3600, 1)
    except ValueError:
        try:
            from datetime import datetime
            start_time = datetime.strptime(start, '%d/%m/%Y %H:%M:%S')
            end_time = datetime.strptime(end, '%d/%m/%Y %H:%M:%S')
            return round((end_time - start_time).total_seconds() / 3600, 1)
        except ValueError:
            return 0
