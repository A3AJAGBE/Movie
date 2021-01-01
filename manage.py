#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_app.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', os.environ.get('DJANGO_CONFIGURATION'))

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)







