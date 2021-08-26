console.log("Device.js is here!!!")
console.log(current_task_number)

function revealinputtext(){
    console.log("Reveal input text");
    if ($('#r3').is(':checked')){
        console.log("is checkeeeed");
        console.log(document.getElementById('reveal-if-active'));
        
        document.getElementById('reveal-if-active').style.opacity = 1;
    }
    else{
        document.getElementById('reveal-if-active').style.opacity = 0;

    }
}

function submit_result(){
    console.log("Submit Result nooooow");
    var selection = document.querySelector('input[name="device"]:checked').value;
    // console.log(selection);
    if (selection == "other"){
        var other_device = document.getElementById('other').value;
        if(other_device == ""){
            $("#other").focus();
            return null;
        }
        selection = other_device;  
    }

    var user_entry = {
        device:selection,
        current_user_id:parseInt(current_user_id)
    }
    fetch(`${window.origin}/device`,{
        method:"POST",
        credentials:"include",
        body: JSON.stringify(user_entry),
        cache:"no-cache",
        headers:new Headers({
            "content-type":"application/json"
        })

    }).then(function (response){
        response.json().then(data => {
            console.log(data);
            console.log("DONE WOHIOOOOO")
            console.log("Current task number",current_task_number)
            console.log("Current user id", current_user_id)
            var submission_complete_url = window.origin + "/submission-complete"+'?'+'current_task_number='+current_task_number + '&'+ 'current_user_id='+current_user_id
            window.location = submission_complete_url
        })

    })
}
