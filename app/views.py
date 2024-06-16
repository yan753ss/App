from flask import Blueprint, request, jsonify
from app import db
from app.models import LogEntry
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/logs', methods=['GET'])
def get_logs():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    ip_address = request.args.get('ip_address')

    query = LogEntry.query

    if start_date:
        start = datetime.strptime(start_date, '%d.%m.%Y')
        query = query.filter(LogEntry.timestamp >= start)
    if end_date:
        end = datetime.strptime(end_date, '%d.%m.%Y')
        query = query.filter(LogEntry.timestamp <= end)
    if ip_address:
        query = query.filter_by(ip_address=ip_address)

    logs = query.all()
    log_list = []
    for log in logs:
        log_list.append({
            'ip_address': log.ip_address,
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'request': log.request,
            'status_code': log.status_code,
            'size': log.size
        })

    return jsonify(log_list)
