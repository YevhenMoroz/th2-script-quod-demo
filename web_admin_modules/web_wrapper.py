""" This module contains functions which are used in web test cases """

import logging
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Event, EventBatch, EventID
from uuid import uuid1

from stubs import Stubs


def get_report(name, status, parent_id, timestamp):
    """ Creates TH2 event
        Parameters:
            name (str): the name of event;
            status (int): the status of event (0 - passed, 1 - failed);
            parent_id (EventID): ID of the parent event;
            timestamp (Timestamp): finish timestamp.
        Returns:
            TH2 event """
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
    """ Executes method and create report depends on this method
            Parameters:
                method (function): function for execute;
                case_id (EventID): ID of the root event.
            Returns:
                TH2 report """
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
