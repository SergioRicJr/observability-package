import pytz
import datetime
import requests
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor

def send_logs(record, log_entry, job_name, log_host):
    headers = {
            'Content-type': 'application/json'
    }
    curr_datetime = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    timestamp_unix_seconds = (curr_datetime - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    timestamp_unix_nanos = int(timestamp_unix_seconds * 1e9)
    data = {
        "streams": [
            {
                "stream": {
                    "job": job_name,
                    "severity": record.levelname,
                    "name": record.name
                },
                "values": [
                    [str(timestamp_unix_nanos), log_entry]
                ]
            }
        ]
    }
    response = requests.post(f'http://{log_host}/loki/api/v1/push', json=data, headers=headers)
    return response

class URLLogHandler(logging.Handler):
    def __init__(self, formatter):
        super(URLLogHandler, self).__init__()
        self.formatter = logging.Formatter(formatter)

    def emit(self, record):
        log_entry = self.format(record)
        response = send_logs(record, log_entry, 'fastapi-app', 'nginx:80')
        return response
    
log_format = format='%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message=%(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(URLLogHandler(log_format))
LoggingInstrumentor().instrument(set_logging_format=True)