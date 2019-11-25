import yaml

with open("211028.yaml", "r") as stream:
	try:
		data = (yaml.safe_load(stream))
		print(data['innings'][0]['1st innings']['deliveries'][24][3.5]['wicket']['fielders'])
		#print(data['innings'][0]['deliveries'][24])

	except yaml.YAMLError as exc:
		print(exc)
