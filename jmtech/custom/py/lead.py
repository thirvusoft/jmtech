def get_data(data=None):
	return {
		"fieldname": "lead",
		"non_standard_fieldnames": {"Customer": "lead_name"},
		"transactions": [
			{"items": ["Customer"]},
		],
	}
