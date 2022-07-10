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
      	var notificationTitle = $('#notificationTitle').val()
		var notificationMessage=$('#notificationMessage').val()
		event.preventDefault();
		$.ajax('/admin/notifier', {
		    type: 'POST',  // http method
			contentType: "application/json",
			dataType: "json",
		    data:JSON.stringify({ notificationTitle: notificationTitle,notificationMessage: notificationMessage}),  // data to submit
			beforeSend: function(){
				if(check_empty(notificationTitle)) {
					display_message("alert-danger","Notification Title is empty");
					return false;
				}
				if(check_empty(notificationMessage)) {
					display_message("alert-danger","Notification Message is empty");
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
$(document).ready(function(){
	$('#displayNotice').click(function(event){
		event.preventDefault();
		$.ajax('/admin/manageNotice/1', {
		    type: 'PUT',  // http method
			contentType: "application/json",
		    success: function (response, status, xhr) {
	            display_message("alert-success",'<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"]);
				setTimeout(function(){
       			location.reload(); 
  				}, 5000);
		    },
		    error: function (jqXhr, textStatus, errorMessage) {
				response = JSON.parse(jqXhr.responseText)
				display_message("alert-danger",'<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
		    }
		});
	});
});
$(document).ready(function(){
	$('#hideNotice').click(function(event){
		event.preventDefault();
		$.ajax('/admin/manageNotice/0', {
		    type: 'PUT',  // http method
			contentType: "application/json",
		    success: function (response, status, xhr) {
	            display_message("alert-success",'<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"]);
				 setTimeout(function(){
       			location.reload(); 
  				}, 5000);
		    },
		    error: function (jqXhr, textStatus, errorMessage) {
				response = JSON.parse(jqXhr.responseText)
				display_message("alert-danger",'<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
		    }
		});
	});
});

