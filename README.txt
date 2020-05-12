DESCRIPTION
-------------
This program makes web requests to the Federal Election Commission's campaign donor database and saves them in .csv format. Currently, it is configured to Schedule A contributions, but feel free to contact me if you'd like to discuss modifying it to make different requests. 

SETUP
-------------
Ensure that you have the following requirements installed:
 - Python3 and all of its native libraries
 - Requests for Python3

Get started:
 - Receive an API key from the FEC's API Key Signup Page. (https://api.data.gov/signup/)
 - Set the environment variable, 'FECAPIKEY'=your key in the desired directory using the following Bash command:
	
	export FECAPIKEY="myapikey"

 - Ensure that you input your key as a string, as the program requires keys inputted as strings to parse correctly.
 - Modify min_date and committee_id variables according to your desired search terms. 
 - Run!  