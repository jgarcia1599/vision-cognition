# script to review, accept, and reject hits
#
# author: tuka
# modified by: Junior
# python 6_list-hit-answers.py -p visionocclusion  -e sandbox
# python3 3_compensate_users.py -p visionocclusion -e production


import boto3
import argparse
from pprint import pformat
import xmltodict

parser = argparse.ArgumentParser()


parser.add_argument('-p', action='store', dest='profile_name',
                    help='AWS credentials profile in ~/.aws/credentials')

parser.add_argument('-e', action='store', dest='environment',
                    help='Defines AMT environment to run tasks')


# ---------------------------------------------------------------------------------------
# Initiating connection to AMT
# ---------------------------------------------------------------------------------------
def initConnection(profile_name, environment):

	# region in which service operates.
	# this shouldn't need to be changed.
	region_name = 'us-east-1'

	if environment == 'sandbox':
		# endpoint of Sandbox developer environment
		endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

	elif environment == 'production':
		# Uncomment this line to use in production
		endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

	else:
		print(' ... cant recognize environment:', environment)
		print(' ... defaulting to sandbox environment')
		endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

	# This reads AWS Access Keys from ~/.aws/credentials
	# profile_name = 'mturk-tuka'
	session = boto3.Session(profile_name = profile_name)

	# initiating connection to service
	client = session.client(
	    service_name='mturk',
	    endpoint_url=endpoint_url,
	    region_name=region_name,
	)

	return client


# ---------------------------------------------------------------------------------------
# retreive and print review of hits
# ---------------------------------------------------------------------------------------
def reviewHits(client):

	# --------------------------------------------------------------------------------
	# Returing information on hits listed
	# --------------------------------------------------------------------------------
	response = client.list_hits(
	    # NextToken='HITs',
	    MaxResults=10
		)

	# --------------------------------------------------------------------------------
	# iterate through each hit
	# --------------------------------------------------------------------------------
	for i, item in enumerate(response['HITs']):

		print(' ... response', i)
		print(' ... HITId', item['HITId'])

		# Get the status of the HIT
		hit = client.get_hit(HITId=item['HITId'])
		item['status'] = hit['HIT']['HITStatus']

		# --------------------------------------------------------------------------------
		# Get a list of the Assignments that have been submitted by Workers
		# --------------------------------------------------------------------------------
		all_assignments = []

		done = False
		counter  = 0
		nextToken = None
		while done == False:
			if counter == 0:
				assignmentsList = client.list_assignments_for_hit(
					HITId=item['HITId'],
					AssignmentStatuses=['Submitted', 'Approved'],
					MaxResults=100
					
				)
			else:
				assignmentsList = client.list_assignments_for_hit(
					HITId=item['HITId'],
					AssignmentStatuses=['Submitted', 'Approved'],
					MaxResults=100, 
					NextToken = nextToken
					
				)

			#add assignments list in array
			all_assignments.append(assignmentsList)

			try:
				nextToken = assignmentsList['NextToken']
			except KeyError:
				done = True
			print(' ... assignment pages counter',counter)
			counter+=1
		all_assignments_count = 0
		for assignmentsList in all_assignments:
			assignments = assignmentsList['Assignments']
			item['assignments_submitted_count'] = len(assignments)

			print(' ... count', item['assignments_submitted_count'])
			print(f'User: {all_assignments_count}')
			all_assignments_count += item['assignments_submitted_count']

			answers = []
			# --------------------------------------------------------------------------------
			# evaluating each assignment
			# --------------------------------------------------------------------------------
			for assignment in assignments:
				# accept assignments based on hitId
				hitId = assignment['HITId']
				print(' ... assignment status:', assignment['AssignmentStatus'])
				print(' ... HITId', hitId)
				# Retreive the attributes for each Assignment
				worker_id = assignment['WorkerId']
				assignment_id = assignment['AssignmentId']
				print(' ... Worker ID: ',worker_id)
				print(' ... Assignment ID: ',assignment_id)
				print()
				print()
				
				# --------------------------------------------------------------------------------
				# Approve the Assignment (if it hasn't already been approved)
				# --------------------------------------------------------------------------------
				if assignment['AssignmentStatus'] == 'Submitted':
					client.approve_assignment(
						AssignmentId=assignment_id,
						OverrideRejection=False
					)
		print(' ')
		print(' ... total number of assignments submitted ',all_assignments_count)
	    



# ---------------------------------------------------------------------------------------
#  main
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":

	# parsing parameters
	params = parser.parse_args()

	# initiating connection to turk server
	client = initConnection(params.profile_name, params.environment)

	reviewHits(client)


# eof