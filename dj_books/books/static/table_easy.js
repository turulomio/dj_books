function myFunction() {
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 1; i < tr.length; i++) {
    var s="";
    td = tr[i].getElementsByTagName("td");
    for (j=0;j<td.length;j++){
        s=s+tr[i].getElementsByTagName("td")[j].innerHTML+" ";
    }
      if (s.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
  }
}
