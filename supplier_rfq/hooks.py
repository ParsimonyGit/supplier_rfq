from __future__ import unicode_literals
from frappe import _


app_name = "supplier_rfq"
app_title = "Supplier Rfq"
app_publisher = "GreyCube Technologies"
app_description = "custom RFQ feature for supplier"
app_icon = "octicon octicon-law"
app_color = "green"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/supplier_rfq/css/supplier_rfq.css"
# app_include_js = "/assets/supplier_rfq/js/supplier_rfq.js"

# include js, css files in header of web template
# web_include_css = "/assets/supplier_rfq/css/supplier_rfq.css"
# web_include_js = "/assets/supplier_rfq/js/supplier_rfq.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "supplier_rfq/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

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
website_route_rules = [
	{"from_route": "/rfq", "to_route": "Request for Quotation"},
	{"from_route": "/rfq/<path:name>", "to_route": "rfq",
		"defaults": {
			"doctype": "Request for Quotation",
			"parents": [{"label": _("Request for Quotation"), "route": "rfq"}]
		}
	},
	# {"from_route": "/supplier-quotations", "to_route": "Supplier Quotation"},
	# {"from_route": "/supplier-quotations/<path:name>", "to_route": "supplier-submitted-quotation",
	# 	"defaults": {
	# 		"doctype": "Supplier Quotation",
	# 		"parents": [{"label": _("Supplier Quotation"), "route": "supplier-submitted-quotation"}]
	# 	}
	# }	
]
website_redirects = [
    {"source": "supplier-quotations", "target": "supplier-submitted-quotation"}
]

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "supplier_rfq.install.before_install"
# after_install = "supplier_rfq.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "supplier_rfq.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"supplier_rfq.tasks.all"
# 	],
# 	"daily": [
# 		"supplier_rfq.tasks.daily"
# 	],
# 	"hourly": [
# 		"supplier_rfq.tasks.hourly"
# 	],
# 	"weekly": [
# 		"supplier_rfq.tasks.weekly"
# 	]
# 	"monthly": [
# 		"supplier_rfq.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "supplier_rfq.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "supplier_rfq.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "supplier_rfq.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"supplier_rfq.auth.validate"
# ]

