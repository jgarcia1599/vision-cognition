
# Script to deploy Image Occlusion HIT as an External question
#
#
# 
# Author: Junior Garcia 

# labs account
# python3 deploy-occlusion-hit.py -p visionocclusion -e sandbox -u https://vision.x-labs.xyz/
# python3 deploy-occlusion-hit.py -p visionocclusion -e production -u https://vision.x-labs.xyz/

# My account 
# python deploy-occlusion-hit.py -p mturkjunior -e sandbox -u https://xvision-occlusion.herokuapp.com/
# python deploy-occlusion-hit.py -p mturkjunior -e sandbox -u https://vision.x-labs.xyz/

import boto3
import argparse
from pprint import pformat
from boto.mturk.question import ExternalQuestion


parser = argparse.ArgumentParser()


parser.add_argument('-p', action='store', dest='profile_name',
                    help='AWS credentials profile in ~/.aws/credentials')

parser.add_argument('-e', action='store', dest='environment',
                    help='Defines AMT environment to run tasks')


parser.add_argument('-u', action='store', dest='user_url',
                    help='Defines URL to be deployed as an External Question in Mturk')


#change this variablee to change number of assignments
max_assignments = 500

class ExternalQuestion:
    """
    An object for constructing an External Question.
    """
    schema_url = "http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd"
    template = '<ExternalQuestion xmlns="%(schema_url)s"><ExternalURL>%%(external_url)s</ExternalURL><FrameHeight>%%(frame_height)s</FrameHeight></ExternalQuestion>' % vars()

    def __init__(self, external_url, frame_height):
        self.external_url = external_url
        self.frame_height = frame_height

    def get_as_params(self, label='ExternalQuestion'):
        return {label: self.get_as_xml()}

    def get_as_xml(self):
        return self.template % vars(self)


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
		preview_url = 'https://workersandbox.mturk.com/mturk/preview'

	elif environment == 'production':
		# Uncomment this line to use in production
		endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
		preview_url = 'https://www.mturk.com/mturk/preview'

	else:
		print(' ... cant recognize environment:', environment)
		print(' ... defaulting to sandbox environment')
		endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
		preview_url = 'https://workersandbox.mturk.com/mturk/preview'

	# This reads AWS Access Keys from ~/.aws/credentials
	# profile_name = 'mturk-tuka'
	session = boto3.Session(profile_name = profile_name)

	# initiating connection to service
	client = session.client(
	    service_name='mturk',
	    endpoint_url=endpoint_url,
	    region_name=region_name,
	)

	# print(client)

	return client, preview_url


# ---------------------------------------------------------------------------------------
# Deploy Hit
# ---------------------------------------------------------------------------------------
def deployHits(client, preview_url,user_url,environment):
    # -----------------------------------------------------------------------------------------
    # Information to render to Turkers
    # -----------------------------------------------------------------------------------------
    # URL that hosts your HIT
    external_url = user_url
    TaskAttributes = {
        'MaxAssignments': max_assignments,                 
        'LifetimeInSeconds': 1209600,           
        'AssignmentDurationInSeconds': 60*15, 
        'Reward': '0.15',                     
        'Title': 'Image Occlusion Task',
        'Keywords': 'Machine Learning, Image Recognition, Classification, Computer Vision',
        'Description': 'This is a study of how humans detect recognize characters and objects in images.If you encounter any problems, please contact us at: jfg388+occlusion@nyu.edu'
    }


    # -----------------------------------------------------------------------------------------
    # Create the task as an external question
    # -----------------------------------------------------------------------------------------
    external_question = ExternalQuestion(external_url=external_url ,
     frame_height=2200)


    # creating hit
    if environment == 'production':
        response = client.create_hit(
            **TaskAttributes,
            Question=external_question.get_as_xml(),
            QualificationRequirements=[
                #Adult Worker
                {'QualificationTypeId':'00000000000000000060',
                'Comparator': 'EqualTo',
                'IntegerValues':[1]},
                # Worker_​PercentAssignmentsApproved
                {'QualificationTypeId':'000000000000000000L0',
                'Comparator': 'GreaterThanOrEqualTo',
                'IntegerValues':[95]},
                #Worker_​NumberHITsApproved
                {'QualificationTypeId':'00000000000000000040',
                'Comparator': 'GreaterThanOrEqualTo',
                'IntegerValues':[1000]}


            ]
        )
    else:
        response = client.create_hit(
            **TaskAttributes,
            Question=external_question.get_as_xml()
        )


    # retreiving hit ID
    hit_type_id = response['HIT']['HITTypeId']

    print(' ')
    print("You can view the HITs here:")
    print(preview_url + "?groupId={}".format(hit_type_id))
    print(' ')


# ---------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":

	# parsing parameters
	params = parser.parse_args()

	# initiating connection to turk server
	client, preview_url = initConnection(params.profile_name, params.environment)

	deployHits(client, preview_url,params.user_url,params.environment)

# eof





# External questions rresources:
# https://stackoverflow.com/questions/57218567/create-a-hit-on-amazon-mechnical-turk-using-externalquestion-with-boto3