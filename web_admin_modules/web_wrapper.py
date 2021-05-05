import logging
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Event, EventBatch, EventID
from uuid import uuid1

from stubs import Stubs


def get_report(name, status, parent_id, timestamp):
    estore = Stubs.factory.event_batch_router
    event = Event(
        id=EventID(id=str(uuid1())),
        name=name,
        status=status,
        body=b'',
        start_timestamp=timestamp,
        end_timestamp=bca.get_timestamp(),
        parent_id=parent_id)
    estore.send(EventBatch(events=[event]))


def call(method, case_id):
    method_name = method.__name__
    logging.info(f'Executing [{method_name}] method ... ')
    start_timestamp = bca.get_timestamp()
    report_status = 0
    try:
        method()
    except Exception:
        report_status = 1
        logging.error(f'Error execution [{method_name}] method', exc_info=True)
    finally:
        get_report(method_name, report_status, case_id, start_timestamp)
        logging.info('done\n')
