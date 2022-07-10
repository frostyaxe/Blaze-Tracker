/*

	Description: Handles the pause/resume build queue requests based on the requirement
	Author: Abhishek Prajapati
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
var resumedCode = "0"
var pausedCode = "1"
$(document).ready(function(){
	$('#resumeQueueBtn').click(function(event){
		$.ajax("/admin/manageBuildQueue/"+resumedCode, {
			    type: 'PUT',  // http method
			    success: function (response, status, xhr) {
					displayToast("bg-success",response["message"]);
					$("#status").html('Resumed');
			    },
			    error: function (jqXhr, textStatus, errorMessage) {
					response = JSON.parse(jqXhr.responseText)
					displayToast("bg-danger",response["message"])
			    }
		});
	});
});
$(document).ready(function(){
	$('#pauseQueueBtn').click(function(event){
		$.ajax("/admin/manageBuildQueue/"+pausedCode, {
			    type: 'PUT',  // http method
			    success: function (response, status, xhr) {
					displayToast("bg-success",response["message"]);
					$("#status").html('Paused');
			    },
			    error: function (jqXhr, textStatus, errorMessage) {
					response = JSON.parse(jqXhr.responseText)
					displayToast("bg-danger",response["message"])
			    }
		});
	});
});