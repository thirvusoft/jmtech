import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def after_migrate():
    lead_property_setter()

def lead_property_setter():
    make_property_setter("Lead", "status", "options", "Lead\nReplied\nQuotation\nLost Quotation\nInterested\nConverted\nDo Not Contact\nSite Visited", "Small Text")