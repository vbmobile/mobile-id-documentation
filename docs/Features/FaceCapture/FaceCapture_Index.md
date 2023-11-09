# Face Capture

The Mobile ID SDK provides a functionality that simplifies the process of obtaining a frame for
biometry checks. To achieve it, we use face detection technology, and capture a frame with the
user’s face. The live photo is then processed and checked against a liveness algorithm that will try
to detect specific characteristics of spoofing attempts, returning a score that indicates if the
person using the app is there or trying to impersonate someone else.

## Initiate Face Capture

The Mobile ID SDK provides a complete set of functionalities that allows capturing and processing
the user’s facial characteristics, and match them against the travel document’s photo. This helps
ensuring that the user who is enrolling is the document’s owner. The biometric face capture should
be the final step before creating a Digital ID in a remote system. If you only need to capture a
frame with the user’s face for biometric quality validation and check against liveness algorithms,
you can use the method biometricFaceCapture.

=== "Android"

    This method is now deprecated and will be removed in the future
    ```kotlin
    override fun biometricFaceCapture(activity: Activity, params: BiometricFaceCaptureParameters) {
        enrolment.biometricFaceCapture(activity, params)
    }
    ```
    The new method contains a new parameter that's responsible to receive the result of this feature
    ```kotlin
    override fun biometricFaceCapture(activity: Activity, params: BoardingPassParserParameters) {
        // More info on the biometricFaceCaptureResultLauncher in the how to get the result section
        enrolment.biometricFaceCapture(context, params, faceCaptureResultLauncher)
    }
    ```

=== "iOS"

    ```swift
    /// Uses the device camera to capture a photo of the user face (selfie). Some tests will be run against this photo to ensure the photo quality and a liveness check verification.
    /// - Parameters:
    ///   - parameters: Configures the check liveness step.
    ///   - viewController: View controller that will present the face capture views.
    ///   - completionHandler: The completion handler to call when the face capture feature is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<BiometricFaceCaptureReport, BiometricFaceCaptureError>
    ///     Where `BiometricFaceCaptureReport` contains  the results of the face capture
    ///     operation and `BiometricFaceCaptureError` the possible errors that may occur during the process.
    func biometricFaceCapture(parameters: BiometricFaceCaptureParameters, viewController: UIViewController, completionHandler: @escaping (Result<BiometricFaceCaptureReport, BiometricFaceCaptureError>) -> Void)
    ```

The SDK provides UI solutions for the capture process and photo preview, as shown in the images
below. The use of the photo preview depends on the BiometricFaceCaptureParameters passed to the
biometricFaceCapture method. Below is an example of that object:

=== "Android"

    ```kotlin
    @Parcelize
    data class BiometricFaceCaptureParameters(
        val showPreview: Boolean,
        val showErrors Boolean,
        val frameFormat: FaceCaptureFrameFormat = FaceCaptureFrameFormat.OVAL,
        val cameraConfig: CameraConfig
    ) : Parcelable
    ```

    ```kotlin
    import androidx.camera.core.CameraSelector
    
    data class CameraConfig(
        val enableCameraToggle: Boolean,
        val defaultCamera: CameraSelector,
    )
    ```

    The **FaceCaptureFrameFormat** is an enum that shapes the frame where the face must be centered to take the selfie. Currently it has two options:
    
    ```kotlin
    enum class FaceCaptureFrameFormat {
        SQUARE,
        OVAL
    }
    ```
=== "iOS"

    ```swift
    public struct BiometricFaceCaptureParameters {
        public let showPreview: Bool
        public let frameShape: BiometricFaceCaptureFrameOptions
        public let showErrors: Bool
        public let cameraConfig: CameraConfig


        public init(showPreview: Bool,
                frameShape:BiometricFaceCaptureFrameOptions = .oval,
                showErrors: Bool,
                cameraConfig: CameraConfig = CameraConfig())
    ```

    The **BiometricFaceCaptureFrameOptions** is an enum that shapes the frame where the face must be centered to take the selfie. Currently it has two options:
    
    ```swift
    public enum BiometricFaceCaptureFrameOptions {
        case oval
        case square
    }
    ```

    The **CameraConfig** is the camera related configurations.

    ```swift
    public struct CameraConfig {
        public let toggleCameraEnable: Bool
        public let defaultCamera: AVCaptureDevice.Position
    }
    ```

The **showPreview** parameter is a boolean that when set to true will show the user’s picture after
taking it. You can also apply your app’s colors and fonts to these
layout solutions, to keep your brand’s image consistent. See Custom styles.

This function is used to acquire a high-resolution selfie with a 9:7 aspect ratio. The photo will
only be taken if the frame conforms to specific parameters that make sure the face is centered and
not too far away, or too close.

