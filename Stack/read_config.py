def get_config_params():
	config_file = open('config.txt', 'r')
	lines = config_file.readlines()
	params = {}
	for line in lines:
		line = line.strip()
		split_line = line.split(":")
		params[split_line[0]] = split_line[1]

	return params