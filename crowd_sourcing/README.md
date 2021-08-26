# Amazon Mechanical Turk Launch Script

The script `deploy-occlusion-hit.py` deploys a Human Intelligence Task (HIT) to the the Amazon Mechanical Turk platform where workers can access the HIT, complete it, and receive compensation.

This HIT shows the website to the Turk Workers on the Mturk platform itself as an [External Question](https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_ExternalQuestionArticle.html). As such, you must first deploy the IOI app on an HTTPS web server so it can be accesible within the Mturk platform. Refer to `../ioiappdeployment/` for more information. Make sure your deployment is under HTTPS.

Once the Vision-Cognition app is deployed and live, you can launch the HIT in Mturk by doing the following steps:

1. Setup your virtual environment

```bash
bash venvsetup.bash
```

2. Run the python script as follows:

```bash
python deploy-occlusion-hit.py -p mturkjunior -e production -u https://xvision-occlusion.herokuapp.com/
```

where

```u``` is the HTTPS URL of the app

```p``` is your AWS CLI profile name. To create one, please read the the [Mturk docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) for more information.

```e``` is the environment you which to deploy the HIT to (production or sandbox).

You can also use the ```compensate_users.py``` script to compensate all users after they are done with the HIT. You can modify it if you wish to establish stricter criterion for compensation. 

```
python compensate_users.py -p mturkjunior -e production -u https://xvision-occlusion.herokuapp.com/
```

## Creating User Profile in AWS CLI
- Create an IAM User following this guidelines:
    - https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html#create-iam-user-or-role

- After IAM user is created, add the user's credentials to the AWS CLI's configuration file:
To open 
```
nano ~/.aws/credentials 
```
- In the credentials file, add your credentials as follows:
```
[mturkname]
aws_access_key_id = **********
aws_secret_access_key = ***********
```
- To see profiles (users) in your AWS CLI:
```
aws configure list-profiles
```
### Resources:
https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html    
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html      
