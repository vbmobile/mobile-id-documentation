# Handle Errors

After obtaining the FeatureError, as shown in the Handle Result section of the feature overview, we pass the object to the handleError function that is going to analyze what error type occurred in this feature and act according to it.
Example can be found here: [FaceCaptureHandleErrors](https://github.com/vbmobile/mobileid-android-sample/tree/main/app/src/main/java/com/example/sample_app_android/presentation/faceCapture/FaceCaptureActivity.kt)

=== "Android"

    ```kotlin
    private fun handleError(error: FaceCaptureReportError?) {
        if (error != null) {
            val errorType = error.featureError?.errorType ?: ErrorType.UnknownError
            when (errorType) {
                ErrorType.InternalError -> {
                    navigateToErrorScreen(error.featureError?.publicMessage ?: error.featureError?.description ?: "", false)
                }
                ErrorType.CommunicationError, ErrorType.PermissionNotGrantedError -> {
                    navigateToErrorScreen(error.featureError?.publicMessage ?: error.featureError?.description ?: "", true)
                }
                ErrorType.UserRepeated -> {
                    retry()
                }
                ErrorType.UserCanceled -> {
                    // User canceled the flow
                    finish()
                }
                ErrorType.Timeout -> {
                    navigateToErrorScreen(error.featureError?.publicMessage ?: error.featureError?.description ?: "", true)
                }
                ErrorType.FaceCaptureError -> {
                    navigateToFailedTests(error.failedTests ?: emptyList(), error.performedTests ?: emptyList())
                }
                else -> {
                    Toast.makeText(this, "An unknown error occurred", Toast.LENGTH_SHORT).show()
                    finish()
                }
            }
        }
    }
    ```    
    The boolean in the navigateToErrorScreen function is to configure if the retry button should appear or not.

=== "iOS"

    // TODO