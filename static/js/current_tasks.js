
/*
	
	Handles the execution in the dashboard page.

*/



(function() {

    const idleDurationSecs = 300;    // X number of seconds
    const redirectUrl = '/';  // Redirect idle users to this URL
    let idleTimeout; // variable to hold the timeout, do not modify

    const resetIdleTimeout = function() {

        // Clears the existing timeout
        if(idleTimeout) clearTimeout(idleTimeout);

        // Set a new idle timeout to load the redirectUrl after idleDurationSecs
        idleTimeout = setTimeout(() => location.href = redirectUrl, idleDurationSecs * 1000);
    };

    // Init on page load
    resetIdleTimeout();

    // Reset the idle timeout on any of the events listed below
    ['click', 'touchstart', 'mousemove'].forEach(evt => 
        document.addEventListener(evt, resetIdleTimeout, false)
    );

})();

function updateTasks(){
{
   $.ajax({

     type: "GET",
     url: "/fetchRunningTasks",
     success: function(data) {
          $('#tasksContainer').html(data);
     }

   });

}

}

window.onload = function(){
	updateTasks()
};

setInterval( updateTasks, 30000 );	