## Handle Result

=== "Android"

    Here's how you can get the result by using the result launcher that's passed as the final parameter:
    ```kotlin
    private val faceCaptureResultLauncher = registerForActivityResult(FaceCaptureResultLauncher())
    { result: FaceCaptureActivityResult ->
        when {
            result.success -> onSuccess(result.faceCaptureReportSuccess)
            result.faceCaptureReportError?.userCanceled == true -> onUserCanceled()
            result.faceCaptureReportError?.termsAndConditionsAccepted == false -> onUserTermsAndConditionsRejected()
            result.faceCaptureReportError?.failedTests != null && result.faceCaptureReportError?.performedTests != null ->
                onFailedTests(
                    result.faceCaptureReportError!!.performedTests!!,
                    result.faceCaptureReportError!!.failedTests!!
                )
            else -> onBiometricFaceCaptureError()
        }
    }
    ```
    Here is how you can get the report when using the deprecated method and handle the onActivityResult:

    ```kotlin
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
    
        if (requestCode == EnrolmentSDKRequestCode.BIOMETRIC_FACE_CAPTURE_REQUEST_CODE) {
            val result = faceCaptureResultHandler.parseResult(resultCode, data)
    
            when {
                result.success -> onSuccess(result.faceCaptureReportSuccess)
                result.faceCaptureReportError?.userCanceled == true -> onUserCanceled()
                result.faceCaptureReportError?.termsAndConditionsAccepted == false -> onUserTermsAndConditionsRejected()
                result.faceCaptureReportError?.failedTests != null && result.faceCaptureReportError?.performedTests != null ->
                    onFailedTests(
                        result.faceCaptureReportError!!.performedTests!!,
                        result.faceCaptureReportError!!.failedTests!!
                    )
                else -> onBiometricFaceCaptureError()
            }
        }
    }
    ```

=== "iOS"

    ```swift
    enrolment?.biometricFaceCapture(parameters: params, viewController: view) { result in
        switch result {
        case .success(let report):
            print("Face capture successful.")
            EnrolmentData.faceCapture = report.photo
            EnrolmentData.biometricFaceCaptureReport = report
            completion(.success(()))
                
        case .failure(let biometricFaceCaptureError):
            EnrolmentData.biometricFaceCaptureReport = nil
                
            if case .cancelled = biometricFaceCaptureError {
                print("Face capture cancelled by user.")
                let error = BiometricFaceCaptureError.unexpected(message: "Face capture cancelled by user.")
                completion(.failure(error))
            } else {
                print("Face capture error: " + biometricFaceCaptureError.localizedDescription)
                completion(.failure(biometricFaceCaptureError))
            }
        }
    }
    ```

You should use the FaceCaptureResultHandler class to parse the result. You will receive a model of the type FaceCaptureActivityResult that will contain the success data (in this case a FaceCaptureReportSuccess) or the error data.

=== "Android"

    ```kotlin
    data class FaceCaptureActivityResult(
        val faceCaptureReportSuccess: FaceCaptureReportSuccess?,
        val faceCaptureReportError: FaceCaptureReportError?
    ) {
        val success get() = faceCaptureReportSuccess != null
    }
    ```

=== "iOS"

    ```swift
    public struct BiometricFaceCaptureReport: Codable {
    
        /// Contains the list of biometric process tests performed in Orchestra during the biometric face capture process.
        public var performedTests: [CheckLivenessTest]
    
        /// Contains the list of biometric process tests failed in Orchestra during the biometric face capture process.
        public var failedTests: [CheckLivenessTest]
    
        /// Flag indicating if liveness check was performed or not during the biometric face capture process.
        public var performedLivenessCheck: Bool
    
        /// Biometric photo
        public var photo: UIImage? 
        
        public init(photo: UIImage, performedTests: [CheckLivenessTest], failedTests: [String], performedLivenessCheck: Bool)
    }
    ```

The FaceCaptureReportError has the following structure:

=== "Android"

    ```kotlin
    data class FaceCaptureReportError(
        val userCanceled: Boolean,
        val termsAndConditionsAccepted: Boolean,
        val featureError: FeatureError?,
        val failedTests: List<String>?,
        val performedTests: List<String>?
    )
    ```

