frappe.listview_settings['Scholar Application'] = {
    onload: (listview) => {
        let is_import_process = false;
        const import_progress_dialog = new frappe.ui.Dialog({
            title: 'Importing Scholar Application',
            fields: [
                {
                    label: 'Progress',
                    fieldname: 'progress',
                    fieldtype: 'HTML',
                    options: ''
                }
            ],
            // primary_action_label: 'Close',
            // primary_action: function () {
            //     dialog.hide();
            // }
        });
        var progress = $(`<div>
                            <div class="progress">
                                <div class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0"
                                    aria-valuemax="100"></div>
                            </div>
                            <div>
                                <span id="import_progress_message"></span>
                            </div>
                        </div>`);
        import_progress_dialog.fields_dict.progress.$wrapper.html(progress);
        import_progress_dialog.$wrapper.find('.modal-backdrop').unbind('click');
        

        const import_dialog = new frappe.ui.Dialog({
            title: __("Select an Excel File"),
            fields: [
                {
                    label: "Files",
                    fieldname: "file",
                    fieldtype: "HTML",
                    options: `<input type="file" id="file_input" accept=".xls,.xlsx" />`,
                }
            ],
            primary_action: function () {

                // frappe.msgprint('test');
                // frappe.preventDefault();
                const input_element = import_dialog.$wrapper.find('#file_input');
                const file = input_element[0].files[0];

                if (!file || file.length == 0) {
                    frappe.msgprint({
                        title: __('Error'),
                        message: __('Please upload a file'),
                        indicator: 'red',
                    });
                    return;
                }

                const reader = new FileReader();
                reader.onload = event => {
                    const byteArray = event.target.result;
                    import_dialog.hide();
                    import_progress_dialog.show();
                    is_import_process = true;
                    $('.modal-backdrop').unbind('click');
                    frappe.call({
                        method: 'pcsms.endpoint.excel.enqueue_import_scholar_application',
                        args: {
                            file_name: file.name,
                            file_data: btoa(String.fromCharCode.apply(null, new Uint8Array(byteArray)))
                        },
                        callback: (r) => {
                            

                        }
                    });


                }
                reader.readAsArrayBuffer(file);
            },
            primary_action_label: __('Load Data')
        });
        listview.page.add_inner_button(__('Import Applications'), function () {
            if (is_import_process && !import_progress_dialog.$wrapper.is(':visible')) {
                import_progress_dialog.show()
            } else {
                import_dialog.$wrapper.find('#file_input').val(null)
                import_dialog.show();
            }

        });

        frappe.realtime.on('import_process', (data) => {
            is_import_process = true;
            console.log(data);
            const progress_wrapper = import_progress_dialog.fields_dict.progress.$wrapper;
            const import_progress_div = progress_wrapper.find('.progress-bar');
            const import_progress_span = progress_wrapper.find('#import_progress_message');
            import_progress_div.css('width', data.progress + '%').attr('aria-valuenow', data.progress);
            import_progress_span.text(data.message);
            if (data.is_completed) {
                is_import_process = false;
                // import_progress_dialog.set_primary_action('Completed', () => {
                //     import_progress_dialog.hide();
                //     import_progress_div.css('width', '0%').attr('aria-valuenow', 0);
                //     import_progress_span.text('');
                // });
                setTimeout(() => {
                    import_progress_dialog.hide();
                    import_progress_div.css('width', '0%').attr('aria-valuenow', 0);
                    import_progress_span.text('');
                    if (data.message) {
                        frappe.msgprint({
                            title: __('Success'),
                            message: __(data.message),
                            indicator: 'green',
                        });
    
                        // frappe.msgprint(__(r.message));
                        listview.refresh();
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: __(data.message),
                            indicator: 'red',
                        });
                    }
                }, 2000);
                
            }

        });
    }
}