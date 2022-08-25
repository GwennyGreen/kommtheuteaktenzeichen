"""Script to manage S3 objects"""

import boto3

from kha.settings import EVENTS_JSON_FILENAME


def upload_events(source_json: str,
                  target_bucket: str,
                  profile_name: str) -> None:
    """Uploads an events database to an S3 bucket.

    Note: The target key is always `events.kha.json`, regardless
    of the file name given in `source_json`.

    :param `source_json`:
        File name to upload.
    :param `target_bucket`:
        Name of the S3 bucket to receive the file.
    :param `profile_name`:
        Name of the AWS profile to use.
    """
    s3_client = boto3.Session(profile_name=profile_name) \
        .client('s3')
    print(f'Uploading {source_json} to bucket: {target_bucket}')
    s3_client.upload_file(Filename=source_json,
                          Bucket=target_bucket,
                          Key=EVENTS_JSON_FILENAME)
    print('Done')
