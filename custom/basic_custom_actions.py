""" This module contains functions which are used in test cases """

from copy import deepcopy
from uuid import uuid1
from datetime import datetime, timedelta, date
from google.protobuf.timestamp_pb2 import Timestamp
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitGetMessageRequest

from th2_grpc_check1.check1_pb2 import PreFilter
from th2_grpc_check1.check1_pb2 import CheckRuleRequest
from th2_grpc_check1.check1_pb2 import CheckSequenceRuleRequest
from th2_grpc_check1.check1_pb2 import CheckpointRequest

from th2_grpc_act_fix_quod.act_fix_pb2 import PlaceMessageRequest
from stubs import Stubs

from th2_grpc_common.common_pb2 import ValueFilter, FilterOperation, MessageMetadata, MessageFilter, ConnectionID, \
    EventID, ListValue, Value, Message, ListValueFilter, MessageID, Event, EventBatch, Direction, Checkpoint
from th2_grpc_common.common_pb2 import ComparisonSettings
from th2_grpc_common.common_pb2 import FIELDS_AND_MESSAGES, NO
from decimal import Decimal


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


def timestamps():
    report_start_time = datetime.now()
    seconds = int(report_start_time.timestamp())
    nanos = int(report_start_time.microsecond * 1000)
    return seconds, nanos


def get_timestamp():
    seconds, nanos = timestamps()
    return Timestamp(seconds=seconds, nanos=nanos)


def client_orderid(length: int) -> str:
    """ Generates unique id in the string format of specified length
        Parameters:
            length (int): the length of generated id.
        Returns:
            client_orderid (str)
    """
    return str(uuid1().time)[-length:]


def message_to_grpc(message_type: str, content: dict, session_alias: str) -> Message:
    """ Creates grpc wrapper for message
        Parameters:
            message_type (str): Type of message (NewOrderSingle, ExecutionReport, etc.)
            content (dict): Fields and values, represented in Python dictionary format ({'Price': 10, 'OrderQty': 100}).
            session_alias (str): Name of connectivity box (fix-bs-eq-trqx, fix-fh-eq-paris, gtwquod3).
        Returns:
            message_to_grpc (Message): grpc wrapper for message
    """
    content = deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            content[tag] = Value(simple_value=str(content[tag]))

        elif isinstance(content[tag], dict):
            content[tag] = Value(message_value=(message_to_grpc(tag, content[tag], session_alias)))

        elif isinstance(content[tag], list):
            if tag == 'NoMDEntriesIR':
                for group in content[tag]:
                    content[tag][content[tag].index(group)] = Value(
                        message_value=(message_to_grpc(tag + '_' + tag + 'IDs', group, session_alias)))
                content[tag] = Value(
                    message_value=Message(
                        metadata=MessageMetadata(message_type=tag),
                        fields={
                            'NoMDEntries': Value(
                                list_value=ListValue(
                                    values=content[tag]
                                )
                            )
                        }
                    )
                )
            elif tag in ['venueStatusMetric', 'venuePhaseSession', 'venuePhaseSessionTypeTIF',
                         'venuePhaseSessionPegPriceType', 'venueOrdCapacity',
                         'ListingBlock', 'hedgedAccountGroup', 'autoHedgerInstrSymbol', 'MDSymbolBlock',
                         'CounterpartBlock', 'UnMatchingBlock']:
                for group in content[tag]:
                    content[tag][content[tag].index(group)] = Value(
                        message_value=(message_to_grpc(tag, group, session_alias)))
                content[tag] = Value(list_value=ListValue(values=content[tag]))
            else:
                for group in content[tag]:
                    content[tag][content[tag].index(group)] = Value(
                        message_value=(message_to_grpc(tag + '_' + tag + 'IDs', group, session_alias)))
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
        metadata=MessageMetadata(
            message_type=message_type,
            id=MessageID(connection_id=ConnectionID(session_alias=session_alias)),
        ),
        fields=content
    )

def message_to_grpc_test(message_type: str, content: dict, session_alias: str) -> Message:
    content = dict(deepcopy(content))
    for tag in dict(content):
        # field
        if isinstance(content[tag], (str, int, float)):
            content[tag] = Value(simple_value=str(content[tag]))
        elif isinstance(content[tag], dict):
            # level 1 component
            name = next(iter(content[tag].items()))[0]
            if isinstance(next(iter(content[tag].items()))[1], list):
                # level 2 repeating group
                for group in content[tag][name]:
                    content[tag][name][content[tag][name].index(group)] = Value(
                        message_value=(message_to_grpc(name, group, session_alias)))
                content[tag] = Value(
                    message_value=Message(
                        metadata=MessageMetadata(message_type=tag),
                        fields={
                            name: Value(
                                list_value=ListValue(
                                    values=content[tag][name]
                                )
                            )
                        }
                    )
                )
            else:
                # level 2 field
                content[tag] = Value(message_value=(message_to_grpc(tag, content[tag], session_alias)))
    return Message(
        metadata=MessageMetadata(
            message_type=message_type,
            id=MessageID(connection_id=ConnectionID(session_alias=session_alias)),
        ),
        fields=content
    )



