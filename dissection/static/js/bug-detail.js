/** @format */

$(document).ready(function () {
  var diffStringMain = humanPatchDiff;
  var targetElement = document.getElementById("myDiffElement");
  var configuration = {
    drawFileList: false,
    fileListToggle: false,
    fileListStartVisible: false,
    fileContentToggle: false,
    matching: "lines",
    outputFormat: "line-by-line",
    synchronisedScroll: true,
    highlight: true,
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
    contributor = value[1];
    var diffString = diffFile;
    var targetElement = document.getElementById(contributor);
    var configuration = {
      drawFileList: false,
      fileListToggle: false,
      fileListStartVisible: false,
      fileContentToggle: false,
      matching: "lines",
      outputFormat: "line-by-line",
      synchronisedScroll: true,
      highlight: true,
      renderNothingWhenEmpty: false,
    };
    var diff2htmlUi = new Diff2HtmlUI(targetElement, diffString, configuration);
    diff2htmlUi.draw();
    diff2htmlUi.highlightCode();
  }
});
