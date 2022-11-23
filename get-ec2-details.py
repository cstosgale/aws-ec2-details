#N.B. This script does not support updating an existing excel file. The excel file specified will be over-written each time the script runs!
import boto3
import botocore
import xlsxwriter
import datetime
import json
import os
from dateutil.relativedelta import relativedelta

#Open config file and populate variables
filepath = os.path.dirname(__file__) + '/config.json'
with open(filepath) as config_file:
	config_json = json.load(config_file)
	credential_profiles = config_json['config_variables']['credential_profiles']
	tags = config_json['config_variables']['tags']
	schema = config_json['config_variables']['schema']
	path = config_json['config_variables']['path']
	wbname = config_json['config_variables']['wbname']
	args = config_json['arguments']


#Function to connect to AWS and pull the cost data as JSON
def get_awscli_json(**args):
	data = []
	for credential_profile in credential_profiles:
		try:
			session = boto3.Session(profile_name=credential_profile)
			client = session.client('ec2')
			response = client.describe_instances(**args)
			
			for reservation in response['Reservations']:
				for instance in reservation['Instances']:
					data_child = []
					#Appends the Account
					data_child.append(credential_profile)
					#Appends any tags defined in the configuration file
					for tag in tags:
					 	data_child.append(get_value_from_key(instance['Tags'], tag))
					#Appends the Instance Type
					data_child.append(instance['InstanceType'])
					data.append(data_child)
			#print('Account: ', credential_profile, '\n')
			#print('Instance Type: ', response['Reservations'][0]['Instances'][0]['InstanceType'], '\n')
			#print('Name', get_value_from_key(response['Reservations'][0]['Instances'][0]['Tags'], 'Name'))
			#print('Response: ', json.dumps(response, indent=4, sort_keys=True).replace('\\n','\n'))
			if "NextToken" in response:
				args['NextToken'] = response['NextToken']
				data += get_awscli_json(**args)
		except botocore.exceptions.ClientError as error:
			if error.response['Error']['Code'] == 'ExpiredTokenException':
				print('There has been an issue authenticating with AWS, please ensure you have a valid token named ', credential_profile, ' defined in your credentials file')
				print('Error Message: ', error.response['Error']['Message'])
			else:
				print('There has been an unknown error communicating with AWS: ', error.response)
			pass
		except Exception as e:
			print('There has been an unknown error communicating with AWS.', '\n', 'Account: ', credential_profile, '\n')
			print(e)
			pass
	return data

#Function to return value based on a key
def get_value_from_key(response, key):
	data = ""
	for value in response:
		if value['Key'] == key:
			data = value['Value']
	return data

def write_xlsx(data):
	headers_dict = {}
	
	# Add a worksheet.
	worksheet = workbook.add_worksheet(name='Data')
	
	# Start from the first cell. Rows and columns are zero indexed.
	lastrow = len(data)
	lastcolumn = len(schema) - 1
	
	#Creates a list of dictionaries containing the headers for the XLSX table, and applies any required formatting
	datetime_format = workbook.add_format({'num_format': 'mmm yy'})
	dollars_format = workbook.add_format({'num_format': '$#,##0.00'})
	for index in range(len(schema)):
		headers_dict[index] = {}
		headers_dict[index]['header'] = schema[index]
		if schema[index] == 'Month':
			headers_dict[index]['format'] = datetime_format
		if schema[index] == 'UnblendedCost':
			headers_dict[index]['format'] = dollars_format
	# Adds a table and writes out the headers
	worksheet.add_table(0, 0, lastrow, lastcolumn, {'data': data, 'columns': headers_dict})
#Run the API call and output to JSON
data = get_awscli_json(**args)
#print(data)

#data = format_data(jsonresponse)

#Create the XLSX file and write the data
print('Writing the output to ', wbname)
workbook = xlsxwriter.Workbook(wbname)
write_xlsx(data)
workbook.close()