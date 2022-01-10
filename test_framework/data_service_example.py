from th2_data_services.data_source import DataSource
from stubs import Stubs
import re
import json
from custom.basic_custom_actions import create_event, create_event_id, timestamps
from google.protobuf.timestamp_pb2 import Timestamp
from th2_grpc_common.common_pb2 import Event, EventBatch, MessageID, ConnectionID
from th2_data_services.data import Data
from datetime import datetime, timedelta

def check_log_period(params: dict):
    data_source = DataSource(f"http://10.0.22.22:31622")  # rpt-data-provider address
    success = True
    passed = False
    ids = []
    idx = 0
    body = {}
    body_fields = {}

    START_TIME = datetime.now() - timedelta(minutes=1)
    END_TIME = datetime.now()
    URL = F"http://10.0.22.22:31622"

    data_source = DataSource(URL)

    events = data_source.get_events_from_data_provider(
        startTimestamp=START_TIME,
        endTimestamp=END_TIME,
        metadataOnly=False,
        attachedMessages=True,
    )

    streams = [
        'fix-bs-eq-paris',
        'fix-bs-eq-trqx',
        'fix-ss-back-office',
        'fix-fh-eq-trqx',
        'quod_rest',
        'fix-ss-310-columbia-standart',
        'gtwquod5',
        'fix-ss-308-mercury-standard',
        'fix-fh-eq-paris',
        'gtwquod3',
    ]
    messages = data_source.get_messages_from_data_provider(
        startTimestamp=START_TIME,
        endTimestamp=END_TIME,
        stream=streams,
    )
    print(messages)



def execute():
    log_msg_params = {
        'Session-alias': 'log305-sats-comments',
        'Start_time': '2021-10-11 06:24:48',
        'End_time': '2021-10-11 06:28:58',
        'Message': 'Cancelling ASOR child order AO1211011062431153001'
    }

    check_log_period(log_msg_params)


if __name__ == "__main__":
    execute()
    Stubs.factory.close()
