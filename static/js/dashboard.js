
/*
	
	Handles the execution in the dashboard page.

*/

var appName = "default"

function set_app_name(appName){
	
	this.appName = appName;
	
}


$(document).ready(function(){
		
		$('#generateCodeBtn').click(function(event){
			var toastMessage =document.getElementById('toastMessage');//select id of toast
	 		var toastBody = $("#toastBody")
				$("#toastMessage").removeClass (function (index, className) {
	  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
				});
					
			
				$.ajax("/"+appName+'/getRemoveTrackerCode', {
					
					    type: 'GET',  // http method
						contentType: "application/json",
						dataType: "json",
					    success: function (response, status, xhr) {
						console.log(response)
							toastMessage.classList.add("bg-success");
							toastBody.empty();
							toastBody.append(response["message"]);
							var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
							bsAlert.show();//show it
			
								
					    },
					    error: function (jqXhr, textStatus, errorMessage) {
							response = JSON.parse(jqXhr.responseText)
							toastMessage.classList.add("bg-danger");
							toastBody.empty();
							toastBody.append(response["message"]);
							var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
							bsAlert.show();//show it
					    }
				});
				
				
			
		});
});

$(document).ready(function(){
	
	
$('#trackerRemoveBtn').click(function(event){
	$("#toastMessage").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
			});
		
	var secretCode = $("#trackerRemoveTxt").val()
	var toastMessage =document.getElementById('toastMessage');//select id of toast
	var toastBody = $("#toastBody")
	if(secretCode){
			
			$.ajax("/"+appName+'/removeTracker/'+secretCode, {
				
				    type: 'DELETE',  // http method
					contentType: "application/json",
					dataType: "json",
				    success: function (response, status, xhr) {
						toastMessage.classList.add("bg-success");
						toastBody.empty();
						toastBody.append(response["message"]);
						
							
				    },
				    error: function (jqXhr, textStatus, errorMessage) {
						response = JSON.parse(jqXhr.responseText)
						toastMessage.classList.add("bg-danger");
						toastBody.empty();
						toastBody.append(response["message"]);
				    }
			});
			
		   
		} else {
			toastMessage.classList.add("bg-danger");
			toastBody.empty();
			toastBody.append("Provided code must not be empty!");
		}
		
		 var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
		 bsAlert.show();//show it
	});
});

function resumePipeline(pauseId, taskName){
	
	$("#toastMessage").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
			});
		
	var secretCode = $("#inputSecretCode"+pauseId).val()
	 var toastMessage =document.getElementById('toastMessage');//select id of toast
	var toastBody = $("#toastBody")
	$.ajax("/"+appName+'/task/resumePipeline', {
		
		    type: 'POST',  // http method
			contentType: "application/json",
			dataType: "json",
		    data:JSON.stringify({resumeCode: secretCode, taskName: taskName  }),  // data to submit
		    success: function (response, status, xhr) {
				toastMessage.classList.add("bg-success");
				toastBody.empty();
				toastBody.append(response["message"]);
				
				setTimeout(function() {
			    location.reload();
				}, 5000);
							
		    },
		    error: function (jqXhr, textStatus, errorMessage) {
				response = JSON.parse(jqXhr.responseText)
				toastMessage.classList.add("bg-danger");
				toastBody.empty();
				toastBody.append(response["message"]);
		    }
	});
	
    var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
    bsAlert.show();//show it

}


(function() {

    const idleDurationSecs = 60;    // X number of seconds
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


function updateTasks(){
{
   $.ajax({

     type: "GET",
     url: '/'+appName+"/getTasks",
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