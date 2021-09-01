frappe.ui.form.on('Supplier Quotation', {
	refresh : function(frm){
			$('[data-fieldname="supplier_quotation_comparisons"] div.btn-open-row').hide()
	},
	onload_post_render: function(frm){
		$('[data-fieldname="supplier_quotation_comparisons"] div.btn-open-row').hide()
}
})