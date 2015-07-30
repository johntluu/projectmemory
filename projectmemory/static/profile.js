  $(document).ready(function(){
    $("#submit").click(function(event){
        var x = window.confirm("Are you satisfied with this message? You cannot edit or view this message after you click submit.");
          if(x){
            /* the OK button should be a LINK (a href) to go to the (next) saved memories page */
            window.location = "/profile"
          }
          else{
            event.preventDefault();
          }
    });
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
    $("#create").click(function(event) {
      $("#overlay").show();
    });

    $("#overlay").click(function(event) {
      if(event.target.id=="overlay"){
        $("#overlay").hide();
      }

    });

  });
