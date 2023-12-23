# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe

def execute(filters = None):
	frappe.log_error(title='RR', message=frappe.request.host)
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [

		{
			'fieldname': 'name',
			'fieldtype': 'Data',
			'label': 'Lead ID',
			'width': 195
		},

		{
			'fieldname': 'lead_name',
			'fieldtype': 'Data',
			'label': 'Lead Name',
			'width': 195
		},

		{
			'fieldname': 'lead_owner',
			'fieldtype': 'Data',
			'label': 'Lead Owner',
			'width': 195
		},
		{
			'fieldname': 'status',
			'fieldtype': 'Data',
			'label': 'Status',
			'width': 182
		},

		{
			'fieldname': 'contact_number',
			'fieldtype': 'Data',
			'label': 'Contact Number',
			'width': 182
		},

		{
			'fieldname': 'remarks',
			'fieldtype': 'Data',
			'label': 'Remarks',
			'width': 400
		},

		{
			'fieldname':'description',
			'fieldtype':'Small Text',
			'label':'Description',
			'width':400
		},

		{
			'fieldname': 'for_number_card',
			'fieldtype': 'Int',
			'label': 'For Number Card',
			'hidden': 1,
		},
	]

	return columns

def get_data(filters):
	data=[]

	follow_up_filter = {}
	lead_filter = {'status':['not in', ['Do Not Contact']]}
	if(filters.get('date')):
		follow_up_filter['date'] = filters.get('date')
	if (filters.get('user')):
		follow_up_filter['followed_by'] = filters.get('user')

	all_leads = frappe.db.get_all('Follow-Up', filters=follow_up_filter, fields=['idx', 'parent','followed_by','description'])
	all_leads1=[]
	max_ids = {}

	for i in all_leads:
		follow_up_filter['parent'] = i['parent']
		if i['parent'] not in max_ids:
			max_ids[i['parent']] = max(frappe.db.get_all('Follow-Up', filters={'parent':i['parent']}, pluck='idx'))

		if(max_ids[i['parent']] == i['idx']):
			if(not i.get("followed_by")):
				all_leads1.append(i)
			elif(not filters.get("user")):
				all_leads1.append(i)
			elif(filters.get("user") and i.get("followed_by")==filters.get("user")):
				all_leads1.append(i)
	desc={i['parent']:[i['description'],i.get("followed_by") or ""] for i in all_leads1}

	leads = [i['parent'] for i in all_leads1]
	site_lead=leads
	lead_filter['name'] = ['in', site_lead]

	leads = frappe.db.get_all('Lead', filters=lead_filter, fields=['name', 'lead_name', 'lead_owner','status', 'custom_remarks as remarks'])

	for i in leads:
		i["for_number_card"] = 1
		i['description']=desc[i["name"]][0]
		i['next_followup_by']=desc[i["name"]][1]
		i['name'] = f'''<button class="btn btn-primary btn-sm primary-action" onclick='frappe.set_route("Form", "Lead", "{i["name"]}" )'>
							{i["name"]}
						</button>'''
		contact=frappe.get_all(
			"Contact",
				filters=[
				["Dynamic Link", "link_doctype", "=", 'Lead'],
				["Dynamic Link", "link_name", "=", i['name']],
				["Contact Phone", 'is_primary_mobile_no', "=", 1]

				],
				fields=['`tabContact Phone`.phone'],
				order_by='`tabContact`.creation desc'
			)
		if contact:
			i['contact_number']=contact[0]['phone']
	data+=leads

	
	return data
	
	