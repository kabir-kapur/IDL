import requests
#from propublicaauth import *

def findParties():
	api = requests.get('https://api.propublica.org/congress/v1/102-116/house/members.json', auth = '1YurrTnmd7KmsLJ7kmCCcjAjtA7K5T49bWUVJUhw')
	print(api.status)