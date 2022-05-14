/*
	
	Handles the activities related to addition/removal of the email addresses.

*/

class AddEmails {
    constructor() {
       this.emailInput = document.getElementById("email");
       this.emailListContainer = document.querySelector("div#emailAddress ul");
    }
    // some regex copied from internet
    isValidEmail(val) {
       let re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
       return re.test(val);
    }

    getEmails() {
       var emails = [];
       document.querySelectorAll("div#emailAddress ul li").forEach((ele) => {
          emails.push(ele.innerHTML.replace(/ /g, ""));
       });

       console.log(JSON.stringify(emails));
    }

    init() {
       this.emailInput.onkeyup = (e) => {

          if (e.keyCode == 0 || e.keyCode == 32 || e.keyCode == 13 || e.keyCode == 188) {

             let val = e.target.value.trim().replace(/ /g, "").replace(/,/g, "");

             if (this.isValidEmail(val)) {
                console.log(val);

                let li = document.createElement('li');
                li.innerHTML = val;
                this.emailListContainer.appendChild(li);
                this.emailInput.value = "";

                // removing email from the list
                li.addEventListener("click", function (e) {

                   e.target.parentNode.removeChild(e.target);
                });

                this.getEmails();

                return;
             }
          }
       }


    }


 }

 var addEmails = new AddEmails();
 addEmails.init();

function getEmails(){
	return addEmails.getEmails()
}