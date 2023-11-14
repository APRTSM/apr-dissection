/** @format */

$(document).ready(function () {
  if (document.getElementById("bug-list") != null) {
    sort_bug_name();
  }

  if (document.getElementById("preview")) {
    desctiption_changed();
  }


});

function sort_bug_name() {
  var list, i, run, items, stop;
  list = document.getElementById("bug-list");
  run = true;

  while (run) {
    run = false;
    items = list.getElementsByClassName("bug");

    for (i = 0; i < items.length - 1; i++) {
      stop = false;

      if (
        items[i]
          .getElementsByClassName("bug-name")[0]
          .innerHTML.toLowerCase() >
        items[i + 1]
          .getElementsByClassName("bug-name")[0]
          .innerHTML.toLowerCase()
      ) {
        stop = true;
        break;
      }
    }

    if (stop) {
      items[i].parentNode.insertBefore(items[i + 1], items[i]);
      run = true;
    }
  }
}

function desctiption_changed() {
  $("#description").change(function () {
    var converter = new showdown.Converter(),
      text = $("#description").val(),
      html = converter.makeHtml(text);
    $("#preview").html(html);
  });
}