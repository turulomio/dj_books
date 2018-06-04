function myFunction() {
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  numfiltered=0
  for (i = 1; i < tr.length; i++) {
    var s="";
    td = tr[i].getElementsByTagName("td");
    for (j=0;j<td.length;j++){
        s=s+tr[i].getElementsByTagName("td")[j].innerHTML+" ";
    }
      if (s.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        numfiltered=numfiltered+1;
      } else {
        tr[i].style.display = "none";
      }
  }
  $(".EasyTableRecords").text("Filtered " + numfiltered + " from " + (tr.length-1) + " records");
}
