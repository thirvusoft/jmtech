import frappe

def default_create():
    create_industry_type()
    create_inlet_water_type()

def create_industry_type():
    industry_type = ['Office/Industries/Warehouse/Commercial Building', 'Single house/Villas/Apartment/Gated Community', 'School/Colleges/Education Institution', 'Hotels/Restaurants/Resorts', 'Hospitals']
    for i in industry_type:
        if not frappe.db.exists('Type of Industry', i):
            ti = frappe.new.doc("Type of Industry")
            ti.industry = i
            ti.save()


def create_inlet_water_type():
    inlet_water_type = ['RO Water', 'Metro Water', 'Bore well', 'Well water']
    for i in inlet_water_type:
        if not frappe.db.exists('Inlet water type', i):
            iwt = frappe.new.doc("Inlet water type")
            iwt.inlet_type = i
            iwt.save()