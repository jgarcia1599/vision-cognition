var opaque_squares = [];
var draw_erased_squares = [];

var mouse_positions_log_click = [];
var mouse_positions_log_noclick = [];
var eraser_side_length;


//variable to track the remaining mask covered
var remaining_mask;

// var date_object  = new Date()
var initial_millis,timeElapsed,remainder_points;

//State variable that termines whether or not the mouse is clicked
var is_mouse_Clicked = false;

function mousePressed() {
    is_mouse_Clicked = true;
    
  }
function mouseReleased(){
    is_mouse_Clicked = false;
}

var five_second_reductions = 0;


var intervalID = window.setInterval(deduct_time_points, 5000); 
function deduct_time_points() { 
    // Your code here 
    console.log("5 seconds passed"); 
    // deduct points based on timee 
    five_second_reductions +=2;
    console.log("Time Points: ",five_second_reductions) 


}

function setup(){
    //Place p5 canvas in canvas Holder element
    createCanvas(400,400).parent('canvasHolder');
    initial_millis = millis();


    //ERASER SIZE FROM BACKEND GETS ASSIGNED HERE, DONT FORGET
    eraser_side_length = task_eraser_size;

    var ids = 1;
    //Opaque Mask creation and placement. lets keep reference of all the cirlces in the canvas  in an array
    for (var x_displacement = 0; x_displacement<width;x_displacement=x_displacement+eraser_side_length){
        for (var y_displacement = 0;y_displacement<height;y_displacement=y_displacement+eraser_side_length){
            var new_opaque_square = new Opaque_Square(x_displacement,y_displacement,eraser_side_length,ids);
            new_opaque_square.draw();
            opaque_squares.push(new_opaque_square);
            ids++;
        }
    }
    console.log(opaque_squares);

    //only display the MNIST image after the opaque mask has been placed on top of it
    $('#mnist_image').show();
}

function draw(){
    //calculate remainder points
    remaining_mask = roundAccurately(((opaque_squares.length - draw_erased_squares.length)*100)/opaque_squares.length,0) 
    remainder_points = remaining_mask - five_second_reductions;
    console.log(remaining_mask);

    // console.log(remainder_points)
    // console.log(draw_erased_squares);
    // display remainder points in point container
    document.getElementById("points").innerHTML = remainder_points

    // time elapsed in milliseconds
    timeElapsed = Math.floor(millis() - initial_millis);
    if((mouseX>0 && mouseX<width)&&(mouseY>0 && mouseY<height) && is_mouse_Clicked == false){
        //Log timeelapsed, user's mouse posiition, and an empty array as the opaque element was not erased 
        mouse_positions_log_noclick.push([timeElapsed,mouseX,mouseY])
    }

    //for all the circles in the canvas, check if the mouse
    //has hovered on top of each one based on the mouse position
    for (var i = 0;i<opaque_squares.length;i++){
        //if mouse has hvered, add the Opaque Circle object in the draw erased circles array.

        // opaque_squares[i].mouseOver(changestate)
        if(opaque_squares[i].checkiferase() && opaque_squares[i].erased == false){
            // change the opaque element property to true
            opaque_squares[i].erased = true;

            // an array that contains the  center's x coordinte, center's y coordinates and the diameter of the erased opaque element and the id of the opaque square
            mouse_positions_log_click.push([timeElapsed,mouseX,mouseY,[opaque_squares[i].x,opaque_squares[i].y,opaque_squares[i].sl,opaque_squares[i].id]])
            draw_erased_squares.push(opaque_squares[i]);
        }
    }

    // using p5's erase function, erase all of the circles that the mouse has hovered on
    if(draw_erased_squares.length!=0){
        for (var i = 0;i<draw_erased_squares.length;i++){
            draw_erased_squares[i].draw_erased();
        }
    }


}

class Opaque_Square{
    //constructor function
    constructor(x_position,y_position,side_length,id){
        this.x = x_position;
        this.y = y_position;
        this.sl = side_length;
        this.erased = false;
        this.id = id;
    }
    draw(){
        //draws the circle with an opaque color

        //use stroke
        noStroke();
        // strokeWeight(1);
        fill(114, 78, 140)
        rect(this.x,this.y,this.sl,this.sl);  


    }
    draw_erased(){
        //use the erase p5 function to erase the circle from the canvas
        erase();
        // rect(this.x,this.y,this.sl,this.sl);  
        rect(this.x,this.y,this.sl,this.sl);  
        noErase();
    }
    checkiferase(){
        //Upper and lower bounds for the circle
        var lower_x = this.x;
        var upper_x = this.x+this.sl;
        var lower_y = this.y;
        var upper_y = this.y+this.sl;


        //Check whether orr not the mouse lies on top of the circle and if the mouse is clicked
        if((lower_x<mouseX && mouseX<upper_x)&&(lower_y<mouseY && mouseY<upper_y) && is_mouse_Clicked ==true){
            return true;
        }
        else{
            return false;
        }
        
    }


}

