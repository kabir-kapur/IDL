import requests
# from propublicaauth import *

def findParties():
	api = requests.get('https://api.propublica.org/congress/v1/102-116/house/members.json', )
	print(api)

findParties()