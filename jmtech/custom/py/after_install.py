import frappe

def default_create():
    create_industry_type()
    create_inlet_water_type()
    create_role()
    create_role_profile()

def create_industry_type():
    industry_type = ['Office/Industries/Warehouse/Commercial Building', 'Single house/Villas/Apartment/Gated Community', 'School/Colleges/Education Institution', 'Hotels/Restaurants/Resorts', 'Hospitals']
    for i in industry_type:
        if not frappe.db.exists('Type of Industry', i):
            ti = frappe.new_doc("Type of Industry")
            ti.industry = i
            ti.save()


def create_inlet_water_type():
    inlet_water_type = ['RO Water', 'Metro Water', 'Bore well', 'Well water']
    for i in inlet_water_type:
        if not frappe.db.exists('Inlet water type', i):
            iwt = frappe.new_doc("Inlet water type")
            iwt.inlet_type = i
            iwt.save()
 
def create_role():
    if(not frappe.db.exists('Role', 'JM Super Admin')):
        new_doc=frappe.new_doc("Role")
        new_doc.update({
            "role_name":"JM Super Admin",
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    if(not frappe.db.exists('Role', 'JM Admin')):
        new_doc=frappe.new_doc("Role")
        new_doc.update({
            "role_name":"JM Admin",
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    if(not frappe.db.exists('Role', 'JM Sales Head')):
        new_doc=frappe.new_doc("Role")
        new_doc.update({
            "role_name":"JM Sales Head",
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    if(not frappe.db.exists('Role', 'JM Sales User')):
        new_doc=frappe.new_doc("Role")
        new_doc.update({
            "role_name":"JM Sales User",
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
                   
def create_role_profile():
    if(not frappe.db.exists('Role Profile', 'Super Admin')):
        new_doc=frappe.new_doc("Role Profile")
        roles=["Sales User", "JM Super Admin", "Sales Manager", "Thirvu Admin", "Thirvu CRM"]
        role_list=[]
        for role in roles:
            role_dict = frappe._dict({
                    "role": role,
                })
            role_list.append(role_dict)
        new_doc.update({
            "role_profile":"Super Admin",
            "roles":role_list,
            "custom_super_admin":1
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    if(not frappe.db.exists('Role Profile', 'Admin')):
        new_doc=frappe.new_doc("Role Profile")
        roles=["Sales User", "JM Admin", "Sales Manager", "Thirvu Admin", "Thirvu CRM"]
        role_list=[]
        for role in roles:
            role_dict = frappe._dict({
                    "role": role,
                })
            role_list.append(role_dict)
        new_doc.update({
            "role_profile":"Admin",
            "roles":role_list
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    if(not frappe.db.exists('Role Profile', 'Sales Head')):
        new_doc=frappe.new_doc("Role Profile")
        roles=["Sales User", "JM Sales Head", "Thirvu CRM"]
        role_list=[]
        for role in roles:
            role_dict = frappe._dict({
                    "role": role,
                })
            role_list.append(role_dict)
        new_doc.update({
            "role_profile":"Sales Head",
            "roles":role_list
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    if(not frappe.db.exists('Role Profile', 'Sales User')):
        new_doc=frappe.new_doc("Role Profile")
        roles=["Sales User", "JM Sales User", "Thirvu CRM"]
        role_list=[]
        for role in roles:
            role_dict = frappe._dict({
                    "role": role,
                })
            role_list.append(role_dict)
        new_doc.update({
            "role_profile":"Sales User",
            "roles":role_list
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()