// Helper function to round appropiately from https://gist.github.com/djD-REK/068cba3d430cf7abfddfd32a5d7903c3 and https://medium.com/swlh/how-to-round-to-a-certain-number-of-decimal-places-in-javascript-ed74c471c1b8
const roundAccurately = (number, decimalPlaces) => Number(Math.round(number + "e" + decimalPlaces) + "e-" + decimalPlaces)

function submit_result(){
    var loading_icon = document.getElementById("loader-container");
    var task = document.getElementById("task-container");

    var user_answer = $('#user_answer').val()
    // only allow for a valid input, which is an integer from 0 to 9
    if (user_answer == '' || user_answer<0 || user_answer>9){
        $('#user_answer').val('');
        $("#user_answer").focus();
    }
    else{
        //show loading screen
        loading_icon.style.display = "block";
        // hide task UI element to prevent accumulation of requests while loading
        task.style.display = "none";
        console.log(user_answer);
        //Remembeer to record time on submission
        console.log("Submit result");
        console.log("User Answer: \n",user_answer);

        MNIST_dataset_index = parseInt(MNIST_dataset_index);
        current_task_number = parseInt(current_task_number);
        last_task_submitted_id = parseInt(last_task_submitted_id);
        var user_entry = {
            actual_label:actual_label,
            MNIST_dataset_index:MNIST_dataset_index,
            eraser_size: eraser_side_length,
            remainder_points:remainder_points,
            answer:user_answer,
            remaining_mask:remaining_mask,
            task_duration: timeElapsed,
            current_user_id : current_user_id,
            current_task_number: current_task_number,
            last_task_submitted_id:last_task_submitted_id,
            mouse_positions_click:mouse_positions_log_click,
            mouse_positions_noclick:mouse_positions_log_noclick
        }
        
        max_task_number =  parseInt(max_task_number)
        
        debugdata(user_entry)
    
        // fetch takes in two arguments: location to post and an init constructor
    


//#######################BACKEND CONNECTION ##################################################

        // Modified from: https://www.youtube.com/watch?v=QKcVjdLEX_s


        fetch(`${window.origin}/processdata`,{
            method:"POST",
            credentials:"include",
            body: JSON.stringify(user_entry),
            cache:"no-cache",
            headers:new Headers({
                "content-type":"application/json"
            })
    
        }).then(function (response){
            console.log(response);
            if (response.status!== 200){
                console.log(`Response status was not 200: [${response.status}]`);
                console.log(response)
                response.json().then(function(data){
                    console.log("400 data, we will redirect the user where he needs to go")
                    console.log(data);
                    var correct_current_task_number = data.current_task_number
                    var current_user_id = data.current_user_id
                    console.log("correct task number",correct_current_task_number);
                    console.log("current user id",current_user_id);
                    window.location = window.origin + "/tasksequence" +'?' + 'current_task_number='+correct_current_task_number+ '&'+ 'current_user_id='+current_user_id
                })
            }
            else{
                response.json().then(function(data){
                    console.log("Use the response to direct user where thye need to go")
                    console.log(data);
                    if (max_task_number < current_task_number){
                        //sent user to submission page, they are done with the task
                        console.log("DONE WOHIOOOOO")
                        console.log("Current task number",current_task_number)
                        console.log("Current user id", current_user_id)
                        var submission_complete_url = window.origin + "/submission-complete"+'?'+'current_task_number='+current_task_number + '&'+ 'current_user_id='+current_user_id
                        console.log(submission_complete_url)
                        window.location = window.origin + "/submission-complete"+'?'+'current_task_number='+current_task_number + '&'+ 'current_user_id='+current_user_id
                        
                
                    }
                    else{
                        var next_task_number = parseInt(current_task_number);
                        next_task_number+=1;
                        console.log("Next task number",next_task_number);
                        // user is still in task sequence
                        var task_submission_url = window.origin + "/tasksequence" +'?' + 'current_task_number='+next_task_number + '&'+ 'current_user_id='+current_user_id
                        console.log("Taks submission url", task_submission_url)
                        window.location = task_submission_url
                
                    }
                })
            }
        })


//#######################BACKEND CONNECTION ##################################################





    }        
}

// Helper function that helps me debug the data that is collected
function debugdata(user_entry){
    console.log(user_entry);

}