# aws-cost-and-usage
Python script which uses AWS CLI to pull down AWS EC2 information into excel, allowing you to select the tags you want to export as columns. This uses the aws ec2 command [describe-instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)

## Configuration
In order to setup the script, please populate the config.json file. This allows you to define:
- The [Credential Profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) you wish to use (use `default` if you are not using credential profiles) - This will iterate through the credential profiles to allow you to pull data from multiple accounts / roles
- The tags to pull back
- The path to write the xlsx file to
- The name of the xlsx file to write the output to
- The Schema. This are the headers written to the excel file. The middle columns are your tags.
- Arguments. This defines the arguments used by the AWS CLI Command. By default no arguments are needed, but can be added if desired

## Pre-requisites
In order for the script to work, you need to have:
- AWS CLI v2 installed
- Python 3.9 or higher
- the following python libraries:
  - boto3
  - xlsxwriter
  - json
  - os
- Appropriate credentials configured that have permission to read ec2 data. These can be set using the `aws configure` command.

The relevant Python libraries can be installed by running:
> pip install boto3 xlsxwriter

## Running the Script
To run the script, run:
Python get-cost-and-usage.py
Your results will be written to the xlsx file specified!
