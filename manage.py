#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import environ
import os
import sys
import dotenv
dotenv.load_dotenv()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stylestore.settings')

    # Initialize environment variables
    env = environ.Env()
    
    # Read environment variables from .env file (if exists)
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_file):
        environ.Env.read_env(env_file)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
