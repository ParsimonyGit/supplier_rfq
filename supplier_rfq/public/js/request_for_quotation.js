frappe.ui.form.on('Request for Quotation', {
	refresh : function(frm){
			$('[data-fieldname="supplier_quotation_comparisons"] button.grid-remove-rows').hide()
			$('[data-fieldname="supplier_quotation_comparisons"] button.grid-add-row').hide()
			if (frm.doc.docstatus!=2 && frm.is_new()==undefined) {
				frm.add_custom_button(__('Refresh Supplier Comparison Data.'),
				function() {
					
					frappe.call('supplier_rfq.supplier_quotation_hook.update_supplier_comparison_for_rfq', {
						request_for_quotation_name: frm.doc.name
				}).then(r => {
						frm.reload_doc();
				})					
				
				}, __("Tools"));
			}
	},
	onload_post_render: function(frm){
		$('[data-fieldname="supplier_quotation_comparisons"] button.grid-remove-rows').hide()
		$('[data-fieldname="supplier_quotation_comparisons"] button.grid-add-row').hide()
}
})