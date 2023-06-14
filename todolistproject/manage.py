#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import asyncio
import multiprocessing
import os
import sys
from telegram_bot import bot as telegram_bot


async def django():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolistproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


async def run_bot_acync():
    telegram_bot.run_bot()


async def main():

    task1 = asyncio.create_task(django())
    task2 = asyncio.create_task(run_bot_acync())

    # Очікуємо завершення обох серверних процесів
    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    asyncio.run(main())
    # main()
