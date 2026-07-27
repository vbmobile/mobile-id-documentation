# How to handle errors

**From version 8 onwards, the errors management changed in the SDK to make it easier to integrate.**

To improve flexibility in error handling, the optional error screen has been removed.

A new example has been added to our sample app with the same user interface for error handling.

You can easily implement your own error handling logic without needing to customize our screen by following the example on each feature -> Handle errors tab

## Error object and properties

Every feature, will send a FeatureError object detailing what happened when something outside the normal flow occurs.

The FeatureError has the following structure:

=== "Android"

    ```kotlin
    /***
    * @param errorType - Enum that classifies the error type
    * @param errorCode - Error code that identifies the error
    * @param description - Error description for log purposes
    * @param publicMessage - Error message suggestion to display in error screens
    */
    @Parcelize
    data class FeatureError(
        val errorType: ErrorType,
        val errorCode: Int,
        val description : String,
        val publicMessage : String
    ) : Parcelable
    ```

    ```kotlin
    enum class ErrorType {
        InternalError,
        CommunicationError,
        PermissionNotGrantedError,
        UserRepeated,
        UserCanceled,
        ScanError,
        Timeout,
        BoardingPassInvalidError,
        DocumentReaderError,
        FaceCaptureError,
        FaceMatchError,
        SubjectError,
        UnknownError,
        ConfigurationError,
        BadConfigurationError
    }
    ```

=== "iOS"

    ```swift
    ///
    /// - Parameters:
    ///     - errorType: Enum that classifies the error type
    ///     - errorCode: Error code that identifies the error
    ///     - description: Error description for log purposes
    ///     - publicMessage: Error message suggestion to display in error screens
    
    public class FeatureError: Error {
        public let errorType: ErrorType
        public let errorCode: Int
        public let description: String
        public let publicMessage: String

        public init(errorType: ErrorType, errorCode: Int, description: String, publicMessage: String, name: String)
    }
    
    public enum ErrorType {
        case configError
        case badConfigError
        case internalError
        case communicationError
        case termsAndConditionsRejected
        case userRepeated
        case permissionNotGrantedError
        case scanError
        case timeout
        case boardingPassInvalid
        case documentReaderError
        case faceCaptureError
        case faceMatchError
        case subjectError
        case unknownError
    }
    ```

Here you can find a list of all the error codes the SDK sends to the client application:

### Android

