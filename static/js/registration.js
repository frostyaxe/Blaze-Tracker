/*

	
	Description: Handles the registration of an application. Displays the danger alert 
				 if application details exists else it will add the record in the database.
			
	Author: Abhishek Prajapati
	Created On: 11-04-2022
	
*/

/*
Description: Verifies the value provided in the field must not be empty. If it is empty then it will return True else False.
*/
function check_empty(value){
	if(value.trim()==''){
		return true;
	}
	return false;
}
/*
Description: Dislays the error message on the alert box over the page.	
*/
function display_message(className,message){
	$('#alertContainer').removeClass("d-flex");
	$('#registrationAlert').text('');
    $('#registrationAlert').append(message);
	$('#alertContainer').addClass("d-flex");
	$('#alertContainer').addClass(className);
	$('#registrationAlert').show();
	$('#alertContainer').show();
}

/*
Submits the details provided for the registration of the desired application
*/
$(document).ready(function(){
	$('#alertContainer').hide();
	$('#submitForm').click(function(event){
			var emails = [];
	       document.querySelectorAll("div#emailAddress ul li").forEach((ele) => {
	          emails.push(ele.innerHTML.replace(/ /g, "").trim());
	       });
			event.preventDefault();
			var applicationName = $('#appName').val()
			var shortDescription = $('#shortDescription').val()
			var emails = emails.join(",")
			$.ajax('/application/registration', {
			    type: 'POST',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ applicationName: applicationName, shortDescription: shortDescription, emailAddress: emails }),  // data to submit
				beforeSend: function(){
					if(check_empty(applicationName)) {
						display_message("alert-danger","Application Name is empty");
						return false;
					}
					if(check_empty(shortDescription)) {
						display_message("alert-danger","Short description is empty");
						return false;
					}
					if(check_empty(emails)) {
						display_message("alert-danger","Email IDs are missing. Please provide the value in the field.");
						return false;
					}
				},
			    success: function (response, status, xhr) {
		            display_message("alert-success",'<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"]);
			    },
			    error: function (jqXhr, textStatus, errorMessage) {
					response = JSON.parse(jqXhr.responseText)
		            display_message("alert-danger",'<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
			    }
			});
	});
});


