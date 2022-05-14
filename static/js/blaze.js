
/*
	
	Included in the base page

*/

var options = {
    "element": "mark",
    "className": "",
    "exclude": [],
    "separateWordSearch": false,
    "accuracy": "partially",
    "diacritics": true,
    "synonyms": {},
    "iframes": false,
    "iframesTimeout": 5000,
    "acrossElements": false,
    "caseSensitive": false,
    "ignoreJoiners": false,
    "ignorePunctuation": [],
    "wildcards": "enabled"
}

function search() {
   var searchText = $("#searchBar").val();
    $( document ).ready(function() {
	  var instance = new Mark(document.querySelector("body"));
		instance.unmark(options);
   		instance.mark(searchText, options);
	
  });
}

$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});