def filter_to_grpc_nfu(message_type: str, content: dict, keys=None, ignored_fields=None) -> MessageFilter:
    """ Creates grpc wrapper for filter without fail unexpected
        Parameters:
            message_type (str): Type of message (NewOrderSingle, ExecutionReport, etc.)
            content (dict): Fields and values, represented in Python dictionary format ({'Price': 10,
                'OrderQty': 100}).
            keys (list): Optional parameter. A list of fields, that must be used as key fields during the message
                verification. Default value is None.
            ignored_fields (list): Optional parameter.
        Returns:
            filter_to_grpc (MessageFilter): grpc wrapper for filter
    """
    if keys is None:
        keys = []
    if ignored_fields is None:
        ignored_fields = []
    ignored_fields += ['header', 'trailer']
    settings = ComparisonSettings(ignore_fields=ignored_fields, fail_unexpected=NO)
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
            content[tag] = ValueFilter(message_filter=(filter_to_grpc_nfu(tag, content[tag], keys)))
        elif isinstance(content[tag], tuple):
            value, operation = content[tag].__iter__()
            content[tag] = ValueFilter(
                simple_filter=str(value), operation=FilterOperation.Value(operation)
            )
        elif isinstance(content[tag], list):
            for group in content[tag]:
                content[tag][content[tag].index(group)] = ValueFilter(
                    message_filter=filter_to_grpc_nfu(tag, group)
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
    return MessageFilter(messageType=message_type, fields=content, comparison_settings=settings)


def filter_to_grpc(message_type: str, content: dict, keys=None, ignored_fields=None) -> MessageFilter:
    """ Creates grpc wrapper for filter
        Parameters:
            message_type (str): Type of message (NewOrderSingle, ExecutionReport, etc.)
            content (dict): Fields and values, represented in Python dictionary format ({'Price': 10,
                'OrderQty': 100}).
            keys (list): Optional parameter. A list of fields, that must be used as key fields during the message
                verification. Default value is None.
            ignored_fields (list): Optional parameter.
        Returns:
            filter_to_grpc (MessageFilter): grpc wrapper for filter
    """
    if keys is None:
        keys = []
    if ignored_fields is None:
        ignored_fields = []
    ignored_fields += ['header', 'trailer']
    settings = ComparisonSettings(ignore_fields=ignored_fields, fail_unexpected=FIELDS_AND_MESSAGES)
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
        elif isinstance(content[tag], dict):
            # level 1 component
            name = next(iter(content[tag].items()))[0]
            if isinstance(next(iter(content[tag].items()))[1], list):
                # level 2 repeating group
                for group in content[tag][name]:
                    content[tag][name][content[tag][name].index(group)] = ValueFilter(
                        message_filter=filter_to_grpc(name, group))
                content[tag] = ValueFilter(
                    message_filter=MessageFilter(
                        fields={
                            name: ValueFilter(
                                list_filter=ListValueFilter(
                                    values=content[tag][name]
                                )
                            )
                        }
                    )
                )
    return MessageFilter(messageType=message_type, fields=content, comparison_settings=settings)


def convert_to_request(description: str, connectivity: str, event_id: EventID, message: Message,
                       key_fields=None) -> PlaceMessageRequest:
    """ Creates grpc request for sending message to the system.
        Parameters:
            description (str): Text for displaying in report.
            connectivity (str): Name of connectivity box (fix-bs-eq-trqx, fix-fh-eq-paris, gtwquod3).
            event_id (str): ID of the parent event.
            message (Message): Message, which must be sent to the system.
            key_fields (list): Optional parameter. A list of fields, that must be used as key fields during the message
                receiving by act box. Default value is None.
        Returns:
            convert_to_request (PlaceMessageRequest): request to act box
    """
    if key_fields is None:
        key_fields = []
    connectivity = ConnectionID(session_alias=connectivity)
    return PlaceMessageRequest(
        message=message,
        connection_id=connectivity,
        parent_event_id=event_id,
        description=description,
        key_fields=key_fields
    )

def convert_to_get_request(description: str, connectivity: str, event_id: EventID, message: Message,
                       request_type: str, response_type: str) -> SubmitGetMessageRequest:
    """ Creates grpc request for sending message to the system.
        Parameters:
            description (str): Text for displaying in report.
            connectivity (str): Name of connectivity box (fix-bs-eq-trqx, fix-fh-eq-paris, gtwquod3).
            event_id (str): ID of the parent event.
            message (Message): Message, which must be sent to the system.
            request_type (str): requestType
            response_type (str): responseType
        Returns:
            convert_to_request (SubmitGetMessageRequest): request to act box
    """
    connectivity = ConnectionID(session_alias=connectivity)
    return SubmitGetMessageRequest(
        message=message,
        connection_id=connectivity,
        parent_event_id=event_id,
        description=description,
        requestType=request_type,
        responseType=response_type
    )


def create_check_rule(description: str, message_filter: MessageFilter, checkpoint: Checkpoint, connectivity: str,
                      event_id: EventID, direction=Direction.Value("FIRST"), timeout=3000) -> CheckRuleRequest:
    """ Creates grpc request for verification only one message
        Parameters:
            description (str): Text for displaying in report.
            message_filter (MessageFilter): Expected values in grpc wrapper.
            checkpoint (Checkpoint): Checkpoint, which is used as start point during message verification.
            connectivity (str): Name of connectivity box (fix-bs-eq-trqx, fix-fh-eq-paris, gtwquod3).
            event_id: ID of the parent event.
            direction (Direction): Optional parameter. Direction of messages stream.
                Values: FIRST - from system to connectivity; SECOND - from connectivity to system
                Default value is FIRST.
            timeout (int): Optional parameter. Time in milliseconds, during which check1 must find message.
                Default value is 3000 ms.
        Returns:
            create_check_rule (CheckRuleRequest): request to check1 box
    """
    return CheckRuleRequest(
        connectivity_id=ConnectionID(session_alias=connectivity),
        filter=message_filter,
        checkpoint=checkpoint,
        timeout=timeout,
        parent_event_id=event_id,
        description=description,
        direction=direction
    )


def create_check_sequence_rule(description: str, prefilter: PreFilter, msg_filters: list, checkpoint: Checkpoint,
                               connectivity: str, event_id: EventID, check_order=True, timeout=3000,
                               direction=Direction.Value("FIRST")) -> CheckSequenceRuleRequest:
    """ Creates grpc request for verification several messages and an order of their receiving
        Parameters:
            description (str): Text for displaying in report.
            prefilter (PreFilter): grpc wrapper for preliminary filtration of messages
            msg_filters (list): A list of filters (a sets of expected values) in grpc wrappers.
            checkpoint (str): Checkpoint id, which is used as start point during message verification.
            connectivity (str): Name of connectivity box (fix-bs-eq-trqx, fix-fh-eq-paris, gtwquod3).
            event_id: ID of the parent event.
            check_order (bool): Optional parameter. Defines if the order of messages is considered
                in the verification or not. Default value is True.
            direction (Direction): Optional parameter. Direction of messages stream.
                Values: FIRST - from system to connectivity; SECOND - from connectivity to system.
                Default value is FIRST.
            timeout (int): Optional parameter. Time in milliseconds, during which check1 must find message.
                Default value is 3000 ms.
        Returns:
            create_check_sequence_rule (CheckSequenceRuleRequest): request to check1 box
    """
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


def create_event_id() -> EventID:
    """ Creates unique id for event.
        Returns:
            create_event_id (EventID): unique id.
    """
    return EventID(id=str(uuid1()))


def create_event(event_name: str, parent_id: EventID = None, status= 'SUCCESS', body='{"text": ""}') -> EventID:
    """ Creates a new event.
        Parameters:
            event_name (str): Text that will be displayed in the report.
            parent_id (EventID): Optional parameter. ID of the parent event. Default value is None.
        Returns:
            create_event (EventID): id of the created event.
    """
    event_store = Stubs.event_store
    seconds, nanos = timestamps()
    event_id = create_event_id()
    event = Event(
        id=event_id,
        name=event_name,
        status=status,
        body=bytes(body, 'utf8'),
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        # end_timestamp=current_timestamp,
        parent_id=parent_id)
    event_batch = EventBatch()
    event_batch.events.append(event)
    event_store.send(event_batch)
    return event_id


def prefilter_to_grpc(content: dict, _nesting_level=0) -> PreFilter:
    """ Creates a grpc wrapper for specified fields and their values to preliminary filtration of messages
        in the stream.
        Parameters:
            content (dict): Fields and their values, which are used to filter.
            _nesting_level (int): For internal purpose.
        Returns:
            prefilter_to_grpc (PreFilter): fields and their values in the grpc wrapper.
    """
    content = deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            content[tag] = ValueFilter(simple_filter=str(content[tag]))
        elif isinstance(content[tag], dict):
            content[tag] = ValueFilter(message_filter=prefilter_to_grpc(content[tag], _nesting_level + 1))
        elif isinstance(content[tag], tuple):
            value, operation = content[tag].__iter__()
            content[tag] = ValueFilter(
                simple_filter=str(value), operation=FilterOperation.Value(operation)
            )
        elif isinstance(content[tag], list):
            for group in content[tag]:
                content[tag][content[tag].index(group)] = ValueFilter(
                    message_filter=prefilter_to_grpc(content[tag][content[tag].index(group)], _nesting_level + 1)
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
        elif isinstance(content[tag], ValueFilter):
            pass
    return PreFilter(fields=content) if _nesting_level == 0 else MessageFilter(fields=content)


def create_checkpoint_request(event_id: EventID, description: str = "Checkpoint") -> CheckpointRequest:
    """ Creates grpc request for sending checkpoint.
        Parameters:
            description (str): free text.
            event_id (EventID): ID of the parent (for checkpoint) event.
        Returns:
            create_checkpoint_request (CheckpointRequest): grpc request with checkpoint
    """
    return CheckpointRequest(description=description, parent_event_id=event_id)


def wrap_message(content, message_type=None, session_alias=None, direction=Direction.Value("SECOND")):
    if isinstance(content, dict):
        fields = dict()
        for tag, value in content.items():
            if isinstance(value, str):
                fields[tag] = Value(simple_value=value)
            elif isinstance(value, (int, float, Decimal)):
                fields[tag] = Value(simple_value=str(value))
            elif isinstance(value, dict):
                fields[tag] = Value(message_value=wrap_message(content=value))
            elif isinstance(value, list):
                fields[tag] = Value(list_value=wrap_message(content=value))
        message = Message(fields=fields)
        if message_type is not None:
            message.metadata.message_type = message_type
            message.metadata.id.direction = direction
            if session_alias is not None:
                message.metadata.id.connection_id.session_alias = session_alias
        return message
    elif isinstance(content, list):
        values = []
        for element in content:
            if isinstance(element, str):
                values.append(Value(simple_value=element))
            elif isinstance(element, (int, float, Decimal)):
                values.append(Value(simple_value=str(element)))
            elif isinstance(element, dict):
                values.append(Value(message_value=wrap_message(content=element)))
            elif isinstance(element, list):
                values.append(Value(list_value=wrap_message(content=element)))
        list_value = ListValue(values=values)
        return list_value

def wrap_filter(content, message_type=None, key_fields=None):
    if key_fields is None:
        key_fields = []
    if isinstance(content, dict):
        fields = dict()
        for tag, value in content.items():
            if value == "*":
                fields[tag] = ValueFilter(operation=FilterOperation.Value("NOT_EMPTY"))
            elif value == "#":
                fields[tag] = ValueFilter(operation=FilterOperation.Value("EMPTY"))
            else:
                if isinstance(value, str):
                    fields[tag] = ValueFilter(simple_filter=value)
                elif isinstance(value, (int, float, Decimal)):
                    fields[tag] = ValueFilter(simple_filter=str(value))
                elif isinstance(value, dict):
                    fields[tag] = ValueFilter(message_filter=wrap_filter(content=value, key_fields=key_fields))
                elif isinstance(value, list):
                    fields[tag] = ValueFilter(list_filter=wrap_filter(content=value, key_fields=key_fields))
                if tag in key_fields:
                    fields[tag].key = True
        msg_filter = MessageFilter(fields=fields)
        if message_type is not None:
            msg_filter.messageType = message_type
        return msg_filter
    elif isinstance(content, list):
        values = []
        for element in content:
            if isinstance(element, str):
                values.append(ValueFilter(simple_filter=element))
            elif isinstance(element, (int, float, Decimal)):
                values.append(ValueFilter(simple_filter=str(element)))
            elif isinstance(element, dict):
                values.append(ValueFilter(message_filter=wrap_filter(content=element, key_fields=key_fields)))
            elif isinstance(element, list):
                values.append(ValueFilter(list_filter=wrap_filter(content=element, key_fields=key_fields)))
        list_filter = ListValueFilter(values=values)
        return list_filter


def get_message_by_field_and_value(content, field: str, value: str, matched_list=None) -> list:
    if matched_list is None:
        matched_list = []
    if isinstance(content, Message):
        for f, v in content.fields.items():
            if f == field and v.simple_value == value:
                matched_list.append(content)
            if v.message_value != Message():
                get_message_by_field_and_value(v.message_value, field, value, matched_list)
            elif v.list_value != ListValue():
                get_message_by_field_and_value(v.list_value, field, value, matched_list)
    elif isinstance(content, ListValue):
        for v in content.values:
            if v.message_value != Message():
                get_message_by_field_and_value(v.message_value, field, value, matched_list)
            elif v.list_value != ListValue():
                get_message_by_field_and_value(v.list_value, field, value, matched_list)
    return matched_list[0] if len(matched_list) > 0 else []
