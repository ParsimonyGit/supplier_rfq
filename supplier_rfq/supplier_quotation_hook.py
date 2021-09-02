import frappe
from frappe.utils import add_to_date
from frappe import _
from erpnext.buying.report.supplier_quotation_comparison.supplier_quotation_comparison import execute 
from frappe.utils import add_days, today, nowdate, get_date_str,now


@frappe.whitelist()
def update_supplier_comparison(supplier_quotation_name):
    supplier_quotation=frappe.get_doc('Supplier Quotation',supplier_quotation_name)
    request_for_quotation=supplier_quotation.items[0].request_for_quotation
    if supplier_quotation.name and supplier_quotation.docstatus!=2  and request_for_quotation:
        filters={
                'company': supplier_quotation.company, 
                'from_date': get_date_str(frappe.db.get_value('Request for Quotation', request_for_quotation, 'transaction_date')),
                'to_date': nowdate(), 
                'supplier': [], 
                'supplier_quotation': [], 
                'request_for_quotation': request_for_quotation, 
                'group_by': 'Group by Item', 
                'include_expired': 1
                }
        columns, data, message, chart_data= execute(filters)
        updated=False
        if data:
            for row in data:
                if row and len(row) >0:
                    supplier_quotation.append("supplier_quotation_comparisons",row)
                    supplier_quotation.save(ignore_permissions=True)
                    frappe.db.commit() 
                    updated=True                
        if updated==True:
            frappe.msgprint(msg=_("Supplier quotation comparison is updated."), indicator='green',alert=True)

    elif not request_for_quotation:
        frappe.msgprint(msg=_("There is no supplier quotation to refresh."), indicator='yellow',alert=True)