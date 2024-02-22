frappe.ui.form.LeadQuickEntryForm = class LeadQuickEntryForm extends (frappe.ui.form.LeadQuickEntryForm ? frappe.ui.form.LeadQuickEntryForm : frappe.ui.form.QuickEntryForm) {
    render_dialog() {
        super.render_dialog();
        var me = this;
        var markers = [];
        this.dialog.get_field('get_current_location').input.onclick = async function () {
            let cur_location = await get_location();
            me.dialog.set_value('latitude', cur_location['latitude'])
            me.dialog.set_value('longitude', cur_location['longitude'])
            me.dialog.fields_dict.lead_location.map.setView([cur_location['latitude'], cur_location['longitude']], 13);
            markers.forEach(m => {
                m?.remove()
            })
            markers.push(L.marker(L.latLng(cur_location['latitude'], cur_location['longitude'])).addTo(me.dialog.fields_dict.lead_location.map))
        }
        this.dialog.get_field('lead_owner').get_query = function() {
            return {
                query: "jmtech.custom.py.lead.get_users"
            }
        }
    }
}

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
