from copy import deepcopy

from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields


class CrossAnnouncement(JavaApiMessage):
    def __init__(self, data_set, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.CrossAnnouncement.value, data_set=data_set)
        super().change_parameters(parameters)
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            JavaApiFields.CrossAnnouncementBlock.value: {
                JavaApiFields.ListingList.value: {JavaApiFields.ListingBlock.value: [
                    {JavaApiFields.ListingID.value: data_set.get_listing_id_by_name('listing_2')}]},
                JavaApiFields.InstrID.value: data_set.get_instrument_id_by_name('instrument_3'),
                JavaApiFields.OrdQty.value: '100',
                JavaApiFields.RouteID.value: data_set.get_route_id_by_name('route_1'),
                JavaApiFields.Price.value: '20'
            }
        }

    def set_default(self, order_id_first, order_id_second):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component(JavaApiFields.CrossAnnouncementBlock.value, {
            JavaApiFields.OrdID1.value: order_id_first,
            JavaApiFields.OrdID2.value: order_id_second,
        })
