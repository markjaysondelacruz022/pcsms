const common_setup = (frm) => {
    frm.filter_linked_field = (doc_field, child_doc_field, filters, is_reset_field) => {
        if (is_reset_field) {
            frm.set_value(doc_field, null);
        }
        if (child_doc_field) {
            frm.fields_dict[doc_field].grid.get_field(child_doc_field).get_query = (doc, cdt, cdn) => {
                return {filters : filters};
            }
        } else {
            frm.fields_dict[doc_field].get_query = (doc, cdt, cdn) => {
                return {filters : filters};
            }
        }
        frm.refresh_field(doc_field);
    }
    frm.remove_field_elements = (field_name, ...elements) => {
        elements.forEach(e => {
            const found_element = frm.fields_dict[field_name].$wrapper.find(e);
            if (found_element) {
                found_element.remove();
            }
        })
    }
}

const common_api_call = (frappe, frm) => {
    frm.api_call = (method, args, err_message) => {
        return new Promise(async (resolve, reject) => {

            const call_details = {
                method,
                callback: (res) => {
                    if (res && res.message) {
                        resolve(res.message);
                    } else {
                        reject(err_message);
                    }
                }
            }
            if (args) {
                call_details.args = args;
            }

            frappe.call(call_details);
        })
    };
    frm.get_academic_level_details = () => {
        return frm.api_call('pcsms.endpoint.scholarship.get_academic_level_group_details', null, 
        'Error fetching academic level group details');
    };
    frm.get_scholarship_programs = () => {
        return frm.api_call('pcsms.endpoint.scholarship.get_scholarship_programs', null, 
        'Error fetching scholarship programs');
    };
}