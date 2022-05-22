# aws-cost-and-usage
Python script which uses AWS CLI to pull down AWS cost and usage information into excel, allowing you to group the data by up to two dimentions.

## Configuration
In order to setup the script, please populate the config.json file. This allows you to define:
- The Billing Account you wish to connect to (if you do not use organisations, - should work here to use the account you're authenticated with)
- The number of months of data to pull back
- The path to write the xlsx file to
- The name of the xlsx file to write the output to
- The Schema. This are the headers written to the excel file. Columns 2 and 3 are the things you are grouping by (see the arguments). In the example config file, there is a cost category called "Tribe" which is being used, as well as usage type. These can be changed to any attributes supported by the AWS CLI.
- Arguments. This defines the arguments used by the AWS CLI Command. In the example, this includes setting the granularity to monthly, and filtering the results to exclude certain types of cost. It also pulls back the unblended cost, and groups the result by the Tribe cost category and the Linked Account dimension.

## Pre-requisites
In order for the script to work, you need to have:
- AWS CLI v2 installed
- Python 3.9 or higher
- the following python libraries:
  - boto3
  - xlsxwriter
  - json
  - os
- Appropriate credentials configured that have permission to read billing data. These can be set using the 'aws configure' command.

The relevant Python libraries can be installed by running:
> pip install boto3 xlsxwriter

## Running the Script
To run the script, run:
Python get-cost-and-usage.py
Your results will be written to the xlsx file specified!