| Name                            | Value | Feature           | When thrown                                                                          |
|---------------------------------|-------|-------------------|--------------------------------------------------------------------------------------|
| InvalidApiKey                   | 010   | Configuration     | API key provided to `configure()` is invalid                                         |
| InvalidEndpoint                 | 011   | Configuration     | Endpoint URL does not use HTTPS                                                      |
| InitFailed                      | 012   | Configuration     | SDK fails to fetch configurations from the server                                    |
| NotReady                        | 013   | Configuration     | SDK feature called before `initialize()` completes                                   |
| InvalidLicense                  | 014   | Configuration     | License signature is invalid                                                         |
| ConfigError                     | 100   | DocumentReader    | Feature configurations are missing                                                   |
| NotReady                        | 101   | DocumentReader    | Document Reader not initialized; call initialize first                               |
| InitFailed                      | 102   | DocumentReader    | Error initializing Document Reader                                                   |
| ReportIsNull                    | 103   | DocumentReader    | Report from preview or RFID scan is null                                             |
| ErrorCertificate                | 104   | DocumentReader    | CSCA certificates not found or not configured on back office                         |
| InvalidCertificate              | 105   | DocumentReader    | CSCA certificate file is invalid                                                     |
| LicenseNotFound                 | 106   | DocumentReader    | License file not found at configured path                                            |
| PermissionNotGranted            | 107   | DocumentReader    | App lacks required permission for document reading                                   |
| FetchingResourcesFailed         | 120   | DocumentReader    | Resources endpoint request failed                                                    |
| TransactionFailed               | 121   | DocumentReader    | Transaction registration failed on server                                            |
| InvalidDatabaseState            | 122   | DocumentReader    | Database download failed and no local backup available                               |
| ProviderNotFound                | 140   | DocumentReader    | No document reader provider was configured                                           |
| InvalidParameters               | 141   | DocumentReader    | Invalid parameter passed by client                                                   |
| MrzError                        | 150   | DocumentReader    | Error reading MRZ via OCR                                                            |
| RegulaError                     | 151   | DocumentReader    | Internal Document Reader scan error                                                  |
| MrzTimeout                      | 152   | DocumentReader    | MRZ scan timed out                                                                   |
| RFIDError                       | 153   | DocumentReader    | Error during RFID process                                                            |
| GenericError                    | 170   | DocumentReader    | Scan or RFID succeeded but results were invalid                                      |
| PAError                         | 171   | DocumentReader    | Passive Authentication failed                                                        |
| MRZRFIDMismatch                 | 172   | DocumentReader    | MRZ and RFID data do not match                                                       |
| UnknownError                    | 180   | DocumentReader    | Unmapped internal error                                                              |
| ConfigError                     | 200   | BoardingPassScan  | Feature configurations are missing                                                   |
| BarcodeUnsupported              | 201   | BoardingPassScan  | Barcode format is not supported                                                      |
| PermissionNotGranted            | 202   | BoardingPassScan  | App lacks required permission for boarding pass feature                              |
| BoardingPassNull                | 203   | BoardingPassScan  | Boarding pass returned from scan is null                                             |
| CameraInitFailed                | 204   | BoardingPassScan  | Camera failed to initialize                                                          |
| TransactionFailed               | 220   | BoardingPassScan  | Transaction registration failed on server                                            |
| CameraPermissionNotGranted      | 230   | BoardingPassScan  | User denied camera permission                                                        |
| BoardingPassScanFailed          | 250   | BoardingPassScan  | Barcode scanning failed                                                              |
| BoardingPassItemParserError     | 251   | BoardingPassScan  | Error parsing a field from the scanned boarding pass                                 |
| BoardingPassInvalid             | 252   | BoardingPassScan  | Scanned barcode is not a valid boarding pass                                         |
| BarcodeEmpty                    | 253   | BoardingPassScan  | Scanned barcode is empty                                                             |
| UnknownError                    | 280   | BoardingPassScan  | Unmapped internal error                                                              |
| ConfigError                     | 300   | BoardingPassParse | Feature configurations are missing                                                   |
| BarcodeUnsupported              | 301   | BoardingPassParse | Barcode format is not supported                                                      |
| PermissionNotGranted            | 302   | BoardingPassParse | App lacks required permission for boarding pass feature                              |
| BoardingPassNull                | 303   | BoardingPassParse | Boarding pass is null                                                                |
| TransactionFailed               | 320   | BoardingPassParse | Transaction registration failed on server                                            |
| BoardingPassItemParserError     | 350   | BoardingPassParse | Error parsing a field from the boarding pass                                         |
| BoardingPassInvalid             | 351   | BoardingPassParse | Boarding pass data is invalid                                                        |
| BarcodeEmpty                    | 352   | BoardingPassParse | Barcode content is empty                                                             |
| BoardingPassImageNoBarcodeFound | 353   | BoardingPassParse | No barcode found in provided image                                                   |
| BoardingPassImageParseError     | 354   | BoardingPassParse | Error occurred while parsing provided image                                          |
| UnknownError                    | 380   | BoardingPassParse | Unmapped internal error                                                              |
| PermissionNotGranted            | 400   | FaceCapture       | App lacks required permission for face capture feature                               |
| ErrorLoadingImageFromStorage    | 401   | FaceCapture       | Failed to load image from internal storage                                           |
| ImagePathIsNull                 | 402   | FaceCapture       | Image path is null                                                                   |
| LoadImageFailed                 | 403   | FaceCapture       | Failed to load image from given path                                                 |
| ProcessReportIsNull             | 404   | FaceCapture       | Face capture process report is null                                                  |
| CameraInitFailed                | 405   | FaceCapture       | Camera failed to initialize                                                          |
| CameraPictureError              | 406   | FaceCapture       | Error occurred while taking picture                                                  |
| ParamsIsNull                    | 407   | FaceCapture       | Face capture configuration parameters are null                                       |
| TransactionFailed               | 420   | FaceCapture       | Transaction registration failed on server                                            |
| BiometricLivenessServiceFailed  | 422   | FaceCapture       | Liveness service call failed                                                         |
| CameraPermissionNotGranted      | 430   | FaceCapture       | User denied camera permission                                                        |
| InvalidParameters               | 440   | FaceCapture       | Invalid parameter passed by client                                                   |
| TestFailed                      | 450   | FaceCapture       | Captured image failed quality tests                                                  |
| LivenessTestsFailed             | 451   | FaceCapture       | Liveness quality tests failed                                                        |
| FaceCaptureTimeout              | 452   | FaceCapture       | Face capture timed out before a valid image was captured                             |
| UnknownError                    | 480   | FaceCapture       | Unmapped internal error                                                              |
| PermissionNotGranted            | 500   | FaceMatch         | App lacks required permission for face match feature                                 |
| ErrorLoadingImages              | 501   | FaceMatch         | Failed to load images for face match                                                 |
| TransactionFailed               | 520   | FaceMatch         | Transaction registration failed on server                                            |
| CommunicationError              | 521   | FaceMatch         | Server communication error during face match                                         |
| MatchFailed                     | 550   | FaceMatch         | Face match between document and selfie failed                                        |
| DataIntegrityFailed             | 551   | FaceMatch         | Provided hashes and images do not match                                              |
| UnknownError                    | 580   | FaceMatch         | Unmapped internal error                                                              |
| PermissionNotGranted            | 600   | Subject           | App lacks required permission for subject feature                                    |
| DataError                       | 601   | Subject           | SDK internal error passing subject object                                            |
| TransactionFailed               | 620   | Subject           | Transaction registration failed on server                                            |
| CommunicationError              | 621   | Subject           | Server communication error during subject action                                     |
| SubjectServiceError             | 650   | Subject           | Subject action failed on server; check parameters and endpoint                       |
| MissingBCBP                     | 651   | Subject           | BCBP is missing and is a mandatory field                                             |
| UnknownError                    | 680   | Subject           | Unmapped internal error                                                              |
| ConfigError                     | 700   | Ultralight        | Feature configurations are missing                                                   |
| NotReady                        | 701   | Ultralight        | Ultralight not initialized; call initialize first                                    |
| InitFailed                      | 702   | Ultralight        | Initialization failed; check API key                                                 |
| BluetoothNotGranted             | 703   | Ultralight        | Bluetooth permission denied                                                          |
| BluetoothNotEnabled             | 704   | Ultralight        | Bluetooth is disabled (Android only)                                                 |
| LocationNotEnabled              | 705   | Ultralight        | Location is disabled (Android only)                                                  |
| UnknownError                    | 780   | Ultralight        | Unmapped internal error                                                              |

