// Copyright (c) 2024, Xurpas Inc. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course', {
	refresh: function(frm) {
		frm.set_df_property('academic_level_group', 'only_select', true);
		frm.fields_dict['academic_level_group'].get_query = (doc, cdt, cdn) => {
			return {
				filters: [['has_courses', '=', '1']]
			};
		}
	}
});
