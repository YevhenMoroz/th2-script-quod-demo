from th2_data_services.data_source import DataSource
from stubs import Stubs
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

    START_TIME = datetime.now() - timedelta(days=1)

    START_CHECK_TIME = datetime.strptime(params['Start_time'], '%Y-%m-%d %H:%M:%S')
    END_CHECK_TIME = datetime.strptime(params['End_time'], '%Y-%m-%d %H:%M:%S')

    # get messages from START_TIME to current time
    messages: Data = data_source.get_messages_from_data_provider(
        startTimestamp=START_TIME,
        stream=params['Session-alias']
    )

    # filter messages with body which contains text we are checking for
    filtered_messages: Data = messages.filter(lambda msg: 'body' in msg.keys()
                                                          and params['Message'] in msg['body']['fields']
                                                          ['Csv_Message']['messageValue']['fields']
                                                          ['Message']['simpleValue'])

    # function for mapping necessary fields in messages
    def map_function(record):
        return {
            "message": record['body']['fields']['Csv_Message']['messageValue']['fields']['Message']['simpleValue'],
            "timestamp": record['body']['metadata']['properties']['logTimestamp'],
            'id': record['messageId']
        }

    # filtering and mapping messages for further checking
    mapped_messages = filtered_messages.map(map_function)

    # checking for count of messages
    msg_count = len(mapped_messages)
    if msg_count == 0:
        success = False
        body = {
            "type": "message",
            "data": 'There are no messages in the log by chosen parameters'
        }
    else:
        for m in mapped_messages:
            idx += 1

            # checking timestamp of messages
            log_time = datetime.strptime(m['timestamp'][:-10], '%Y-%m-%d %H:%M:%S')
            passed = START_CHECK_TIME <= log_time <= END_CHECK_TIME

            # creating MessageID of each message for showing in report event
            msg_id = m['id'].split(':')
            ids.append(
                MessageID(
                    connection_id=ConnectionID(
                        session_alias=msg_id[0]
                    ),
                    direction=0,
                    sequence=int(msg_id[2]),
                    subsequence=0))

            # creating lines in report event with checking data for each message
            body_fields[f'Message [{idx}]'] = {
                "expected": f"{START_CHECK_TIME} - {END_CHECK_TIME}",
                "actual": str(log_time),
                "key": False,
                "type": "field",
                "status": "PASSED" if passed else "FAILED"
            }

            body = {"fields": body_fields, "type": "verification"}

    if msg_count == 1:
        success &= passed

    # creating root report event
    case_name = f"Checking timestamp of message in '{params['Session-alias']}' log"
    parent_id = create_event(case_name)
    event_body = bytes(json.dumps([body]), 'utf-8')
    seconds, nanos = timestamps()
    event_id = create_event_id()

    # creating child report event
    event = Event(
        id=event_id,
        name=f"Message '{params['Message']}'",
        status="SUCCESS" if success else "FAILED",
        body=event_body,
        attached_message_ids=ids,
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        parent_id=parent_id)

    event_batch = EventBatch()
    event_batch.events.append(event)
    Stubs.event_store.send(event_batch)


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
