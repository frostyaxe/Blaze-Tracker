/*

	
	Description: Handles the password update of the admin user.
			
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
 	$('#newPass, #confirmPass').on('keyup', function () {
	    $("#status").removeClass (function (index, className) {
  			return (className.match (/(^|\s)fa-\S+/g) || []).join(' ');
		});
		  if ($('#newPass').val() == $('#confirmPass').val()) {
		    $('#status').addClass('fa fa-check').css('color', 'green').attr('title',"Password Matched");
		  } else {
		    $('#status').addClass('fa fa-close').css('color', 'red').attr('title',"Password didn't match");
		}
	  });
	$('#submitForm').click(function(event){
			event.preventDefault();
			var newPassword = $('#newPass').val()
			var confirmPassword = $('#confirmPass').val() 
			$.ajax('/admin/passwordChange', {
			    type: 'POST',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ newPassword: newPassword, confirmPassword:  confirmPassword}),  // data to submit
				beforeSend: function(){
					if(check_empty(newPassword)) {
						display_message("alert-danger","Please provide new password for the password change!");
						return false;
					}
					if(check_empty(confirmPassword)) {
						display_message("alert-danger","Please provide the new password again in confirm password field!");
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


