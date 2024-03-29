app_name = "jmtech"
app_title = "JM Technologies"
app_publisher = "Thirvusoft"
app_description = "JM Technologies"
app_email = "admin@thirvusoft.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/jmtech/css/jmtech.css"
app_include_js = [
    "/assets/jmtech/js/address.js",
    "/assets/jmtech/js/lead.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/jmtech/css/jmtech.css"
# web_include_js = "/assets/jmtech/js/jmtech.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "jmtech/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Lead" : "custom/js/lead.js"
}
# doctype_list_js = {"Lead" : "custom/js/lead_listview.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "jmtech/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "jmtech.utils.jinja_methods",
#	"filters": "jmtech.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "jmtech.install.before_install"
# after_install = "jmtech.install.after_install"
after_migrate ="jmtech.custom.py.after_migrate.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "jmtech.uninstall.before_uninstall"
# after_uninstall = "jmtech.uninstall.after_uninstall"
after_install = ["jmtech.custom.py.after_install.default_create"]



# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "jmtech.utils.before_app_install"
# after_app_install = "jmtech.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "jmtech.utils.before_app_uninstall"
# after_app_uninstall = "jmtech.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jmtech.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Role Profile": "jmtech.custom.py.user.role_profile_permission",
}
#
has_permission = {
	"Role Profile": "jmtech.custom.py.user.has_role_profile_permission",
}

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Lead": "jmtech.custom.py.lead._Lead"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Lead": {
		"on_update": ["jmtech.custom.py.lead.lead_contact","jmtech.custom.py.lead.title"],
        "after_rename": "jmtech.custom.py.lead.title"
	},
	"User":{
		"on_update":"jmtech.custom.py.user.user_permission_create"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"jmtech.tasks.all"
#	],
#	"daily": [
#		"jmtech.tasks.daily"
#	],
#	"hourly": [
#		"jmtech.tasks.hourly"
#	],
#	"weekly": [
#		"jmtech.tasks.weekly"
#	],
#	"monthly": [
#		"jmtech.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "jmtech.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "jmtech.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Lead": "jmtech.custom.py.lead.get_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["jmtech.utils.before_request"]
# after_request = ["jmtech.utils.after_request"]

# Job Events
# ----------
# before_job = ["jmtech.utils.before_job"]
# after_job = ["jmtech.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"jmtech.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
#	"Logging DocType Name": 30  # days to retain logs
# }

