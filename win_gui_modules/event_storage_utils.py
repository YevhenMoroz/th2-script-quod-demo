from grpc_modules import event_store_pb2
from grpc_modules import event_store_pb2_grpc
from grpc_modules import infra_pb2

from google.protobuf.timestamp_pb2 import Timestamp

from datetime import datetime, timedelta

import uuid


class EvStorage:
    event_store_service = None


def create_event_id() -> infra_pb2.EventID:
    return infra_pb2.EventID(id=str(uuid.uuid1()))


def set_channel(channel):
    EvStorage.event_store_service = event_store_pb2_grpc.EventStoreServiceStub(channel)


def parent_event(event_name: str, parent_id: infra_pb2.EventID) -> infra_pb2.EventID:
    seconds, nanos = timestamps()
    event_id = create_event_id()
    event = infra_pb2.Event(
        id=event_id,
        name=event_name,
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        # end_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        parent_id=parent_id,
        body=None,
        status=infra_pb2.EventStatus.SUCCESS
    )
    EvStorage.event_store_service.StoreEvent(event_store_pb2.StoreEventRequest(event=event))
    return event_id


def timestamps():
    report_start_time = datetime.now()
    seconds = int(report_start_time.timestamp())
    nanos = int(report_start_time.microsecond * 1000)
    return seconds, nanos
