# Handle Errors

After obtaining the FeatureError, as shown in the Handle Result section of the feature overview, we pass the object to the handleError function that is going to analyze what error type occurred in this feature and act according to it.

=== "Android"

    Example can be found here: [SubjectHandleErrors](https://github.com/vbmobile/mobileid-android-sample/tree/main/app/src/main/java/com/example/sample_app_android/presentation/subjectManagement/SubjectManagementActivity.kt)
    ```kotlin
    private fun handleError(error: FaceCaptureReportError?) {
        if (error != null) {
            val errorType = error.featureError?.errorType ?: ErrorType.UnknownError
            when (errorType) {
                ErrorType.InternalError -> {
                    navigateToErrorScreen(error.featureError?.publicMessage ?: error.featureError?.description ?: "", false)
                }
                ErrorType.CommunicationError,
                ErrorType.SubjectError -> {
                    navigateToErrorScreen(error.featureError?.publicMessage ?: error.featureError?.description ?: "", true)
                }
                ErrorType.UserRepeated -> {
                    retry()
                }
                ErrorType.UserCanceled -> {
                    // User canceled the flow
                    finish()
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

    Example can be found here: [Sample Project](https://github.com/vbmobile/mobileid-ios-sample-)
