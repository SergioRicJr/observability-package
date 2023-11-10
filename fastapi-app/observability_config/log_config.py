import pytz
import datetime
from datetime import timezone
import requests
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor
import os
from dotenv import load_dotenv
load_dotenv()

def send_logs(record, log_entry, job_name, log_url):
    headers = {
            'Content-type': 'application/json'
    }
    dt = datetime.datetime.now(timezone.utc) 
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp() 
    timestamp_unix_nanos = int(utc_timestamp * 1e9)
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
    response = requests.post(log_url, json=data, headers=headers)
    return response

class URLLogHandler(logging.Handler):
    def __init__(self, formatter):
        super(URLLogHandler, self).__init__()
        self.formatter = logging.Formatter(formatter)

    def emit(self, record):
        log_entry = self.format(record)
        response = send_logs(record, log_entry, 'fastapi-app', os.environ.get('LOKI_URL'))
        return response
    
log_format = format='%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(URLLogHandler(log_format))
LoggingInstrumentor().instrument(set_logging_format=True)