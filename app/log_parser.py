from app import db
from app.models import LogEntry
from datetime import datetime

def parse_log_line(line):
    parts = line.split()
    return LogEntry(
        ip_address=parts[0],
        timestamp=datetime.strptime(parts[3][1:] + " " + parts[4][:-1], '%d/%b/%Y:%H:%M:%S %z'),
        request=parts[5] + " " + parts[6] + " " + parts[7],
        status_code=int(parts[8]),
        size=int(parts[9])
    )

def parse_log_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = parse_log_line(line)
            db.session.add(log_entry)
        db.session.commit()
