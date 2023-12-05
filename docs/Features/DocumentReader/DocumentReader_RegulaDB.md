# Database download methods
The document reader requires a document database of templates.

## Runtime download

Usually this file is downloaded in runtime and since it's a large file can take sometime to finish, depending on the user internet.
This download will happen in the first run and everytime the database is outdated. 

There are two ways to download this file:
- By default, the download will happen in the beginning of the document reader
- You can trigger this download at anytime in your app by calling the enrolment facade method:

=== "Android"

    ```kotlin
    enrolment.startDatabaseUpdate(object: RegulaDatabaseListener {
      override fun onDownloadProgressChanged(progress: Int) {
        Log.i("RegulaDBUpdate", "progress = {$progress}")
      }
    
      override fun onReady() {
        Log.i("RegulaDBUpdate", "Regula Database updated")
      }
    
      override fun unableToPrepareDatabase(error: String?) {
        Log.i("RegulaDBUpdate", "error = $error")
      }
    })
    ```

=== "iOS"

    ``` swift
    func startUpdateDatabase(progressHandler: ((Progress) -> Void)?, completion: @escaping (Result<Void, DocumentReaderError>) -> Void)
    ```

With this method you can start the download at anytime decreasing the loading time of the document reader.

=== "Android"

    If you need to stop listening for the download progress, you can remove the callback at anytime by calling the method:

    ```kotlin
    override fun removeDatabaseUpdateListener() {
        enrolment.removeDatabaseUpdateListener(yourListener)
    }
    ```

=== "iOS"

    At this time it is not possible to remove handlers during the process. They will be automatically removed when the download is completed successfully or in error.

## Bundled option

It's also possible to pre-bundle the database into your own application in order to speed document reader init time.
Keep in mind that the final apk size will increase significantly using this method.

In order to bundle the database into your application you will need to:

1. Go to the Client Portal.
2. Sign up if you are not registered yet.
3. Go to the Databases page and download the database provided there.
4. Depending on your platform, complete the remaining step:

=== "Android"

    Add the downloaded database file to the app/src/main/assets/Regula folder of the project.

=== "iOS"

    Add the downloaded database file to the desired [project's target](https://developer.apple.com/library/archive/featuredarticles/XcodeConcepts/Concept-Targets.html).

**Everytime there's a new version available, Mobile ID SDK will still download the newest version and replace it, 
so this method requires to manually update the source often in order to be effective.**
