import frappe
from frappe.modules.import_file import import_file_by_path
from frappe.utils import get_bench_path
import os
from os.path import join


def after_migrations():
	supplier_rfq_app_folder_path='/apps/supplier_rfq/supplier_rfq/import_records'

	if(not frappe.db.exists('Custom Field','Supplier Quotation-supplier_uploaded_attachment_cf')):
		fname="custom_field.json"
		import_folder_path="{bench_path}/{app_folder_path}".format(bench_path=get_bench_path(),app_folder_path=supplier_rfq_app_folder_path)
		make_records(import_folder_path,fname)

	if(not frappe.db.exists('Property Setter','Supplier Quotation-terms-label')):
		fname="property_setter.json"
		import_folder_path="{bench_path}/{app_folder_path}".format(bench_path=get_bench_path(),app_folder_path=supplier_rfq_app_folder_path)
		make_records(import_folder_path,fname)


def make_records(path, fname):
	if os.path.isdir(path):
		import_file_by_path("{path}/{fname}".format(path=path, fname=fname))