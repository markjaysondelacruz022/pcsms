// Copyright (c) 2023, Xurpas Inc. and contributors
// For license information, please see license.txt
frappe.ui.form.on("Scholar Application", {
    setup: (frm) => {
        common_setup(frm);
        common_api_call(frappe, frm);
        frm.academic_level_details = [];
        frm.scholarship_programs = [];
        frm.form_fields_refresh = () => {
            
            frm.set_df_property('applicant', 'only_select', true);
            frm.set_df_property('type_of_application', 'only_select', true);
            frm.set_df_property('scholarship_program', 'only_select', true);
            frm.set_df_property('academic_grade_level', 'only_select', true);
            frm.set_df_property('course', 'only_select', true);
            frm.set_df_property('academic_level_type', 'only_select', true);
            frm.remove_field_elements('applicant', '.link-btn');
            frm.remove_field_elements('type_of_application', '.link-btn');
            frm.remove_field_elements('scholarship_program', '.link-btn');
            frm.remove_field_elements('academic_grade_level', '.link-btn');
            frm.remove_field_elements('course', '.link-btn');
            frm.remove_field_elements('academic_level_type', '.link-btn');
            // frm.remove_field_elements('attachments', '.sortable-handle');
        }
        frm.load_scholarship_programs = () => {
            frm.get_scholarship_programs().then(data => {
                frm.scholarship_programs = data;
                frm.filter_application_type()
            }).catch(err => frappe.msgprint(__(err)));
        }
        frm.load_academic_level_details = () => {
            frm.get_academic_level_details().then(data => {
                frm.academic_level_details = data;
                // frm.toggle_course();
                // frm.toggle_graduate_date();
            }).catch(err => frappe.msgprint(__(err)));
        }
        // frm.filter_scholarship_program = (is_reset_field) => {
        //     const current_date = frappe.datetime.get_today();
        //     const filters = [
        //         ['active', '=', '1'], 
        //         ['start_date', '<=', current_date], 
        //         ['end_date', '>=', current_date], 
        //         ['academic_level_type', '=', frm.doc.academic_level_type]];
        //     frm.filter_linked_field('scholarship_program', null, filters, is_reset_field)
        // }
        frm.filter_courses = (is_reset_field) => {
            const filters = [
                ['active', '=', '1'], 
                ['academic_level_type', '=', frm.doc.academic_level_type]];
            frm.filter_linked_field('course', null, filters, is_reset_field)

        }
        frm.filter_academic_level = (is_reset_field) => {
            const filters = [
                ['active', '=', '1'], 
                ['academic_level_type', '=', frm.doc.academic_level_type]];
                frm.filter_linked_field('academic_grade_level', null, filters, is_reset_field);
        }
        frm.filter_application_type = (is_reset_field) => {
             let application_types = [];
             const current_date = frappe.datetime.get_today();
             frm.scholarship_programs.forEach(program => {
                if (program.start_date <= current_date && program.end_date >= current_date 
                    && program.application_type_filters && program.application_type_filters.length != 0) {
                    application_types = application_types.concat(program.application_type_filters);
                }
             });
            const program_application_type_ids = application_types.map(type => type.id);
            const filters = [
                ['active', '=', '1'], 
                ['name', 'in', program_application_type_ids]];
                frm.filter_linked_field('type_of_application', null, filters, is_reset_field);
        }
        frm.toggle_course = () => {
            const selected_academic_level_detail = frm.academic_level_details.find(d => String(d.id) === String(frm.doc.academic_level_type));
            const has_courses = selected_academic_level_detail && selected_academic_level_detail.has_courses
            frm.toggle_display('course', has_courses);
            if (!has_courses) {
                frm.set_value('course', null)
                frm.refresh_field('course');
            } 
        }
        // frm.toggle_graduate_date = () => {
        //     const selected_academic_level_detail = frm.academic_level_details.find(d => String(d.id) === String(frm.doc.academic_level_type));
        //     const academic_grade_level = selected_academic_level_detail && selected_academic_level_detail.academic_grade_level
        //     ? selected_academic_level_detail.academic_grade_level.find(level => String(level.id) === String(frm.doc.academic_grade_level) ) : null;
        //     const is_graduation_level = academic_grade_level && academic_grade_level.graduation_level === 1;
        //     frm.toggle_display('graduation_date', is_graduation_level);
        //     if (!is_graduation_level) {
        //         frm.set_value('graduation_date', null)
        //         frm.refresh_field('graduation_date');
        //     }
        // }
    },
    
	refresh: (frm) => {
        // $(".sortable-handle").hide();
        frm.toggle_display('course', false);
        // frm.toggle_display('graduation_date', false);
        frm.load_scholarship_programs();
        frm.load_academic_level_details();
        frm.form_fields_refresh();
        // frm.filter_scholarship_program();
        // frm.filter_courses();
        // frm.filter_academic_level();
	},
    academic_level_type: (frm) => {
        // frm.filter_scholarship_program(true);
        // frm.filter_academic_level(true);
        // frm.filter_courses(true);
        // frm.toggle_course();
        // frm.toggle_graduate_date();
    },
    academic_grade_level: (frm) => {
        // frm.toggle_graduate_date();
    },
    
});

frappe.ui.form.on('Family Information', {
    family_information_add: (frm, cdt, cdn) => {
        
        // $(".sortable-handle").hide();
    },
    family_information_remove: (frm, cdt, cdn) => {
        
        // $(".sortable-handle").hide();
    },
    family_information_move: (frm, cdt, cdn) => {
        
        // $(".sortable-handle").hide();
    }
});

frappe.ui.form.on('Scholarship Attachments', {
    attachments_add: (frm, cdt, cdn) => {
        // frm.remove_field_elements('attachments', '.sortable-handle');
    },
    attachments_remove: (frm, cdt, cdn) => {
        // frm.remove_field_elements('attachments', '.sortable-handle');
    },
    attachments_move: (frm, cdt, cdn) => {
        // frm.remove_field_elements('attachments', '.sortable-handle');
    },
    
})