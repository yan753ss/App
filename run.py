from app import create_app
import click
from flask.cli import with_appcontext

app = create_app()

@click.group()
def cli():
    """Management script for the application."""
    pass

@cli.command()
@with_appcontext
def parse_logs():
    """Parse the logs and save to the database."""
    from app.log_parser import parse_log_file
    import os
    config_file = 'config.ini'
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    log_directory = config['default']['files_dir']
    log_extension = config['default']['ext']
    
    for filename in os.listdir(log_directory):
        if filename.endswith(log_extension):
            parse_log_file(os.path.join(log_directory, filename))
    print("Logs have been parsed and saved to the database.")

@cli.command()
@click.argument('start_date')
@click.argument('end_date', required=False)
@click.option('--ip', is_flag=True)
@click.option('--status', is_flag=True)
@with_appcontext
def view_logs(start_date, end_date=None, ip=False, status=False):
    """View logs filtered by date range and optionally by IP and status."""
    from app.models import LogEntry
    from datetime import datetime

    start = datetime.strptime(start_date, '%d.%m.%Y')
    end = datetime.strptime(end_date, '%d.%m.%Y') if end_date else None

    query = LogEntry.query.filter(LogEntry.timestamp >= start)
    if end:
        query = query.filter(LogEntry.timestamp <= end)

    if ip:
        query = query.group_by(LogEntry.ip_address)

    if status:
        query = query.group_by(LogEntry.status_code)

    results = query.all()
    for result in results:
        print(result)

if __name__ == '__main__':
    cli()
