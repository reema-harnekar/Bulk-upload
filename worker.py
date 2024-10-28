import os
import sys

if __name__ == '__main__':
    from app import celery_instance
    # Starting celery worker, press ctrl+z to stop the process.
    celery_instance.start(["worker"])