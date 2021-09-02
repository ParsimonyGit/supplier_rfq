import frappe
from frappe.utils import add_to_date
from frappe import _
from erpnext.buying.report.supplier_quotation_comparison.supplier_quotation_comparison import execute 
from frappe.utils import add_days, today, nowdate, get_date_str,now

def onload(self,method):
    request_for_quotation=self.items[0].request_for_quotation
    if self.name and self.docstatus!=2  and request_for_quotation and len(self.supplier_quotation_comparisons)==0:
        filters={
                'company': self.company, 
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
                    self.append("supplier_quotation_comparisons",row)
                    self.save(ignore_permissions=True)
                    frappe.db.commit() 
                    updated=True                
        if updated==True:
            frappe.msgprint(msg=_("Supplier quotation comparison is updated."), indicator='green',alert=True)