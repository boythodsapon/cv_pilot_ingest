"""
Move file from ingest s3 bucket to ITS DataHub sandbox s3.

"""

from __future__ import print_function

import logging
import os
import traceback


from s3FileMover import cvPilotFileMover


logger = logging.getLogger()
logger.setLevel(logging.INFO)  # necessary to make sure aws is logging

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
TARGET_BUCKET = os.environ['TARGET_BUCKET']
SOURCE_BUCKET_PREFIX = 'usdot-its-datahub-'
SOURCE_KEY_PREFIX = os.environ['SOURCE_KEY_PREFIX'] or ""


def lambda_handler(event, context):
    """AWS Lambda handler. """

    mover = cvPilotFileMover(target_bucket=TARGET_BUCKET,
                             source_bucket_prefix=SOURCE_BUCKET_PREFIX,
                             source_key_prefix=SOURCE_KEY_PREFIX)

    for bucket, key in mover.get_fps_from_event(event):
        try:
            mover.move_file(bucket, key)
        except Exception as e:
            # send_to_slack(traceback.format_exc())
            logger.error("Error while processing event record: {}".format(event))
            logger.error(traceback.format_exc())
            raise e

    logger.info('Processed events')