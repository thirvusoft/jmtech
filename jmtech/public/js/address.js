frappe.ui.form.AddressQuickEntryForm = class AddressQuickEntryForm extends (frappe.ui.form.AddressQuickEntryForm ? frappe.ui.form.AddressQuickEntryForm : frappe.ui.form.QuickEntryForm) {
    render_dialog() {
        super.render_dialog();
        setTimeout(() => {
            this.dialog.get_field("link_doctype").set_value(frappe.dynamic_link.doctype);
            setTimeout(() => {
                this.dialog.get_field("link_name").set_value(frappe.dynamic_link.doc[frappe.dynamic_link.fieldname]);
            }, 100)
        }, 1)
    }
}