// Copyright (c) 2024, Xurpas Inc. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Scholarship Master List"] = {
	"filters": [
		{
			'fieldname': 'name',
			'label': __('Application Id'),
			'fieldtype': 'Link',
			'options': 'Scholar Application'
		},
		{
			"fieldname": "first_name",
			"label": __("First Name"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "last_name",
			"label": __("Last Name"),
			"fieldtype": "Data",
		}

	]
};
