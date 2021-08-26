#Flask imports
from flask import render_template, request, jsonify, make_response, abort, redirect, url_for,session

#MNIST handler function
from image_occlusion.MNIST import choose_random_MNIST

# Additional Utilities
import random
from datetime import datetime,timedelta
import csv

#import utilities from other py files
from image_occlusion.models import User,Task,Mouse_Position_with_Click,Mouse_Position_without_Click,Admin,MNIST_Tracker
from image_occlusion.forms import LoginForm

#import app
from image_occlusion import app,db

#mturk api libraries
import boto3
import argparse
from pprint import pformat
import xmltodict


# Global variables that determine the number of tasks the user needs to do
max_task_number = app.config['MAX_TASK_NUMBER']
# max_task_number = 4




# ([('assignmentId', '31Z0PCVWUKF9UBN6L6OAYQM03IUT76'), ('hitId', '3Y3CZJSZ9KTE58Y13MZGC7C6MW7R5P'), ('workerId', 'A2A0X1DWOWB01S'), ('turkSubmitTo', 'https://workersandbox.mturk.com')])

################################################################################
# Home route for the flask app

# Input: Client HTTP request
# Output: html template and any necessary data that will then be displayed to the user

################################################################################
@app.route('/', methods = ["GET","POST"])
def instructions():
    if len(request.args) == 0:
        # sent instructions form
        turkuser = False
        return render_template('instructions.html', turkuser = turkuser)
    else:
        #turk user, make sure to parse through the arguments and save it in thee session
        turkuser = True
        assignmentId = request.args.get('assignmentId')
        hitId = request.args.get('hitId')
        turkSubmitTo = request.args.get('turkSubmitTo')
        workerID = request.args.get('workerId')    
        # sent instructions form
        return render_template('instructions.html',turkuser=turkuser,assignmentId = assignmentId , hitId = hitId ,turkSubmitTo = turkSubmitTo, workerID = workerID)
        


################################################################################
# Process consent form route

# Input: Client HTTP POST request
# Output: user is redirected to the task sequence route if theyve consented to participate in 
# this study. Otherwise, they are redirected to the instructions page.

################################################################################
@app.route('/processconsentform', methods = ['POST'])
def process_consent_form():
    # Obtain all necessary variables
    turkuser =  parseBoolean(request.args.get('turkuser'))
    assignmentId = request.args.get('assignmentId')
    hitId = request.args.get('hitId')
    turkSubmitTo = request.args.get('turkSubmitTo')
    workerID = request.args.get('workerID')
    if request.method == "POST":
        # if the useer has consented to participate in this study
        if turkuser == True:
            if request.form['consent']=='on' and assignmentId!='ASSIGNMENT_ID_NOT_AVAILABLE':
                #set up 'current task number variable' in the session
                current_task_number = 1
                session['current_task_number'] = current_task_number
                #create a new user and fill in the mturk data
                new_user = User(tasks_submitted = max_task_number,
                                is_turker = True,
                                finished_HIT = False,
                                is_compensated = False,
                                turkSubmitTo = turkSubmitTo
                )
                db.session.add(new_user)
                db.session.commit()
                current_user_id = new_user.unique_id
                session['current_user_id'] = new_user.unique_id
                # redirect user to task sequence
                return redirect(url_for('task_sequence',turkuser=turkuser,current_task_number = current_task_number, current_user_id = current_user_id))
            else:
                #otherwise, the user hasnt consented or hasnt accepted the hit and needs to be redireected to the consent form
                return redirect(request.referrer)
        else:
            if request.form['consent'] == "on":
                #set up 'current task number variable' in the session
                current_task_number = 1
                session['current_task_number'] = current_task_number

                new_user = User(tasks_submitted = max_task_number,
                                is_turker = False,
                                finished_HIT = False,
                )
                db.session.add(new_user)
                db.session.commit()
                current_user_id = new_user.unique_id
                # redirect user to task sequence
                return redirect(url_for('task_sequence',turkuser=turkuser,current_task_number = current_task_number,current_user_id=current_user_id))
            else:
                #otherwise, the user hasnt consented and needs to be redireected to the consent form
                return redirect(request.referrer)

################################################################################
# Task Sequence Routee

# Input: Client HTTP GET request
# Output: Displays the Image Occlusion Task to the user. A random image from the MNIST dataset is chosen
# and displayed to the user. This route also makes sure that the user only does the required number of tasks 
# and that the user has signed the consent form as a prerequisite to enter this route.

