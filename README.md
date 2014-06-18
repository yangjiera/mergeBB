#Merging Bounding Box

The service run in SURFsara HPC. Supppose you have a input file called test.json, to call the service, use 'curl' command as follows:

```curl -i -H "Content-Type: application/json" -X POST -d @test.json http://145.100.58.60:12345/merge/api/v1.0/mergeBB```