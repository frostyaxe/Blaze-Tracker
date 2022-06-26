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

function display_error(message){
	$('#registrationAlert').text('')
    $('#registrationAlert').append(message);
	$('#alertContainer').addClass("d-flex")
	$('#alertContainer').addClass("alert-danger")
	$('#registrationAlert').show();
	$('#alertContainer').show()
}

$(document).ready(function(){

	$('#submitForm').click(function(event){
		   $("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
			});

	      	var notificationTitle = $('#notificationTitle').val()
			var notificationMessage=$('#notificationMessage').val()
			event.preventDefault();
			$('#alertContainer').removeClass("d-flex");
			$('#alertContainer').hide();
			$.ajax('/admin/notifier', {
			    type: 'POST',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ notificationTitle: notificationTitle,notificationMessage: notificationMessage}),  // data to submit
				beforeSend: function(){
					if(check_empty(notificationTitle)) {
						display_error("Notification Title is empty");
						return false;
					}
					if(check_empty(notificationMessage)) {
						display_error("Notification Message is empty");
						return false;
					}
				},
			    success: function (response, status, xhr) {
				
					$('#registrationAlert').text('')
		            $('#registrationAlert').append('<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"]);
					$('#alertContainer').addClass("d-flex")
					$('#alertContainer').addClass("alert-success")
					$('#registrationAlert').show();
					$('#alertContainer').show()

			    },
			    error: function (jqXhr, textStatus, errorMessage) {
				
						response = JSON.parse(jqXhr.responseText)
						display_error('<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
					
			    }
			});
	});
});


$(document).ready(function(){

	$('#displayNotice').click(function(event){
		   $("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
			});

			event.preventDefault();
			$('#alertContainer').removeClass("d-flex");
			$('#alertContainer').hide();
			$.ajax('/admin/manageNotice/1', {
			    type: 'PUT',  // http method
				contentType: "application/json",
			    success: function (response, status, xhr) {
				
					$('#registrationAlert').text('')
		            $('#registrationAlert').append('<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"]);
					$('#alertContainer').addClass("d-flex")
					$('#alertContainer').addClass("alert-success")
					$('#registrationAlert').show();
					$('#alertContainer').show()
					
					setTimeout(function(){
           			location.reload(); 
      				}, 5000);

			    },
			    error: function (jqXhr, textStatus, errorMessage) {
				
						response = JSON.parse(jqXhr.responseText)
						display_error('<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
					
			    }
			});
	});
});

$(document).ready(function(){

	$('#hideNotice').click(function(event){
		   $("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
			});

			event.preventDefault();
			$('#alertContainer').removeClass("d-flex");
			$('#alertContainer').hide();
			$.ajax('/admin/manageNotice/0', {
			    type: 'PUT',  // http method
				contentType: "application/json",
			    success: function (response, status, xhr) {
					
					
					$('#registrationAlert').text('')
		            $('#registrationAlert').append('<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"]);
					$('#alertContainer').addClass("d-flex")
					$('#alertContainer').addClass("alert-success")
					$('#registrationAlert').show();
					$('#alertContainer').show()
					
					 setTimeout(function(){
           			location.reload(); 
      				}, 5000);

			    },
			    error: function (jqXhr, textStatus, errorMessage) {
				
						response = JSON.parse(jqXhr.responseText)
						display_error('<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
					
			    }
			});
	});
});

