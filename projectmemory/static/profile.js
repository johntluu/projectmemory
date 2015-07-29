$(document).ready(function(){
  $("#delete").click(function(){

      var x = window.confirm("Are you sure you want to delete this message?");
        if(x){
          /* 1. delete this message
             2. redirect to self, probably self.redirect('/profile') or
                window.location = "/profile"*/
        }
        else{
          /* close alert */
        }

  });

});
