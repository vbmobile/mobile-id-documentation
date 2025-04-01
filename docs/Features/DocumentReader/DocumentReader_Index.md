# Document Reader

The document reader is used to extract the user’s document information and perform all necessary
security validations. This functionality works in two steps: the MRZ of the travel document is
scanned (using the device's camera) and then, if it is an electronic document (i.e. with a chip),
and the client app indicated that it wants to read the chip, the user is prompted to place the
mobile device over the travel e-Document in order to perform a RFID scan to extract available data.

## Configure

To use this feature, you must provide the DocumentReaderConfig to your preferred Provider like the
following example:

=== "Android"

    ```kotlin
    val provider: RegulaProvider = RegulaProvider.getInstance(documentReaderConfig)
    ```

=== "iOS"

    ``` swift
    var provider = RegulaDocumentReaderScan(config: documentReaderConfig)
    ```

The DocumentReaderConfig has the following structure:

=== "Android"

    ```kotlin
    data class DocumentReaderConfig(
      val multipageProcessing: Boolean,
      val databaseId: String,
      val checkHologram: Boolean = false,
      val scenario: DocumentReaderScenario = DocumentReaderScenario.OCR
    ) : Parcelable
    ```
    
    - multipageProcessing: controls the workflow for documents that might need to have different pages
    scanned;
    - databaseId: specify database Id to be used with the document reader functionality (provided by
    Regula);
    - checkHologram: checks the presence of holographic effect on the document
    - scenario: the process in which the document is captured

    ```kotlin
    enum class DocumentReaderScenario(val scenario: String) {
        OCR(Scenario.SCENARIO_OCR),
        MRZ(Scenario.SCENARIO_MRZ),
    }
    ```
    
=== "iOS"

    ``` swift
    public struct DocumentReaderConfig {
        public let multipageProcessing: Bool
        public let databaseID: String
        public let databasePath: String?
        public let scannerTimeout: TimeInterval
        public let checkHologram: Bool
        public let scenario: DocumentReaderScenario
        
        public init(multipageProcessing: Bool, databaseID: String, databasePath: String? = nil, scannerTimeout: TimeInterval = 30, checkHologram: Bool = false, scenario: DocumentReaderScenario = .ocr)
    }
    
    public enum DocumentReaderScenario: CaseIterable {
        case ocr
        case mrz
    
        public var value: String {
            switch self {
            case .ocr:
                return "RGL_SCENARIO_OCR"
            case .mrz:
                return "RGL_SCENARIO_MRZ"
            }
        }
    }
    ```

    - multipageProcessing: controls the workflow for documents that might need to have different pages
    scanned;
    - databaseId: specify database Id to be used with the document reader functionality (provided by
    Regula);
    - databasePath: Database path for .dat file to initialize Regula documents database. Default value is `nil`.
    - scannerTimeout: Document scan timeout, in seconds. Default value is `30` seconds.
    - checkHologram: Indicates whether or not the document reader supports Hologram Reading
    - scenario: Changes the scanning scenario in which the document is captured
    
## Initiate Scan

The document reader functionality enables the client application to extract and validate data from
travel documents from different countries, by calling the readDocument method.

=== "Android"

    ```kotlin
    /**
     * Reads the information contained in a personal document.
     *
     * @param activity [Activity] that will launch the face capture feature
     * @param params [DocumentReaderParameters] with some configurations for the document reader feature.
     * @param onReadDocumentCompletion [OnReadDocumentCompletion] callback to handle Success and Error scenarios
     */
    fun readDocument(
        activity: Activity,
        params: DocumentReaderParameters,
        onReadDocumentCompletion: OnReadDocumentCompletion,
    )
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
      val rfidRead: Boolean,
      @IntRange(from = 10_000, to = 60_000)
      val mrzReadTimeout: Long = TimeUnit.SECONDS.toMillis(30),
      @IntRange(from = 10_000, to = 60_000)
      val rfidReadTimeout: Long = TimeUnit.SECONDS.toMillis(30),
      val showRFIDInstructions: Boolean = true,
    ) : Parcelable
    ```

=== "iOS"

    ``` swift
    public struct ReadDocumentParameters {
        public let readRFID: Bool
        public let showRFIDStatus: Bool
        public let scannerTimeout: TimeInterval
        public let rfidTimeout: TimeInterval
        public let showRFIDInstructions: Bool
        
        public init(readRFID: Bool,
                    showRFIDStatus: Bool = false,
                    scannerTimeout: TimeInterval = 30,
                    rfidTimeout: TimeInterval = 30,
                    showRFIDInstructions: Bool = true)
    }
    ```

Both mrzReadTimeout and rfidReadTimeout values must be between 10 and 60 seconds, otherwise an InvalidParameters error will occur.
It's no longer possible to disable either of this timeout.

If both scans are enabled and the RFID scan fails for some reason, the MRZ scan data is always
returned as the default set of data read from the travel document. The mrzReadTimeout is the timeout
value in seconds before closing the document reading screen if no document is scanned during this
period.

The showRFIDInstructions field, when set to false, allows the RFID Scan to start automatically as soon as the document has been read using OCR successfully, not showing the instructions screen when using it nor giving the chance to skip rfid scan.

It's also possible to implement your own OCR scan and then use our DocumentReader just for the RFID reading process.
For this, you will need to pass the DocumentReaderRFIDParameters and call the readDocumentRFID facade method:

=== "Android"

    ```kotlin
    data class DocumentReaderRFIDParameters(
      @IntRange(from = 10_000, to = 60_000)
      val rfidReadTimeout: Long = TimeUnit.SECONDS.toMillis(30),
      val showRFIDInstructions: Boolean = true,
      val mrzString: String
    ) : Parcelable
    ```

=== "iOS"

    ``` swift
    //TODO
    ```

## Handle Result

Here is how you can get the document reader report and handle the result for document reader:

=== "Android"

    You can get the result by registering the callback
    ```kotlin
    interface OnReadDocumentCompletion {
        fun onReadDocumentSuccess(documentReaderReport: DocumentReaderReport)
        fun onReadDocumentError(documentReaderError: DocumentReaderError)
    }
    ```
    
    The DocumentReaderError has the following structure:

    ```kotlin
    data class DocumentReaderError(
        val userCanceled: Boolean,
        val featureError: FeatureError?,
    )
    ```

=== "iOS"

    ``` swift
    self.enrolment.readDocument( parameters: parameters, viewController: view) { [weak self] result in
        switch result {
            case .success(let documentReaderReport):
               // handle DocumentReaderReport
                
            case .failure(let error):
                if error.userCanceled {
                    print("onUserCancel")
                } else {
                    print(error.featureError.publicMessage)
                }
            }
        }
    }
    ```
    The DocumentReaderError has the following structure:
    
    ```swift
    public class DocumentReaderError: Error {
        public var userCanceled: Bool
        public var termsAndConditionsAccepted: Bool
        public var featureError: FeatureError
    }
    ```

### Document Reader Report

=== "Android"

    ```kotlin
    @Serializable
    data class DocumentReaderReport(
      val documentData: DocumentData,
      val idDocument: IdDocument,
      val status: List<DocumentDataStatus>,
      val rfidStatus: RFIDStatus,
      val documentType: DocumentType,
      val documentPhotoHash: String, // Portrait Image
      val documentDataHash: String, // DocumentData object
      val idDocumentHash: String, // IdDocument object
    ) : Parcelable
    ```
    
=== "iOS"
    ```swift
    public struct DocumentReaderReport: Codable {
        public let documentData: DocumentData
        public let documentType: DocumentType
        public let documentRFIDStatus: DocumentRFIDStatus
        public let documentStatuses: [DocumentDataStatus]
        public let documentPhotoHash: String?
        public let documentDataHash: String?
    }
    ```

The `DocumentReaderReport` includes three hash fields that that are used to verify data integrity when building a [Subject](../SubjectManagement/SubjectManagement_Index.md).

The DocumentData is now deprecated and will be removed in the next major version.

Instead, we recommend to start using the IdDocument class that contains more information with different sources depending on the document type. 

You can check the structure here:

=== "Android"

    ```kotlin
    data class IdDocument(
      val info: InfoSection? = null,
      val data: DataSection? = null,
      val viz: VIZSection? = null,
      val mrz: MRZSection? = null,
      val rfid: RFIDSection? = null,
      val validations: Validations? = null
    ): Parcelable
    ```
    ```kotlin
    data class InfoSection(
      val id: Int? = null, // A unique identifier for the document.
      val documentName: String? = null, // Indicates the type and issuing country of the document
      val icaoCode: String? = null, // The International Civil Aviation Organization code for the issuing country.
      val type: String? = null, // Enum: ['P', 'I', 'D', 'C'], Passport, ID card, Drivers license, C?
      val isElectronic: Int? = null, // Based on the chip page, will indicate if the document is electronic. Enum: [0, 1, 2] Description:  • 0: not electronic  • 1: Electronic  • 2: Unknown
      val chipPage: Int? = null, // Determines the presence and location of an RFID chip in a document. Enum: [0, 1, 2, 3] Description:  0: no chip; 1: chip is located in the document data page; 2: chip is located in the back page or inlay of the document; 3: Unknown
    ): Parcelable
    ```
    ```kotlin
    /**
      * Data priority: chip > MRZ > VIZ
    */
    data class DataSection(
      val mrzString: String? = null, // Combined raw MRZ data string.
      val docType: String? = null, // Combined document type (e.g., “P” for passport). Data priority: chip > MRZ > VIZ Enum: ['P', 'PC', 'I', 'D', 'C', 'OTHER']
      val surname: String? = null, // Combined passport holder’s surname.
      val name: String? = null, // Combined passport holder’s given names.
      val docNumber: String? = null, // Combined passport document number.
      val checkDigit: String? = null, // Combined check digit for the document number.
      val nationality: String? = null, // Combined nationality ISO code.
      val birthDate: String? = null, // Combined date of birth in YY-MM-DD format.
      val birthDateDigit: String? = null, // Combined check digit for the birth date.
      val sex: String? = null, // Combined gender of the passport holder. Enum: ['M', 'F', 'X']
      val expiryDate: String? = null, // Combined passport expiry date in YY-MM-DD format.
      val expiryDateDigit: String? = null, // Combined check digit for the expiry date.
      val optionalData: String? = null, // Combined additional optional data (e.g., personal identification number).
      val optionalDataDigit: String? = null, // Combined check digit for the optional data.
      val mrzType: String? = "unknown", // Combined format of the MRZ (e.g., “ID-3”). Enum: ['ID-1', 'ID-2', 'ID-3']
      val docImagePath: String = PhotoPath.DOCUMENT_IMAGE_PATH,
      val holderImagePath: String = PhotoPath.PORTRAIT_PHOTO_PATH,
    ): Parcelable
    ```
    ```kotlin
    data class VIZSection(
      val docType: String? = null, // Document type in the VIZ. Enum: ['PC', 'ID', 'C', 'OTHER']
      val issueState: String? = null, // Issuing country code.
      val surname: String? = null, // Passport/ID card holder’s surname as shown in the VIZ.
      val name: String? = null, // Passport/ID card holder’s given names as shown in the VIZ.
      val sex: String? = null, // Gender of the passport holder. Enum: ['M', 'F', 'X'] Nullable: true
      val docNumber: String? = null, // Passport/ID card document number.
      val nationality: String? = null, // Nationality in native language.
      val issueDate: String? = null, //Date when the passport/ID card was issued.
      val personalNumber: String? = null, // Personal identification number.
      val height: String? = null, // Height of the passport/ID card holder.
      val expiryDate: String? = null, // Expiry date of the passport/ID card.
      val docImagePath: String = PhotoPath.DOCUMENT_IMAGE_PATH,
      val holderImagePath: String = PhotoPath.PORTRAIT_PHOTO_PATH,
      val validations: VIZValidation = VIZValidation(), // Validation status indicating if the document is expired
    ): Parcelable
    ```
    ```kotlin
    data class MRZSection(
      val mrzString: String? = null, // Raw MRZ data string.
      val docType: String? = null, // Document type from MRZ. Enum: ['P', 'I', 'A', 'V', 'C', 'OTHER']
      val surname: String? = null, // Passport/ID card holder’s surname from MRZ.
      val name: String? = null, // Passport/ID card holder’s given names from MRZ.
      val docNumber: String? = null, // Passport/ID card document number from MRZ.
      val checkDigit: String? = null, // Check digit for the document number from MRZ.
      val nationality: String? = null, // Nationality code from MRZ.
      val birthDate: String? = null, // Date of birth from MRZ in YY-MM-DD format.
      val birthDateDigit: String? = null, // Check digit for the birth date from MRZ.
      val sex: String? = null, // Gender from MRZ. Enum: ['M', 'F', 'X']
      val expiryDate: String? = null, // Expiry date from MRZ in YY-MM-DD format.
      val expiryDateDigit: String? = null, // Check digit for the expiry date from MRZ.
      val optionalData: String? = null, // Optional data from MRZ.
      val optionalDataDigit: String? = null, // Check digit for the optional data from MRZ.
      val mrzType: String? = null, // Format of the MRZ. Enum: ['ID-1', 'ID-2', 'ID-3']
      val validations: MRZValidation = MRZValidation(),
    ): Parcelable
    ```
    ```kotlin
    data class RFIDSection(
      val mrzString: String? = null, // Raw MRZ data string from RFID chip.
      val docType: String? = null, // Document type from RFID chip. Enum: ['P', 'I', 'V', 'C']
      val surname: String? = null, // Passport/ID card holder’s surname from RFID chip.
      val name: String? = null, // Passport/ID card holder’s given names from RFID chip.
      val docNumber: String? = null, // Passport/ID card document number from RFID chip.
      val checkDigit: String? = null, // Check digit for the document number from RFID chip.
      val nationality: String? = null, // Nationality code from RFID chip.
      val birthDate: String? = null, // Date of birth from RFID chip in YY-MM-DD format.
      val birthDateDigit: String? = null, // Check digit for the birth date from RFID chip.
      val sex: String? = null, // Gender from RFID chip. Enum: ['M', 'F', 'X']
      val expiryDate: String? = null, // Expiry date from RFID chip in YY-MM-DD format.
      val expiryDateDigit: String? = null, // Check digit for the expiry date from RFID chip.
      val optionalData: String? = null, // Optional data from RFID chip.
      val optionalDataDigit: String? = null, // Check digit for the optional data from RFID chip.
      val mrzType: String? = null, // Format of the MRZ from RFID chip. Enum: ['ID-1', 'ID-2', 'ID-3']
      val holderImagePath: String = PhotoPath.PORTRAIT_PHOTO_PATH,
      val validations: RFIDValidation = RFIDValidation(),
    ): Parcelable
    ```

    The validations on each class contains information about the field status:

    ```kotlin
    data class VIZValidation(
      val expired: Int = 2, // Enum: [0, 1, 2] Description: • 0: Failed • 1: Success • 2: Unknown
    ): Parcelable
    
    data class MRZValidation(
      val checkDigit: Int = 2, // Enum: [0, 1, 2] Description: • 0: Failed • 1: Success • 2: Unknown
      val format: Int = 2, // Enum: [0, 1, 2] Description: • 0: Failed • 1: Success • 2: Unknown
      val expired: Int = 2, // Enum: [0, 1, 2] Description: • 0: Failed • 1: Success • 2: Unknown
    ): Parcelable
    
    data class RFIDValidation(
      val checkDigit: Int = 2, // Enum: [0, 1, 2] Description: • 0: Failed • 1: Success • 2: Unknown
      val expired: Int = 2, // Enum: [0, 1, 2] Description: • 0: Failed • 1: Success • 2: Unknown
    ): Parcelable
    
    /**
      * Enum: [0, 1, 2]  0: Failed  • 1: Success  • 2: Unknown
      * Data sources(exception on mrzType):
      * - When chip read: chip + MRZ
      * - When chip not read: MRZ + VIZ
      * - When only MRZ: MRZ
    */
    data class Validations(
      val status: Int = 2, // Overall validation/comparison status of the document.
      val chip: Int = 2, // Overall validation of the chip read operation.
      val docType: Int = 2, // Overall validation/comparison status of document type.
      val surname: Int = 2, // Overall validation/comparison status of surname.
      val name: Int = 2, // Overall validation/comparison status of name.
      val docNumber: Int = 2, // Overall validation/comparison status of document number.
      val checkDigit: Int = 2, // Overall validation/comparison status of check digit.
      val nationality: Int = 2, // Overall validation/comparison status of nationality.
      val birthDate: Int = 2, // Overall validation/comparison status of birth date.
      val birthDateDigit: Int = 2, // Overall validation/comparison status of birth date check digit.
      val sex: Int = 2, // Overall validation/comparison status of sex.
      val expiryDate: Int = 2, // Overall validation/comparison status of expiry date.
      val expiryDateDigit: Int = 2, // Overall validation/comparison status of expiry date check digit.
      val optionalData: Int = 2, // Overall validation/comparison status of optional data.
      val optionalDataDigit: Int = 2, // Overall validation/comparison status of optional data check digit.
      val mrzType: Int = 2, // Overall validation/comparison status of MRZ type. When chip read: chip + MRZ  • When only MRZ: MRZ
      val checkDigitCalculation: Int = 2, // Overall check digit calculation validation/comparison.
      val expired: Int = 2, // Overall expiry validation/comparison indicating if the document is expired.
      val aa: Int = 2, // Active Authentication status.
      val bac: Int = 2, // Basic Access Control status.
      val ca: Int = 2, // Chip Authentication status.
      val pa: Int = 2, // Passive Authentication status.
      val pace: Int = 2, // Password Authenticated Connection Establishment status.
      val ta: Int = 2, // Terminal Authentication status.
    ): Parcelable
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
    
        /// Chip page
        public var chipPage: Int?
        
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
        /// Document  id
        public let documentId: Int
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
        case passiveAuthDisabled
    }
    ```

    The `chipPage` indicates the presence and location of an RFID chip. 0 - No RFID chip. 1 - Chip is located in the document data page. 2 - Chip is located in the back page or inlay of the document.
    
## DocumentReaderCustomViews
The SDK provides default UI solutions for the document reader feature flow, as
shown in the following images:
![Document Reader Flow](Assets/DR_Flow.png "Document Reader Flow"){: style="display: block; margin: 0 auto"}

The use of the rfid related layouts depends on the **rfidRead** flag in the DocumentReaderParameters.

You can also apply your app’s colors and fonts to these layout solutions, to keep your brand’s image consistent.
Check Customization tab to learn more about branding of each view.

=== "Android"

    ```kotlin
    class DocumentReaderCustomViews(
        val loadingView: Class<out ICustomDocumentReader.LoadingView>? = null,
        val rfidInstructionsView: Class<out ICustomDocumentReader.RfidInstructionsView>? = null,
        val rfidSearchView: Class<out ICustomDocumentReader.RfidSearchView>? = null,
        val rfidProcessView: Class<out ICustomDocumentReader.RfidProcessView>? = null,
    )
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
