from copy import deepcopy
from datetime import datetime

from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionPolicyConst, OrdTypes, \
    TimeInForces, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.MultiLegOrderModificationRequest import \
    MultiLegOrderModificationRequest


class MultiLegOrderModificationRequestOMS(MultiLegOrderModificationRequest):
    def __init__(self, data_set, parameters: dict = None):
        super().__init__(data_set, parameters)
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            JavaApiFields.MultiLegOrderModificationRequestBlock.value:
                {JavaApiFields.LegOrderElements.value: {
                    JavaApiFields.LegOrderBlock.value: [{JavaApiFields.LegNumber.value: 1,
                                                         JavaApiFields.LegInstrID.value: self.get_data_set().get_instrument_id_by_name(
                                                             'instrument_12_leg_2_of_multileg_paris'),
                                                         JavaApiFields.LegPrice.value: 0},
                                                        {JavaApiFields.LegNumber.value: 2,
                                                         JavaApiFields.LegInstrID.value: self.get_data_set().get_instrument_id_by_name(
                                                             'instrument_12_leg_2_of_multileg_paris'),
                                                         JavaApiFields.LegPrice.value: 0}]},
                    JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                    JavaApiFields.Price.value: 20,
                    JavaApiFields.TimeInForce.value: TimeInForces.DAY.value,
                    JavaApiFields.PositionEffect.value: "O",
                    JavaApiFields.OrdQty.value: '100',
                    JavaApiFields.OrdCapacity.value: OrderReplyConst.OrdCapacity_A.value,
                    JavaApiFields.TransactTime.value: datetime.utcnow().isoformat(),
                    JavaApiFields.MaxPriceLevels.value: 1,
                    JavaApiFields.BookingType.value: "REG",
                    JavaApiFields.SettlCurrency.value: self.get_data_set().get_currency_by_name('currency_1'),
                    JavaApiFields.RouteID.value: 24,
                    JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value,
                    JavaApiFields.AccountGroupID.value: self.get_data_set().get_client_by_name('client_1'),
                    JavaApiFields.WashBookAccountID.value: self.get_data_set().get_washbook_account_by_name(
                        'washbook_account_3'),
                    JavaApiFields.PriceDelta.value: 0
                }
        }

    def set_default_modify(self, order_id, qty=100, price=20):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component(JavaApiFields.MultiLegOrderModificationRequestBlock.value,
                                        {
                                            JavaApiFields.OrdQty.value: qty,
                                            JavaApiFields.Price.value: price,
                                            JavaApiFields.OrdID.value: order_id
                                        })
        return self
