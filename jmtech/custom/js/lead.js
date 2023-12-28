frappe.ui.form.on("Lead", {
    custom_view_follow_up_details: function (frm) {
        if ((frm.doc.custom_followup || []).length == 0) {
            frappe.show_alert({
                message: "No Follow Up Details.",
                indicator: "red"
            });
            return;
        }

        let data = `
        <table style="font-size:14px; border:1px solid black;width:100%">
			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
                    <center>
                        S.No
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px;">
                    <center>
                        Date
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px;">
                    <center>
                        Mode of Communication
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px;">
                    <center>
                        Followed By
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px;">
                    <center>
                        Description
                    </center>
				</td>
			</tr>
		`

        frm.doc.custom_followup.forEach(row => {
            data += `
			<tr style="border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px; word-break: break-word;">
                    <center>
                        ${row.idx || ""}
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px; word-break: break-word;">
                    <center>
                        ${frappe.format(row.date, { fieldtype: 'Date' })}
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px; word-break: break-word;">
                    <center>
                        ${row.mode_of_communication || ""}
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px; word-break: break-word;">
                    <center>
                        ${row.user_name || ""}
                    </center>
				</td>
				<td style="border:1px solid black; padding:5px; word-break: break-word;">
                    <center>
                        ${row.description || ""}
                    </center>
				</td>
			</tr>
			`
        });

        data += `</table>`
        var d = new frappe.ui.Dialog({
            title: __("Follow Up Details"),
            size: "extra-large",
            fields: [
                {
                    fieldname: 'html_data',
                    fieldtype: "HTML",
                    options: data
                }
            ]
        });
        d.show();
    },

    validate: function (frm) {
        var primaryMobileCount = 0;
        var primaryMobileNumber = null;
        $.each(frm.doc.table_ibty || [], function (i, row) {
            if (row.is_primary_mobile) {
                primaryMobileCount++;
                primaryMobileNumber = row.contact_number;
            }
        });
        if (primaryMobileCount == 1) {
            frm.doc.mobile_no = primaryMobileNumber;
        } else if (primaryMobileCount > 1) {
            frappe.msgprint(__('Only one mobile number can be the primary number.'));
            frappe.validated = false;
        }
    }
});

var original = cur_frm.add_custom_button;
cur_frm.add_custom_button = extendedFunc;
function extendedFunc(...args) {
    if (!["Customer"].includes(args[0])) {
        return
    }
    original.call(cur_frm, ...args);
}

