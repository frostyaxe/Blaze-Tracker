/*
	
	Handles the execution in the dashboard page.

*/
function check_empty(value){
	if(value.trim()==''){
		return true;
	}
	return false;
}
function displayToast(alertClass, message){
	$("#toastMessage").removeClass (function (index, className) {
	  	 return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
	});
	var toastMessage =document.getElementById('toastMessage');//select id of toast
	var toastBody = $("#toastBody")
	toastMessage.classList.add(alertClass);
	toastBody.empty();
	toastBody.append(message);
	var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
	bsAlert.show();//show it
}
var appName = "default"
var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
function set_app_name(appName){ this.appName = appName; }
$(document).ready(function(){
	$('#generateCodeBtn').click(function(event){
		$.ajax("/"+appName+'/getRemoveTrackerCode', {
		    type: 'GET',  // http method
			contentType: "application/json",
			dataType: "json",
		    success: function (response, status, xhr) {
			displayToast("bg-success",response["message"]);
		    },
		    error: function (jqXhr, textStatus, errorMessage) {
				response = JSON.parse(jqXhr.responseText)
				displayToast("bg-danger",response["message"])
		    }
		});
	});
});
$(document).ready(function(){
	$('#trackerRemoveBtn').click(function(event){
	var secretCode = $("#trackerRemoveTxt").val()
	if(secretCode){
		$.ajax("/"+appName+'/removeTracker/'+secretCode, {
			    type: 'DELETE',  // http method
				contentType: "application/json",
				dataType: "json",
				beforeSend: function(){
					if(check_empty(secretCode)) {
						displayToast("bg-danger","Cannot proceed with the empty secret code.");
						return false;
					}
				},
			    success: function (response, status, xhr) {
					displayToast("bg-success",response["message"]);
			    },
			    error: function (jqXhr, textStatus, errorMessage) {
					response = JSON.parse(jqXhr.responseText)
					displayToast("bg-danger",response["message"]);
			    }
			});
		} else {
			displayToast("bg-danger","Provided code must not be empty!");
		}
	});
});
function resumePipeline(pauseId, taskName){
	var secretCode = $("#inputSecretCode"+pauseId).val()
	$.ajax("/"+appName+'/task/resumePipeline', {
		    type: 'POST',  // http method
			contentType: "application/json",
			dataType: "json",
		    data:JSON.stringify({resumeCode: secretCode, taskName: taskName  }),  // data to submit
			beforeSend: function(){
					if(check_empty(secretCode)) {
						displayToast("bg-danger","Cannot proceed with the empty secret code.");
						return false;
					}
					if(check_empty(taskName)) {
						displayToast("bg-danger","Cannot proceed with the empty task name.");
						return false;
					}
				},
		    success: function (response, status, xhr) {
				displayToast("bg-success",response["message"]);
				setTimeout(function() {
			    location.reload();
				}, 5000);
		    },
		    error: function (jqXhr, textStatus, errorMessage) {
				response = JSON.parse(jqXhr.responseText)
				displayToast("bg-danger",response["message"]);
		    }
	});
}
(function() {

    const idleDurationSecs = 300;    // X number of seconds
    const redirectUrl = '/';  // Redirect idle users to this URL
    let idleTimeout; // variable to hold the timeout, do not modify

    const resetIdleTimeout = function() {

        // Clears the existing timeout
        if(idleTimeout) clearTimeout(idleTimeout);

        // Set a new idle timeout to load the redirectUrl after idleDurationSecs
        idleTimeout = setTimeout(() => location.href = redirectUrl, idleDurationSecs * 1000);
    };

    // Init on page load
    resetIdleTimeout();

    // Reset the idle timeout on any of the events listed below
    ['click', 'touchstart', 'mousemove'].forEach(evt => 
        document.addEventListener(evt, resetIdleTimeout, false)
    );

})();

function updateTimeZone(){
	
	timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
	document.getElementById("report_download").setAttribute("href","/"+ appName +"/report?timezone="+timezone);
}
function updateTasks(){
{
   updateTimeZone()
   $.ajax({

     type: "GET",
     url: '/'+appName+"/getTasks",
	 data: {"timezone":timezone},
     success: function(data) {
          $('#tasksContainer').html(data);
     }

   });

}

}

window.onload = function(){
	updateTasks()
};

setInterval( updateTasks, 30000 );	