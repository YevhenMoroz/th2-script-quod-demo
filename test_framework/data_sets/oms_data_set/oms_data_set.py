from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsVenues, OmsClients, OmsAccounts, \
    OmsWashbookAccounts, OmsRecipients, OmsFixInstruments, OmsListingId, OmsInstrumentId, OmsMic, OmsCurrency, \
    OmsVenueClientNames, OmsRoutes, OmsLookupForVenues, OmsVenueClientAccounts, OMSCommissionProfiles, OMSFeeType, \
    OMSExecScope, OMSFee, OMSCommission, OmsRouteID, OMSFeeOrderScope, OMSPset, OmsCounterparts, OmsQtyTypes, \
    OMSBasketTemplates


class OmsDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    fix_instruments = OmsFixInstruments
    venues = OmsVenues
    clients = OmsClients
    accounts = OmsAccounts
    washbook_accounts = OmsWashbookAccounts
    recipients = OmsRecipients
    listing_id = OmsListingId
    instrument_id = OmsInstrumentId
    mic = OmsMic
    currency = OmsCurrency
    venue_client_names = OmsVenueClientNames
    routes = OmsRoutes
    route_id = OmsRouteID
    lookups = OmsLookupForVenues
    venue_client_accounts = OmsVenueClientAccounts
    commission_profiles = OMSCommissionProfiles
    misc_fee_type = OMSFeeType
    fee_exec_scope = OMSExecScope
    fee = OMSFee
    commission = OMSCommission
    fee_order_scope = OMSFeeOrderScope
    counterparts = OmsCounterparts
    qty_types = OmsQtyTypes
    pset = OMSPset
    basket_templates = OMSBasketTemplates
