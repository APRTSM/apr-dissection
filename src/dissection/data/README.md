# Entities

## Benchmarks
```
{
    "name": "Defects4J",
    "id": 1
}
```

## Bugs
```
{
    "id": 1,
    "benchmarkId": 1,
    "name": "Chart_6",
    "bugId": 6,
    "changedFiles": {
      "org/jfree/chart/util/ShapeList.java": { "changes": [[111]] }
    },
    "diff": "--- a/source/org/jfree/chart/util/ShapeList.java\n+++ b/source/org/jfree/chart/util/ShapeList.java\n@@ -108,7 +108,14 @@ public boolean equals(Object obj) {\n         if (!(obj instanceof ShapeList)) {\n             return false;\n         }\n-        return super.equals(obj);\n+        ShapeList that = (ShapeList) obj;\n+        int listSize = size();\n+        for (int i = 0; i < listSize; i++) {\n+           if (!ShapeUtilities.equal((Shape) get(i), (Shape) that.get(i))) {\n+               return false;\n+           }\n+        }\n+        return true;\n \n     }\n \n",
    "failingTests": [
      {
        "className": " org.jfree.chart.util.junit.ShapeListTests",
        "error": "junit.framework.AssertionFailedError",
        "message": "expected:<org.jfree.chart.util.ShapeList@d0e55451> but was:<org.jfree.chart.util.ShapeList@d951b68f>",
        "methodName": "testSerialization"
      },
      {
        "className": " org.jfree.chart.util.junit.ShapeListTests",
        "error": "junit.framework.AssertionFailedError",
        "message": "",
        "methodName": "testEquals"
      }
    ],
    "metrics": {
      "chunks": 1,
      "classes": 1,
      "files": 1,
      "linesAdd": 7,
      "linesMod": 1,
      "linesRem": 0,
      "methods": 1,
      "sizeInLines": 8,
      "spreadAllLines": 0,
      "spreadCodeOnly": 0
    },
    "observations": "",
    "program": "jfreechart",
    "project": "Chart",
    "repairActions": [
      "assignAdd",
      "condBranIfAdd",
      "loopAdd",
      "mcAdd",
      "mcRem",
      "retBranchAdd",
      "retExpChange",
      "varAdd"
    ],
    "repairPatterns": ["condBlockRetAdd", "wrongComp"],
    "repairTools": ["rtCardumen"],
    "revisionId": "1166",
    "extraInformation": "",
    "references": [
      { "referenceId": 1, "fieldNames": "All except the mentioned ones!" },
      {
        "referenceId": 0,
        "fieldNames": [
          "id",
          "benchmarkId",
          "name",
          "extraInformation",
          "references"
        ]
      }
    ]
}
```

## Patches
```
{
    "id": 1,
    "bugId": 309,
    "name": "Patch_1_1",
    "tool": "Cardumem",
    "diff": "--- /tmp/Cardumen_Defects4J_Math_85/src/java/org/apache/commons/math/analysis/solvers/UnivariateRealSolverUtilsjava\n+++ /tmp/Cardumen_Defects4J_Math_85/src/java/org/apache/commons/math/analysis/solvers/UnivariateRealSolverUtilsjava\n@@ -195,7 +195,7 @@\n \t\t} while ((((fa * fb) > 0.0) && (numIterations < maximumIterations)) && \n \t\t((a > lowerBound) || (b < upperBound)) );\n \n-\t\tif ((fa * fb) >= 0.0) {\n+\t\tif (((b * b) > 0.0) && (maximumIterations < maximumIterations)) {\n \t\t\tthrow new org.apache.commons.math.ConvergenceException(\n \t\t\t(\"number of iterations={0}, maximum iterations={1}, \" + \n \t\t\t(\"initial={2}, lower bound={3}, upper bound={4}, final a value={5}, \" + ",
    "correctness": "P",
    "faultLocalization": "n",
    "rules": [],
    "extraInformation": "",
    "references": [
      { "referenceId": 3, "fieldNames": "All except the mentioned ones!" },
      {
        "referenceId": 0,
        "fieldNames": ["id", "bugId", "rules.extraInformation", "extraInformation", "references"]
      }
    ]
}
```

## Rules
```
{
    "id": 4,
    "name": "R4",
    "description": "if statement instead of a ternary operator",
    "extraInformation": "The APR patch is implemented by inserting new if statement but not a ternary operator to fix the bug.",
    "references": [
      {
        "referenceId": 3,
        "fieldNames": "All except the mentioned ones!"
      },
      {
        "referenceId": 0,
        "fieldNames": ["id", "references"]
      }
    ]
}
```