### iOS

| Name | Value | Feature | When thrown |
|------|-------|---------|-------------|
| InvalidApiKey | 010 | Configuration | The API key is missing or invalid. |
| InvalidEndpoint | 011 | Configuration | The endpoint is missing, malformed, or does not use HTTPS. |
| InitFailed | 012 | Configuration | SDK configuration could not be retrieved or decoded during initialization. |
| NotReady | 013 | Configuration | An SDK operation is requested before initialization completes successfully. |
| InvalidLicense | 014 | Configuration | The SDK license token is invalid, expired, incorrectly signed, or issued for another application. |
| InvalidGatewayConfig | 015 | Configuration | Mobile API Gateway configuration is missing or invalid. |
| GatewayAuthenticationFailed | 016 | Configuration | Authentication with Mobile API Gateway fails. |
| ConfigError | 100 | Document Reader | Document Reader configuration is unavailable. |
| NotReady | 101 | Document Reader | Document Reader is used before its provider is initialized. |
| InitFailed | 102 | Document Reader | The configured provider fails to initialize. |
| ReportIsNull | 103 | Document Reader | A document scan or RFID operation completes without a report. |
| ErrorCertificate | 104 | Document Reader | Required CSCA certificates cannot be loaded. |
| InvalidCertificate | 105 | Document Reader | A supplied CSCA certificate is invalid. |
| LicenseNotFound | 106 | Document Reader | The provider license cannot be found. |
| PermissionNotGranted | 107 | Document Reader | The application is not permitted to use Document Reader. |
| FetchingResourcesFailed | 120 | Document Reader | Provider resources cannot be downloaded. |
| TransactionFailed | 121 | Document Reader | Transaction registration fails before document reading. |
| InvalidDatabaseState | 122 | Document Reader | The provider database cannot be downloaded and no usable local database is available. |
| ProviderNotFound | 140 | Document Reader | No document reader provider was supplied. |
| InvalidParameter | 141 | Document Reader | A Document Reader parameter is invalid. |
| MrzError | 150 | Document Reader | MRZ or OCR processing fails. |
| RegulaError | 151 | Document Reader | The Regula provider reports a scan error. |
| MrzTimeout | 152 | Document Reader | MRZ scanning exceeds the configured timeout. |
| RFIDError | 153 | Document Reader | RFID chip reading or chip-data validation fails. |
| Repeated | 160 | Document Reader | The user chooses to repeat the document-reading flow. |
| Unknown | 180 | Document Reader | A Document Reader error cannot be mapped to a known code. |
| TCNotAccepted | 190 | Document Reader | The user rejects the terms and conditions. |
| ConfigError | 200 | Boarding Pass Scan | Boarding Pass Scanner configuration is unavailable. |
| BarcodeUnsupported | 201 | Boarding Pass Scan | The scanned barcode format is unsupported. |
| PermissionNotGranted | 202 | Boarding Pass Scan | The application is not permitted to use Boarding Pass Scanner. |
| BoardingPassNull | 203 | Boarding Pass Scan | Scanning completes without boarding-pass data. |
| CameraInitFailed | 204 | Boarding Pass Scan | The camera cannot be initialized. |
| TransactionFailed | 220 | Boarding Pass Scan | Transaction registration fails before scanning. |
| CameraPermissionNotGranted | 230 | Boarding Pass Scan | The user denies camera permission. |
| BoardingPassScanFailed | 250 | Boarding Pass Scan | Barcode capture fails. |
| BoardingPassItemParserError | 251 | Boarding Pass Scan | A field in the scanned BCBP payload cannot be parsed. |
| BoardingPassInvalid | 252 | Boarding Pass Scan | The scanned BCBP payload fails validation. |
| BarcodeEmpty | 253 | Boarding Pass Scan | The scanned barcode contains no data. |
| Repeated | 260 | Boarding Pass Scan | The user chooses to repeat the boarding-pass scan. |
| Unknown | 280 | Boarding Pass Scan | A scan error cannot be mapped to a known code. |
| TCNotAccepted | 290 | Boarding Pass Scan | The user rejects the terms and conditions. |
| ConfigError | 300 | Boarding Pass Parse | Reserved; raw-barcode configuration failures currently return Boarding Pass Scan code `200`. |
| BarcodeUnsupported | 301 | Boarding Pass Parse | No supported barcode is found in the supplied image. |
| PermissionNotGranted | 302 | Boarding Pass Parse | Reserved; this code is not currently returned by the iOS parser. |
| BoardingPassNull | 303 | Boarding Pass Parse | Reserved; this code is not currently returned by the iOS parser. |
| TransactionFailed | 320 | Boarding Pass Parse | Transaction registration fails before parsing. |
| BoardingPassItemParserError | 350 | Boarding Pass Parse | Reserved; BCBP field parsing failures currently return Boarding Pass Scan code `251`. |
| BoardingPassInvalid | 351 | Boarding Pass Parse | The supplied image cannot be converted or does not contain usable boarding-pass data. |
| BarcodeEmpty | 352 | Boarding Pass Parse | Reserved; empty raw barcodes currently return Boarding Pass Scan code `253`. |
| Repeated | 360 | Boarding Pass Parse | Reserved; parser retries are logged internally and this code is not returned to the application. |
| Unknown | 380 | Boarding Pass Parse | A parser error cannot be mapped to a known code. |
| TCNotAccepted | 390 | Boarding Pass Parse | The user rejects the terms and conditions. |
| PermissionNotGranted | 400 | Face Capture | The application is not permitted to use Face Capture. |
| ErrorLoadingImageFromStorage | 401 | Face Capture | A captured image cannot be loaded from internal storage. |
| ImagePathIsNull | 402 | Face Capture | Face Capture completes without an image path. |
| LoadImageFailed | 403 | Face Capture | The image at the returned path cannot be loaded. |
| ProcessReportIsNull | 404 | Face Capture | Face Capture processing completes without a report. |
| CameraInitFailed | 405 | Face Capture | The camera cannot be initialized. |
| CameraPictureError | 406 | Face Capture | The camera fails while taking the picture. |
| ParamsIsNull | 407 | Face Capture | Required Face Capture parameters are missing. |
| TransactionFailed | 420 | Face Capture | Transaction registration fails before capture. |
| CommunicationError | 421 | Face Capture | Communication with a biometric service fails. |
| BiometricLivenessServiceFailed | 422 | Face Capture | Reserved; this code is not currently returned by the iOS SDK. |
| CameraPermissionNotGranted | 430 | Face Capture | The user denies camera permission. |
| InvalidParameter | 440 | Face Capture | A Face Capture parameter is invalid. |
| TestFailed | 450 | Face Capture | The captured image fails one or more configured quality tests. |
| LivenessTestsFailed | 451 | Face Capture | Biometric processing reports one or more failed liveness checks. |
| FaceCaptureTimeout | 452 | Face Capture | No valid face is captured before the configured timeout. |
| Repeated | 460 | Face Capture | The user chooses to retake the face image. |
| Unknown | 480 | Face Capture | A Face Capture error cannot be mapped to a known code. |
| TCNotAccepted | 490 | Face Capture | The user rejects the terms and conditions. |
| PermissionNotGranted | 500 | Face Match | The application is not permitted to use Face Match. |
| ErrorLoadingImages | 501 | Face Match | The candidate or reference image cannot be loaded. |
| TransactionFailed | 520 | Face Match | Transaction registration fails before matching. |
| CommunicationError | 521 | Face Match | Communication with the biometric matching service fails. |
| MatchFailed | 550 | Face Match | The candidate face does not match the reference face. |
| DataIntegrityFailed | 551 | Face Match | Image data does not match its supplied integrity hash. |
| Repeated | 560 | Face Match | The user chooses to repeat Face Match. |
| Unknown | 580 | Face Match | A Face Match error cannot be mapped to a known code. |
| TCNotAccepted | 590 | Face Match | The user rejects the terms and conditions. |
| PermissionNotGranted | 600 | Subject | The application is not permitted to use Subject Management. |
| DataError | 601 | Subject | Subject data cannot be built or converted for the requested operation. |
| TransactionFailed | 620 | Subject | Transaction registration fails before the subject operation. |
| CommunicationError | 621 | Subject | Communication with the Subject service fails. |
| SubjectServiceError | 650 | Subject | The Subject service rejects or fails the requested operation. |
| MissingBCBP | 651 | Subject | A required BCBP is missing from the subject data. |
| Repeated | 660 | Subject | The user chooses to repeat the subject flow. |
| Unknown | 680 | Subject | A Subject error cannot be mapped to a known code. |
| TCNotAccepted | 690 | Subject | The user rejects the terms and conditions. |
| ConfigError | 700 | Ultralight | Ultralight configuration is missing or invalid. |
| NotReady | 701 | Ultralight | Ultralight is used before initialization completes. |
| InitFailed | 702 | Ultralight | Ultralight initialization fails. |
| BluetoothNotGranted | 703 | Ultralight | Bluetooth permission is not granted. |
| Unknown | 780 | Ultralight | An Ultralight error cannot be mapped to a known code. |

