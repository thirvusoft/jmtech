// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.query_reports["Missed Follow Ups"] = {
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
			fieldtype: 'Autocomplete',
			options: []
		}
	],
	onload: function(report){
		frappe.db.get_value("User", {"name": frappe.session.user}, "username", (r) => {
			frappe.query_report.set_filter_value('user', r.username);
		})

		frappe.call({
			method: "jmtech.jm_technologies.report.missed_follow_ups.missed_follow_ups.get_user_list",
			args: {user: frappe.session.user},
			callback(r){
				if ((r.message).length < 2){
					frappe.query_report.page.fields_dict.user.df.hidden = 1;
				}

				frappe.query_report.page.fields_dict.user.set_data(r.message);
				frappe.query_report.page.fields_dict.user.refresh();
			}
		});
	}
};
