/*

	
	Description: Handles the unregistration of an application. Displays the danger alert 
				 if application details does not exist.
			
	Author: Abhishek Prajapati
	Created On: 11-04-2022
	
*/
function check_empty(value){
	if(value.trim()==''){
		return true;
	}
	return false;
}
function display_message(className, message){
	$("#alertContainer").removeClass (function (index, className) {
  	  	return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
	});
	$('#alertContainer').removeClass("d-flex");
	$('#registrationAlert').text('')
    $('#registrationAlert').append(message);
	$('#alertContainer').addClass("d-flex")
	$('#alertContainer').addClass(className)
	$('#registrationAlert').show();
	$('#alertContainer').show()
}
$(document).ready(function(){
	$('#alertContainer').hide();
	$('#submitForm').click(function(event){
			var emails = [];
	       document.querySelectorAll("div#emailAddress ul li").forEach((ele) => {
	          emails.push(ele.innerHTML.replace(/ /g, ""));
	       });
			var applicationName = $('#appName').val()
			event.preventDefault();
			$.ajax('/application/unregistration', {
			    type: 'DELETE',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ applicationName:  applicationName}),  // data to submit
				beforeSend: function(){
					if(check_empty(applicationName)) {
						display_message("alert-danger","Application Name is empty");
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


