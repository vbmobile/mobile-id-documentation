# Document Reader

The document reader is used to extract the user’s document information and perform all necessary
security validations. This functionality works in two steps: the MRZ of the travel document is
scanned (using the device's camera) and then, if it is an electronic document (i.e. with a chip),
and the client app indicated that it wants to read the chip, the user is prompted to place the
mobile device over the travel e-Document in order to perform a RFID scan to extract available data.

## Configure

To use this feature, you must provide the DocumentReaderConfig to the EnrolmentBuilder like the
following example:

=== "Android"

    ```kotlin
    val builder: EnrolmentBuilder = EnrolmentBuilder
        .of(context, config)
        .withDocumentReaderConfig(documentReaderConfig)
        .build()
    ```

=== "iOS"

    ``` swift
    var enrolment: EnrolmentProtocol = EnrolmentBuilder
            .of(enrolmentConfig: enrolmentConfig)
            .with(documentReaderConfig: documentReaderConfig)
            .with(viewRegister: viewRegister)
            .build()
    ```

The DocumentReaderConfig has the following structure:

=== "Android"

    ```kotlin
    @Parcelize
    data class DocumentReaderConfig(
      val multipageProcessing: Boolean,
      val databaseId: String
    ) : Parcelable
    ```
    
    - multipageProcessing: controls the workflow for documents that might need to have different pages
    scanned;
    - databaseId: specify database Id to be used with the document reader functionality (provided by
    Regula);
    
=== "iOS"

    ``` swift
    public struct DocumentReaderConfig {
        public let multipageProcessing: Bool
        public let databaseID: String
        public let databasePath: String?
        public let scannerTimeout: TimeInterval
        
        public init(multipageProcessing: Bool, databaseID: String, databasePath: String? = nil, scannerTimeout: TimeInterval = 30) 
    }
    ```

    - multipageProcessing: controls the workflow for documents that might need to have different pages
    scanned;
    - databaseId: specify database Id to be used with the document reader functionality (provided by
    Regula);
    - databasePath: Database path for .dat file to initialize Regula documents database. Default value is `nil`.
    - scannerTimeout: Document scan timeout, in seconds. Default value is `30` seconds.

## Initiate Scan

The document reader functionality enables the client application to extract and validate data from
travel documents from different countries, by calling the readDocument method.

=== "Android"

    This method is now deprecated and will be removed in the future
    ```kotlin
    override fun readDocument(activity: Activity, params: DocumentReaderParameters) {
        enrolment.readDocument(activity, params)
    }
    ```
    The new method contains a new parameter that's responsible to receive the result of this feature
    ```kotlin
    override fun readDocument(context: Context, params: DocumentReaderParameters) {
        // More info on the documentReaderResultLauncher in the how to get the result section
        enrolment.readDocument(context, params, documentReaderResultLauncher)
    }
    ```

=== "iOS"

    ``` swift
    func readDocument(parameters: ReadDocumentParameters,
                      viewController: UIViewController,
                      completionHandler: @escaping (Result<DocumentReaderReport, DocumentReaderError>) -> Void) throws
    ```

This method can perform a full travel document read in two steps:

- MRZ scan: using the device's camera, the SDK reads the MRZ section of the travel document and
  extracts information from it. During this step, and if available, a document picture is also
  scanned and saved.
- RFID scan: the user is prompted to move the device over the e-Document and, using NFC, the chip
  data is scanned. This step is available only for electronic documents (i.e. with a chip) and is
  optional (i.e. the client app must indicate that it wants to read the document's chip, setting the
  readRFID flag to true when calling the readDocument method). You can use specific parameters when
  using this functionality for passport scanning. Below is an example on how to provide those
  parameters:

=== "Android"

    ```kotlin
    data class DocumentReaderParameters(
        val showPreview: Boolean,
        val showErrors: Boolean,
        val rfidRead: Boolean,
        val showSecurityCheck: Boolean = true,
        val showRFIDStatus: Boolean = false,
        val mrzReadTimeout: Long = TimeUnit.SECONDS.toMillis(30),
        val rfidReadTimeout: Long = TimeUnit.SECONDS.toMillis(30),
    ) : Parcelable {
    init {
        require(!(mrzReadTimeout < TimeUnit.SECONDS.toMillis(10) || mrzReadTimeout > TimeUnit.SECONDS.toMillis(60))) { "mrzReadTimeout value must be between 10 and 60 seconds." }
        require(!(rfidReadTimeout < TimeUnit.SECONDS.toMillis(10) || rfidReadTimeout > TimeUnit.SECONDS.toMillis(60))) { "rfidReadTimeout value must be between 10 and 60 seconds." }
    }
    ```

=== "iOS"

    ``` swift
    public struct ReadDocumentParameters {
        public let showPreview: Bool
        public let readRFID: Bool
        public let showRFIDStatus: Bool
        public let scannerTimeout: TimeInterval
        public let rfidTimeout: TimeInterval
    
        public init(showPreview: Bool,
                    readRFID: Bool,
                    showRFIDStatus: Bool = false,
                    scannerTimeout: TimeInterval = 30,
                    rfidTimeout: TimeInterval = 30)
    }
    ```

Both mrzReadTimeout and rfidReadTimeout values must be between 10 and 60 seconds, otherwise an illegal argument exception will be thrown.
It's no longer possible to disable either of this timeout.

If both scans are enabled and the RFID scan fails for some reason, the MRZ scan data is always
returned as the default set of data read from the travel document. The mrzReadTimeout is the timeout
value in seconds before closing the document reading screen if no document is scanned during this
period. The functionality provides UI solution for both document scanning and returned data
preview (as shown in the following images), with an option to retry the scan. The preview is only
shown if the flag showPreview in the DocumentReaderParameters is set to true when calling the
readDocument method. The showRFIDStatus is a flag to show an icon in the preview screen that
indicates if the document was scanned using RFID and properly validated and authenticated. The
showSecurityCheck is used to activate a security mechanism to protect user data in the preview
screen. If it is true, the device will use its own locking mechanism in this screen and the user
will need to authenticate and unlock his device to check the preview data (for example, using
fingerprint or face ID).

## Handle Result

Here is how you can get the document reader report and handle the result for document reader:

=== "Android"

    When using the new document reader method, it's no longer needed to override the onActivityResult.
    You can get the result by using the result launcher that's passed as the final parameter:
    ```kotlin
    private val documentReaderResultLauncher = registerForActivityResult(DocumentReaderResultLauncher())
    { result: DocumentReaderActivityResult ->
        when {
            result.success -> onSuccess(result.documentReaderReport)
            result.documentReaderError?.userCanceled == true -> userCancelled()
            result.documentReaderError?.termsAndConditionsAccepted == false -> onTermsAndConditionsRejected()
            else -> onDocumentReaderError()
        }
    }
    ```
    Here is how you can get the report when using the deprecated method and handle the onActivityResult:
    ```kotlin
    private val documentReadResultHandler by lazy { DocumentReaderResultHandler() }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
    
        when (requestCode) {
            EnrolmentSDKRequestCode.READ_DOCUMENT_REQUEST_CODE -> {
                val result = documentReadResultHandler.parseResult(resultCode, data)
                when {
                    result.success -> onSuccess(result.documentReaderReport)
                    result.documentReaderError?.userCanceled == true -> userCancelled()
                    result.documentReaderError?.termsAndConditionsAccepted == false -> onTermsAndConditionsRejected()
                    else -> onDocumentReaderError()
                }
            }
        }
    }
    ```
    
    You should use the DocumentReaderResultHandler class to parse the result. You will receive a model of the type DocumentReaderActivityResult that will contain the success data (in this case a DocumentReaderReport) or the error data.
    
    ```kotlin
    data class DocumentReaderActivityResult(
        val documentReaderReport: DocumentReaderReport?,
        val documentReaderError: DocumentReaderError?
    ) {
        val success get() = documentReaderReport != null
    }
    ```
    
    The DocumentReaderError has the following structure:

    ```kotlin
    data class DocumentReaderError(
        val userCanceled: Boolean,
        val termsAndConditionsAccepted: Boolean,
        val featureError: FeatureError?,
    )
    ```
    The FeatureError has the following structure:
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

    ``` swift
    self.enrolment.readDocument( parameters: parameters, viewController: view) { [weak self] result in
        switch result {
            case .success(let documentReaderReport):
               // handle DocumentReaderReport
                
            case .failure(let error):
                EnrolmentData.shared.documentReaderReport = nil
                switch error {
                    case .cancelled:
                        print("onUserCancel")
                    case .configNotFound:
                        print("Document Reader config not found")
                    default:
                        print("Document read: \(error.localizedDescription)")
            }
        }
    }
    ```
    The DocumentReaderError has the following structure:
    
    ```swift
    public enum DocumentReaderError: Error {
        /// [DocumentReaderError] that occurs when there's an error in the parameters `ReadDocumentParameters`
        case invalidParameter(String?)
        /// [DocumentReaderError] that occurs when there's an error while reading OCR or MRZ.
        case mrzOcr
        /// [DocumentReaderError] that occurs when there's a timeout while reading OCR or MRZ.
        case mrzOcrTimeout
        /// [DocumentReaderError] that occurs when there's an error initializing the Document Reader.
        case docReaderInitFailed
        /// [DocumentReaderError] that occurs when there's an error requesting the resources endpoint.
        case fetchingResources
        /// [DocumentReaderError] that occurs when Document Reader isn't ready.
        case notReady
        /// [DocumentReaderError] that occurs when there's an error reading the document.
        case regulaError
        /// [DocumentReaderError] that occurs when user cancels document reading.
        case cancelled
        /// [DocumentReaderError] that occurs when config wasn't provided.
        case configNotFound
        /// [DocumentReaderError] that occurs when license wasn't provided.
        case licenseNotFound
        /// [DocumentReaderError] that occurs when there is an invalid databaseId and a local database file was not provided.
        case invalidDatabaseState(String?)
        /// [DocumentReaderError] that occurs when there are no CSCA certificates configured for the APIKey.
        case missingCSCACertificates
        /// [DocumentReaderError] that occurs when the certificate for document reader is invalid.
        case invalidCertificate(error: InvalidDSCertificateError)
        /// [DocumentReaderError] that occurs when there's an error during a pre/pos feature process.
        case feature(error: FeatureError)
        /// [DocumentReaderError] that occurs when there's an error during a register transaction process.
    }
    ```
    
    The InvalidDSCertificateError has the following structure:
        
    ```swift
    public enum InvalidDSCertificateError: Error {
        /// Data was not found.
        case invalidData
        /// File has unsuported extension.
        case invalidExtension
    }
    ```
    
    The FeatureError has the following structure:
    
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
    The EnrolmentServerError has the following structure:
    ```swift
    public struct EnrolmentServerError {
        public let type: String
        public let statusCode: Int
        public let title: String
        public let detail: String?
        public let instance: String?
        public let traceId: String?
        public let errors: [String: [String]]?
    }
    ```
    The FeatureOperationErrorType has the following structure:
    ```swift
    public enum FeatureOperationErrorType {
        case rgpd
        case permission
        case registerTransaction
    }
    ```
    
The document reader report has the following structure:

=== "Android"

    ```kotlin
    @Parcelize
    data class DocumentReaderReport(
        val documentData: DocumentData,
        val status: List<DocumentDataStatus>,
        val rfidStatus: RFIDStatus,
        val documentType: DocumentType
    ) : Parcelable
    ```
    
=== "iOS"
    ```swift
    public struct DocumentReaderReport: Codable {
        public let documentData: DocumentData
        public let documentType: DocumentType
        public let documentRFIDStatus: DocumentRFIDStatus
        public let documentStatuses: [DocumentDataStatus]
    }
    ```

The DocumentData contains the document data. You can check the structure here:

=== "Android"

    ```kotlin
    data class DocumentData(
        val hasChip: Boolean,
        val documentNumber: DocumentDataField?,
        val dateOfExpiry: Date?,
        val dateOfBirth: Date?,
        val age: DocumentDataField?,
        val personalNumber: DocumentDataField?,
        val sex: DocumentDataField?,
        val issuingStateCode: DocumentDataField?,
        val issuingState: DocumentDataField?,
        val dateOfIssue: Date?,
        val nationalityCode: DocumentDataField?,
        val nationality: DocumentDataField?,
        val givenNames: DocumentDataField?,
        val surname: DocumentDataField?,
        val surnameAndGivenNames: DocumentDataField?,
        val documentClassCode: DocumentDataField?,
        val documentNumberCheckDigit: DocumentDataField?,
        val dateOfBirthCheckDigit: DocumentDataField?,
        val dateOfExpiryCheckDigit: DocumentDataField?,
        val optionalDataCheckDigit: DocumentDataField?,
        val finalCheckDigit: DocumentDataField?,
        val optionalData: DocumentDataField?,
        val cardAccessNumber: DocumentDataField?,
        val remainderTerm: DocumentDataField?,
        val mrzType: DocumentDataField?,
        val mrzStrings: DocumentDataField?,
        val mrzStringsWithCorrectCheckSums: DocumentDataField?,
        val dsCertificateSubject: DocumentDataField?,
        val dsCertificateValidFrom: DocumentDataField?,
        val dsCertificateValidTo: DocumentDataField?,
        val documentImagePath: String,
        val portraitPhotoPath: String,
        val documentTypeData: DocumentTypeData?
    )
    ```
    ```kotlin
    data class DocumentDataField(
        val value: String,
        var status: DocumentDataFieldStatus
    )
    ```
    ```kotlin
    enum class DocumentDataFieldStatus {
        /**
         * field was verified and passed verification successfully.
         */
        OK,
      
        /**
         * verification of the field has failed for some non-specified reason, either it wasn't read correctly or
         * the check digit verification failed. These data are not reliable and should not be used.
         */
        ERROR,
      
        /**
         * field was not verified for correctness.
         */
        NOT_CHECKED
    }
    ```
    ```kotlin
    @Parcelize
        data class DocumentTypeData(
        val type: DocumentType,
        val infoVal: DocumentTypeInfo?
    ) : Parcelable    
    ```
    ```kotlin
    enum class DocumentType { 
        PASSPORT, 
        VISA, 
        ID_CARD, 
        DRIVING_LICENSE, 
        UNKNOWN
    }
    ```
    ```kotlin
    @Parcelize
    data class DocumentTypeInfo(
        val documentId: Int,
        val dTypeId: Int,
        val documentName: String?,
        val icaoCode: String?
    ) : Parcelable   
    ```

    The DocumentDataStatus, RFIDStatus and DocumentType are enums that have the following possibilities:

    ```kotlin
    enum class DocumentDataStatus {
        OK, // No problem found in document.
        VALIDATION_ERROR, // Some field.
        EXPIRED_DOCUMENT, // Date of expiration is already in the past.
        RFID_PASSIVE_AUTHENTICATION, // Document ID is not present in the current master list associated with yout api key.
        MRZ_RFID_MISMATCH, // Regula error stating that the mrz and rfid information do not match (user might have scanned one document and read chip from another).
        RFID_TIMEOUT, // Chip couldn't be read in due time.
        RFID_PERMISSION_NOT_GRANTED, // User did not concede permission to use NFC.
        RFID_TAG_NOT_FOUND, // Warning stating that the document scanned is not eletronic or rfid tag was not detected.
        RFID_NFC_NOT_SUPPORTED, // Smartphone used in scan does not support NFC operations.
        RFID_GENERIC_ERROR, // Unknown error while rfid read was occuring (Usually a break in the reading process due to the user moved the phone too much).
        USER_SKIPPED_RFID // Warning mentioning that rfid was available but user decided to skip it.
    }
    ```
    ```kotlin
    enum class RFIDStatus {
        UNDEFINED, 
        SUCCESS, 
        ERROR
    }
    ```
    
=== "iOS"

    ``` swift
    public class DocumentData: Codable {
        /// Indicates if the document has chip.
        public var hasChip: Bool = false
        /// Document number.
        public var documentNumber: DocumentDataField?
        /// Expiry date of the document.
        public var dateOfExpiry: Date?
        /// Date of birth.
        public var dateOfBirth: Date?
        /// Age.
        public var age: DocumentDataField?
        /// Personal number.
        public var personalNumber: DocumentDataField?
        /// Sex.
        public var sex: DocumentDataField?
        /// Issuing state code in compliance with 3166-1 standard (ICAO doc 9303).
        public var issuingStateCode: DocumentDataField?
        /// Human-readable name of the issuing country, according to the current locale.
        public var issuingState: DocumentDataField?
        /// Date of issue.
        public var dateOfIssue: Date?
        /// Nationality code in compliance with ISO3166-1 standard (ICAO doc 9303).
        public var nationalityCode: DocumentDataField?
        /// Human-readable name of nationality country of the document holder, according to the current locale.
        public var nationality: DocumentDataField?
        /// Given name(s).
        public var givenNames: DocumentDataField?
        /// Surname.
        public var surname: DocumentDataField?
        /// Surname and given name(s).
        public var surnameAndGivenNames: DocumentDataField?
        /// Document class code.
        public var documentClassCode: DocumentDataField?
        /// Check digit for document number.
        public var documentNumberCheckDigit: DocumentDataField?
        /// Check digit for date of birth.
        public var dateOfBirthCheckDigit: DocumentDataField?
        /// Check digit for document expiry date.
        public var dateOfExpiryCheckDigit: DocumentDataField?
        /// Check digit for optional data.
        public var optionalDataCheckDigit: DocumentDataField?
        /// Final check digit (for the whole MRZ).
        public var finalCheckDigit: DocumentDataField?
        /// Optional data.
        public var optionalData: DocumentDataField?
        /// Access number for RFID chip.
        public var cardAccessNumber: DocumentDataField?
        /// Months to expire.
        public var remainderTerm: DocumentDataField?
        /// MRZ type (ID-1 – 0, ID-2 – 1, ID-3 – 2).
        public var mrzType: DocumentDataField?
        /// MRZ lines.
        public var mrzStrings: DocumentDataField?
        /// MRZ with correct checksums.
        public var mrzStringsWithCorrectCheckSums: DocumentDataField?
        /// Textual information about the document issuer.
        public var dsCertificateSubject: DocumentDataField?
        /// Start date of the DS-certificate validity.
        public var dsCertificateValidFrom: DocumentDataField?
        /// Expiration date of the DS-certificate.
        public var dsCertificateValidTo: DocumentDataField?
    
        /// Model that wraps information about the document type
        public var documentTypeData: DocumentTypeData?
    
        /// Photo of the document owner.
        public var portrait: UIImage? {
            return portraitData.flatMap { UIImage(data: $0) }
        }
    
        /// Document image.
        public var documentImage: UIImage? {
            return documentImageData.flatMap { UIImage(data: $0) }
        }
    
        var documentImageData: Data?
    
        var portraitData: Data?
    }
    ```
    ``` swift
    public struct DocumentDataField: Codable {
        public var value: String
        public var status: DocumentDataFieldStatus
    }
    ```
    ``` swift
    public enum DocumentDataFieldStatus: String, Codable {
        /// The field was verified and passed verification successfully.
        case ok
        /// The verification of the field has failed for some non-specified reason, either it wasn't read correctly or the check digit verification failed.
        /// These data are not reliable and should not be used.
        case error
        /// The field was not verified for correctness.
        case notChecked
    }
    ```
    ``` swift
    public struct DocumentTypeData: Codable {
        /// Type of document, ex: Passport, Visa, etc.
        public let type: DocumentType
        /// Model that contains information about the document type
        public let info: DocumentTypeInfo?
    }
    ```
    ``` swift
    public struct DocumentTypeInfo: Codable {
        /// Document type id
        public let dTypeId: Int
        /// Document Name
        public let documentName: String?
        /// Country code
        public let icaoCode: String?
    }
    ```
    ``` swift
    public enum DocumentType: String, Codable {
        case passport
        case visa
        case idCard
        case drivingLicense
        case unknown
    }
    ```
        
    The DocumentRFIDStatus, DocumentDataStatus and DocumentType are enums that have the following possibilities:

    ``` swift
    public enum DocumentType: String, Codable {
        case passport
        case visa
        case idCard
        case drivingLicense
        case unknown
    }
    ```
    ``` swift
    public enum DocumentRFIDStatus: String, Codable {
        case error
        case success
        case undefined
    }
    ```
    ``` swift
    public enum DocumentDataStatus: String, Codable {
        case ok
        case validationError
        case expiredDocument
        case rfidPassiveAuthentication
        case mrzRFIDMismatch
        case rfidNFCNotSupported
        case rfidGenericError
        case rfidTimeouError
        case userSkipedRfid
    }
    ```
    
## DocumentReaderCustomViews
The SDK provides default UI solutions for the document reader feature flow, as
shown in the following images:
![Document Reader Flow](Assets/DocumentReaderFlow.PNG "Document Reader Flow"){: style="display: block; margin: 0 auto"}

The use of the preview layout depends on the **showPreview** flag in the DocumentReaderParameters.

The use of the rfid related layouts depends on the **rfidRead** flag in the DocumentReaderParameters.

You can also apply your app’s colors and fonts to these layout solutions, to keep your brand’s image consistent.
Check Customization tab to learn more about branding of each view.

=== "Android"

    ```kotlin
    @Parcelize
    class DocumentReaderCustomViews(
        val loadingView: Class<out ICustomDocumentReader.LoadingView>? = null,
        val rfidInstructionsView: Class<out ICustomDocumentReader.RfidInstructionsView>? = null,
        val rfidSearchView: Class<out ICustomDocumentReader.RfidSearchView>? = null,
        val rfidProcessView: Class<out ICustomDocumentReader.RfidProcessView>? = null,
    ) : Parcelable
    ```
    You can use your own custom views in the document reader functionality. Your view must implement the
    SDK view interfaces. For example, if you want to add a custom loading view, your view class must
    implement the ICustomDocumentReader.LoadingView interface.
    
=== "iOS"

    ``` swift
    public class EnrolmentViewRegister {
        ...
        // MARK: - Document Reader
        public func registerDocumentReaderRFIDInstructionsView(_ viewType: DocumentReaderRFIDInstructionsViewType)
        public func registerDocumentReaderLoadingView(_ viewType: DocumentReaderLoadingViewType)
        ...
    }    
    ```
    
    Our SDK also allows you to pass your own custom views. The only requirement is that your view must implement the SDK view protocols. For example, if you want to add a custom loading view, your view class must implement the DocumentReaderLoadingViewType.



In the customization tab you will also find examples to create your own custom views.
