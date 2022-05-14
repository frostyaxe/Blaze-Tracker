
/*

	Description: Verifies the application name and navigates to the dashboard URL
	Author: Abhishek Prajapati
	Created On: 09-04-2022
	
*/

$(document).ready(function(){
	$("#appNameForm").submit(function(e){
		
		$("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
			});
		
		e.preventDefault();
		var appName = $("#appName").val()
		
		if( !appName ) {
         	alert("Application name must not be empty!")
    	}
	
		$.ajax('/', {
			    type: 'POST',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ applicationName: $('#appName').val() }),  // data to submit
			    success: function (response, status, xhr) {
				
					$('#indexAlert').text('')
		            $('#indexAlert').append('<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"] + " redirecting to dashboard page...");
					$('#alertContainer').addClass("d-flex")
					$('#alertContainer').addClass("alert-success")
					$('#indexAlert').show();
					$('#alertContainer').show()
					setTimeout(function() {
						window.location.href = "/"+appName+"/view/dashboard";  
					}, 2000);
					return true

			    },
			    error: function (jqXhr, textStatus, errorMessage) {
				
						response = JSON.parse(jqXhr.responseText)
						$('#indexAlert').text('')
			            $('#indexAlert').append('<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
						$('#alertContainer').addClass("d-flex")
						$('#alertContainer').addClass("alert-danger")
						$('#indexAlert').show();
						$('#alertContainer').show()
						return false
			    }
			});
		
	});
});

