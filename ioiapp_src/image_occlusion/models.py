
from image_occlusion import db
from datetime import datetime


# Admin Model for Dashboard

class Admin(db.Model):
    #unique user id for the admin
    unique_id = db.Column(db.Integer,primary_key = True)
    # username for the admin user
    username = db.Column(db.String(15),unique = True)
    #password for the admin user 
    password = db.Column(db.String(80),unique = True)

    def __repr__(self):
        return f"Admin [ ID = {self.unique_id}] [Username = {self.username }] [ Password = {self.password}] \n"

# Define models

# This class represents the high level information of the Mturk Worker
class User(db.Model):
    #unique user id for the user
    unique_id = db.Column(db.Integer,primary_key = True)
    # Number of tasks the user completed
    tasks_submitted = db.Column(db.Integer,nullable = True)
    # turker boolean
    is_turker = db.Column(db.Boolean,nullable = False)
    # Device
    device = db.Column(db.String(140),nullable = True)
    # turksubmito url
    turkSubmitTo = db.Column(db.String(140),nullable = True)
    # finished HIT
    finished_HIT = db.Column(db.Boolean,nullable = True)
    #compensated
    is_compensated = db.Column(db.Boolean,nullable = True)
    #User's Tasks
    tasks = db.relationship('Task',backref = 'user',lazy = True)

    def __repr__(self):
        return f"User [ ID = {self.unique_id}] [is_turker = {self.is_turker} ] [ hitId = {self.hitId}] [workerId = {self.workerId}] [finishedhit = {self.finished_HIT}] [is_compensated ={self.is_compensated}]\n User {self.unique_id} [Device: {self.device}] Tasks: \n {self.tasks} "

class MNIST_Tracker(db.Model):
    #unique id
    unique_id = db.Column(db.Integer,primary_key = True)
    #dataset index
    dataset_index = db.Column(db.Integer,nullable = False)
    # Number of unique submissions
    unique_submissions = db.Column(db.Integer,nullable = False)
    #image label
    MNIST_label = db.Column(db.Integer,nullable= False)

    def __repr__(self):
        return f"MNIST Unique Dataset submission [ Dataset Index = {self.dataset_index}] [ MNIST Label= {self.MNIST_label}]  [Unique Submissions = {self.unique_submissions }] \n"


#This class represents the information of each image occlusssion task the user completes on the app 
class Task(db.Model):
    #unique id used as the primary key
    unique_id = db.Column(db.Integer, primary_key = True)
    #index in the MNIST dataset
    dataset_index = db.Column(db.Integer,nullable= False)
    # Task number
    task_number = db.Column(db.Integer,nullable = False)
    #Eraser size
    eraser_size = db.Column(db.Integer,nullable = True)
    #Percentage if the occlusion canvas that remains covered
    remaining_mask = db.Column(db.Integer,nullable = True)
    #Remaining points
    points = db.Column(db.Integer,nullable = True)
    # Id of the user who owns the task
    user_id = db.Column(db.Integer,db.ForeignKey('user.unique_id'),nullable = False)
    #Correct MNIST Label
    actual_MNIST_label = db.Column(db.Integer,nullable= False)
    # Label that the user submitted
    submitted_MNIST_label = db.Column(db.Integer,nullable= False)
    # The duration of the task
    task_duration = db.Column(db.Float,nullable = False)
    #Different mouse positions the user's moved with clicking
    mouse_positions_click = db.relationship('Mouse_Position_with_Click',backref="Task",lazy = True)
    #Different mouse positions the user's mouse moved without clicking
    mouse_positions_noclick = db.relationship('Mouse_Position_without_Click',backref="Task",lazy = True)

    def __repr__(self):
        return f"Task [ Task Number = {self.task_number}] [ User ID = {self.user_id}] [ Submitted MNIST Label = {self.submitted_MNIST_label}] [Actual MNIST Label = {self.actual_MNIST_label}] [Points Remaining out of 100 = {self.points}] [Eraser size = {self.eraser_size}]\n"

# This class represents the Mouse Movement information per user. 
class Mouse_Position_with_Click(db.Model):
    #unique id used as the primary key
    unique_id = db.Column(db.Integer, primary_key = True)
    # Task that the mouse position belongs to
    task_id = db.Column(db.Integer,db.ForeignKey('task.unique_id'),nullable = False)
    # Mouse position with click  timestamp
    timestamp = db.Column(db.Float,nullable = False)
    # X coordinate of the Mouse Position
    mouse_X = db.Column(db.Float,nullable = False)
    # Y coordinate of the Mouse Position
    mouse_Y = db.Column(db.Float,nullable = False)
    # Area revealed by the click

    # X coordinate of the Center
    center_X = db.Column(db.Integer, nullable = False)

    # Y coordinate of the Center
    center_Y = db.Column(db.Integer, nullable = False)

    # Diameter of the element
    diameter = db.Column(db.Integer, nullable = False)

    # id of the occlusion square
    occlusion_square_id = db.Column(db.Float,nullable = True)




    def __repr__(self):
        return f'Mouse Position with Click [Task ID: {self.task_id}] [Time Stamp = {self.timestamp}] [Mouse X = {self.mouse_X}] [Mouse Y = {self.mouse_Y}] [Area Revealed =  center_X = {self.center_X} center_Y = {self.center_Y} diameter = {self.diameter}] \n'


class Mouse_Position_without_Click(db.Model):
    #unique id used as the primary key
    unique_id = db.Column(db.Integer, primary_key = True)
    # Task that the mouse position belongs to
    task_id = db.Column(db.Integer,db.ForeignKey('task.unique_id'),nullable = False)
    # Mouse position without click  timestamp
    timestamp = db.Column(db.Float,nullable = False)
    # X coordinate of the Mouse Position
    mouse_X = db.Column(db.Float,nullable = False)
    # Y coordinate of the Mouse Position
    mouse_Y = db.Column(db.Float,nullable = False)

    def __repr__(self):
        return f'Mouse Position without Click [Task ID: {self.task_id}] [Time Stamp = {self.timestamp}] [Mouse X = {self.mouse_X}] [Mouse Y = {self.mouse_Y}] \n'

