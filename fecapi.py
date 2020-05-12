# gqSCsqNyEqmnJzLT6iyhAWcz1vJeBbGycNkm9Gyv -- current key
# reminder -- 81 elements per dictionary entry

import requests, json, csv, time, threading, os

class Fecdata:
	def __init__(self, min_date = "2019-07-01", committee_id = "C00401224", key = os.environ.get('FECAPIKEY')):
		self.min_date = min_date
		self.committee_id = committee_id
		self.key = key

	def create_payload_and_url(self, min_date, committee_id, key):
		# url with my key -- will change to include .env implementation
		url = "https://fec-dev-api.app.cloud.gov/v1/schedules/schedule_a/?api_key="
		self.url_with_key = url + self.key
		data = requests.get(self.url_with_key + "&committee_id=" + str(self.committee_id))
		self.fieldnames = data.json()["results"][0].keys()
		self.payload = {"committee_id" : committee_id, 
					"per_page": 100, 
					"min_date" : min_date,
					"sort" : "contribution_receipt_date",
					"pages" : data.json()["pagination"]["pages"] # must run endpoint once to find this values -- might work on optimizing this
					}
# self.payload["pages"]

	def make_csv(self, payload):	
		with open("fecdata.csv", 'w') as f:
			my_writer = csv.DictWriter(f, fieldnames = self.fieldnames)
			my_writer.writeheader()
			request_counter = 0
			epoch = time.time()
			for contribution in range(2): #iterate through the json file 'pages' number of times	self.payload["pages"]
				if (time.time() - epoch) >=60.:
					request_counter = 0
					epoch = time.time()
				elif request_counter >= 120:
					request_counter = 0
					time.rest(61 - (time.time() - epoch))
					epoch = time.time()
					# url_with_key = "https://fec-dev-api.app.cloud.gov/v1/schedules/schedule_a/?api_key=gqSCsqNyEqmnJzLT6iyhAWcz1vJeBbGycNkm9Gyv"
				paginated_data = requests.get(self.url_with_key, self.payload)
				request_counter += 1
				# -- iterably append to our dataframe
				for i in paginated_data.json()["results"]:
					my_writer.writerow(i)
				self.payload["last_index"] = paginated_data.json()["pagination"]["last_indexes"]["last_index"]
				self.payload["last_contribution_receipt_date"] = paginated_data.json()["pagination"]["last_indexes"]["last_contribution_receipt_date"]

	



# items to conduct search through API

# url with my key -- will change to include .env implementation


def main():
	req = Fecdata()
	req.create_payload_and_url(req.min_date, req.committee_id, req.key)
	req.make_csv(req.payload)

main()