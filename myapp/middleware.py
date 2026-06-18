import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_FILE = BASE_DIR / 'metrics.log'

_metrics = {
    'total_requests': 0,
    'requests_2xx': 0,
    'requests_4xx': 0,
    'requests_5xx': 0,
}


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        _metrics['total_requests'] += 1
        status = response.status_code
        if 200 <= status < 300:
            _metrics['requests_2xx'] += 1
        elif 400 <= status < 500:
            _metrics['requests_4xx'] += 1
        elif 500 <= status < 600:
            _metrics['requests_5xx'] += 1

        line = (
            f"total={_metrics['total_requests']} "
            f"2xx={_metrics['requests_2xx']} "
            f"4xx={_metrics['requests_4xx']} "
            f"5xx={_metrics['requests_5xx']}"
        )
        print(line)
        with open(METRICS_FILE, 'a') as f:
            f.write(line + '\n')

        return response
