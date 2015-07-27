$(document).ready(function(){
  $("#submit").click(function(){
      var x = window.confirm("Are you satisfied with this message? You cannot edit or view this message after you click submit.");
        if(x){
          /* the OK button should be a LINK (a href) to go to the (next) saved memories page */
          window.location = "http://www.google.com"
        }
        else{
          /* close alert */
        }
  });

});
