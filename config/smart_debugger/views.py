from django.shortcuts import render
from django.http import HttpResponse
import requests, json, csv
import csv
from .models import APIRequest


def home(request):
    response = None
    root_cause = None
    solution_msg = None

    if request.method == 'POST':
        api_url = request.POST.get('api_url')
        method = request.POST.get('method')

        try:
            if method == 'GET':
                res = requests.get(api_url, timeout=5)
            else:
                res = requests.post(api_url, timeout=5)

            try:
                response = json.dumps(res.json(), indent=4)
            except:
                response = res.text

            if res.status_code >= 500:
                root_cause = "Server Error"
                solution_msg = "API server issue"
            elif res.status_code == 404:
                root_cause = "Not Found"
                solution_msg = "Check API URL"
            elif res.status_code >= 400:
                root_cause = "Client Error"
                solution_msg = "Check request"
            else:
                root_cause = "Success"
                solution_msg = "Working fine"

        except Exception as e:
            error_msg = str(e).lower()

            if "timeout" in error_msg:
                solution_msg = "Server timeout"
            elif "connection" in error_msg:
                solution_msg = "Check internet"
            else:
                solution_msg = "Unknown error"

            root_cause = str(e)
            response = None

        api_request = APIRequest.objects.create(url=api_url, method=method)

        APIResult.objects.create(
            request=api_request,
            response=response,
            error=root_cause if root_cause != "Success" else None,
            solution=solution_msg
        )

    history = APIRequest.objects.all().order_by('-created_at')[:10]

    total = APIRequest.objects.count()
    success = APIResult.objects.filter(error__isnull=True).count()
    failure = APIResult.objects.filter(error__isnull=False).count()

    return render(request, 'smart_debugger/home.html', {
        'response': response,
        'root_cause': root_cause,
        'solution': solution_msg,
        'history': history,
        'total': total,
        'success': success,
        'failure': failure
    })


def download_logs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="api_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['URL', 'Method', 'Status', 'Timestamp'])

    logs = APIRequest.objects.all()

    for log in logs:
        try:
            status = "Failed" if log.apiresult.error else "Success"
        except:
            status = "Unknown"

        writer.writerow([
            log.url,
            log.method,
            status,
            log.timestamp
        ])

    return response