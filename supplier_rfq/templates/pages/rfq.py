# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# from erpnext.buying.doctype.request_for_quotation.request_for_quotation import add_items
import frappe, json
from frappe import _
from frappe.utils import formatdate
from erpnext.controllers.website_list_for_contact import get_customers_suppliers
from six import string_types
from erpnext.accounts.party import get_party_account_currency
from frappe.handler import ALLOWED_MIMETYPES
from frappe.utils import cint
from frappe import _, is_whitelisted

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.name)
	context.parents = frappe.form_dict.parents
	context.doc.supplier = get_supplier()
	context.doc.rfq_links = get_link_quotation(context.doc.supplier, context.doc.name)
	unauthorized_user(context.doc.supplier)
	update_supplier_details(context)
	context["title"] = frappe.form_dict.name

def get_supplier():
	doctype = frappe.form_dict.doctype
	parties_doctype = 'Request for Quotation Supplier' if doctype == 'Request for Quotation' else doctype
	customers, suppliers = get_customers_suppliers(parties_doctype, frappe.session.user)

	return suppliers[0] if suppliers else ''

def check_supplier_has_docname_access(supplier):
	status = True
	if frappe.form_dict.name not in frappe.db.sql_list("""select parent from `tabRequest for Quotation Supplier`
		where supplier = %s""", (supplier,)):
		status = False
	return status

def unauthorized_user(supplier):
	status = check_supplier_has_docname_access(supplier) or False
	if status == False:
		frappe.throw(_("Not Permitted"), frappe.PermissionError)

def update_supplier_details(context):
	supplier_doc = frappe.get_doc("Supplier", context.doc.supplier)
	context.doc.currency = supplier_doc.default_currency or frappe.get_cached_value('Company',  context.doc.company,  "default_currency")
	context.doc.currency_symbol = frappe.db.get_value("Currency", context.doc.currency, "symbol", cache=True)
	context.doc.number_format = frappe.db.get_value("Currency", context.doc.currency, "number_format", cache=True)
	context.doc.buying_price_list = supplier_doc.default_price_list or ''

def get_link_quotation(supplier, rfq):
	quotation = frappe.db.sql(""" select distinct `tabSupplier Quotation Item`.parent as name,
		`tabSupplier Quotation`.status, `tabSupplier Quotation`.transaction_date from
		`tabSupplier Quotation Item`, `tabSupplier Quotation` where `tabSupplier Quotation`.docstatus < 2 and
		`tabSupplier Quotation Item`.request_for_quotation =%(name)s and
		`tabSupplier Quotation Item`.parent = `tabSupplier Quotation`.name and
		`tabSupplier Quotation`.supplier = %(supplier)s order by `tabSupplier Quotation`.creation desc""",
		{'name': rfq, 'supplier': supplier}, as_dict=1)

	for data in quotation:
		data.transaction_date = formatdate(data.transaction_date)

	return quotation or None

# This method is used to make supplier quotation from supplier's portal.
@frappe.whitelist()
def create_supplier_quotation(doc):
	print('+'*100)
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	try:
		sq_doc = frappe.get_doc({
			"doctype": "Supplier Quotation",
			"supplier": doc.get('supplier'),
			"supplier_notes": doc.get("supplier_notes"),
			"terms": doc.get("company_terms"),
			"supplier_uploaded_attachment_cf":doc.get("supplier_uploaded_attachment_cf"),
			"company": doc.get("company"),
			"currency": doc.get('currency') or get_party_account_currency('Supplier', doc.get('supplier'), doc.get('company')),
			"buying_price_list": doc.get('buying_price_list') or frappe.db.get_value('Buying Settings', None, 'buying_price_list')
		})
		add_items(sq_doc, doc.get('supplier'), doc.get('items'))
		sq_doc.flags.ignore_permissions = True
		sq_doc.run_method("set_missing_values")
		sq_doc.save()
		frappe.msgprint(_("Supplier Quotation {0} Created").format(sq_doc.name))
		return sq_doc.name
	except Exception:
		return None


def add_items(sq_doc, supplier, items):
	for data in items:
		if data.get("qty") > 0:
			if isinstance(data, dict):
				data = frappe._dict(data)
			create_rfq_items(sq_doc, supplier, data)

def create_rfq_items(sq_doc, supplier, data):
	args = {}

	for field in ['item_code', 'item_name', 'description', 'qty', 'rate', 'conversion_factor',
		'warehouse', 'material_request', 'material_request_item', 'stock_qty','schedule_date']:
		args[field] = data.get(field)

	args.update({
		"request_for_quotation_item": data.name,
		"request_for_quotation": data.parent,
		"project":frappe.db.get_value("Request for Quotation",data.parent, "project_cf"),
		"supplier_part_no": frappe.db.get_value("Item Supplier",
			{'parent': data.item_code, 'supplier': supplier}, "supplier_part_no")
	})

	sq_doc.append('items', args)		


@frappe.whitelist(allow_guest=True)
def upload_file():
	user = None
	if frappe.session.user == 'Guest':
		if frappe.get_system_settings('allow_guests_to_upload_files'):
			ignore_permissions = True
		else:
			return
	else:
		user = frappe.get_doc("User", frappe.session.user)
		ignore_permissions = True

	files = frappe.request.files
	is_private = frappe.form_dict.is_private
	doctype = frappe.form_dict.doctype
	docname = frappe.form_dict.docname
	fieldname = frappe.form_dict.fieldname
	file_url = frappe.form_dict.file_url
	folder = frappe.form_dict.folder or 'Home'
	method = frappe.form_dict.method
	content = None
	filename = None

	if 'file' in files:
		file = files['file']
		content = file.stream.read()
		filename = file.filename

	frappe.local.uploaded_file = content
	frappe.local.uploaded_filename = filename

	if frappe.session.user == 'Guest' or (user and not user.has_desk_access()):
		import mimetypes
		filetype = mimetypes.guess_type(filename)[0]
		if filetype not in ALLOWED_MIMETYPES:
			frappe.throw(_("You can only upload JPG, PNG, PDF, or Microsoft documents."))

	if method:
		method = frappe.get_attr(method)
		is_whitelisted(method)
		return method()
	else:
		ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
			"attached_to_field": fieldname,
			"folder": folder,
			"file_name": filename,
			"file_url": file_url,
			"is_private": cint(is_private),
			"content": content
		})
		ret.save(ignore_permissions=ignore_permissions)
		frappe.db.set_value(doctype, docname, 'supplier_uploaded_attachment_cf', ret.file_url)

		return ret	