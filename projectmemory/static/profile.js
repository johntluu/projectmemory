  $(document).ready(function(){
    $("#delete").click(function(event){

        var x = window.confirm("Are you sure you want to delete this message? This action is permanent.");
          if(x){
            /* the OK button should be a LINK (a href) to go to the (next) saved memories page */
            $(this).closest('tr').remove()
          }
          else{
            event.preventDefault();
          }

    });

  });
