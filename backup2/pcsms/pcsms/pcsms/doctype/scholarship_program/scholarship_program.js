// Copyright (c) 2024, Xurpas Inc. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scholarship Program', {
	setup: (frm) => {
		common_setup(frm);
		common_api_call(frappe,frm);
		frm.academic_level_details = [];
		frm.academic_levels = [];
		frm.load_academic_level_details = () => {
            frm.get_academic_level_details().then(data => {
                frm.academic_level_details = data;
				frm.academic_level_details.forEach(detail => frm.academic_levels.push(...detail.academic_grade_level))
				frm.update_academic_levels();
			}).catch(err => frappe.msgprint(__(err)))
        }
		frm.filter_academic_level = (is_reset_field) => {
			const academic_level_type_ids = frm.doc.academic_level_types 
			? frm.doc.academic_level_types.map(type => type.academic_level_type) : [];
            const filters = [
                ['active', '=', '1'], 
                ['academic_level_type', 'in', academic_level_type_ids]];
                frm.filter_linked_field('academic_levels', 'academic_level', filters, is_reset_field);
        },
		frm.update_academic_levels = () => {
			frm.filter_academic_level();
			const academic_level_type_ids = frm.doc.academic_level_types 
			? frm.doc.academic_level_types.map(type => String(type.academic_level_type)) : [];
			frm.doc.academic_levels = frm.doc.academic_levels.filter(level => {
				const academic_level = frm.academic_levels.find(l => String(l.id) === String(level.academic_level));
				return academic_level && academic_level_type_ids.indexOf(String(academic_level.academic_level_type)) !== -1;
			});
			frm.refresh_field('academic_levels');
		}

	},
	refresh: (frm) => {
		frm.load_academic_level_details();
	}
});

frappe.ui.form.on('Academic Level Types', {
	academic_level_type: (frm, cdt, cdn) => {
		frm.update_academic_levels();
	},
	academic_level_types_remove: (frm, cdt, cdn) => {
		frm.update_academic_levels();
	}
})
