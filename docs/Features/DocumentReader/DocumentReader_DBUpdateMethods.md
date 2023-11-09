# Download database
The document reader requires a document database templates. 
This file is downloaded in runtime and since it's a large file can take sometime to finish, depending on the user internet.
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

