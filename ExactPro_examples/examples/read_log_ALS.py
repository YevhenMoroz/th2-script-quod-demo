import logging
from time import sleep

from th2_grpc_common.common_pb2 import Direction

from custom import basic_custom_actions as bca
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id):
    verifier = Stubs.verifier
    case_name = "Log_ALS_example"
    case_id = bca.create_event(case_name, report_id)

    checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(report_id))
    checkpoint = checkpoint_response1.checkpoint
    sleep(30)
    als_logs_params = {
        "ConfirmationID": "*",
        "ConfirmStatus": "New"
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "ALS Log Msg Received",
            bca.filter_to_grpc("Csv_Message", als_logs_params),
            checkpoint, 'log317-als-email-report', case_id, timeout=9000)
    )
