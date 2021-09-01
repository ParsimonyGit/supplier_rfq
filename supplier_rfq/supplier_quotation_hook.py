import frappe
from frappe.utils import add_to_date
from frappe import _
from erpnext.buying.report.supplier_quotation_comparison.supplier_quotation_comparison import execute 
from frappe.utils import add_days, today, nowdate, get_date_str,now

def onload(self,method):
    request_for_quotation=self.items[0].request_for_quotation
    if self.name and self.docstatus==1  and request_for_quotation:
        
        filters={
'company': self.company, 
'from_date': get_date_str(frappe.db.get_value('Request for Quotation', request_for_quotation, 'transaction_date')),
'to_date': nowdate(), 
'supplier': [], 
'supplier_quotation': [], 
'request_for_quotation': request_for_quotation, 
'group_by': 'Group by Item', 
'include_expired': 1}
        columns, data, message, chart_data= execute(filters)
        print('-'*100,'filters',filters)
        print('data',data,'columns',columns)
        if data:
            for row in data:
                self.append("supplier_quotation_comparisons",row)
                self.save(ignore_permissions=True)
                frappe.db.commit()                 
        # self.append("supplier_quotation_comparisons", {
        #         "ac_serial_no":serial_no,
        #         "truck_vin": installation_note.truck_vin_cf or '',
        #         "truck_number":installation_note.truck_number_cf or '',
        #         "installed_by":supervisor_name_cf or '',
        #         "installation_date":installation_note.inst_date or '',
        #         "remarks":installation_note.remarks or ''
        #     })  
        # frappe.msgprint(msg=_("Installation details are updated."), indicator='green',alert=True)
        # self.save(ignore_permissions=True)
        # frappe.db.commit()        