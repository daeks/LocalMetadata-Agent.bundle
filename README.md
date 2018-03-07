# LocalMetadata-Agent.bundle

This agent uses local json files to apply metadata information if .plexmetadata file exists within the folder

Example:

```
{
  "title" : "Test Series",
  "originally_available_at" : "1900-01-01",
  "posters" : [
    "C:\\media\shows\Test Series\\poster.jpg"
  ],
  "summary": "This is my test summary",
  "seasons" : {
    "01" : {
      "episodes" : {
        "01" : {
          "title" : "First Episode",
          "summary" : "Summary of episode 01"
        }
      }
    }
  }
}
```