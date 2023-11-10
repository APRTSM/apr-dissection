# Entities

## Benchmarks
```
{
  "id": 1,
  "name": "Defects4J",
  "description": "",
  "references": [
    {
      "referenceId": 1,
      "fieldNames": []
    },
    {
      "referenceId": 0,
      "fieldNames": ["description", "references"]
    }
  ]
}
```

## Bugs
- Bug name should be unique
```
{
  "id": 1,
  "benchmarkId": 1,
  "name": "Chart_6",
  "changedFiles": {
    "org/jfree/chart/util/ShapeList.java": { "changes": [[111]] }
  },
  "humanPatchId": 1,
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
  "program": "jfreechart",
  "project": "Chart",
  "description": "",
  "references": [
    { "referenceId": 1, "fieldNames": [] },
    { "referenceId": 0, "fieldNames": ["id", "description", "references"] }
  ]
}
```

## Patches
```
{
  "id": 1,
  "bugId": 1,
  "name": "",
  "tool": "Human",
  "diff": "--- a/source/org/jfree/chart/util/ShapeList.java\n+++ b/source/org/jfree/chart/util/ShapeList.java\n@@ -108,7 +108,14 @@ public boolean equals(Object obj) {\n         if (!(obj instanceof ShapeList)) {\n             return false;\n         }\n-        return super.equals(obj);\n+        ShapeList that = (ShapeList) obj;\n+        int listSize = size();\n+        for (int i = 0; i < listSize; i++) {\n+           if (!ShapeUtilities.equal((Shape) get(i), (Shape) that.get(i))) {\n+               return false;\n+           }\n+        }\n+        return true;\n \n     }\n \n",
  "description": "",
  "tags": [],
  "references": [
    { "referenceId": 1, "fieldNames": [] },
    {
      "referenceId": 0,
      "fieldNames": ["id", "name", "description", "references"]
    }
  ]
}
```

## Tags
```
{
  "id": 2,
  "name": "Plausible",
  "typeId": 1,
  "value": null,
  "description": "",
  "references": [
    {
      "referenceId": 0,
      "fieldNames": []
    }
  ]
}
```

## Types
```
{
  "id": 1,
  "name": "Correctness",
  "description": "",
  "references": [
    {
      "referenceId": 0,
      "fieldNames": []
    }
  ]
}
```
