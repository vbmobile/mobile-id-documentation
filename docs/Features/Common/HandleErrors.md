# Error handling

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
        val publicMessage : String = ""
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
        FaceCaptureError,
        FaceMatchError,
        SubjectError,
        FormError,
        UnknownError,
        ConfigurationError,
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

        init(errorType: ErrorType, errorCode: Int, description: String, publicMessage: String, name: String) 
    }
    
    public enum ErrorType {
        case internalError
        case communicationError
        case termsAndConditionsRejected
        case userRepeated
        case permissionNotGrantedError
        case scanError
        case scanTimeout
        case boardingPassInvalid
        case faceCaptureError
        case faceMatchError
        case subjectError
        case unknownError
    }
    ```

Here you can find a list of all the error codes the SDK sends to the client application:

| Name                            | Value | Feature           |
|---------------------------------|-------|-------------------|
| InvalidApiKey                   |  10   | Configuration     |
| InvalidEndpoint                 |  11   | Configuration     |
| InitFailed                      |  12   | Configuration     |
| NotReady                        |  13   | Configuration     |
| ConfigError                     | 100   | DocumentReader    |
| NotReady                        | 101   | DocumentReader    |
| InitFailed                      | 102   | DocumentReader    |
| ReportIsNull                    | 103   | DocumentReader    |
| ErrorCertificate                | 104   | DocumentReader    |
| InvalidCertificate              | 105   | DocumentReader    |
| LicenseNotFound                 | 106   | DocumentReader    |
| PermissionNotGranted            | 107   | DocumentReader    |
| FetchingResourcesFailed         | 120   | DocumentReader    |
| TransactionFailed               | 121   | DocumentReader    |
| InvalidDatabaseState            | 122   | DocumentReader    |
| MrzError                        | 150   | DocumentReader    |
| RegulaError                     | 151   | DocumentReader    |
| MrzTimeout                      | 152   | DocumentReader    |
| Repeated                        | 160   | DocumentReader    |
| UnknownError                    | 180   | DocumentReader    |
| ConfigError                     | 200   | BoardingPassScan  |
| BarcodeUnsupported              | 201   | BoardingPassScan  |
| PermissionNotGranted            | 202   | BoardingPassScan  |
| BoardingPassNull                | 203   | BoardingPassScan  |
| CameraInitFailed                | 204   | BoardingPassScan  |
| TransactionFailed               | 220   | BoardingPassScan  |
| CameraPermissionNotGranted      | 230   | BoardingPassScan  |
| BoardingPassScanFailed          | 250   | BoardingPassScan  |
| BoardingPassItemParserError     | 251   | BoardingPassScan  |
| BoardingPassInvalid             | 252   | BoardingPassScan  |
| BarcodeEmpty                    | 253   | BoardingPassScan  |
| Repeated                        | 260   | BoardingPassScan  |
| UnknownError                    | 280   | BoardingPassScan  |
| ConfigError                     | 300   | BoardingPassParse |
| BarcodeUnsupported              | 301   | BoardingPassParse |
| PermissionNotGranted            | 302   | BoardingPassParse |
| BoardingPassNull                | 303   | BoardingPassParse |
| TransactionFailed               | 320   | BoardingPassParse |
| BoardingPassItemParserError     | 350   | BoardingPassParse |
| BoardingPassInvalid             | 351   | BoardingPassParse |
| BarcodeEmpty                    | 352   | BoardingPassParse |
| BoardingPassImageNoBarcodeFound | 353   | BoardingPassParse |
| BoardingPassImageParseError     | 354   | BoardingPassParse |
| Repeated                        | 360   | BoardingPassParse |
| UnknownError                    | 380   | BoardingPassParse |
| PermissionNotGranted            | 400   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 401   | FaceCapture       |
| PermissionNotGranted            | 402   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 403   | FaceCapture       |
| PermissionNotGranted            | 404   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 405   | FaceCapture       |
| PermissionNotGranted            | 406   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 407   | FaceCapture       |
| PermissionNotGranted            | 420   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 422   | FaceCapture       |
| PermissionNotGranted            | 430   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 450   | FaceCapture       |
| PermissionNotGranted            | 451   | FaceCapture       |
| ErrorLoadingImageFromStorage    | 452   | FaceCapture       |
| Repeated                        | 460   | FaceCapture       |
| UnknownError                    | 480   | FaceCapture       |
| PermissionNotGranted            | 500   | FaceMatch         |
| ErrorLoadingImages              | 501   | FaceMatch         |
| TransactionFailed               | 520   | FaceMatch         |
| CommunicationError              | 521   | FaceMatch         |
| MatchFailed                     | 550   | FaceMatch         |
| DataIntegrityFailed             | 551   | FaceMatch         |
| Repeated                        | 560   | FaceMatch         |
| UnknownError                    | 580   | FaceMatch         |
| PermissionNotGranted            | 600   | Subject           |
| DataError                       | 601   | Subject           |
| TransactionFailed               | 620   | Subject           |
| CommunicationError              | 621   | Subject           |
| SubjectServiceError             | 650   | Subject           |
| MissingBCBP                     | 651   | Subject           |
| Repeated                        | 660   | Subject           |
| UnknownError                    | 680   | Subject           |
| PermissionNotGranted            | 800   | Form              |
| TransactionFailed               | 820   | Form              |
| CommunicationError              | 821   | Form              |
| FormServiceError                | 850   | Form              |
| UnknownError                    | 880   | Form              |

You can use the result code to provide accurate feedback to the user or use the new property inside **FeatureError**, called **errorType** that classifies the type of error.
We suggest that errors should be handled by **errorType**.

Alongside with the error code and description that are useful for logging and tracing, we also provide a publicErrorMessage that is a suggestion of what you can show to the final user as an error message.

The value of publicErrorMessage is filled depending on the error type and you can change the default texts or provide additional translations by overriding these strings:

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
    //configurationError
    Theme.shared.strings.errorsPublicMessages.configError
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
    //scanTimeout
    Theme.shared.strings.errorsPublicMessages.scanTimeout
    //boardingPassInvalid
    Theme.shared.strings.errorsPublicMessages.boardingPassInvalid
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

This is a brief overview of what each ErrorType corresponds to:

- When it's an internal error, you have to contact VisionBox and share some stacktrace or way to replicate the bug. It usually means that there is some invalid configuration or missing property from our backoffice.
- Communication errors are mostly caused by internet connection issues, so trying again can solve the problem, it's recommended to allow the user to re-send the request. It can also mean an invalid url of some sort, so if the problem persists you can contact VisionBox.
- PermissionNotGrantedError means that the user didn't grant permission to use some part of the hardware that is required, as recommended you should have a rationale to explain why that permission is required and block the user from proceeding until he grants the permission.
- User repeated and user canceled are not exactly errors, they are just warnings to inform that the user wants to try again or canceled the operation.
- Scan error happens when there is a regula error or any error with the scan of the boarding pass, this usually requires debugging, so it's recommended to share the stacktrace and communicate to VisionBox.
- Timeout it means that either the timer of document reader or face capture has reached the end and it wasn't possible to capture the image successfully, you can inform the user of that, suggesting how he should scan the document (on the table, with a high contrast from the table, with the proper angle etc..), or take the selfie in better conditions and let the user try again.
- Boarding pass invalid means that the scan or parse of the boarding pass was correct but some issues were found. Can be the format that is not supported by us, or simply it's not actually a boarding pass barcode.
- FaceCaptureError means that the feature failed, either due to our quality tests failing, and in that case you will receive a report saying which tests failed, or liveness service failed due to the quality of the image or being a image of an image and not a real person.
- SubjectError happens when the subject action the user was trying to make failed. eg: User tried to add an invalid subject.
- Unknown errors should not happen but any error that we have unmapped will return unknown error and must be reported for investigation.
