from copy import deepcopy
from uuid import uuid1
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

from grpc_modules import act_fix_pb2
from grpc_modules import event_store_pb2

from grpc_modules.infra_pb2 import Value
from grpc_modules.infra_pb2 import ListValue
from grpc_modules.infra_pb2 import Message
from grpc_modules.infra_pb2 import MessageMetadata
from grpc_modules.infra_pb2 import ValueFilter
from grpc_modules.infra_pb2 import ListValueFilter
from grpc_modules.infra_pb2 import MessageFilter
from grpc_modules.infra_pb2 import FilterOperation
from grpc_modules.infra_pb2 import EventID
from grpc_modules.infra_pb2 import Event
from grpc_modules.infra_pb2 import ConnectionID
from grpc_modules.infra_pb2 import Direction

from grpc_modules.verifier_pb2 import PreFilter
from grpc_modules.verifier_pb2 import CheckRuleRequest
from grpc_modules.verifier_pb2 import CheckSequenceRuleRequest

from grpc_modules.quod_simulator_pb2 import TemplateQuodNOSRule
from grpc_modules.quod_simulator_pb2 import TemplateQuodOCRRule
from grpc_modules.quod_simulator_pb2 import TemplateQuodMDRRule


# Debug output
PrintMessages = False


def timestamps():
    report_start_time = datetime.now()
    seconds = int(report_start_time.timestamp())
    nanos = int(report_start_time.microsecond * 1000)
    return seconds, nanos


def client_orderid(length: int) -> str:
    return str(uuid1().time)[-length:]


def message_to_grpc(message_type: str, content: dict) -> Message:
    content = deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            content[tag] = Value(simple_value=str(content[tag]))
        elif isinstance(content[tag], dict):
            content[tag] = Value(message_value=(message_to_grpc(tag, content[tag])))

        elif isinstance(content[tag], list):
            for group in content[tag]:
                content[tag][content[tag].index(group)] = Value(
                    message_value=(message_to_grpc(tag + '_' + tag + 'IDs', group)))
            content[tag] = Value(
                message_value=Message(
                    metadata=MessageMetadata(message_type=tag),
                    fields={
                        tag: Value(
                            list_value=ListValue(
                                values=content[tag]
                            )
                        )
                    }
                )
            )
    return Message(
        metadata=MessageMetadata(message_type=message_type),
        fields=content
    )


def filter_to_grpc(message_type: str, content: dict, keys=None) -> MessageFilter:
    if keys is None:
        keys = []
    content = deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            if content[tag] == '*':
                content[tag] = ValueFilter(operation=FilterOperation.NOT_EMPTY)
            elif content[tag] == '#':
                content[tag] = ValueFilter(operation=FilterOperation.EMPTY)
            else:
                content[tag] = ValueFilter(
                    simple_filter=str(content[tag]), key=(True if tag in keys else False)
                )
        elif isinstance(content[tag], bytes):
            content[tag] = ValueFilter(
                simple_filter=content[tag], key=(True if tag in keys else False)
            )
        elif isinstance(content[tag], dict):
            content[tag] = ValueFilter(message_filter=(filter_to_grpc(tag, content[tag], keys)))
        elif isinstance(content[tag], tuple):
            value, operation = content[tag].__iter__()
            content[tag] = ValueFilter(
                simple_filter=str(value), operation=FilterOperation.Value(operation)
            )
        elif isinstance(content[tag], list):
            for group in content[tag]:
                content[tag][content[tag].index(group)] = ValueFilter(
                    message_filter=filter_to_grpc(tag, group)
                )
            content[tag] = ValueFilter(
                message_filter=MessageFilter(
                    fields={
                        tag: ValueFilter(
                            list_filter=ListValueFilter(
                                values=content[tag]
                            )
                        )
                    }
                )
            )
    return MessageFilter(messageType=message_type, fields=content)


def convert_to_request(description: str, connectivity: str, event_id: EventID, message: dict,
                       key_fields=None) -> act_fix_pb2.PlaceMessageRequest:
    if key_fields is None:
        key_fields = []
    connectivity = ConnectionID(session_alias=connectivity)
    return act_fix_pb2.PlaceMessageRequest(
        message=message,
        connection_id=connectivity,
        parent_event_id=event_id,
        description=description,
        key_fields=key_fields
    )


def create_check_rule(description: str, message_filter: MessageFilter, checkpoint, connectivity: str, event_id: EventID,
                      direction=Direction.Value("FIRST"), timeout=3000) -> CheckRuleRequest:
    return CheckRuleRequest(
        connectivity_id=ConnectionID(session_alias=connectivity),
        filter=message_filter,
        checkpoint=checkpoint,
        timeout=timeout,
        parent_event_id=event_id,
        description=description,
        direction=direction
    )


def create_check_sequence_rule(description: str, prefilter: PreFilter, msg_filters: list, checkpoint, connectivity: str,
                               event_id: EventID, check_order=True, timeout=3000, direction=Direction.Value("FIRST")):
    return CheckSequenceRuleRequest(
        connectivity_id=ConnectionID(session_alias=connectivity),
        pre_filter=prefilter,
        message_filters=msg_filters,
        checkpoint=checkpoint,
        timeout=timeout,
        parent_event_id=event_id,
        description=description,
        check_order=check_order,
        direction=direction
    )


def create_event_id():
    return EventID(id=str(uuid1()))


def create_event(event_store, event_name, event_id, parent_id=None):
    seconds, nanos = timestamps()
    event = Event(
        id=event_id,
        name=event_name,
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        # end_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        parent_id=parent_id)
    return event_store.StoreEvent(event_store_pb2.StoreEventRequest(event=event))


def create_store_event_request(event_name, event_id, parent_id=None):
    seconds, nanos = timestamps()
    event = Event(
        id=event_id,
        name=event_name,
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        # end_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        parent_id=parent_id
    )
    return event_store_pb2.StoreEventRequest(event=event)


def prefilter_to_grpc(content: dict, _nesting_level=0) -> PreFilter:
    content = deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            content[tag] = ValueFilter(simple_filter=str(content[tag]))
        elif isinstance(content[tag], dict):
            content[tag] = ValueFilter(message_filter=prefilter_to_grpc(content[tag], _nesting_level+1))
        elif isinstance(content[tag], tuple):
            value, operation = content[tag].__iter__()
            content[tag] = ValueFilter(
                simple_filter=str(value), operation=FilterOperation.Value(operation)
            )
        elif isinstance(content[tag], ValueFilter):
            pass
    return PreFilter(fields=content) if _nesting_level == 0 else MessageFilter(fields=content)


def create_sim_rule_nos(*args, **kwargs) -> TemplateQuodNOSRule:
    return TemplateQuodNOSRule(
        connection_id=ConnectionID(session_alias=args[0] if len(args) > 0 else kwargs['session_alias'])
    )


def create_sim_rule_ocr(*args, **kwargs) -> TemplateQuodOCRRule:
    return TemplateQuodOCRRule(
        connection_id=ConnectionID(session_alias=args[0] if len(args) > 0 else kwargs['session_alias'])
    )


def create_sim_rule_mdr(*args, **kwargs) -> TemplateQuodMDRRule:
    return TemplateQuodMDRRule(
        connection_id=ConnectionID(session_alias=args[0] if len(args) > 0 else kwargs['session_alias']),
        sender=args[1] if len(args) > 1 else kwargs['sender'],
        md_entry_size=args[2] if len(args) > 2 else kwargs['md_entry_size'],
        md_entry_px=args[3] if len(args) > 3 else kwargs['md_entry_px']
    )
