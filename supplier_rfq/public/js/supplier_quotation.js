frappe.ui.form.on('Supplier Quotation', {
	refresh : function(frm){
			$('[data-fieldname="supplier_quotation_comparisons"] div.btn-open-row').hide()
			if (frm.doc.docstatus!=2) {
				frm.add_custom_button(__('Refresh Supplier Comparison Data.'),
				function() {
					frm.reload_doc();
				}, __("Tools"));
			}
	},
	onload_post_render: function(frm){
		$('[data-fieldname="supplier_quotation_comparisons"] div.btn-open-row').hide()
}
})