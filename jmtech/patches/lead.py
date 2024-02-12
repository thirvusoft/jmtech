
import frappe
from frappe.utils import cint

def execute():
    leadlist = frappe.get_all("Lead", order_by="name")
    lead_id = '0'
    for i in leadlist:
        lead_number = i.name.split('-')[-1]
        if int(lead_number) > int(lead_id):
            lead_id = lead_number
        new_lead_name = f"L{lead_number}"
        frappe.rename_doc("Lead", i.name, new_lead_name, force=1)
        lead = frappe.get_doc('Lead',new_lead_name)
        frappe.db.set_value('Lead' ,new_lead_name, 'custom_display_title',f"{new_lead_name}-{lead.lead_name}", update_modified=False)
    Series = frappe.qb.DocType("Series")
    frappe.qb.update(Series).set(Series.current, cint(lead_id)).where(Series.name == 'L').run()