################################################################################
@app.route('/tasksequence', methods = ["GET"])
def task_sequence():
    # Get necessary variables
    current_task_number = int(request.args.get('current_task_number'))
    current_user_id = int(request.args.get('current_user_id'))
    current_user = User.query.get(current_user_id)
    users_tasks_completed = len(current_user.tasks)
    turkuser =  parseBoolean(request.args.get('turkuser'))
    try:
        last_task_submitted_id = current_user.tasks[-1].task_number
    except IndexError as error:
        last_task_submitted_id = 0

    
    # if user has not started the task sequence, they cant enter this route and need to be redirected to instructions page
    if len(request.args)==0:
        return redirect(url_for('instructions'))
    else:
        #GET request handling : only let users enter this path if they are still in the task sequence
        if current_task_number<=max_task_number:
            #get eraser size 
            eraser_size = app.config['EXPERIMENT_1_ERASER_SIZES'][current_task_number-1]
            MNIST_dataset_items = MNIST_Tracker.query.all()
            current_index_fromtracker = len(MNIST_dataset_items)  % 70000

            MNIST_dataset_index = current_index_fromtracker


            #obtain MNIST image label and file path from the choose_random_MNIST function
            MNIST_imagelabel,MNIST_filepath,MNIST_dataset_index = choose_random_MNIST(current_index_fromtracker)

            #save daset index in DB table fopr tracking datset-specific unique submissions
            MNIST_dataset_item = MNIST_Tracker.query.filter_by(dataset_index=MNIST_dataset_index).first()
            if MNIST_dataset_item == None:
                MNIST_dataset_item = MNIST_Tracker(dataset_index = MNIST_dataset_index,
                                                    unique_submissions = 1,
                                                    MNIST_label = MNIST_imagelabel)
                db.session.add(MNIST_dataset_item)
                db.session.commit()
            else:
                MNIST_dataset_item.unique_submissions +=1
                db.session.commit()      



            #unique cache busting parameter for recently created image to show
            timestamp = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")

            # modify filepath with the timestamp parameter to force the client to seek the updated image from the server
            MNIST_filepath = MNIST_filepath+'?'+timestamp

            #render the template with all the necessary variables
            return render_template('index.html',label=MNIST_imagelabel,image_url =MNIST_filepath,current_task_number=current_task_number,max_task_number=max_task_number,MNIST_dataset_index=MNIST_dataset_index,eraser_size=eraser_size,current_user_id = current_user_id, last_task_submitted_id = last_task_submitted_id)
        else: 
            #user is done with task sequence, he needs to be redirected to the submissioncomplete view
            return redirect(url_for('device',turkuser = turkuser,current_task_number= current_task_number, current_user_id=current_user_id))


################################################################################
# Process data route 

# Input: Client HTTP POST request
# Output: This route receives the data collected from the user as a JSON, processes it by calling the 
# savetoDB() function, and returns and HTTP 200 response to verify the proper proccessing of the data. 

################################################################################

@app.route('/processdata', methods = ["POST"])
def processdata():
    #get the json response from the user
    user_response = request.get_json()

    current_user_id = int(user_response['current_user_id'])
    current_user = User.query.get(current_user_id)
    last_task_submitted_id = user_response['last_task_submitted_id']
    current_task_number = user_response['current_task_number']
    try:
        last_task_submitted_id = current_user.tasks[-1].task_number
    except IndexError as error:
        last_task_submitted_id = 0

    if (current_task_number -last_task_submitted_id) ==1:
        savetoDB(user_response)

        res = make_response(jsonify({
            "message":"user_response_received"
        }),200)

        return res
    else:
        correct_current_task_number = last_task_submitted_id+1
        res = make_response(jsonify({
            "message":"you cant go back, the next task is the following:",
            "current_task_number": correct_current_task_number,
            "current_user_id": current_user_id

        }),400)
        return res

@app.route('/device', methods = ['GET','POST'])
def device():
    if request.method =='GET':
        current_task_number = int(request.args.get('current_task_number'))
        current_user_id = int(request.args.get('current_user_id'))
        turkuser =  parseBoolean(request.args.get('turkuser'))
        return render_template('device.html', current_task_number =current_task_number, current_user_id = current_user_id , turkuser = turkuser)
    else:
        #get the json response from the user
        user_response = request.get_json()
        # extract device and user id from json response
        current_user_id = user_response['current_user_id']
        device = user_response['device']
        # query user from db and save the device variable
        current_user = User.query.get(current_user_id)
        current_user.device = device
        db.session.commit()


        # return 200 success response to client 
        res = make_response(jsonify({
        "message":"user_response_received"
        }),200)
        return res