You can use the result code to provide accurate feedback to the user or use the new property inside **FeatureError**, called **errorType** that classifies the type of error.
We suggest that errors should be handled by **errorType**.

Alongside with the error code and description that are useful for logging and tracing, we also provide a `publicMessage` that is a suggestion of what you can show to the final user as an error message.

The value of `publicMessage` is filled depending on the error type and you can change the default texts or provide additional translations by overriding these strings:

=== "Android"

    ```xml
    <string name="error_internal_sdk_enrolment">Oops! There was an unexpected error, please contact support.</string>
    <string name="error_communication_sdk_enrolment">There was an error while communicating with the server, please try again.</string>
    <string name="error_android_permission_sdk_enrolment">The required permission was not given.</string>
    <string name="error_scan_failed_sdk_enrolment">There was an error with the scan, please try again.</string>
    <string name="error_document_reader_timeout_sdk_enrolment">Oops! You took too long, please try again.</string>
    <string name="error_boarding_pass_invalid_sdk_enrolment">The boarding pass is invalid.</string>
    <string name="error_face_capture_failed_sdk_enrolment">We were unable to detect a face, please try again.</string>
    <string name="error_face_match_failed_sdk_enrolment">The images don\'t match, please redo the process.</string>
    <string name="error_subject_failed_sdk_enrolment">We were unable to identify the related subject.</string>
    <string name="error_canceled_sdk_enrolment">The user chose to cancel the operation.</string>
    <string name="error_repeated_sdk_enrolment">The user repeated the operation.</string>
    <string name="error_terms_and_conditions_rejected_sdk_enrolment">Unfortunately, since you did not accept the terms and conditions we can\'t proceed.</string>
    <string name="error_unknown_sdk_enrolment">Oops! An unidentified problem occurred, please try again.</string>
    ```

