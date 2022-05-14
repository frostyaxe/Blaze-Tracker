/*

	
	Description: Handles the unregistration of an application. Displays the danger alert 
				 if application details does not exist.
			
	Author: Abhishek Prajapati
	Created On: 11-04-2022
	
*/

$(document).ready(function(){

	$('#submitForm').click(function(event){
		   $("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
			});
			var emails = [];
	       document.querySelectorAll("div#emailAddress ul li").forEach((ele) => {
	          emails.push(ele.innerHTML.replace(/ /g, ""));
	       });
	
	       console.log(JSON.stringify(emails));
			event.preventDefault();
			$('#alertContainer').removeClass("d-flex");
			$('#alertContainer').hide();
			$.ajax('/application/unregistration', {
			    type: 'DELETE',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ applicationName: $('#appName').val() }),  // data to submit
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


