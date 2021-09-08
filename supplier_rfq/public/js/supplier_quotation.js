frappe.ui.form.on('Supplier Quotation', {
	refresh : function(frm){
			cur_frm.fields_dict.supplier_quotation_comparisons.grid.update_docfield_property("remarks","hidden",1)

			$('[data-fieldname="supplier_quotation_comparisons"] div.btn-open-row').hide()
			if (frm.doc.docstatus!=2 && frm.is_new()==undefined) {
				frm.add_custom_button(__('Refresh Supplier Comparison Data.'),
				function() {
					
					frappe.call('supplier_rfq.supplier_quotation_hook.update_supplier_comparison', {
						supplier_quotation_name: frm.doc.name
				}).then(r => {
						frm.reload_doc();
				})					
				
				}, __("Tools"));
			}
	},
	onload_post_render: function(frm){
		$('[data-fieldname="supplier_quotation_comparisons"] div.btn-open-row').hide()
}
})