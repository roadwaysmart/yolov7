import requests
import json
import time
from threading import Thread
from queue import Queue

class ReportController:
    def __init__(self, report_url, report_threshold):
        self.url = report_url
        self.report_threshold = report_threshold
        self.queue = Queue()
        self.report_status = {}
        self.worker = Thread(target=self.worker_thread, args=(), daemon=True)
        
    def start(self):
        self.worker.start()
        
    def last_report(self, camera_id):
        # if available , return the tuple of (report timestamp, reported person objects)
        return self.report_status.get(camera_id, (None, []))

    def worker_thread(self):
        server_failure_time = None

        while True:
            msg = self.queue.get()
            timestamp = msg["timestamp"]
            
            to_report = {
                "timestamp": timestamp,
                "cameras": {}
            }
            
            report_num = 0
            for id in msg["cameras"]:
                persons = msg["cameras"][id]
                report_time, report_persons = self.last_report(id)
                if report_time is None or timestamp - report_time >= self.report_threshold or len(persons) > len(report_persons):
                    # to_report
                    to_report["cameras"][id] = persons
                    report_num += 1
                    
            if report_num == 0:
                continue

            now = time.time()
            if server_failure_time is None or now - server_failure_time > 5:
                try:
                    r = requests.post(self.url, json.dumps(to_report), timeout=0.2)
                    if r.status_code == 200:
                        # success, commit the report status to report_status
                        server_failure_time = None
                        for id in to_report["cameras"]:
                            self.report_status[id] = (timestamp, to_report["cameras"][id])
                    else:
                        # failed
                        server_failure_time = time.time()
                except:
                    server_failure_time = time.time()

    def deliver(self, msg):
        self.queue.put(msg)