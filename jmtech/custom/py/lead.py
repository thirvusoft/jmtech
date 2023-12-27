import frappe
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
        existing_lead_contact = frappe.get_all('Dynamic Link', filters={'link_name': self.name}, fields=['name', 'parent'])
        if existing_lead_contact:
            lead_contact = frappe.get_doc("Contact", existing_lead_contact[0].parent)
            lead_contact.phone_nos = []
            lead_contact.email_ids = []
            for i in self.table_ibty:
                lead_contact.append("phone_nos", {
                    "phone": i.contact_number,
                    "is_primary_mobile_no": i.is_primary_mobile
                })
                lead_contact.append("email_ids", {
                    "email_id": i.email_id,
                    "is_primary": i.is_primary_mobile
                })
            lead_contact.save()
        else:
            contact = frappe.new_doc("Contact")
            contact.first_name = self.first_name or self.company_name

            for i in self.table_ibty:
                contact.append("phone_nos", {
                    "phone": i.contact_number,
                    "is_primary_mobile_no": i.is_primary_mobile
                })
                contact.append("email_ids", {
                    "email_id": i.email_id,
                    "is_primary": i.is_primary_mobile
                })
            contact.append("links", {
                "link_doctype": "Lead",
                "link_name": self.name
            })
            contact.save()

    if self.custom_followup:
        last_followup = self.custom_followup[-1]
        if last_followup.get('status'):
            self.status = last_followup.get('status')

