# gqSCsqNyEqmnJzLT6iyhAWcz1vJeBbGycNkm9Gyv -- current key
# reminder -- 81 elements per dictionary entry

import requests, json, csv
import pandas as pd
class Fecdata:
	def __init__(self, min_date = "2019-07-01", committee_id = "C00401224", key = "gqSCsqNyEqmnJzLT6iyhAWcz1vJeBbGycNkm9Gyv"):
		self.min_date = min_date
		self.committee_id = committee_id
		self.key = key

	def create_payload_and_url(self, min_date, committee_id, key):
		# url with my key -- will change to include .env implementation
		url = "https://fec-dev-api.app.cloud.gov/v1/schedules/schedule_a/?api_key="
		self.url_with_key = url + self.key
		data = requests.get(self.url_with_key + "&committee_id=" + str(self.committee_id))
		self.payload = {"committee_id" : committee_id, 
					"per_page": 100, 
					"min_date" : min_date,
					"sort" : "contribution_receipt_date",
					"pages" : data.json()["pagination"]["pages"] # must run endpoint once to find this values -- might work on optimizing this
					}
# self.payload["pages"]

	def make_csv(self, payload):
		with open("fecdata.csv", 'w') as f:
			my_writer = csv.writer(f)
			for contribution in self.payload["pages"]: #iterate through the json file 'pages' number of times	self.payload["pages"]
			# url_with_key = "https://fec-dev-api.app.cloud.gov/v1/schedules/schedule_a/?api_key=gqSCsqNyEqmnJzLT6iyhAWcz1vJeBbGycNkm9Gyv"
				paginated_data = requests.get(self.url_with_key, self.payload)
			# -- iterably append to our dataframe
				for entry in range(len(paginated_data.json()["results"])):
					my_writer.writerow(paginated_data.json()[entry])
				self.payload["last_index"] = paginated_data.json()["pagination"]["last_indexes"]["last_index"]
				self.payload["last_contribution_receipt_date"] = paginated_data.json()["pagination"]["last_indexes"]["last_contribution_receipt_date"]

	def make_df(self, payload):	#O(n^2) i think
		df = pd.DataFrame()
		data_list = []
		for contribution in range(self.payload["pages"]): #iterate through the json file 'pages' number of times	self.payload["pages"]
			# url_with_key = "https://fec-dev-api.app.cloud.gov/v1/schedules/schedule_a/?api_key=gqSCsqNyEqmnJzLT6iyhAWcz1vJeBbGycNkm9Gyv"
			paginated_data = requests.get(self.url_with_key, self.payload)
			# -- iterably append to our dataframe
			for entry in paginated_data.json()["results"]:
				data_list.append(entry)
			self.payload["last_index"] = paginated_data.json()["pagination"]["last_indexes"]["last_index"]
			self.payload["last_contribution_receipt_date"] = paginated_data.json()["pagination"]["last_indexes"]["last_contribution_receipt_date"]
		print(self.payload["pages"])
		print(data_list)

	def test(self, payload):
		for i in range(2):	
			data = requests.get(self.url_with_key, self.payload)

			for entry in range(len(data.json()["results"])):
				print(data.json()["results"][entry]["contributor_name"])
			print("------------------------------------------------------------------")
			self.payload["last_index"] = data.json()["pagination"]["last_indexes"]["last_index"]
			self.payload["last_contribution_receipt_date"] = data.json()["pagination"]["last_indexes"]["last_contribution_receipt_date"]




# items to conduct search through API

# url with my key -- will change to include .env implementation


def main():
	data = Fecdata()
	data.create_payload_and_url(data.min_date, data.committee_id, data.key)
	data.test(data.payload)

main()