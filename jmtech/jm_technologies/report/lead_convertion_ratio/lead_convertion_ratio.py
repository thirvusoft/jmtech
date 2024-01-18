# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe

def execute(filters = None):
	columns = get_columns(filters)
	data = get_data(filters)
	chart_summary = get_chart_summary(data,filters)
	return columns, data, None, None, chart_summary

def get_chart_summary(data,filters):

	status1 = {
		'Open':0,
		'Replied':0,
		'Quotation Created':0,
		'Opportunity Closed':0,
		'Opportunity Open':0,
		'Do Not Disturb':0
	}

	for i in data:
		if(i.get('status') not in status1.keys()):
			status1[i.get('status')] = 1
		else:
			status1[i.get('status')] += 1
	status = status1.copy()
	for i in status1:
		if(status[i] == 0):
			status.pop(i)
	color =  {
		'Open':'purple',
		'Replied':'blue',
		'Quotation Created':'green',
		'Opportunity Closed':'red',
		'Opportunity Open':'cyan',
		'Do Not Disturb':'orange'
	}
	
	summary = []

	for i in status:
		summary.append(
		{
			"value":  status[i] or "Not Mentioned",
			"label": f'''<p><span style="color:{color.get(i).lower() if color.get(i) else ''}; font-weight: bold; font-size:20px;">{i }</span></p>''',
			"datatype": "Float",
		}
		)
	summary.append(
		{
			"value":  sum(status.values()) or 0,
			"label": f"<b style='font-size:20px;color:#ff5500'>Total Lead</b>",
			"datatype": "Float",
		}
		)
	return summary

def get_columns(filters):
	columns = [
	{
			'fieldname': 'id',
			'fieldtype': 'Link',
			'label': 'Lead ID',
			'options':'Lead',
			'width': 200
		},
		{
			'fieldname': 'name',
			'fieldtype': 'Data',
			'label': 'Lead Name',
			'width': 200
		},
		{
			'fieldname': 'owner',
			'fieldtype': 'Data',
			'label': 'Lead Owner',
			'width': 200
		},
		{
			'fieldname': 'territory',
			'fieldtype': 'Link',
			'label': 'Territory',
			'options': 'Territory',
			'width': 182,
			'hidden':1
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
	]

	return columns

def get_data(filters):
	data = []
	data = frappe.db.sql(f'''
		SELECT
			'Lead' as doctype,
			lead.name AS id,
			lead.lead_name as name,
			lead.lead_owner as owner,
			lead.status as status,
			lead.custom_remarks as remarks,
			(
				SELECT follow.description
				FROM `tabFollow-Up` AS follow
				WHERE follow.parent = lead.name
				ORDER BY follow.idx DESC
				LIMIT 1
			) AS description,
			(
				SELECT (CASE WHEN IFNULL(contact.mobile_no) != '' THEN contact.mobile_no
					  ELSE IFNULL(
						(SELECT phone.phone FROM `tabContact Phone` phone where phone.parenttype = 'Contact' AND phone.parent = contact.name AND phone.parentfield = 'phone_nos' ORDER BY idx ASC LIMIT 1),
						''
						)
					  END
					  ) mobile_no
				FROM `tabContact` AS contact
				INNER JOIN `tabDynamic Link` AS dynamiclink ON contact.name = dynamiclink.parent
				WHERE dynamiclink.link_name = lead.name
				AND dynamiclink.link_doctype = 'Lead'
				ORDER BY contact.creation DESC
				LIMIT 1
			) AS contact_number
		FROM `tabLead` AS lead
		WHERE lead.creation BETWEEN '{filters.get("from_date")}' AND DATE_ADD('{filters.get("to_date")}', INTERVAL 1 DAY)
	''', as_dict=1)


	return data