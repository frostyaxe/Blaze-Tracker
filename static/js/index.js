
/*

	Description: Verifies the application name and navigates to the dashboard URL
	Author: Abhishek Prajapati
	Created On: 09-04-2022
	
*/

function display_message(className, message){
	$('#alertContainer').removeClass("d-flex")
	$('#indexAlert').text('')
    $('#indexAlert').append(message);
	$('#alertContainer').addClass("d-flex")
	$('#alertContainer').addClass(className)
	$('#indexAlert').show();
	$('#alertContainer').show()
}
function check_empty(value){
	if(value.trim()==''){
		return true;
	}
	return false;
}
$(document).ready(function(){
	$('#alertContainer').hide();
	$("#appNameForm").submit(function(e){
		$("#alertContainer").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)alert-\S+/g) || []).join(' ');
		});
		e.preventDefault();
		var appName = $("#appName").val()

		$.ajax('/', {
			    type: 'POST',  // http method
				contentType: "application/json",
				dataType: "json",
			    data:JSON.stringify({ applicationName: appName }),  // data to submit
				beforeSend: function(){
					if(check_empty(appName)) {
						display_message("alert-danger",'Application Name must not be empty!')
						return false;
					}
				},
			    success: function (response, status, xhr) {
					display_message("alert-success",'<b>Status:</b> ' + response["status"] +", <b>Message:</b> " + response["message"] + " redirecting to dashboard page...")
					setTimeout(function() {
						window.location.href = "/"+appName+"/view/dashboard";  
					}, 2000);
					return true
			    },
			    error: function (jqXhr, textStatus, errorMessage) {
					response = JSON.parse(jqXhr.responseText)
		            display_message("alert-danger",'<b>Error:</b> ' + errorMessage +", <b>Message:</b> " + response["message"]);
					return false
			    }
		 });
	});
});

