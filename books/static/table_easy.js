function TableEasy_search_onkeyup(tableeasydiv_id) {
  var tableEasy=document.getElementById(tableeasydiv_id);
  var input = $(tableEasy).find("#"+tableeasydiv_id+"_search");
  var filter = $(input).val().toUpperCase();
  var labelRecords=$(tableEasy).find("#"+tableeasydiv_id+"_records");
  var table = $(tableEasy).find("#"+tableeasydiv_id+"_table");
  var numfiltered=0;
  $(table).find("tr.data").each(
      function() {
         var s="";
         $(this).find("td").each(
             function() {
                 s=s+$(this).html();
             });
         if (s.toUpperCase().indexOf(filter) > -1) {
             $(this).show();
             numfiltered=numfiltered+1;
         } else {
             $(this).hide();
         };
      });

  $(labelRecords).text("Filtered " + numfiltered + " from " + ($(table).find("tr").length-1) + " records");
}

function TableEasy_chkAll_onclick(tableeasydiv_id) {
  var tableEasy=$(document).find("#" + tableeasydiv_id);
  var chkAll=$(tableEasy).find(".TableEasyCheckBoxAll");
  $(tableEasy).find(".TableEasyCheckBox").each(
      function() {
         if( $(chkAll).prop('checked')){
             $(this).prop('checked',true);
         }else{
             $(this).prop('checked',false);
         };
      });
}
