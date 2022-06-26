$(document).ready(function(){
	
	
$('#resumeQueue').click(function(event){
	$("#toastMessage").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
			});
		
			var toastMessage =document.getElementById('toastMessage');//select id of toast
			var toastBody = $("#toastBody")
			$.ajax("/admin/manageBuildQueue/0", {
				
				    type: 'PUT',  // http method
				    success: function (response, status, xhr) {
						toastMessage.classList.add("bg-success");
						toastBody.empty();
						toastBody.append(response["message"]);
				    },
				    error: function (jqXhr, textStatus, errorMessage) {
						response = JSON.parse(jqXhr.responseText)
						toastMessage.classList.add("bg-danger");
						toastBody.empty();
						toastBody.append(response["message"]);
				    }
			});
			var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
		 	bsAlert.show();//show it
			
	});
});


	
$(document).ready(function(){
$('#pauseQueue').click(function(event){
	$("#toastMessage").removeClass (function (index, className) {
  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
			});
		
			var toastMessage =document.getElementById('toastMessage');//select id of toast
			var toastBody = $("#toastBody")
			$.ajax("/admin/manageBuildQueue/1", {
				
				    type: 'PUT',  // http method
				    success: function (response, status, xhr) {
						toastMessage.classList.add("bg-success");
						toastBody.empty();
						toastBody.append(response["message"]);
				    },
				    error: function (jqXhr, textStatus, errorMessage) {
						response = JSON.parse(jqXhr.responseText)
						toastMessage.classList.add("bg-danger");
						toastBody.empty();
						toastBody.append(response["message"]);
				    }
			});
			var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
		 	bsAlert.show();//show it
			
	});
});