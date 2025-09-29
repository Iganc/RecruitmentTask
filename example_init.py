import sys
import os
from django import setup as dj_setup
from io import StringIO
from django.core.management import call_command  # noqa
from django.utils import timezone  # noqa


def statements_load(file_path):
    from statements.tools import statement_import
    with open(file_path) as fh:
        statement_import(fh)

def main(file_path):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    dj_setup()
    call_command('migrate')
    statements_load(file_path)

if __name__ == '__main__':
    main('example_data.csv' if len(sys.argv) == 1 else sys.argv[1])
