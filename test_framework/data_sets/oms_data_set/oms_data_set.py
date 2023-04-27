from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsVenues, OmsClients, OmsAccounts, \
    OmsWashbookAccounts, OmsRecipients, OmsFixInstruments, OmsListingId, OmsInstrumentId, OmsMic, OmsCurrency, \
    OmsVenueClientNames, OmsRoutes, OmsLookupForVenues, OmsVenueClientAccounts, OMSCommissionProfiles, OMSFeeType, \
    OMSExecScope, OMSFee, OMSCommission, OmsRouteID, OMSFeeOrderScope, OMSPset, OmsCounterparts, OmsQtyTypes, \
    OMSCommissionAndFeeBasis, OMSBasketTemplates, OMSGiveUpBrokers, OMSClientDesks, OMSBookingTicketFeeType, \
    OMSNetGrossInd, OMSStatus, OMSMatchStatus, OMSExecutionPolicy, OMSTimeInForce, OMSOrdType, OMSCapacity, \
    OMSBagScenario, OMSBagStrategy, OMSVenueID, OMSCounterpartID, OMSInstrType, OMSContraFirm, \
    OMSCommonVenueSecAccountNamesOfAcc, OMSClearingAccountTypes, VenueAccountIDSource, \
    OMSVenueListForCommissionAndFees, OMSWashBookRule, OMSReferencePrice, OMSClientListID, OMSISINSecurityAltIDs, \
    OMSSecurityIDSourceForListings, OMS_SymbolForListingsFromWebAdmin, OMSTickSizeProfile, OmsJavaApiInstruments, \
    OMSCounterPartyIDs_FIX, OMSCounterPartyIDs_JavaAPI, OMSVenueClientAccountName, OMSGatingRuleIDs, \
    OMSVenueAccountNamesOfSecurityAccounts, OMSCounterParty_JavaAPI_FOR_ES, OMSChargesType, OMSPartyRoles, \
    OMSCashAccountIDs


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
    counterpart = OmsCounterparts
    qty_types = OmsQtyTypes
    pset = OMSPset
    commission_basis = OMSCommissionAndFeeBasis
    basket_templates = OMSBasketTemplates
    give_up_brokers = OMSGiveUpBrokers
    client_desks = OMSClientDesks
    fee_type_in_booking_ticket = OMSBookingTicketFeeType
    net_gross_ind_type = OMSNetGrossInd
    middle_office_status = OMSStatus
    middle_office_match_status = OMSMatchStatus
    exec_policy = OMSExecutionPolicy
    time_in_force = OMSTimeInForce
    order_type = OMSOrdType
    capacity = OMSCapacity
    scenario = OMSBagScenario
    strategy = OMSBagStrategy
    venue_id = OMSVenueID
    counterpart_id = OMSCounterpartID
    cl_list_id = OMSClientListID
    instr_type = OMSInstrType
    contra_firm = OMSContraFirm
    reference_price = OMSReferencePrice
    washbook_rules = OMSWashBookRule
    all_venue_sec_account_names_of_acc = OMSCommonVenueSecAccountNamesOfAcc
    clearing_account_type = OMSClearingAccountTypes
    account_id_source = VenueAccountIDSource
    venue_list = OMSVenueListForCommissionAndFees
    oms_route_id = OmsRouteID
    isin_security_alt_ids = OMSISINSecurityAltIDs
    security_id_source = OMSSecurityIDSourceForListings
    symbols = OMS_SymbolForListingsFromWebAdmin
    tick_size_profile = OMSTickSizeProfile
    java_api_instruments = OmsJavaApiInstruments
    counterpart_id_fix = OMSCounterPartyIDs_FIX
    counterpart_id_java_api = OMSCounterPartyIDs_JavaAPI
    venue_client_account_name = OMSVenueClientAccountName
    gating_rule_ids = OMSGatingRuleIDs
    venue_account_name = OMSVenueAccountNamesOfSecurityAccounts
    counterpart_java_api_for_es = OMSCounterParty_JavaAPI_FOR_ES
    charges_type = OMSChargesType
    party_role = OMSPartyRoles
    cash_accounts = OMSCashAccountIDs

