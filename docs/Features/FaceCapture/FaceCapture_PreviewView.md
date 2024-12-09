# Preview View

**From version 8 onwards, the preview management changed in the SDK to make it easier to integrate.**

To improve flexibility in the preview screen, the optional preview screen has been removed.

To add a preview feature to your app you can follow the example from our sample app, where we provide an example with the same user interface.

=== "Android"

    Example can be found here: [FaceCapturePreview](https://github.com/vbmobile/mobileid-android-sample/tree/main/app/src/main/java/com/example/sample_app_android/presentation/faceCapture/preview/PreviewPhotoActivity.kt)
    ```kotlin
    private fun onSuccess(faceCaptureSuccess: FaceCaptureReportSuccess) {
        val photo = readPhotoFromInternalStorage(context, faceCaptureSuccess.faceCaptureReport.faceCaptureImagePath)
        binding.imgFaceCapturePhoto.run {
            setBackgroundResource(R.drawable.bg_face_capture_preview_image)
            setImageBitmap(photo)
        }
    }
    ```

=== "iOS"

    Example can be found here: [Sample Project](https://github.com/vbmobile/mobileid-ios-sample-)