=== "iOS"

    ```swift
    //configError
    Theme.shared.strings.errorsPublicMessages.configError
    //badConfigError
    Theme.shared.strings.errorsPublicMessages.badConfigError
    //internalError
    Theme.shared.strings.errorsPublicMessages.internalError
    //communicationError
    Theme.shared.strings.errorsPublicMessages.communicationError
    //termsAndConditionsRejected
    Theme.shared.strings.errorsPublicMessages.termsAndConditionsRejected
    //userRepeated
    Theme.shared.strings.errorsPublicMessages.userRepeated
    //permissionNotGrantedError
    Theme.shared.strings.errorsPublicMessages.permissionNotGrantedError
    //scanError
    Theme.shared.strings.errorsPublicMessages.scanError
    //timeout
    Theme.shared.strings.errorsPublicMessages.timeout
    //boardingPassInvalid
    Theme.shared.strings.errorsPublicMessages.boardingPassInvalid
    //documentReaderError
    Theme.shared.strings.errorsPublicMessages.documentReaderError
    //faceCaptureError
    Theme.shared.strings.errorsPublicMessages.faceCaptureError
    //faceMatchError
    Theme.shared.strings.errorsPublicMessages.faceMatchError
    //subjectError
    Theme.shared.strings.errorsPublicMessages.subjectError
    //unknownError
    Theme.shared.strings.errorsPublicMessages.unknownError
    ```

