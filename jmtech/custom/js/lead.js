var original = cur_frm.add_custom_button;
cur_frm.add_custom_button = extendedFunc;
function extendedFunc(...args) {
    if (!["Customer", "Toggle Editable"].includes(args[0])) {
        return
    }
    original.call(cur_frm, ...args);
}

var markers = [], isEditable = false, write_fields = [];

frappe.ui.form.on("Lead", {
    refresh: function (frm) {
        if (!frm.is_new()) {
            if (!write_fields.length) {
                write_fields = cur_frm.fields.map((a) => a.disp_status == "Write" ? a.df.fieldname : undefined);
            }
            toggleEditFields(frm, isEditable);
            isEditable = !isEditable;
            frm.add_custom_button(('Toggle Editable'), function () {
                toggleEditFields(frm, isEditable);
                isEditable = !isEditable;
            });
        }
        var childTable = frm.doc.table_ibty;
        if (childTable && childTable.length > 0) {
            var buttonsHtml = '';
            for (var i = 0; i < childTable.length; i++) {
                var mobileNo = childTable[i].contact_number;
                var name = childTable[i].name1;
                if (mobileNo) {
                    var call = `tel:${mobileNo}`;
                    buttonsHtml += `<button onclick="window.location.href = '${call}'"> &#128222; ${name} - ${mobileNo}</button><br><br>`;
                }
            }

            frm.set_df_property('custom_phone_call', 'options', buttonsHtml);
        }
        markers.forEach(m => {
            m?.remove()
        })
        frm.fields_dict.lead_location.refresh();
        if (frm.doc.latitude && frm.doc.longitude) {
            frm.fields_dict.lead_location.map.setView([frm.doc.latitude, frm.doc.longitude], 13);
            markers.push(L.marker(L.latLng(frm.doc.latitude, frm.doc.longitude)).addTo(cur_frm.fields_dict.lead_location.map))
        }
    },
    after_save: function (frm) {
        frappe.set_route("List", "Lead");
    },
    get_current_location: async function (frm) {
        let cur_location = await get_location();
        frm.set_value('latitude', cur_location['latitude'])
        frm.set_value('longitude', cur_location['longitude'])
        frm.fields_dict.lead_location.map.setView([frm.doc.latitude, frm.doc.longitude], 13);
        markers.forEach(m => {
            m?.remove()
        })
        markers.push(L.marker(L.latLng(frm.doc.latitude, frm.doc.longitude)).addTo(cur_frm.fields_dict.lead_location.map))

    },
    custom_open_location: function(frm) {
        if (frm.doc.latitude && frm.doc.longitude) {
            window.open(`https://www.google.com/maps?q=${frm.doc.latitude},${frm.doc.longitude}`)
        } else {
            frm.scroll_to_field('get_current_location')
            frappe.show_alert({message: 'Please get the location', indicator: 'red'})
        }
    },
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

function check_location_permission() {
    if ("geolocation" in navigator) {
        // Geolocation is available
    } else {
        // Geolocation is not available
        window.alert("Geolocation is not supported in this browser.");
    }
}

async function get_location() {
    check_location_permission()
    async function getLocation() {
        let latitude, longitude;
        try {
            let position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject);
            });

            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
        } catch (error) {
            // Handle errors by displaying them as alerts
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    window.alert("User denied the request for Geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    window.alert("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    window.alert("The request to get user location timed out.");
                    break;
                default:
                    window.alert("An unknown error occurred.");
            }
        }
        return { "latitude": latitude, "longitude": longitude }
    }
    return await getLocation();
}


function toggleEditFields(frm, isEditable) {
    var fieldnames = Object.keys(frm.fields_dict);
    for (var i = 0; i < fieldnames.length; i++) {
        var fieldname = fieldnames[i];
        if (write_fields.includes(fieldname) && fieldname != 'custom_followup') {
            frm.toggle_enable(fieldname, isEditable);
            frm.refresh_field(fieldname)
        }
    }
}
