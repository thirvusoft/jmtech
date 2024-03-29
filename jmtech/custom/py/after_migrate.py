# import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_migrate():
    lead_property_setter()
    followup_table_property_setter()

def lead_property_setter():
    make_property_setter("Lead", "status", "options", 'Open\nSite visit\nGeneral visit\nActive\nQuotation\nClosed\nWaiting for customer reply\nNot interested\nMissed\nCall not taken', "Select")

def followup_table_property_setter():
    make_property_setter("Follow-Up", "status", "options", 'Open\nSite visit\nGeneral visit\nActive\nQuotation\nClosed\nWaiting for customer reply\nNot interested\nMissed\nCall not taken', "Select")

# def user_property_setter():
#     make_property_setter("User", "roles_html", "permlevel", 2, "Int")
#     make_property_setter("User", "module_profile", "default", "CRM", "Small Text")
#     make_property_setter("User", "role_profile_name", "default", "CRM", "Small Text")
    