// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Follow Up Status"] = {
	"filters": [
		{
			fieldname: 'date',
			label: 'Date',
			fieldtype: 'Date',
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: 'user',
			label: 'Follow Up By',
			fieldtype: 'Link',
			options: 'User',
			default: frappe.session.user
		}
	]
};