################################################################################
# Submission View
# Input: HTTP GET request
# Output : Displays the Verification Code the user needs to submit in the MTURK webiste 

################################################################################

@app.route('/submission-complete')
def submission_complete_view():
    current_task_number = int(request.args.get('current_task_number'))
    current_user_id = int(request.args.get('current_user_id'))
    turkuser =  parseBoolean(request.args.get('turkuser'))
    if len(request.args)==0:
        #user didnt start the task, they need to be redirected to the instructions page
        return(redirect(url_for('instructions')))
    else:
        if current_task_number<max_task_number:
            #user is not done, they need to finish the task sequence
            return redirect(url_for('task_sequence',current_task_number= current_task_number, current_user_id = current_user_id))
        else: 
            #user has finished the task sequence, they can be redirected to submissions page
                #randomly choose verification key
            current_user = User.query.get(current_user_id)
            if current_user.is_turker == True:
                
                current_user.finished_HIT = True
                db.session.commit()
                submission_url = current_user.turkSubmitTo+ '/mturk/externalSubmit' +  '?' +'assignmentId=' + str(current_user.assignmentId) + '&' + 'internal_user_id=' + str(current_user_id)

                return render_template('done.html',submission_url =submission_url)
            else:
                current_user.finished_HIT = True
                db.session.commit()
                return render_template('done.html')
     

################################################################################
# Admin View
# Input: HTTP GET or POST request
# Output : Displays the Login Form for a user to enter the admin dashboard

