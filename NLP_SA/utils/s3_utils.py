import os
import sys
import threading

class ProgressPercentage:
    def __init__(self, filename, filesize):
        self._filename = filename
        self._filesize = filesize
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._filesize) * 100
            sys.stdout.write(
                f"\r📦 Downloading {self._filename}: {self._seen_so_far / 1024 / 1024:.2f} MB "
                f"of {self._filesize / 1024 / 1024:.2f} MB ({percentage:.2f}%)"
            )
            sys.stdout.flush()



import boto3
from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError
from NLP_SA.logger.log import logging

def download_from_s3(bucket: str, key: str, local_path: str) -> None:
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    try:
        logging.info("📡 Getting file size for progress tracking...")
        response = s3.head_object(Bucket=bucket, Key=key)
        filesize = response['ContentLength']

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        logging.info("⬇️ Initiating download...")
        s3.download_file(
            bucket,
            key,
            local_path,
            Callback=ProgressPercentage(key, filesize)
        )

        print(f"\n✅ Download complete: s3://{bucket}/{key} → {local_path}")
    except ClientError as e:
        logging.error(f"❌ Failed to download from S3: {e}")
        raise
