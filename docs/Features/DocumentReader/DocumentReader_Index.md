# Overview

The document reader is used to extract the user’s document information and perform all necessary
security validations. This functionality works in two steps: the MRZ of the travel document is
scanned (using the device's camera) and then, if it is an electronic document (i.e. with a chip),
and the client app indicated that it wants to read the chip, the user is prompted to place the
mobile device over the travel e-Document in order to perform a RFID scan to extract available data.

## Configure

=== "Android"

    To use this feature, you must instantiate the provider that you desire to use and pass it to the Enrolment initialization. Below is an example of how to initialize the Enrolment with the Amadeus DocScanMrz provider.

    ```kotlin
    DocScanMrz.initialize(
        context = <Context>,
        docScanMrzConfig = <DocScanMrzConfig>
    )

    val documentReaderProvider = DocScanMrz.getInstance()

    Enrolment.initialize(
        ...
        documentReaderProvider = documentReaderProvider,
        ...
    )
    ```

=== "iOS"

    Since version 9, the Document Reader is built on a **provider model**. Instead of a single,
    fixed configuration, you pick the provider(s) you want to use and pass them to the
    Enrolment initialization. Each provider has its own setup and is supplied through the
    `documentScanProvider` (OCR/MRZ) and `documentRFIDProvider` (RFID/NFC) parameters of
    `Enrolment.shared.initWith(...)`.

    The available providers are:

    - **Amadeus DocScanMrz** (`AMADocScanMrziOS`) — OCR/MRZ document scanning.
    - **Amadeus Doc RFID Read** (`AMADocRfid`) — RFID/NFC chip reading.

    Any scan provider can be used as long as it conforms to `DocumentReaderScanProtocol`, and any RFID
    provider as long as it conforms to `DocumentReaderRFIDProtocol`. You can combine providers (for
    example, scan with DocScanMrz and read RFID with Amadeus Doc RFID Read).

    ``` swift
    Enrolment.shared.initWith(
        enrolmentConfig: enrolmentConfig,
        documentScanProvider: documentScanProvider,   // any DocumentReaderScanProtocol
        documentRFIDProvider: documentRFIDProvider,    // any DocumentReaderRFIDProtocol, or nil
        ultralightProvider: nil,
        viewRegister: nil,
        completionHandler: completionHandler
    )
    ```

    Each provider has its own import steps, configuration and instantiation. See the
    [Custom Providers](DocumentReader_Providers.md) page for the per-provider details on how to import
    and build each one.
    
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
     * @param mode [DocumentReaderMode] selects which scan flow to run (SCAN, RFID, or DTC).
     * @param onReadDocumentCompletion [OnReadDocumentCompletion] callback to handle Success and Error scenarios
     */
    fun readDocument(
        activity: Activity,
        params: DocumentReaderParameters,
        mode: DocumentReaderMode,
        onReadDocumentCompletion: OnReadDocumentCompletion,
    )
    ```

    The `DocumentReaderMode` enum selects which scan flow is executed:

    ```kotlin
    enum class DocumentReaderMode {
        SCAN, // OCR/MRZ scan via camera, optionally followed by RFID if enabled in DocumentReaderParameters
        RFID, // RFID-only scan; requires MRZ data to be supplied via DocumentReaderRFIDParameters
        DTC,  // Digital Travel Credential read flow
    }
    ```

=== "iOS"

    ``` swift
    /// Starts document scan process.
    /// - Parameters:
    ///   - parameters: Parameteres for the Read Document flow.
    ///   - viewController: View controller that will present the document scan views.
    ///   - completionHandler: The completion handler to call when the document reader feature is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<DocumentReaderReport, FeatureError>
    ///     Where `DocumentReaderReport` contains  the results of the document reader
    ///     operation and `FeatureError` the possible errors that may occur during the process.
    ///     throws a
    final public func readDocument(parameters: MobileIdSDKiOS.ReadDocumentParameters, viewController: UIViewController, completionHandler: @escaping (Result<MobileIdSDKiOS.DocumentReaderReport, MobileIdSDKiOS.DocumentReaderError>) -> Void)
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
	/// Parameters for the Read Document flow.
	public struct ReadDocumentParameters {
	
	    /// Whether or not to read Document's RFID (using NFC).
	    public let readRFID: Bool
	
	    /// Property indicating if icon indicating RFID reading status should be visible or not. Default value is `false`.
	    public let showRFIDStatus: Bool
	
	    /// Document scan timeout, in seconds. Default value is `30` seconds. Minimum value is `10` seconds. Maximum value is `60` seconds.
	    public let scannerTimeout: TimeInterval
	
	    /// Document rfid timeout, in seconds.  Default value is `30` seconds. Minimum value is `10` seconds. Maximum value is `60` seconds.
	    public let rfidTimeout: TimeInterval
	
	    /// If true, it will display a RFID Instructions Screen, else will automatically starts in the RFID Scan
	    public let showRFIDInstructions: Bool
	
	    public init(readRFID: Bool, showRFIDStatus: Bool = false, scannerTimeout: TimeInterval = 30, rfidTimeout: TimeInterval = 30, showRFIDInstructions: Bool = true)
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
    public struct ReadRFIDDocumentParameters {
        public let documentNumber: String
        public let documentMRZ: String
        public let dateOfExpiry: Date
        public let dateOfBirth: Date
        public let showRFIDStatus: Bool
        public let rfidTimeout: TimeInterval
        public let showRFIDInstructions: Bool

        public init(documentNumber: String,
                documentMRZ: String,
                dateOfExpiry: Date,
                dateOfBirth: Date,
                showRFIDStatus: Bool = false,
                rfidTimeout: TimeInterval = 30
        ) 
    }
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
    // The view controller responsible for presenting the document scanner camera interface
    var viewController: UIViewController!
    
    let parameters: MobileIdSDKiOS.ReadDocumentParameters = .init(readRFID: false,
                                                                  showRFIDStatus: false, // Optional
                                                                  scannerTimeout: 30, // Optional
                                                                  showRFIDInstructions: false) // Optional
    Enrolment.shared.readDocument(
       parameters: parameters,
        viewController: viewController
    ) { result in
        switch result {
        case let .success(documentReaderReport):
            // handle DocumentReaderReport
            print(documentReaderReport)
        case let .failure(error):
            if error.userCanceled {
                   print("onUserCancel")
               } else {
                   print(error.featureError.publicMessage)
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
      val idDocument: IdDocument,
      val status: List<DocumentDataStatus>,
      val rfidStatus: RFIDStatus,
      val documentType: DocumentType,
      val documentPhotoHash: String, // Portrait Image
      val idDocumentHash: String, // IdDocument object
    ) : Parcelable
    ```
    
=== "iOS"

    ```swift
	/// Holds the report of the document reader process.
	public struct DocumentReaderReport: Codable {   
	    /// New identification document data.
	    public let idDocument: IdDocument
	    /// Type of document, ex: Passport, Visa, etc.
	    public let documentType: DocumentType
	    /// Identification document RFID Status
	    public let documentRFIDStatus: DocumentRFIDStatus
	    /// Possible document data status.
	    public let documentStatuses: [DocumentDataStatus]
	    /// Portrait Image Hash
	    public let documentPhotoHash: String?
	    /// idDocument object Hash
	    public let idDocumentHash: String?
    }
    ```

The `DocumentReaderReport` includes hash fields that are used to verify data integrity when building a [Subject](../SubjectManagement/SubjectManagement_Index.md).

The `IdDocument` class contains all document information with different sources depending on the document type.

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
        val type: InfoTypeEnum? = null, // Document type (e.g., "P" for passport)
        val isElectronic: ValidationElectronicChip? = null, // Specifies if the document is electronic
        val chipPage: ValidationChipPage? = ValidationChipPage.UNKNOWN, // Status of the chip read operation
    ): Parcelable
    ```
    ```kotlin
    /**
      * Data priority: chip > MRZ > VIZ
    */
    data class DataSection(
        val mrzString: String? = null, // Combined raw MRZ data string.
        val docType: DocTypeEnum? = null, // Combined document type (e.g., “P” for passport). Data priority: chip > MRZ > VIZ
        val surname: String? = null, // Combined passport holder’s surname.
        val name: String? = null, // Combined passport holder’s given names.
        val docNumber: String? = null, // Combined passport document number.
        val checkDigit: String? = null, // Combined check digit for the document number.
        val nationality: String? = null, // Combined nationality ISO code.
        val birthDate: String? = null, // Combined date of birth in YY-MM-DD format.
        val birthDateDigit: String? = null, // Combined check digit for the birthdate.
        val sex: ValidationSex? = null, // Combined gender of the passport holder.
        val validFrom: String? = null, // Combined validFrom or issuedDate date in YY-MM-DD format. Data priority: chip > VIZ. Nullable: true
        val expiryDate: String? = null, // Combined passport expiry date in YY-MM-DD format.
        val expiryDateDigit: String? = null, // Combined check digit for the expiry date.
        val optionalData: String? = null, // Combined additional optional data (e.g., personal identification number).
        val optionalDataDigit: String? = null, // Combined check digit for the optional data.
        val mrzType: ValidationMrzType? = ValidationMrzType.UNKNOWN, // Combined format of the MRZ (e.g., “ID-3”).
        private val docImageByteArray: ByteArray? = null,
        private val holderImageByteArray: ByteArray? = null,
    ): Parcelable {
        val docImage get() = docImageByteArray?.toBitmap()
        val holderImage get() = holderImageByteArray?.toBitmap()
    } 
    ```
    ```kotlin
    data class VIZSection(
        val docType: VizDocTypeEnum? = null, // Document type in the VIZ.
        val issueState: String? = null, // Issuing country code.
        val surname: String? = null, // Passport/ID cardholder’s surname as shown in the VIZ.
        val name: String? = null, // Passport/ID cardholder’s given names as shown in the VIZ.
        val sex: ValidationSex? = null, // Gender of the passport holder.
        val docNumber: String? = null, // Passport/ID card document number.
        val nationality: String? = null, // Nationality in native language.
        val validFrom: String? = null, // Combined validFrom or issuedDate date in YY-MM-DD format. Data priority: chip > VIZ. Nullable: true
        val issueDate: String? = null, //Date when the passport/ID card was issued.
        val personalNumber: String? = null, // Personal identification number.
        val height: String? = null, // Height of the passport/ID cardholder.
        val expiryDate: String? = null, // Expiry date of the passport/ID card.
        private val docImageByteArray: ByteArray? = null,
        private val holderImageByteArray: ByteArray? = null,
        val validations: VIZValidation = VIZValidation(), // Validation status indicating if the document is expired
    ): Parcelable {
        val docImage get() = docImageByteArray?.toBitmap()
        val holderImage get() = holderImageByteArray?.toBitmap()
    }
    ```
    ```kotlin
    data class MRZSection(
        val mrzString: String? = null, // Raw MRZ data string.
        val docType: MrzDocTypeEnum? = null, // Document type from MRZ.
        val surname: String? = null, // Passport/ID cardholder’s surname from MRZ.
        val name: String? = null, // Passport/ID cardholder’s given names from MRZ.
        val docNumber: String? = null, // Passport/ID card document number from MRZ.
        val checkDigit: String? = null, // Check digit for the document number from MRZ.
        val nationality: String? = null, // Nationality code from MRZ.
        val birthDate: String? = null, // Date of birth from MRZ in YY-MM-DD format.
        val birthDateDigit: String? = null, // Check digit for the birthdate from MRZ.
        val sex: ValidationSex? = null, // Gender from MRZ.
        val expiryDate: String? = null, // Expiry date from MRZ in YY-MM-DD format.
        val expiryDateDigit: String? = null, // Check digit for the expiry date from MRZ.
        val optionalData: String? = null, // Optional data from MRZ.
        val optionalDataDigit: String? = null, // Check digit for the optional data from MRZ.
        val mrzType: ValidationMrzType? = ValidationMrzType.UNKNOWN, // Format of the MRZ.
        val validations: MRZValidation = MRZValidation(),
    ): Parcelable
    ```
    ```kotlin
    data class RFIDSection(
        val mrzString: String? = null, // Raw MRZ data string from RFID chip.
        val docType: DocTypeEnum? = null, // Document type from RFID chip.
        val surname: String? = null, // Passport/ID cardholder’s surname from RFID chip.
        val name: String? = null, // Passport/ID cardholder’s given names from RFID chip.
        val docNumber: String? = null, // Passport/ID card document number from RFID chip.
        val checkDigit: String? = null, // Check digit for the document number from RFID chip.
        val nationality: String? = null, // Nationality code from RFID chip.
        val birthDate: String? = null, // Date of birth from RFID chip in YY-MM-DD format.
        val birthDateDigit: String? = null, // Check digit for the birthdate from RFID chip.
        val validFrom: String? = null, // Combined validFrom or issuedDate date in YY-MM-DD format. Data priority: chip > VIZ. Nullable: true
        val sex: ValidationSex? = null, // Gender from RFID chip.
        val expiryDate: String? = null, // Expiry date from RFID chip in YY-MM-DD format.
        val expiryDateDigit: String? = null, // Check digit for the expiry date from RFID chip.
        val optionalData: String? = null, // Optional data from RFID chip.
        val optionalDataDigit: String? = null, // Check digit for the optional data from RFID chip.
        val mrzType: ValidationMrzType? = ValidationMrzType.UNKNOWN, // Format of the MRZ from RFID chip.
        private val holderImageByteArray: ByteArray? = null,
        val validations: RFIDValidation = RFIDValidation(),
    ): Parcelable {
        val holderImage get() = holderImageByteArray?.toBitmap()
    }
    ```

    The validations on each class contains information about the field status:

    ```kotlin
    data class VIZValidation(
        val expired: ValidationCheck? = ValidationCheck.UNKNOWN, // Validation check for expiration
    ): Parcelable
    
    data class MRZValidation(
        val checkDigit: ValidationCheck? = ValidationCheck.UNKNOWN, // Check digit validation status
        val format: ValidationCheck? = ValidationCheck.UNKNOWN, // Format validation status
        val expired: ValidationCheck? = ValidationCheck.UNKNOWN, // Expiry validation status
    ): Parcelable
    
    data class RFIDValidation(
        val checkDigit: ValidationCheck? = ValidationCheck.UNKNOWN, // Check digit validation status
        val expired: ValidationCheck? = ValidationCheck.UNKNOWN, // Expiry validation status
    ): Parcelable
    
    /**
      * Enum: [0, 1, 2]  0: Failed  • 1: Success  • 2: Unknown
      * Data sources(exception on mrzType):
      * - When chip read: chip + MRZ
      * - When chip not read: MRZ + VIZ
      * - When only MRZ: MRZ
    */
    data class Validations(
        val status: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of the document.
        val chip: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation of the chip read operation.
        val docType: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of document type.
        val surname: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of surname.
        val name: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of name.
        val docNumber: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of document number.
        val checkDigit: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of check digit.
        val nationality: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of nationality.
        val birthDate: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of birth date.
        val birthDateDigit: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of birth date check digit.
        val sex: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of sex.
        val expiryDate: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of expiry date.
        val expiryDateDigit: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of expiry date check digit.
        val optionalData: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of optional data.
        val optionalDataDigit: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of optional data check digit.
        val mrzType: ValidationCheck = ValidationCheck.UNKNOWN, // Overall validation/comparison status of MRZ type.
        val checkDigitCalculation: ValidationCheck = ValidationCheck.UNKNOWN, // Overall check digit calculation validation/comparison.
        val expired: ValidationCheck = ValidationCheck.UNKNOWN, // Overall expiry validation/comparison indicating if the document is expired.
        val AA: ValidationCheck = ValidationCheck.UNKNOWN, // Active Authentication status.
        val BAC: ValidationCheck = ValidationCheck.UNKNOWN, // Basic Access Control status.
        val CA: ValidationCheck = ValidationCheck.UNKNOWN, // Chip Authentication status.
        val PA: ValidationCheck = ValidationCheck.UNKNOWN, // Passive Authentication status.
        val PACE: ValidationCheck = ValidationCheck.UNKNOWN, // Password Authenticated Connection Establishment status.
        val TA: ValidationCheck = ValidationCheck.UNKNOWN, // Terminal Authentication status.
    ): Parcelable
    ```
    
=== "iOS"

    #### IdDocument

    ```swift
	public final class IdDocument: Codable, Sendable, Equatable {
	    // MARK: - Nested Types
	
	    public enum ValidationChipPage: Int, Codable, Sendable {
	        /// No chip present
	        case noChip = 0
	        /// Chip is located in the document data page
	        case chipOnDataPage = 1
	        /// Chip is located in the back page or inlay of the document
	        case chipOnBackPage = 2
	        /// Unknown chip location
	        case unknown = 3
	    }
	
	    public enum ValidationElectronicChip: Int, Codable, Sendable {
	        /// Document is not electronic
	        case notElectronic = 0
	        /// Document is electronic
	        case electronic = 1
	        /// Unknown if document is electronic
	        case unknown = 2
	    }
	
	    // MARK: - Properties
	
	    public let info: InfoSection?
	    public let data: DataSection?
	    public let viz: VIZSection?
	    public let mrz: MRZSection?
	    public let rfid: RFIDSection?
	    public let validations: Validations?
	
	    // MARK: - Initialization
	
	    public init(
	        info: InfoSection? = nil,
	        data: DataSection? = nil,
	        viz: VIZSection? = nil,
	        mrz: MRZSection? = nil,
	        rfid: RFIDSection? = nil,
	        validations: Validations? = nil
	    ) {
	        self.info = info
	        self.data = data
	        self.viz = viz
	        self.mrz = mrz
	        self.rfid = rfid
	        self.validations = validations
	    }
	
	    public static func == (lhs: IdDocument, rhs: IdDocument) -> Bool {
	        lhs.info == rhs.info &&
	            lhs.data == rhs.data &&
	            lhs.viz == rhs.viz &&
	            lhs.mrz == rhs.mrz &&
	            lhs.rfid == rhs.rfid &&
	            lhs.validations == rhs.validations
	    }
	}
    ```
    
    #### InfoSection

    ```swift
    public enum InfoTypeEnum: String, Codable, Sendable {
	    /// Passport
	    case passport = "P"
	    /// ID card
	    case idCard = "I"
	    /// Driver's license
	    case driverLicense = "D"
	    /// Document C (Visa's)
	    case documentC = "C"
	}

	public final class InfoSection: Codable, Sendable, Equatable {
	    // MARK: - Properties
	
	    /// A unique identifier for the document.
	    public let id: Int?
	
	    /// Indicates the type and issuing country of the document
	    public let documentName: String?
	
	    /// The International Civil Aviation Organization code for the issuing country.
	    public let ICAOCode: String?
	
	    /// Document type (e.g., "P" for passport)
	    public let type: InfoTypeEnum?
	
	    /// Specifies if the document is electronic
	    public let isElectronic: IdDocument.ValidationElectronicChip?
	
	    /// Status of the chip read operation
	    public let chipPage: IdDocument.ValidationChipPage?
	
	    // MARK: - Initialization
	
	    public init(
	        id: Int? = nil,
	        documentName: String? = nil,
	        ICAOCode: String? = nil,
	        type: InfoTypeEnum? = nil,
	        isElectronic: IdDocument.ValidationElectronicChip? = nil,
	        chipPage: IdDocument.ValidationChipPage? = .unknown
	    ) {
	        self.id = id
	        self.documentName = documentName
	        self.ICAOCode = ICAOCode
	        self.type = type
	        self.isElectronic = isElectronic
	        self.chipPage = chipPage
	    }
	
	    public static func == (lhs: InfoSection, rhs: InfoSection) -> Bool {
	        lhs.id == rhs.id &&
	            lhs.documentName == rhs.documentName &&
	            lhs.ICAOCode == rhs.ICAOCode &&
	            lhs.type == rhs.type &&
	            lhs.isElectronic == rhs.isElectronic &&
	            lhs.chipPage == rhs.chipPage
	    }
	}
    ```

	#### DataSection
	
    ```swift
	public enum DocTypeEnum: String, Codable, Sendable {
	    /// Passport
	    case passport = "P"
	    /// Document PC
	    case documentPC = "PC"
	    /// ID card
	    case idCard = "I"
	    /// Driver's license
	    case driverLicense = "D"
	    /// Document C
	    case documentC = "C"
	    /// Other document type
	    case other = "OTHER"
	}
	
	public final class DataSection: Codable, Sendable, Equatable {
	    // MARK: - Properties
	
	    /// Combined raw MRZ data string. Data priority: chip > MRZ
	    public let mrzString: String?
	
	    /// Combined document type (e.g., "P" for passport). Data priority: chip > MRZ > VIZ
	    public let docType: DocTypeEnum?
	
	    /// Combined passport holder's surname. Data priority: chip > MRZ > VIZ
	    public let surname: String?
	
	    /// Combined passport holder's given names. Data priority: chip > MRZ > VIZ
	    public let name: String?
	
	    /// Combined passport document number. Data priority: chip > MRZ > VIZ
	    public let docNumber: String?
	
	    /// Combined check digit for the document number. Data priority: chip > MRZ > VIZ
	    public let checkDigit: String?
	
	    /// Combined nationality ISO code. Data priority: chip > MRZ > VIZ
	    public let nationality: String?
	
	    /// Combined date of birth in YY-MM-DD format. Data priority: chip > MRZ > VIZ
	    public let birthDate: String?
	
	    /// Combined check digit for the birth date. Data priority: chip > MRZ > VIZ
	    public let birthDateDigit: String?
	
	    /// Combined gender of the passport holder. Data priority: chip > MRZ > VIZ
	    public let sex: ValidationSex?
	    
	    /// Combined validFrom or issuedDate date in YY-MM-DD format. Data priority: chip > VIZ. Nullable: true
	    public let validFrom: String?
	
	    /// Combined passport expiry date in YY-MM-DD format. Data priority: chip > MRZ > VIZ
	    public let expiryDate: String?
	
	    /// Combined check digit for the expiry date. Data priority: chip > MRZ > VIZ
	    public let expiryDateDigit: String?
	
	    /// Combined additional optional data (e.g., personal identification number). Data priority: chip > MRZ > VIZ
	    public let optionalData: String?
	
	    /// Combined check digit for the optional data. Data priority: chip > MRZ > VIZ
	    public let optionalDataDigit: String?
	
	    /// Combined format of the MRZ (e.g., "ID-3"). Data priority: chip > MRZ > VIZ
	    public let mrzType: ValidatiomMrzType?
	
	    /// Base64-encoded string of the passport/ID card holder's photo. Data priority: chip > MRZ > VIZ
	    public let holderImage: Data?
	
	    /// Base64-encoded string of the passport/id card photo
	    public let docImage: Data?
	
	    // MARK: - Computed Properties
	
	    public var holderImageUIImage: UIImage? {
	        holderImage.flatMap { UIImage(data: $0) }
	    }
	
	    public var docImageUIImage: UIImage? {
	        docImage.flatMap { UIImage(data: $0) }
	    }
	
	    // MARK: - Initialization
	
	    public init(
	        mrzString: String? = nil,
	        docType: DocTypeEnum? = nil,
	        surname: String? = nil,
	        name: String? = nil,
	        docNumber: String?,
	        checkDigit: String? = nil,
	        nationality: String? = nil,
	        birthDate: String?,
	        birthDateDigit: String? = nil,
	        sex: ValidationSex? = nil,
	        validFrom: String? = nil,
	        expiryDate: String? = nil,
	        expiryDateDigit: String? = nil,
	        optionalData: String? = nil,
	        optionalDataDigit: String? = nil,
	        mrzType: ValidatiomMrzType? = .unknown,
	        holderImage: UIImage? = nil,
	        docImage: UIImage? = nil,
	        holderImageData: Data? = nil,
	        docImageData: Data? = nil
	    ) {
	        self.mrzString = mrzString
	        self.docType = docType
	        self.surname = surname
	        self.name = name
	        self.docNumber = docNumber
	        self.checkDigit = checkDigit
	        self.nationality = nationality
	        self.birthDate = birthDate
	        self.birthDateDigit = birthDateDigit
	        self.sex = sex
	        self.validFrom = validFrom
	        self.expiryDate = expiryDate
	        self.expiryDateDigit = expiryDateDigit
	        self.optionalData = optionalData
	        self.optionalDataDigit = optionalDataDigit
	        self.mrzType = mrzType
	        self.holderImage = holderImageData ?? holderImage?.pngData()
	        self.docImage = docImageData ?? docImage?.pngData()
	    }
	
	    public static func == (lhs: DataSection, rhs: DataSection) -> Bool {
	        lhs.mrzString == rhs.mrzString &&
	            lhs.docType == rhs.docType &&
	            lhs.surname == rhs.surname &&
	            lhs.name == rhs.name &&
	            lhs.docNumber == rhs.docNumber &&
	            lhs.checkDigit == rhs.checkDigit &&
	            lhs.nationality == rhs.nationality &&
	            lhs.birthDate == rhs.birthDate &&
	            lhs.birthDateDigit == rhs.birthDateDigit &&
	            lhs.sex == rhs.sex &&
	            lhs.validFrom == rhs.validFrom &&
	            lhs.expiryDate == rhs.expiryDate &&
	            lhs.expiryDateDigit == rhs.expiryDateDigit &&
	            lhs.optionalData == rhs.optionalData &&
	            lhs.optionalDataDigit == rhs.optionalDataDigit &&
	            lhs.mrzType == rhs.mrzType &&
	            lhs.holderImage == rhs.holderImage &&
	            lhs.docImage == rhs.docImage
	    }
	}
    ```
    
    #### VIZSection
    
    ```swift
	public final class VIZSection: Codable, Sendable, Equatable {
	    // MARK: - Nested Types
	
	    public enum VizDocTypeEnum: String, Codable, Sendable {
	        /// Document PC
	        case documentPC = "PC"
	        /// ID card
	        case idCard = "ID"
	        /// Document C
	        case documentC = "C"
	        /// Other document type
	        case other = "OTHER"
	    }
	
	    // MARK: - Properties
	
	    /// Document type in the VIZ
	    public let docType: VizDocTypeEnum?
	
	    /// Issuing country code
	    public let issueState: String?
	
	    /// Passport/ID card holder's surname as shown in the VIZ
	    public let surname: String?
	
	    /// Passport/ID card holder's given names as shown in the VIZ
	    public let name: String?
	
	    /// Gender of the passport holder
	    public let sex: ValidationSex?
	
	    /// Passport/ID card document number
	    public let docNumber: String?
	
	    /// Nationality in native language
	    public let nationality: String?
	
	    /// Date when the passport/ID card was issued
	    public let issueDate: String?
	
	    /// Combined validFrom or issuedDate date in YY-MM-DD format. Data priority: chip > VIZ. Nullable: true
	    public let validFrom: String?
	    
	    /// Personal identification number
	    public let personalNumber: String?
	
	    /// Height of the passport/ID card holder
	    public let height: String?
	
	    /// Expiry date of the passport/ID card
	    public let expiryDate: String?
	
	    /// VIZ validations
	    public let validations: VIZValidation?
	
	    /// Base64-encoded string of the passport/ID card holder's photo in the VIZ
	    public let holderImage: Data?
	
	    /// VIZ base64-encoded string of the passport/id card photo
	    public let docImage: Data?
	
	    // MARK: - Computed Properties
	
	    public var holderImageUIImage: UIImage? {
	        holderImage.flatMap { UIImage(data: $0) }
	    }
	
	    public var docImageUIImage: UIImage? {
	        docImage.flatMap { UIImage(data: $0) }
	    }
	
	    // MARK: - Initialization
	
	    public init(
	        docType: VizDocTypeEnum? = nil,
	        issueState: String? = nil,
	        surname: String? = nil,
	        name: String? = nil,
	        sex: ValidationSex? = nil,
	        docNumber: String?,
	        nationality: String? = nil,
	        issueDate: String? = nil,
	        validFrom: String? = nil,
	        personalNumber: String? = nil,
	        height: String? = nil,
	        expiryDate: String?,
	        holderImage: UIImage? = nil,
	        docImage: UIImage? = nil,
	        holderImageData: Data? = nil,
	        docImageData: Data? = nil,
	        validations: VIZValidation? = VIZValidation()
	    ) {
	        self.docType = docType
	        self.issueState = issueState
	        self.surname = surname
	        self.name = name
	        self.sex = sex
	        self.docNumber = docNumber
	        self.nationality = nationality
	        self.issueDate = issueDate
	        self.validFrom = validFrom
	        self.personalNumber = personalNumber
	        self.height = height
	        self.expiryDate = expiryDate
	        self.validations = validations
	        self.holderImage = holderImageData ?? holderImage?.pngData()
	        self.docImage = docImageData ?? docImage?.pngData()
	    }
	
	    public static func == (lhs: VIZSection, rhs: VIZSection) -> Bool {
	        lhs.docType == rhs.docType &&
	            lhs.issueState == rhs.issueState &&
	            lhs.surname == rhs.surname &&
	            lhs.name == rhs.name &&
	            lhs.sex == rhs.sex &&
	            lhs.docNumber == rhs.docNumber &&
	            lhs.nationality == rhs.nationality &&
	            lhs.issueDate == rhs.issueDate &&
	            lhs.validFrom == rhs.validFrom &&
	            lhs.personalNumber == rhs.personalNumber &&
	            lhs.height == rhs.height &&
	            lhs.expiryDate == rhs.expiryDate &&
	            lhs.validations == rhs.validations &&
	            lhs.holderImage == rhs.holderImage &&
	            lhs.docImage == rhs.docImage
	    }
	}
	

    ```
    
    #### MRZSection
    
    ```swift
	public final class MRZSection: Codable, Sendable, Equatable {
	    // MARK: - Nested Types
	
	    public enum MrzDocTypeEnum: String, Codable, Sendable {
	        /// Passport
	        case passport = "P"
	        /// ID card
	        case idCard = "I"
	        /// Document A
	        case documentA = "A"
	        /// Visa
	        case visa = "V"
	        /// Document C
	        case documentC = "C"
	        /// Other document type
	        case other = "OTHER"
	    }
	
	    // MARK: - Properties
	
	    /// Raw MRZ data string
	    public let mrzString: String?
	
	    /// Document type from MRZ
	    public let docType: MrzDocTypeEnum?
	
	    /// Passport/ID card holder's surname from MRZ
	    public let surname: String?
	
	    /// Passport/ID card holder's given names from MRZ
	    public let name: String?
	
	    /// Passport/ID card document number from MRZ
	    public let docNumber: String?
	
	    /// Check digit for the document number from MRZ
	    public let checkDigit: String?
	
	    /// Nationality code from MRZ
	    public let nationality: String?
	
	    /// Date of birth from MRZ in YY-MM-DD format
	    public let birthDate: String?
	
	    /// Check digit for the birth date from MRZ
	    public let birthDateDigit: String?
	
	    /// Gender from MRZ
	    public let sex: ValidationSex?
	
	    /// Expiry date from MRZ in YY-MM-DD format
	    public let expiryDate: String?
	
	    /// Check digit for the expiry date from MRZ
	    public let expiryDateDigit: String?
	
	    /// Optional data from MRZ
	    public let optionalData: String?
	
	    /// Check digit for the optional data from MRZ
	    public let optionalDataDigit: String?
	
	    /// Format of the MRZ
	    public let mrzType: ValidatiomMrzType?
	
	    /// MRZ validations
	    public let validations: MRZValidation?
	
	    // MARK: - Initialization
	
	    public init(
	        mrzString: String? = nil,
	        docType: MrzDocTypeEnum? = nil,
	        surname: String? = nil,
	        name: String? = nil,
	        docNumber: String?,
	        checkDigit: String? = nil,
	        nationality: String? = nil,
	        birthDate: String?,
	        birthDateDigit: String? = nil,
	        sex: ValidationSex? = nil,
	        expiryDate: String?,
	        expiryDateDigit: String? = nil,
	        optionalData: String? = nil,
	        optionalDataDigit: String? = nil,
	        mrzType: ValidatiomMrzType? = .unknown,
	        validations: MRZValidation? = MRZValidation()
	    ) {
	        self.mrzString = mrzString
	        self.docType = docType
	        self.surname = surname
	        self.name = name
	        self.docNumber = docNumber
	        self.checkDigit = checkDigit
	        self.nationality = nationality
	        self.birthDate = birthDate
	        self.birthDateDigit = birthDateDigit
	        self.sex = sex
	        self.expiryDate = expiryDate
	        self.expiryDateDigit = expiryDateDigit
	        self.optionalData = optionalData
	        self.optionalDataDigit = optionalDataDigit
	        self.mrzType = mrzType
	        self.validations = validations
	    }
	
	    public static func == (lhs: MRZSection, rhs: MRZSection) -> Bool {
	        lhs.mrzString == rhs.mrzString &&
	            lhs.docType == rhs.docType &&
	            lhs.surname == rhs.surname &&
	            lhs.name == rhs.name &&
	            lhs.docNumber == rhs.docNumber &&
	            lhs.checkDigit == rhs.checkDigit &&
	            lhs.nationality == rhs.nationality &&
	            lhs.birthDate == rhs.birthDate &&
	            lhs.birthDateDigit == rhs.birthDateDigit &&
	            lhs.sex == rhs.sex &&
	            lhs.expiryDate == rhs.expiryDate &&
	            lhs.expiryDateDigit == rhs.expiryDateDigit &&
	            lhs.optionalData == rhs.optionalData &&
	            lhs.optionalDataDigit == rhs.optionalDataDigit &&
	            lhs.mrzType == rhs.mrzType &&
	            lhs.validations == rhs.validations
	    }
	}
	
	// MARK: - MRZValidation
	
	public final class MRZValidation: Codable, Sendable, Equatable {
	    /// Check digit validation status
	    public let checkDigit: ValidationCheck?
	
	    /// Format validation status
	    public let format: ValidationCheck?
	
	    /// Expiry validation status
	    public let expired: ValidationCheck?
	
	    public init(
	        checkDigit: ValidationCheck? = .unknown,
	        format: ValidationCheck? = .unknown,
	        expired: ValidationCheck? = .unknown
	    ) {
	        self.checkDigit = checkDigit
	        self.format = format
	        self.expired = expired
	    }
	
	    public static func == (lhs: MRZValidation, rhs: MRZValidation) -> Bool {
	        lhs.checkDigit == rhs.checkDigit &&
	            lhs.format == rhs.format &&
	            lhs.expired == rhs.expired
	    }
	}
    ```
    
    #### RRIDSection
    
    ```swift
	public final class RFIDSection: Codable, Sendable, Equatable {
	    // MARK: - Nested Types
	
	    public enum RfidDocTypeEnum: String, Codable, Sendable {
	        /// Passport
	        case passport = "P"
	        /// ID card
	        case idCard = "I"
	        /// Visa
	        case visa = "V"
	        /// Document C
	        case documentC = "C"
	        /// Other document type
	        case other = "OTHER"
	    }
	
	    // MARK: - Properties
	
	    /// Raw MRZ data string from RFID chip
	    public let mrzString: String?
	
	    /// Document type from RFID chip
	    public let docType: RfidDocTypeEnum?
	
	    /// Passport/ID card holder's surname from RFID chip
	    public let surname: String?
	
	    /// Passport/ID card holder's given names from RFID chip
	    public let name: String?
	
	    /// Passport/ID card document number from RFID chip
	    public let docNumber: String?
	
	    /// Check digit for the document number from RFID chip
	    public let checkDigit: String?
	
	    /// Nationality code from RFID chip
	    public let nationality: String?
	
	    /// Date of birth from RFID chip in YY-MM-DD format
	    public let birthDate: String?
	
	    /// Check digit for the birth date from RFID chip
	    public let birthDateDigit: String?
	
	    /// Gender from RFID chip
	    public let sex: ValidationSex?
	    
	    /// Combined validFrom or issuedDate date in YY-MM-DD format. Data priority: chip > VIZ. Nullable: true
	    public let validFrom: String?
	
	    /// Expiry date from RFID chip in YY-MM-DD format
	    public let expiryDate: String?
	
	    /// Check digit for the expiry date from RFID chip
	    public let expiryDateDigit: String?
	
	    /// Optional data from RFID chip
	    public let optionalData: String?
	
	    /// Check digit for the optional data from RFID chip
	    public let optionalDataDigit: String?
	
	    /// Format of the MRZ from RFID chip
	    public let mrzType: ValidatiomMrzType?
	
	    /// Base64-encoded string of the passport/ID card holder's photo from RFID chip
	    public let holderImage: Data?
	
	    /// RFID validations
	    public let validations: RFIDValidation?
	
	    // MARK: - Computed Properties
	
	    public var holderImageUIImage: UIImage? {
	        holderImage.flatMap { UIImage(data: $0) }
	    }
	
	    // MARK: - Initialization
	
	    public init(
	        mrzString: String? = nil,
	        docType: RfidDocTypeEnum? = nil,
	        surname: String? = nil,
	        name: String? = nil,
	        docNumber: String?,
	        checkDigit: String? = nil,
	        nationality: String? = nil,
	        birthDate: String?,
	        birthDateDigit: String? = nil,
	        sex: ValidationSex? = nil,
	        validFrom: String? = nil,
	        expiryDate: String? = nil,
	        expiryDateDigit: String? = nil,
	        optionalData: String? = nil,
	        optionalDataDigit: String? = nil,
	        mrzType: ValidatiomMrzType? = .unknown,
	        holderImage: UIImage? = nil,
	        holderImageData: Data? = nil,
	        validations: RFIDValidation? = RFIDValidation()
	    ) {
	        self.mrzString = mrzString
	        self.docType = docType
	        self.surname = surname
	        self.name = name
	        self.docNumber = docNumber
	        self.checkDigit = checkDigit
	        self.nationality = nationality
	        self.birthDate = birthDate
	        self.birthDateDigit = birthDateDigit
	        self.sex = sex
	        self.validFrom = validFrom
	        self.expiryDate = expiryDate
	        self.expiryDateDigit = expiryDateDigit
	        self.optionalData = optionalData
	        self.optionalDataDigit = optionalDataDigit
	        self.mrzType = mrzType
	        self.validations = validations
	        self.holderImage = holderImageData ?? holderImage?.pngData()
	    }
	
	    public static func == (lhs: RFIDSection, rhs: RFIDSection) -> Bool {
	        lhs.mrzString == rhs.mrzString &&
	            lhs.docType == rhs.docType &&
	            lhs.surname == rhs.surname &&
	            lhs.name == rhs.name &&
	            lhs.docNumber == rhs.docNumber &&
	            lhs.checkDigit == rhs.checkDigit &&
	            lhs.nationality == rhs.nationality &&
	            lhs.birthDate == rhs.birthDate &&
	            lhs.birthDateDigit == rhs.birthDateDigit &&
	            lhs.sex == rhs.sex &&
	            lhs.validFrom == rhs.validFrom &&
	            lhs.expiryDate == rhs.expiryDate &&
	            lhs.expiryDateDigit == rhs.expiryDateDigit &&
	            lhs.optionalData == rhs.optionalData &&
	            lhs.optionalDataDigit == rhs.optionalDataDigit &&
	            lhs.mrzType == rhs.mrzType &&
	            lhs.validations == rhs.validations &&
	            lhs.holderImage == rhs.holderImage
	    }
	}
	
	// MARK: - RFIDValidation
	
	public final class RFIDValidation: Codable, Sendable, Equatable {
	    /// Check digit validation status
	    public let checkDigit: ValidationCheck?
	
	    /// Expiry validation status
	    public let expired: ValidationCheck?
	
	    public init(
	        checkDigit: ValidationCheck? = .unknown,
	        expired: ValidationCheck? = .unknown
	    ) {
	        self.checkDigit = checkDigit
	        self.expired = expired
	    }
	
	    public static func == (lhs: RFIDValidation, rhs: RFIDValidation) -> Bool {
	        lhs.checkDigit == rhs.checkDigit &&
	            lhs.expired == rhs.expired
	    }
	}
	
	// MARK: - Validations
	
	public final class Validations: Codable, Sendable, Equatable {
	    /// Overall validation/comparison status of the document
	    public let status: ValidationCheck?
	
	    /// Overall validation of the chip read operation
	    public let chip: ValidationCheck?
	
	    /// Overall validation/comparison status of document type
	    public let docType: ValidationCheck?
	
	    /// Overall validation/comparison status of surname
	    public let surname: ValidationCheck?
	
	    /// Overall validation/comparison status of name
	    public let name: ValidationCheck?
	
	    /// Overall validation/comparison status of document number
	    public let docNumber: ValidationCheck?
	
	    /// Overall validation/comparison status of check digit
	    public let checkDigit: ValidationCheck?
	
	    /// Overall validation/comparison status of nationality
	    public let nationality: ValidationCheck?
	
	    /// Overall validation/comparison status of birth date
	    public let birthDate: ValidationCheck?
	
	    /// Overall validation/comparison status of birth date check digit
	    public let birthDateDigit: ValidationCheck?
	
	    /// Overall validation/comparison status of sex
	    public let sex: ValidationCheck?
	
	    /// Overall validation/comparison status of expiry date
	    public let expiryDate: ValidationCheck?
	
	    /// Overall validation/comparison status of expiry date check digit
	    public let expiryDateDigit: ValidationCheck?
	
	    /// Overall validation/comparison status of optional data
	    public let optionalData: ValidationCheck?
	
	    /// Overall validation/comparison status of optional data check digit
	    public let optionalDataDigit: ValidationCheck?
	
	    /// Overall validation/comparison status of MRZ type
	    public let mrzType: ValidationCheck?
	
	    /// Overall check digit calculation validation/comparison
	    public let checkDigitCalculation: ValidationCheck?
	
	    /// Overall expiry validation/comparison indicating if the document is expired
	    public let expired: ValidationCheck?
	
	    /// Active Authentication status
	    public let AA: ValidationCheck?
	
	    /// Basic Access Control status
	    public let BAC: ValidationCheck?
	
	    /// Chip Authentication status
	    public let CA: ValidationCheck?
	
	    /// Passive Authentication status
	    public let PA: ValidationCheck?
	
	    /// Password Authenticated Connection Establishment status
	    public let PACE: ValidationCheck?
	
	    /// Terminal Authentication status
	    public let TA: ValidationCheck?
	
	    public init(
	        status: ValidationCheck? = .unknown,
	        chip: ValidationCheck? = .unknown,
	        docType: ValidationCheck? = .unknown,
	        surname: ValidationCheck? = .unknown,
	        name: ValidationCheck? = .unknown,
	        docNumber: ValidationCheck? = .unknown,
	        checkDigit: ValidationCheck? = .unknown,
	        nationality: ValidationCheck? = .unknown,
	        birthDate: ValidationCheck? = .unknown,
	        birthDateDigit: ValidationCheck? = .unknown,
	        sex: ValidationCheck? = .unknown,
	        expiryDate: ValidationCheck? = .unknown,
	        expiryDateDigit: ValidationCheck? = .unknown,
	        optionalData: ValidationCheck? = .unknown,
	        optionalDataDigit: ValidationCheck? = .unknown,
	        mrzType: ValidationCheck? = .unknown,
	        checkDigitCalculation: ValidationCheck? = .unknown,
	        expired: ValidationCheck? = .unknown,
	        AA: ValidationCheck? = .unknown,
	        BAC: ValidationCheck? = .unknown,
	        CA: ValidationCheck? = .unknown,
	        PA: ValidationCheck? = .unknown,
	        PACE: ValidationCheck? = .unknown,
	        TA: ValidationCheck? = .unknown
	    ) {
	        self.status = status
	        self.chip = chip
	        self.docType = docType
	        self.surname = surname
	        self.name = name
	        self.docNumber = docNumber
	        self.checkDigit = checkDigit
	        self.nationality = nationality
	        self.birthDate = birthDate
	        self.birthDateDigit = birthDateDigit
	        self.sex = sex
	        self.expiryDate = expiryDate
	        self.expiryDateDigit = expiryDateDigit
	        self.optionalData = optionalData
	        self.optionalDataDigit = optionalDataDigit
	        self.mrzType = mrzType
	        self.checkDigitCalculation = checkDigitCalculation
	        self.expired = expired
	        self.AA = AA
	        self.BAC = BAC
	        self.CA = CA
	        self.PA = PA
	        self.PACE = PACE
	        self.TA = TA
	    }
	
	    public static func == (lhs: Validations, rhs: Validations) -> Bool {
	        lhs.status == rhs.status &&
	            lhs.chip == rhs.chip &&
	            lhs.docType == rhs.docType &&
	            lhs.surname == rhs.surname &&
	            lhs.name == rhs.name &&
	            lhs.docNumber == rhs.docNumber &&
	            lhs.checkDigit == rhs.checkDigit &&
	            lhs.nationality == rhs.nationality &&
	            lhs.birthDate == rhs.birthDate &&
	            lhs.birthDateDigit == rhs.birthDateDigit &&
	            lhs.sex == rhs.sex &&
	            lhs.expiryDate == rhs.expiryDate &&
	            lhs.expiryDateDigit == rhs.expiryDateDigit &&
	            lhs.optionalData == rhs.optionalData &&
	            lhs.optionalDataDigit == rhs.optionalDataDigit &&
	            lhs.mrzType == rhs.mrzType &&
	            lhs.checkDigitCalculation == rhs.checkDigitCalculation &&
	            lhs.expired == rhs.expired &&
	            lhs.AA == rhs.AA &&
	            lhs.BAC == rhs.BAC &&
	            lhs.CA == rhs.CA &&
	            lhs.PA == rhs.PA &&
	            lhs.PACE == rhs.PACE &&
	            lhs.TA == rhs.TA
	    }
	}
    ```
    
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