################################################################################
@app.route('/admin', methods = ['GET','POST'])
def admin():
    #  Get ADMIN USERNAME and password from configuration files
    ADMIN_USERNAME = app.config['ADMIN_USERNAME']
    ADMIN_PASSWORD = app.config['ADMIN_PASSWORD']
    # Check if admin username was created already
    if Admin.query.filter_by(username=ADMIN_USERNAME).first() == None:
    # If its not, then create the admin user and save it in the DB
        admin = Admin(username = ADMIN_USERNAME, password = ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
    else:
        # Query the user name
        admin = Admin.query.filter_by(username=ADMIN_USERNAME).first()

    # Instantiate the form to render in the frontend
    form = LoginForm()
    # Check if the form was submitted and validated in a POST request
    if form.validate_on_submit():
        # filter the DB to see if the username and password provided is correct
        admin = Admin.query.filter_by(username = form.username.data, password = form.password.data).first()

        # If the admin is found, display the dashboard to the user
        if admin:
            session['logged_in'] = True
            return(redirect(url_for('dashboard')))
        # if its not then redirect users to login page
        else:
            return(redirect(url_for('admin')))

    return render_template('login.html',form = form)

################################################################################
# Dashboard View
# Input: HTTP GET request
# Output : Returns the template along with the data to be displayed to the admin user 
# regarding stats on the progress of the data collection

################################################################################
@app.route('/dashboard')
def dashboard():
    # only display the dashboard if the user is logged in
    if 'logged_in' in session:


        # get all the count of all of the users whove done an Image Occlusion Task
        users =  User.query.filter_by(finished_HIT = True).all()
        # finished hit users list
        finished_HIT_users_list = []
        for user in users:
            finished_HIT_users_list.append(user.unique_id)
        #Query the different tasks 
        # List to hold the submission count for each label
        per_label_submission_count = []
        # for each label i.e. 0-9 
        for tag in range(10):
            # query the database and count all the queried submissions
            label_count = len(Task.query.filter_by(actual_MNIST_label = tag).filter(Task.user_id.in_(finished_HIT_users_list)).all())
            # add the count above to the submission list
            per_label_submission_count.append(label_count)


        user_count = len(users)
        # unique submissions dictionary to save the per_user unique submissions
        unique_submission_dictionary = {}

        # mnist dataset submissiom
        MNIST_dataset_items = {}

        # add all keys
        for key in range(0,10):
            unique_submission_dictionary[key] = 0
        # for each user who has submitted
        for user in users:
            # get all the tasks the user submitted
            user_tasks = user.tasks
            # dictionary where we will save whether a user has submitted a specific MNIST Label
            user_submission_dictionary = {}
            # for each task the user submitted
            for task in user_tasks:
                # set as the key the label and a True boolen as the value to indicate the user has submitted that label
                user_submission_dictionary[task.actual_MNIST_label] = True
                if task.dataset_index in MNIST_dataset_items:
                    MNIST_dataset_items[task.dataset_index] +=1
                else:
                    MNIST_dataset_items[task.dataset_index] = 1
            # a list of the keys of the user submissions dictionary willl return the unique submissions label for that user
            user_unique_submissions = list(user_submission_dictionary.keys())
            # for each unique submissions label
            for unique_submission_label in user_unique_submissions:
                # save the count on the unique submissions dictionary.
                unique_submission_dictionary[unique_submission_label] = unique_submission_dictionary[unique_submission_label] + 1

        MNIST_dataset_items_sorted = {}
        for key in sorted(MNIST_dataset_items.keys()) :
            MNIST_dataset_items_sorted[key] = MNIST_dataset_items[key]

        # obtain dataset specific data 

        # MNIST_dataset_items = MNIST_Tracker.query.filter(Task.user_id.in_(finished_HIT_users_list)).all()

        all_users = User.query.all()
        non_compensated_users = User.query.filter_by(is_turker=True,is_compensated=False,finished_HIT = True).all()
        non_compensated_users_count = len(non_compensated_users)

        for user in non_compensated_users:
            print(user)

        # obtain the total number of tasks submitted
        total_task_count = len(Task.query.filter(Task.user_id.in_(finished_HIT_users_list)).all())
        # total_task_count = len(Task.query.all())

        # return the dashboard data along with the data items to be displayed to the user
        return render_template('dashboard.html', per_label_submission_count = per_label_submission_count, user_count = user_count,unique_submission_dictionary = unique_submission_dictionary,MNIST_dataset_items = MNIST_dataset_items_sorted , total_task_count=total_task_count)
    else:
        # redirect user to the login route if the havent entered this route 
        return redirect(url_for('admin'))






################################################################################
# Save to DB

# Input: A user's data on the Image Occlusion Interface
# Output: None
# This function gets the user's task data from the Front end and its saves it on the corresponding tables
# on the relational databse

################################################################################
def savetoDB(user_response):
    # saving stuff to the database

    current_user_id = user_response['current_user_id']
    # query user from database
    current_user = User.query.get( current_user_id)


    MNIST_dataset_index = user_response['MNIST_dataset_index']
    MNIST_imagelabel = user_response['actual_label']


    # create current Task
    current_task = Task(task_number = user_response['current_task_number'],
                        user_id = current_user.unique_id,
                        eraser_size = user_response['eraser_size'],
                        dataset_index = user_response['MNIST_dataset_index'],
                        actual_MNIST_label = user_response['actual_label'], 
                        submitted_MNIST_label = user_response['answer'] ,
                        points = user_response['remainder_points'],
                        remaining_mask = user_response['remaining_mask'],
                        task_duration = user_response['task_duration'])
    # added and save it to the db
    db.session.add(current_task)
    db.session.commit()
    

    # save all of thee mouse movements to the Mouse_Position_with_Click table
    # print("Mouse movementss with click")
    mouse_position_with_click_list = []
    for mouse_event in user_response['mouse_positions_click']:
        mouse_position_with_click = Mouse_Position_with_Click(task_id = current_task.unique_id,
                                                              timestamp = mouse_event[0], 
                                                              mouse_X = mouse_event[1],
                                                              mouse_Y = mouse_event[2],
                                                              center_X = mouse_event[3][0],
                                                              center_Y = mouse_event[3][1],
                                                              diameter = mouse_event[3][2],
                                                              occlusion_square_id = mouse_event[3][3] )
        mouse_position_with_click_list.append(mouse_position_with_click)
    db.session.add_all(mouse_position_with_click_list)
    db.session.commit()

    # save all of thee mouse movements to the Mouse_Position_without_Click table
    mouse_position_without_click_list = []
    for mouse_event in user_response['mouse_positions_noclick']:
        mouse_position_without_click = Mouse_Position_without_Click(task_id = current_task.unique_id,
                                                              timestamp = mouse_event[0], 
                                                              mouse_X = mouse_event[1],
                                                              mouse_Y = mouse_event[2],
                                                              )
        mouse_position_without_click_list.append(mouse_position_without_click)
    db.session.add_all(mouse_position_without_click_list)
    db.session.commit()


def parseBoolean(variable):
    if variable == 'True':
        return True
    elif variable == 'False':
        return False
    else:
        return None