=== "iOS"

    ```swift
    public enum BiometricFaceCaptureError: Error {
        /// [BiometricFaceCaptureError] that wraps a message error a controlled error occurs at the service.
        case service(message: String)
        /// [BiometricFaceCaptureError] that occurs when there's an error on the request.
        case client(error: EnrolmentServerError?)
        /// [BiometricFaceCaptureError] that occurs when there's an error on the server.
        case server(error: EnrolmentServerError?)
        /// [BiometricFaceCaptureError] Unexpected error.
        case unexpected(message: String)
        /// [BiometricFaceCaptureError] Unreachable error.
        case unreachable(message: String)
        /// [BiometricFaceCaptureError] that occurs when there's an error with the pinned certificate.
        case serverCertificatePinning(message: String)
        /// [BiometricFaceCaptureError] Biometric process completed, but biometric tests were failed.
        case biometricTestsFailed(failedTests: [CheckLivenessTest], performedTests: [CheckLivenessTest])
        /// [BiometricFaceCaptureError] Biometric process operation was cancelled by the user.
        case cancelled
        /// [BiometricFaceCaptureError] that occurs when there's an error during a pre/pos feature process.
        case feature(error: FeatureError)
    }
    ```

The FeatureError has the following structure:

=== "Android"

    ```kotlin
    data class FeatureError(
        val errorMessage : String,
        val apiError: ApiError?
    ) : Parcelable
    ```

    The ApiError has the following structure:

    ```kotlin
    data class ApiError(
        val errors: Map<String, String>?,
        val type: String,
        val title: String,
        val status: Int,
        val detail: String?,
        val instance: String?,
    ) : Parcelable
    ```
    
=== "iOS"

    ```swift
    public enum FeatureError: Error {
        /// [FeatureError] that wraps a message error a controlled error occurs at the server.
        case server(error: EnrolmentServerError?)
        /// [FeatureError] that occurs when there's an unexpected error.
        case unexpected(message: String)
        /// [FeatureError] that wraps a `FeatureOperationErrorType` indicating the underlying cause for the error.
        case feature(operationType: FeatureOperationErrorType)
    }
    ```

The failed tests might include one or more of the following tests:

| Name                         | Description                                                                                                                                                            |
|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FaceTooFarTest               | Error indicating that the face was very far.                                                                                                                           |
| FaceTooCloseTest             | Error indicating that the face was very close.                                                                                                                         |
| FaceNotCenteredTest          | Error indicating that the face was not centered.                                                                                                                       |
| MultipleFacesDetectedTest    | Error indicating that multiple faces were detected in the image.                                                                                                       |
| FaceRotatedTest              | Error indicating that the face was rotated in Z angle. A face with a positive Euler Z angle is rotated counter-clockwise relative to the camera.                       |
| NoFaceDetectedTest           | Error indicating that no face was detected in the picture.                                                                                                             |
| EyesClosedTest               | Error indicating that the eyes are closed.                                                                                                                             |
| SmilingTest                  | Error indicating that the user was smiling.                                                                                                                            |
| FaceSidewaysTest             | Error indicating that the face was rotated in Y angle. A face with a positive Euler Y angle is looking to the right of the camera, or looking to the left if negative. |
| FaceVerticalTest             | Error indicating that the face was rotated in X angle. A face with a positive Euler X angle is facing upward.                                                          |
| MouthOpenTest                | Error indicating that the user has the mouth open.                                                                                                                     |
| ImageBlurredTest             | Error indicating that the image is blurred.                                                                                                                            |
| FaceCropFailedTest           | Error indicating that the face crop failed.                                                                                                                            |
| LivenessCheckQualityTest     | Error indicating that the liveness quality test failed.                                                                                                                |
| LivenessCheckProbabilityTest | Error indicating that the liveness probability test failed.                                                                                                            |

## BiometricFaceCaptureCustomViews
The SDK provides default UI solutions for the document reader feature flow, as shown in the following images:

![Biometric Face Capture Example](Assets/FaceCaptureFlow.PNG "Biometric Face Capture Default Error Screen"){: style="height:600px;width:300px;display: block; margin: 0 auto"}

The use of the preview layout depends on the showPreview flag in the BiometricFaceCaptureParameters.

The use of the Errors layout depends on the showErrors flag in the BiometricFaceCaptureParameters.

=== "Android"

    ```kotlin
    @Parcelize
    class BiometricFaceCaptureCustomViews(
        val loadingView: Class<out ICustomBiometricFaceCapture.LoadingView>? = null
    ) : Parcelable
    ```


=== "iOS"

    ```swift
    public class EnrolmentViewRegister {
        ...
        
        public func registerBiometricFaceCaptureLoadingView(_ viewType: FaceCaptureLoadingViewType)
        ...
    }
    ```

You can use your own custom views in the biometric face capture functionality. Your view must
implement the SDK view interfaces. For example, if you want to add a custom loadingView, your view
class must implement the ICustomBiometricFaceCapture.LoadingView interface.

In the customization tab you will also find examples to create your own custom views.
