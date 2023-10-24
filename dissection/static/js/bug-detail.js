/** @format */

$(document).ready(function () {
  var diffStringMain = humanPatchDiff;
  var targetElement = document.getElementById("myDiffElement");
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
    diffStringMain,
    configuration
  );
  diff2htmlUi.draw();
  diff2htmlUi.highlightCode();

  diffsAndContributors.forEach(generateDiff);
  function generateDiff(value, index, array) {
    diffFile = value[0];
    id = value[1];
    var diffString = diffFile;
    var targetElement = document.getElementById(id);
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
    var diff2htmlUi = new Diff2HtmlUI(targetElement, diffString, configuration);
    diff2htmlUi.draw();
    diff2htmlUi.highlightCode();
  }
});
