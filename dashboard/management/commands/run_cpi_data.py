from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.config import settings

import os
import boto3

import logging

logger = logging.getLogger(__name__)

# aws
s3_client = boto3.client("s3")


def upload_file_to_bucket(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        # upload the file
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(
            f"""
              File {file_name} uploaded
              successfully to {bucket_name}/{object_name}
              """
        )
    except Exception as e:
        logger.error("ERROR: {e}")
        raise e

    return


FILE_PATH = os.path.join(settings.BASE_DIR, "data", "cpi.xlsx")


class Command(BaseCommand):
    help = "uploads cpi data to s3"

    def handle(self, *args, **kwargs):

        # get file

        # upload file

        # print
        self.stdout.write(self.style.SUCCESS("text here"))
