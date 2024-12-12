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

    ```kotlin
    /**
     * Uses the device camera to capture a photo of the user face (selfie).
     *
     * Some tests will be run against this photo to ensure the photo quality and a liveness check verification.
     *
     * @param activity [Activity] that will launch the face capture feature
     * @param params [BiometricFaceCaptureParameters] configurations parameters.
     * @param onFaceCaptureComplete [OnBiometricFaceCaptureCompletion] Callback to handle Success and Error scenarios.
     */
    fun biometricFaceCapture(
        activity: Activity,
        params: BiometricFaceCaptureParameters,
        onFaceCaptureComplete: OnBiometricFaceCaptureCompletion,
    )
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
    ///     operation and `FaceCaptureReportError` the possible errors that may occur during the process.
        func biometricFaceCapture(parameters: BiometricFaceCaptureParameters, viewController: UIViewController, completionHandler: @escaping (Result<BiometricFaceCaptureReport, FaceCaptureReportError>) -> Void)
    ```

The SDK provides UI solutions for the capture process, as shown in the images
below. Below is an example of the BiometricFaceCaptureParameters:

=== "Android"

    ```kotlin
    @Parcelize
    data class BiometricFaceCaptureParameters(
        val frameFormat: FaceCaptureFrameFormat = FaceCaptureFrameFormat.OVAL,
        val cameraConfig: CameraConfig,
        val faceCaptureTimeout: Long? = null
    ) : Parcelable{
        init {
            if (faceCaptureTimeout != null) {
                require(faceCaptureTimeout >= TimeUnit.SECONDS.toMillis(30)) { "faceCaptureTimeout value must be at least 30 seconds." }
            }
        }
    }
    ```

    The **FaceCaptureFrameFormat** is an enum that shapes the frame where the face must be centered to take the selfie. Currently it has two options:
    
    ```kotlin
    enum class FaceCaptureFrameFormat {
        SQUARE,
        OVAL
    }
    ```

    The **CameraConfig** is another data class that lets your configure the visibility of the toggle button and change the camera direction (Front or Back).

    data class CameraConfig(
        val enableCameraToggle: Boolean,
        val defaultCamera: CameraSelector,
    )
=== "iOS"

    ```swift
    public struct BiometricFaceCaptureParameters {
        public let frameShape: BiometricFaceCaptureFrameOptions
        public let cameraConfig: CameraConfig
        public let faceCaptureTimeout: TimeInterval?
        
        public init(frameShape:BiometricFaceCaptureFrameOptions = .oval,
                cameraConfig: CameraConfig = CameraConfig(),
                faceCaptureTimeout: TimeInterval? = nil)
    ```

    The **BiometricFaceCaptureFrameOptions** is an enum that shapes the frame where the face must be centered to take the selfie. Currently it has two options:
    
    ```swift
    public enum BiometricFaceCaptureFrameOptions {
        case oval
        @available(*, deprecated, message: "Will be removed in future versions (9.x)")
        case square
    }
    ```
    
    The **CameraConfig** is an enum that struct the frame where the face must be centered to take the selfie. Currently it has two options:
    
    ```swift
    public struct CameraConfig {
        public let toggleCameraEnable: Bool
        public let defaultCamera: AVCaptureDevice.Position
    
        public init(toggleCameraEnable: Bool = true,
                defaultCamera:AVCaptureDevice.Position = .front) {
            self.toggleCameraEnable = toggleCameraEnable
            self.defaultCamera = defaultCamera
        }
    }
    ```

This function is used to acquire a high-resolution selfie with a 9:7 aspect ratio. The photo will
only be taken if the frame conforms to specific parameters that make sure the face is centered and
not too far away, or too close.

## Handle Result

=== "Android"

    You can get the result by registering the callback:
    ```kotlin
    interface OnBiometricFaceCaptureCompletion {
        fun onBiometricFaceCaptureSuccess(faceCaptureReport: FaceCaptureReportSuccess)
        fun onBiometricFaceCaptureError(faceCaptureReportError: FaceCaptureReportError)
    }
    ```

=== "iOS"

    ```swift
    enrolment?.biometricFaceCapture(parameters: params, viewController: view) { result in
        switch result {
        case .success(let report):
            print("Face capture successful.")
            completion(.success(()))
                
        case .failure(let biometricFaceCaptureError):
            if biometricFaceCaptureError.userCanceled {
                print("Face capture cancelled by user.")
                completion(.failure(biometricFaceCaptureError))
            } else {
                print(biometricFaceCaptureError.featureError.publicMessage)
                completion(.failure(biometricFaceCaptureError))
            }
        }
    }
    ```
    
### Face Capture Report 

You will receive a model of the type FaceCaptureReport that will contain the success data.

=== "Android"

    ```kotlin
    data class FaceCaptureReport(
        val livenessCheckStatus: LivenessCheckStatus,
        val performedTests: List<String>?,
        val biometricHash: String
    ) : Parcelable
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
        
        /// Biometric photo hash
        public var biometricHash: String?
        
        /// Biometric photo
        public var photo: UIImage? 
        
        public init(photo: UIImage, performedTests: [CheckLivenessTest], failedTests: [String], performedLivenessCheck: Bool, biometricHash: String?)
    }
    ```

The FaceCaptureReportError has the following structure:

=== "Android"

    ```kotlin
    data class FaceCaptureReportError(
        val userCanceled: Boolean,
        val featureError: FeatureError?,
        val failedTests: List<String>?,
        val performedTests: List<String>?
    )
    ```

=== "iOS"

    ```swift
    public class FaceCaptureReportError: Error {
        public var userCanceled: Bool
        public var termsAndConditionsAccepted: Bool
        public var featureError: FeatureError
        public var failedTests: [String]?
        public var performedTests: [String]?
    }
    ```

The `FaceCaptureReportSuccess` includes a `biometricHash` attribute that needs to be included in the [Match](../BiometricMatch/BiometricMatch_Index.md) operation to verify data integrity. It also used when building a [Subject](../SubjectManagement/SubjectManagement_Index.md).

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

![Biometric Face Capture Example](Assets/FC_Flow.png "Biometric Face Capture Default Error Screen"){: style="height:600px;width:300px;display: block; margin: 0 auto"}

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
