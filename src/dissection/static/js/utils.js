/** @format */

$(document).ready(function () {
  if (document.getElementById("bug-list") != null) {
    sort_bug_name();
  }

  if (document.getElementById("preview")) {
    desctiption_changed();
  }

  if (document.getElementsByClassName("diff").length) {
    add_diff();
  }

  if (document.getElementsByClassName("markdown").length) {
    set_markdowns();
  }
});

function truncate(str, n){
  return str.length > n ?  "&hellip;" + str.slice(str.length-n, str.length) : str;
};

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
        items[i].getElementsByClassName("bug-name")[0].innerHTML.toLowerCase() >
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

function add_diff() {
  $(".diff").each(function () {
    var diffFile = this.innerHTML;

    var diffString = diffFile;
    var targetElement = this;
    
    var configuration = {
      drawFileList: false,
      fileListToggle: false,
      fileListStartVisible: false,
      fileContentToggle: true,
      matching: "lines",
      outputFormat: "line-by-line",
      synchronisedScroll: false,
      highlight: false,
      renderNothingWhenEmpty: false,
    };
    var diff2htmlUi = new Diff2HtmlUI(
      targetElement,
      diffString,
      configuration
    );
    diff2htmlUi.draw();
    diff2htmlUi.highlightCode();
    $(".d2h-code-line").css({
      "width": "100%",
      "padding-right": "15px",
    });
  });
  $(".d2h-file-name").each(function () {
    this.innerHTML = truncate(this.innerHTML, 50);
  });
}

function set_markdowns() {
  $(".markdown").each(function () {
    var converter = new showdown.Converter();
    var text = $(this).text();
    var html = converter.makeHtml(text);
    $(this).html(html);
  });
}