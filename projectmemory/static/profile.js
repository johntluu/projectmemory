$(document).ready(function(){
  $('input[type="button"]').click(function(e){
   $(this).closest('tr').remove()
})

  });
