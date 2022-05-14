
/*

	Handles the activities related to the application details update.
	
*/

$(document).ready(function(){
		
		$('#appNameBtn').click(function(event){
				var toastMessage =document.getElementById('toastMessage');//select id of toast
		 		var toastBody = $("#toastBody")
					$("#toastMessage").removeClass (function (index, className) {
		  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
					});
					
				var appName = $("#appName").val()
				$("#shortDescription").val("")
				$("div#emailAddress ul").empty();
				$.ajax("/admin/"+appName+'/getApplicationDetails', {
					
					    type: 'GET',  // http method
						contentType: "application/json",
						dataType: "json",
					    success: function (response, status, xhr) {
						toastMessage.classList.add("bg-success");
						toastBody.empty();
						toastBody.append(response["message"]);
						var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
						bsAlert.show();//show it
						
						$("#shortDescription").val(response["details"]["APPLICATION_DESCRIPTION"])
						var emailIds = response["details"]["NOTIFICATION_EMAIL_IDS"].split(",")
						emailIds.forEach(function( item ) {
							
							let li  = document.createElement('li');
               				li.innerHTML = item;
							$("div#emailAddress ul").append(li)
							li.addEventListener("click", function (e) {
			
			                   e.target.parentNode.removeChild(e.target);
			                });
						});
								
					    },
					    error: function (jqXhr, textStatus, errorMessage) {
							response = JSON.parse(jqXhr.responseText)
							console.log(response["message"]);
							toastMessage.classList.add("bg-danger");
							toastBody.empty();
							toastBody.append(response["message"]);
							var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
							bsAlert.show();//show it
					    }
				});
				
				
			
		});
});

$(document).ready(function(){
		
		$('#submitForm').click(function(event){
				var toastMessage =document.getElementById('toastMessage');//select id of toast
		 		var toastBody = $("#toastBody")
					$("#toastMessage").removeClass (function (index, className) {
		  	  			return (className.match (/(^|\s)bg-\S+/g) || []).join(' ');
					});
					
				var appName = $("#appName").val()
				var emails = [];
		        document.querySelectorAll("div#emailAddress ul li").forEach((ele) => {
		          emails.push(ele.innerHTML.replace(/ /g, ""));
		       });
					
				
				$.ajax("/admin/registrationUpdate", {
					
					    type: 'PUT',  // http method
						contentType: "application/json",
						dataType: "json",
						data:JSON.stringify({ applicationName: $('#appName').val(), shortDescription: $('#shortDescription').val(), emailAddress: emails.join(",") }), 
					    success: function (response, status, xhr) {
						toastMessage.classList.add("bg-success");
						toastBody.empty();
						toastBody.append(response["message"]);
						var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
						bsAlert.show();//show it
						
					    },
					    error: function (jqXhr, textStatus, errorMessage) {
							response = JSON.parse(jqXhr.responseText)
							console.log(response["message"]);
							toastMessage.classList.add("bg-danger");
							toastBody.empty();
							toastBody.append(response["message"]);
							var bsAlert = new bootstrap.Toast(toastMessage);//inizialize it
							bsAlert.show();//show it
					    }
				});
				
				
			
		});
});
