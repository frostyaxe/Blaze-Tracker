
/*

	Handles the activities related to the application details update.
	
*/


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

/*
Description: Verifies the value provided in the field must not be empty. If it is empty then it will return True else False.
*/
function check_empty(value){
	if(value.trim()==''){
		return true;
	}
	return false;
}

$(document).ready(function(){
		
		$('#appNameBtn').click(function(event){
			
				var appName = $("#appName").val()
				$("#shortDescription").val("")
				$("div#emailAddress ul").empty();
				$.ajax("/admin/"+appName+'/getApplicationDetails', {
					
					    type: 'GET',  // http method
						contentType: "application/json",
						dataType: "json",
						beforeSend: function(){
							if(check_empty(appName)) {
								displayToast("bg-danger","Application Name is empty")
								return false
							}
						},
						success: function (response, status, xhr) {
						displayToast("bg-success",response["message"])
						
						$("#shortDescription").val(response["details"]["APPLICATION_DESCRIPTION"])
						var emailIds = response["details"]["NOTIFICATION_EMAIL_IDS"].split(",")
						emailIds.forEach(function( item ) {
							
							let li  = document.createElement('li');
               				li.innerHTML = item;
							$("div#emailAddress ul").append(li)
							li.addEventListener("click", function (e) {
			
			                   e.target.parentNode.removeChild(e.target);
			                });
						});
								
					    },
					    error: function (jqXhr, textStatus, errorMessage) {
							response = JSON.parse(jqXhr.responseText)
							displayToast("bg-danger",response["message"])
					    }
				});
				
				
			
		});
});

$(document).ready(function(){
		
		$('#submitForm').click(function(event){
				
				var applicationName = $("#appName").val()
				var shortDescription = $('#shortDescription').val()
				var emails = [];
		        document.querySelectorAll("div#emailAddress ul li").forEach((ele) => {
		          emails.push(ele.innerHTML.replace(/ /g, ""));
		       });
					
				var emailAddress =  emails.join(",")
				$.ajax("/admin/registrationUpdate", {
					
					    type: 'PUT',  // http method
						contentType: "application/json",
						dataType: "json",
						data:JSON.stringify({ applicationName: applicationName, shortDescription: shortDescription, emailAddress: emailAddress}),
						beforeSend: function(){
							if(check_empty(applicationName)) {
								displayToast("bg-danger","Application Name is empty")
								return false
							}
							if(check_empty(shortDescription)) {
								displayToast("bg-danger","Short Description is empty")
								return false
							}
							if(check_empty(emailAddress)) {
								displayToast("bg-danger","Email Address is empty")
								return false
							}
						},
					    success: function (response, status, xhr) {
						displayToast("bg-success",response["message"])
					    },
					    error: function (jqXhr, textStatus, errorMessage) {
							response = JSON.parse(jqXhr.responseText)
							displayToast("bg-danger",response["message"])
					    }
				});
		});
});
