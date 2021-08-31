// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

window.doc={{ doc.as_json() }};

$(document).ready(function() {
	new rfq();
	doc.supplier = "{{ doc.supplier }}"
	doc.currency = "{{ doc.currency }}"
	doc.number_format = "{{ doc.number_format }}"
	doc.buying_price_list = "{{ doc.buying_price_list }}"
});

rfq = Class.extend({
	init: function(){
		this.onfocus_select_all();
		this.change_qty();
		this.change_rate();
		this.terms();
		this.submit_rfq();
		this.navigate_quotations();
		this.upload_attachment();
		// this.upload_file()
	},

	onfocus_select_all: function(){
		$("input").click(function(){
			$(this).select();
		})
	},

	upload_attachment: function(){
		// vue js upload code
		$('.btn-upload-attachment').click(function(){
			new frappe.ui.FileUploader({
				on_success: (file_doc) => {
					console.log('file_doc',file_doc)
					this.attachment_uploaded(file_doc);
						doc.supplier_uploaded_attachment_cf = this.attachment_uploaded(file_doc);
				}
			});
		})

	},

	change_qty: function(){
		var me = this;
		$('.rfq-items').on("change", ".rfq-qty", function(){
			me.idx = parseFloat($(this).attr('data-idx'));
			me.qty = parseFloat($(this).val()) || 0;
			me.rate = parseFloat($(repl('.rfq-rate[data-idx=%(idx)s]',{'idx': me.idx})).val());
			me.update_qty_rate();
			$(this).val(format_number(me.qty, doc.number_format, 2));
		})
	},

	change_rate: function(){
		var me = this;
		$(".rfq-items").on("change", ".rfq-rate", function(){
			me.idx = parseFloat($(this).attr('data-idx'));
			me.rate = parseFloat($(this).val()) || 0;
			me.qty = parseFloat($(repl('.rfq-qty[data-idx=%(idx)s]',{'idx': me.idx})).val());
			me.update_qty_rate();
			$(this).val(format_number(me.rate, doc.number_format, 2));
		})
	},

	terms: function(){
		$(".supplier-notes").on("change", ".supplier-notes-feedback", function(){
			doc.supplier_notes = $(this).val();
		})
	},

	update_qty_rate: function(){
		var me = this;
		doc.grand_total = 0.0;
		$.each(doc.items, function(idx, data){
			if(data.idx == me.idx){
				data.qty = me.qty;
				data.rate = me.rate;
				data.amount = (me.rate * me.qty) || 0.0;
				$(repl('.rfq-amount[data-idx=%(idx)s]',{'idx': me.idx})).text(format_number(data.amount, doc.number_format, 2));
			}

			doc.grand_total += flt(data.amount);
			$('.tax-grand-total').text(format_number(doc.grand_total, doc.number_format, 2));
		})
	},
	submit_rfq: function(){
		var me = this;
		doc.company_terms=document.getElementsByClassName('company-terms')[0].innerHTML
		$('.btn-submit').click(function(){
			frappe.freeze();
			frappe.call({
				type: "POST",
				method: "supplier_rfq.templates.pages.rfq.create_supplier_quotation",
				args: {
					doc: doc
				},
				btn: this,
				callback: function(r){
					frappe.unfreeze();
					if(r.message){
						console.log(r,'r')
					

					me.upload_file(r)		
						
						// frappe.call({
						// 	type: 'POST',
						// 	method: "frappe.handler.upload_file",
						// 	args: {
						// 		file_url: document.getElementById("avatar").files[0].name,
						// 		doctype: 'Supplier Quotation',
						// 		docname: r.message.name
						// 	}
						// });						
						$('.btn-sm').hide()
						window.location.href = "/supplier-submitted-quotation?name=" + encodeURIComponent(r.message);
					}
				}
			})
		})
	},	
	upload_file: function(r){
						console.log('called')
						// upload file once doc is generated
							let file = $('#myfile').prop('files')[0];
							file = {
									file_obj: file,
									name: file.name,
									folder: 'Home/Attachments',
									doctype: 'Supplier Quotation',
									docname: r.message
							}
							console.log(file,'file')
							
							return new Promise((resolve, reject) => {
									let xhr = new XMLHttpRequest();
									xhr.upload.addEventListener('loadstart', (e) => {
											file.uploading = true;
									})
									xhr.upload.addEventListener('progress', (e) => {
											if (e.lengthComputable) {
													file.progress = e.loaded;
													file.total = e.total;
											}
									})
									xhr.upload.addEventListener('load', (e) => {
											file.uploading = false;
											resolve();
									})
									xhr.addEventListener('error', (e) => {
											file.failed = true;
											reject();
									})
									xhr.onreadystatechange = () => {
											if (xhr.readyState == XMLHttpRequest.DONE) {
													if (xhr.status === 200) {
															let r = null;
															let file_doc = null;
															try {
																	r = JSON.parse(xhr.responseText);
																	if (r.message.doctype === 'File') {
																			file_doc = r.message;
																	}
															} catch (e) {
																	r = xhr.responseText;
															}
			
															file.doc = file_doc;
			
															if (this.on_success) {
																	this.on_success(file_doc, r);
															}
													} else if (xhr.status === 403) {
															let response = JSON.parse(xhr.responseText);
															frappe.msgprint({
																	title: __('Not permitted'),
																	indicator: 'red',
																	message: response._error_message
															});
													} else {
															file.failed = true;
															let error = null;
															try {
																	error = JSON.parse(xhr.responseText);
															} catch (e) {
																	// pass
															}
															// frappe.request.cleanup({}, error);   
													}
											}
									}
									xhr.open('POST', '/api/method/upload_file', true);
									xhr.setRequestHeader('Accept', 'application/json');
									console.log('frappe.csrf_token',frappe.csrf_token)
									let form_data = new FormData();
									console.log('file1'.file)
									if (file.file_obj) {
											form_data.append('file', file.file_obj, file.name);
									}
									form_data.append('is_private', +file.private);
									form_data.append('folder', file.folder);
			
									if (file.file_url) {
											form_data.append('file_url', file.file_url);
									}
			
									if (file.doctype && file.docname) {
											form_data.append('doctype', file.doctype);
											form_data.append('docname', file.docname);
									}
									console.log('form_data',form_data)
									xhr.setRequestHeader('X-Frappe-CSRF-Token', frappe.csrf_token);

									xhr.send(form_data);
							});
	},


	navigate_quotations: function() {
		$('.quotations').click(function(){
			name = $(this).attr('idx')
			window.location.href = "/quotations/" + encodeURIComponent(name);
		})
	}
})
