from th2_common.schema.factory.common_factory import CommonFactory
from th2_grpc_common.common_pb2 import EventID, Event, EventBatch
from config_vars import ConfigVars

from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timedelta, date
import uuid
import logging

factory = CommonFactory(grpc_router_config_filepath="./configs/grpc.json",
                        rabbit_mq_config_filepath="./configs/rabbit.json",
                        mq_router_config_filepath="./configs/mq.json",
                        custom_config_filepath="./configs/script-params.json")

event_store = factory.event_batch_router

custom_config = factory.create_custom_configuration()
config_vars = ConfigVars(custom_config)


def create_event_id() -> EventID:
    return EventID(id=str(uuid.uuid1()))


def timestamps():
    report_start_time = datetime.now()
    seconds = int(report_start_time.timestamp())
    nanos = int(report_start_time.microsecond * 1000)
    return seconds, nanos


def create_event_batch(report_name, start_timestamp, event_id, parent_id):
    event = Event(
            id=event_id,
            name=report_name,
            start_timestamp=start_timestamp,
            parent_id=parent_id)
    event_batch = EventBatch()
    event_batch.events.append(event)
    return event_batch


def store_event(event_name: str, event_id: EventID = None, parent_id: EventID = None) -> EventID:

    if event_id is None:
        event_id = create_event_id()

    seconds, nanos = timestamps()
    batch = create_event_batch(event_name, Timestamp(seconds=seconds, nanos=nanos), event_id, parent_id)
    event_store.send(batch)
    return event_id


def create_timestamp(year: int, month: int, day: int) -> Timestamp:
    timestamp = Timestamp()
    date = datetime(year, month, day)
    timestamp.FromDatetime(date)
    return timestamp


def create_related_timestamp(shift: int) -> Timestamp:
    timestamp = Timestamp()
    date = datetime.now() + timedelta(days=shift)
    timestamp.FromDatetime(date)
    return timestamp


def __find_closest_workday(from_date: date, is_weekend_holiday: bool) -> date:
    if not is_weekend_holiday:
        return from_date
    else:
        current_date = from_date
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)
        return current_date


def get_t_plus_date(shift: int, from_date: date = date.today(), is_weekend_holiday: bool = True) -> date:
    current_date = __find_closest_workday(from_date, is_weekend_holiday)
    for i in range(shift):
        current_date += timedelta(days=1)
        current_date = __find_closest_workday(current_date, is_weekend_holiday)

    return current_date