## How to setup error handling

When you call one of our facade methods, then you will need to pass a completion handler, and it will be called when the result is ready, either successfully or with an error.

**You can check more details how to obtain the FeatureError object on the "Handle result" section of the overview page of each feature.**

### iOS error-handling example

Feature-specific errors expose a `featureError` property. Handle its `errorType`
to decide whether to retry, explain a missing permission, or end the flow:

```swift
private func handleError(_ error: FeatureError) {
    switch error.errorType {
    case .userRepeated:
        retry()
    case .permissionNotGrantedError:
        showPermissionRationale()
    case .communicationError, .scanError, .timeout:
        showError(message: error.publicMessage, canRetry: true)
    default:
        showError(message: error.publicMessage, canRetry: false)
    }
}
```

This is a brief overview of what each ErrorType corresponds to:

- When it's an internal error, you have to contact Amadeus and share some stacktrace or way to replicate the bug. It usually means that there is some invalid configuration or missing property from our backoffice.
- Communication errors are mostly caused by internet connection issues, so trying again can solve the problem, it's recommended to allow the user to re-send the request. It can also mean an invalid url of some sort, so if the problem persists you can contact Amadeus.
- PermissionNotGrantedError means that the user didn't grant permission to use some part of the hardware that is required, as recommended you should have a rationale to explain why that permission is required and block the user from proceeding until he grants the permission.
- User repeated is not exactly an error; it indicates that the user wants to try the operation again.
- Scan error happens when there is an error on document scan or any error with the scan of the boarding pass, this usually requires debugging, so it's recommended to share the stacktrace and communicate to Amadeus.
- Timeout it means that either the timer of document reader or face capture has reached the end and it wasn't possible to capture the image successfully, you can inform the user of that, suggesting how he should scan the document (on the table, with a high contrast from the table, with the proper angle etc..), or take the selfie in better conditions and let the user try again.
- Boarding pass invalid means that the scan or parse of the boarding pass was correct but some issues were found. Can be the format that is not supported by us, or simply it's not actually a boarding pass barcode.
- FaceCaptureError means that the feature failed, either due to our quality tests failing, and in that case you will receive a report saying which tests failed, or liveness service failed due to the quality of the image or being a image of an image and not a real person.
- SubjectError happens when the subject action the user was trying to make failed. eg: User tried to add an invalid subject.
- Unknown errors should not happen but any error that we have unmapped will return unknown error and must be reported for investigation.
