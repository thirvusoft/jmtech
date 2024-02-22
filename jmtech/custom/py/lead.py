from erpnext.crm.doctype.lead.lead import Lead
import frappe
from frappe.utils import cint
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def get_data(data=None):
    return {
        "fieldname": "lead",
        "non_standard_fieldnames": {"Customer": "lead_name"},
        "transactions": [
            {"items": ["Customer"]},
        ],
    }


def lead_contact(self, event):
    if self.table_ibty:
        existing_lead_contact = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Lead', 'link_name': self.name}, fields=['name', 'parent'])
        if existing_lead_contact:
            lead_contact = frappe.get_doc("Contact", existing_lead_contact[0].parent)
            lead_contact.phone_nos = []
            lead_contact.email_ids = []
            for i in self.table_ibty:
                if i.contact_number:
                    lead_contact.append("phone_nos", {
                        "phone": i.contact_number,
                        "is_primary_mobile_no": i.is_primary_mobile
                    })
                if i.email_id:
                    lead_contact.append("email_ids", {
                        "email_id": i.email_id,
                        "is_primary": i.is_primary_mobile
                    })
            lead_contact.save()
        else:
            contact = frappe.new_doc("Contact")
            contact.first_name = self.first_name or self.company_name

            for i in self.table_ibty:
                if i.contact_number:
                    contact.append("phone_nos", {
                        "phone": i.contact_number,
                        "is_primary_mobile_no": i.is_primary_mobile
                    })
                if i.email_id:
                    contact.append("email_ids", {
                        "email_id": i.email_id,
                        "is_primary": i.is_primary_mobile
                    })
            contact.append("links", {
                "link_doctype": "Lead",
                "link_name": self.name
            })
            contact.save()
    else:
        existing_lead_contact = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Lead', 'link_name': self.name}, fields=['name', 'parent'])
        if existing_lead_contact:
            for lead in existing_lead_contact:
                try:
                    frappe.delete_doc("Contact", lead.name)
                except:
                    frappe.log_error()

    if self.custom_followup:
        
        last_followup = self.custom_followup[-1]
        if last_followup.get('status'):
            self.status = last_followup.get('status')

def title(self,event,old =None,new =None,merge =None):
    self.db_set("custom_display_title", f"{self.name}-{self.lead_name}")
    self.reload()

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_users(doctype, txt, searchfield, start, page_len, filters):
    STANDARD_USERS = ("Guest", "Administrator")

    from frappe.desk.reportview import get_filters_cond

    doctype = "User"
    conditions = []

    user_type_condition = "and user_type != 'Website User'"
    if filters and filters.get("ignore_user_type") and frappe.session.data.user_type == "System User":
        user_type_condition = ""
    filters and filters.pop("ignore_user_type", None)

    txt = f"%{txt}%"
    return frappe.db.sql(
        """SELECT `name`, CONCAT_WS(' ', first_name, middle_name, last_name)
        FROM `tabUser`
        WHERE `enabled`=1
            {user_type_condition}
            AND `docstatus` < 2
            AND `name` NOT IN ({standard_users})
            AND ({key} LIKE %(txt)s
                OR CONCAT_WS(' ', first_name, middle_name, last_name) LIKE %(txt)s)
            {fcond}
        ORDER BY
            CASE WHEN `name` LIKE %(txt)s THEN 0 ELSE 1 END,
            CASE WHEN concat_ws(' ', first_name, middle_name, last_name) LIKE %(txt)s
                THEN 0 ELSE 1 END,
            NAME asc
        LIMIT %(page_len)s OFFSET %(start)s
    """.format(
            user_type_condition=user_type_condition,
            standard_users=", ".join(frappe.db.escape(u) for u in STANDARD_USERS),
            key=searchfield,
            fcond=get_filters_cond(doctype, filters, conditions),
        ),
        dict(start=start, page_len=page_len, txt=txt),
    )

class _Lead(Lead):
    def check_permission(self, permtype="read", permlevel=None):
        make_property_setter("Lead", 'lead_owner', 'ignore_user_permissions', 1, 'Check')
        make_property_setter("Lead", 'custom_assigned_to', 'ignore_user_permissions', 1, 'Check')
        value = super().check_permission(permtype, permlevel)
        make_property_setter("Lead", 'lead_owner', 'ignore_user_permissions', 0, 'Check')
        make_property_setter("Lead", 'custom_assigned_to', 'ignore_user_permissions', 0, 'Check')
        return value
    