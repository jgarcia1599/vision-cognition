console.log("Hiiii")

//UI function to scroll down user to the bottom of the page
$('#scrolldownimg').click(function(){
    $("html, body").animate({ scrollTop: $(document).height() }, 1000);
})
// function to toggle the Unique MNIST Dataset submission element
function showMNISTData(){
    var data = document.getElementById("mnistuniquesubmissiondata");
    var scroll_down = document.getElementById("scrolldownimg");
    if (data.style.display === "none") {
      data.style.display = "block";
      scroll_down.style.display = "block";

    } else {
      data.style.display = "none";
      scroll_down.style.display = "none";
    }
}