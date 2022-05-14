/*

	
	Description: Handles the password update of the admin user.
			
	Author: Abhishek Prajapati
	Created On: 11-04-2022
	
*/

$(document).ready(function(){

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
		
		   $("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
			});
			
			event.preventDefault();
			$('#alertContainer').removeClass("d-flex");
			$('#alertContainer').hide();
			$.ajax('/admin/passwordChange', {
			    type: 'POST',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ newPassword: $('#newPass').val(), confirmPassword: $('#confirmPass').val()  }),  // data to submit
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
						$('#registrationAlert').text('')
			            $('#registrationAlert').append('<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
						$('#alertContainer').addClass("d-flex")
						$('#alertContainer').addClass("alert-danger")
						$('#registrationAlert').show();
						$('#alertContainer').show()
			    }
			});
			
	});
});


