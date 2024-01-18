import frappe

def execute():
    leads = frappe.get_all("Lead", {"status": ["!=", "Closed"]})
    print(f"Total Leads: {len(leads)}")

    for lead in leads:
        doc = frappe.get_doc("Lead", lead.name)
        doc.append("custom_followup", {
            "date": "2024-01-22",
            "followed_by": doc.lead_owner,
            "next_follow_up_by": doc.lead_owner
        })
        doc.save()
