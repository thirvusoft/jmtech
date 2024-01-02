import frappe

def user_permission_create(doc, action):
    if doc.role_profile_name == "Sales User":
        user_permission_exists = frappe.db.exists(
			"User Permission", {"allow": "User", "for_value": doc.name, "user": doc.name}
		)
        if user_permission_exists:
            return
        else:
            permission_doc=frappe.new_doc("User Permission")
            permission_doc.user = doc.name
            permission_doc.allow = "User"
            permission_doc.for_value = doc.name
            permission_doc.save(ignore_permissions = True)
            
def role_profile_permission(user):
    if not user:
        user = frappe.session.user
    if user == "Administrator":
        return ''
    roleprofile=frappe.db.get_value("User", {"name":user}, "role_profile_name")
    if roleprofile:
        if frappe.db.get_value("Role Profile", roleprofile, "custom_super_admin") == 1:
            return ''
        else:
            return f"""(`tabRole Profile`.custom_super_admin = 0)"""

def has_role_profile_permission(doc, user):
    if (user or frappe.session.user) == "Administrator":
        return True
    roleprofile=frappe.db.get_value("User", {"name":user}, "role_profile_name")
    if roleprofile:
        if frappe.db.get_value("Role Profile", roleprofile, "custom_super_admin") == 1:
            return True
        else:
            if frappe.db.get_value("Role Profile", roleprofile, "custom_super_admin") == 0 and doc.custom_super_admin ==0:
                return True 
    return False