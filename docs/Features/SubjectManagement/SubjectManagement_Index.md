# Subject Manager

A subject consists of a set of data that represents a digital ID in the enrolment process. The
Mobile ID SDK provides a set of operations that allows you to manage the subjects on a server-side
platform, such as adding, updating, deleting, or building a subject, or reading its data.

## Use Subject Manager

You can manage subjects using the subject management functions available in the enrolment facade.
Subjects are the result of the enrolment process and need to be successfully created in the
server-side platform, to complete any process requiring a digital form of identification. The subject will always be null
when returned from the facade's method subject builder. This field will only be filled by our
backend services, depending on if the subject is fully authenticated or not. If the user is not
fully authenticated, the subject token will be filled only on when the app fetches the subject on
the facade's get subject method. If the subject token is not null, it will contain a base 64 QR code
that the user must present on the physical gate for a full authentication.

=== "Android"

    ```kotlin
    data class Subject(
        val id: String,
        val language: String,
        val document: Document,
        val biometrics: List<Biometric>,
        val validationStatus: ValidationStatus,
        val subjectToken: SubjectToken?,
        var boardingPass: BoardingPass? = null
    )
    ```
    
=== "iOS"

    ``` swift
    public struct Subject {
        public let id: String
        public let document: Document
        public let biometrics: [Biometric]?
        public var boardingPass: BoardingPass?
        public var validationStatus: ValidationStatus
        public var subjectToken: SubjectToken?
        public var language: Locale
    }
    ```

The biometrics is a list of biometric data. This biometric data contains its type and a base64 of
the image and you can get the image bitmap by calling the method getBiometricImage(). Here is the
structure of the Biometric data:

=== "Android"

    ```kotlin
    data class Biometric(
        val source: BiometricSource,
        val data: String
    )
    ```
    
=== "iOS"

    ``` swift
    public struct Biometric {
        public let source: BiometricSource
        public let data: Data
        public let photo: UIImage?
    }
    ```
    
The BiometricSource is a enum with the source of the biometric photo and will have the following structure:

=== "Android"

    ```kotlin
    enum class BiometricSource {
        DOCUMENT,
        CAPTURED,
        ENROLLMENT
    }
    ```
    
=== "iOS"

    ``` swift
    public enum BiometricSource: String {
        case document = "DOCUMENT"
        case captured = "CAPTURED"
        case enrollment = "ENROLLMENT"
    }
    ```
    
The SubjectToken will have the following structure:

=== "Android"

    The SubjectToken will also provide a method to return the QR code as a bitmap. For this you just
    need to call the method getQRCodeImage().
    
    ```kotlin
    data class SubjectToken(
        val qrCodeBase64: String
    )
    ```
  
=== "iOS"

    ``` swift
    public struct SubjectToken {
        public var qrCodeBase64: String
        public var qrCodeImage: UIImage?
    }
    ```
    
The ValidationStatus will have the following structure:   

=== "Android"

    ```kotlin
    data class ValidationStatus(
        val documentAuthenticated: Boolean,
        val livenessCheckPassed: Boolean,
        val biometryMatched: Boolean
    )
    ```
  
=== "iOS"

    ``` swift 
    public struct ValidationStatus {
        /// Field indicating if the Enrolment photos matched.
        public var biometryMatched: Bool
        /// Field indicating if the liveness check test was performed with success.
        public var livenessCheckPassed: Bool
        /// Field indicating if the RFID scan of the document was performed with success.
        public var documentAuthenticated: Bool
    }
    ```

The Document and BoardingPass classes can be consulted in the respective feature.

You can create a new subject using the addSubject method.
Subject data can be automatically submitted to the server-side platform after a successful document
reading and face matching operation, as shown in the following example:

=== "Android"

    This method is now deprecated and will be removed in the future
    ```kotlin
    override fun addSubject(context: Context, params: AddSubjectParameters) {
        enrolment.addSubject(context, subject)
    }
    ```
    The new method contains a new parameter that's responsible to receive the result of this feature
    ```kotlin
    override fun addSubject(activity: Activity, params: AddSubjectParameters) {
        // More info on the addSubjectResultLauncher in the how to get the result section
        enrolment.addSubject(context, subject, addSubjectResultLauncher)
    }
    ```
    
=== "iOS"

    ``` swift 
    /// Saves a Subect to server.
    /// - Parameters:
    ///   - parameters: Parameteres for the Add Subject flow.
    ///   - viewController: View controller base from when to present required SDK view controllers.
    ///   - completionHandler: The completion handler to call when the add subject operation is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<Void, SubjectError>
    ///     Where `SubjectError` contains the possible errors that may occur during the process.
    func addSubject(parameters: AddSubjectParameters, viewController: UIViewController, completionHandler: @escaping (Result<Void, SubjectError>) -> Void)
    ```
    
If you just need to build a subject, you must have the documentData object. The documentData must be
filled by the client app, or it can be acquired from the DocumentReaderReport when scanning with the
SDK scan document feature. The documentPhoto can also be acquired from the document data when using
the scan document feature. The enrolmentPhoto and the processReport can be acquired from the face
capture feature, same as the boardingPass object can be acquired from the boarding pass scan
feature. The matchReport is a result of using the facade's face match feature. The language field
is, by default, the locale in use on the device, but it can be changed by client apps. With this
data you can create the BuildSubjectParameters object. This object has the following structure:

=== "Android"

    ```kotlin
    data class BuildSubjectParameters(
        val documentData: DocumentData,
        val documentPhoto: Bitmap,
        val enrolmentPhoto: Bitmap,
        val boardingPass: BoardingPass? = null,
        val processReport: ProcessReport? = null,
        val matchReport: MatchReport? = null,
        val documentReaderReport: DocumentReaderReport? = null,
        val language: Locale = Locale.getDefault(),
    )
    ```
    
=== "iOS"

    ``` swift 
    public struct BuildSubjectParameters {
        public let showErrors: Bool
        public let documentData: DocumentData
        public let documentDataValidated: Bool
        public let documentImage: UIImage
        public let enrolmentImage: UIImage        
        public let boardingPass: BoardingPass?
        public let language: Locale
        
        public init(documentData: DocumentData,
                documentImage: UIImage,
                enrolmentImage: UIImage,
                boardingPass: BoardingPass?,
                documentReaderReport: DocumentReaderReport? = nil,
                biometricFaceCaptureReport: BiometricFaceCaptureReport? = nil,
                matchReport: MatchReport? = nil,
                language: Locale? = nil,
                showErrors: Bool)
    }
    ```
    
The following example shows how you can build a subject:

=== "Android"

    ```kotlin
    launch {
        val params = BuildSubjectParameters(
            documentData = documentData,
            documentPhoto = documentPhoto,
            enrolmentPhoto = enrolmentPhoto,
            boardingPass = boardingPass,
            processReport = processReport,
            matchReport = matchReport,
            documentReaderReport = documentReaderReport
        )
        val result = enrolment.buildSubject(params)
    }
    ```
    Because the Subject model might become a big object it may cause the parcelable too large exception. For this reason, it’s not parcelable. If you need to transform the Subject model in a parcelable object, you can use the helper method “toSubjectParcelable()” and after using it on a Bundle, you should reconvert it to a Subject using the method “toSubject()”.
     
=== "iOS"

    ```swift
    let parameters = BuildSubjectParameters(
        documentData: documentData,
        documentImage: documentImage,
        enrolmentImage: enrolmentImage,
        boardingPass: EnrolmentData.shared.boardingPass,
        documentReaderReport: EnrolmentData.shared.documentReaderReport,
        biometricFaceCaptureReport: EnrolmentData.shared.biometricMatchReport,
        matchReport: EnrolmentData.shared.matchReport,
        language: Locale.current,
        showErrors: true
    )
    
    guard let vco = self.view as? UIViewController else {
        return
    }
        
    self.enrolment.buildSubject(
        parameters: parameters,
        viewController: vco) { [weak self] result in
        switch result {
        case .success(let subject):
            self?.addSubject(subject: subject)
        case .failure:
            self?.view?.onBuildSubjectError()
        }
    }
    ```
    
You can also update a previously created subject. All new data will override the previously stored
information on that subject using the updateSubject method or delete a subject by calling the
deleteSubject method, using the subjectId to identify the subject you need to remove from the
platform. 
The SDK does not provide any UI solutions for subject representation. You should build
your own layouts and use the information that is relevant for your mobile solution.
BuildSubjectParameters by default, it is created with a language field equal to the device's default locale. This field allows the user to continue the enrollment in a kiosk with the correct language.

Those are all the subject methods: 

=== "Android"

    ```kotlin
    /**
    * Builds a [Subject] instance with the given [params].
    *
    * @param params [BuildSubjectParameters] that contains the necessary data to build the subject.
    * @return a [Result] with a [Subject] or [SubjectBuilderError].
    */
    fun buildSubject(
        activity: Activity,
        params: BuildSubjectParameters
    ): Result<Subject, SubjectBuilderError>

    /**
     * Gets a [Subject] for the given [subjectId].
     *
     * @param activity [Activity][android.app.Activity] that will handle the results via [onActivityResult][android.app.Activity.onActivityResult].
     * @param params get subject parameters
     */
    @Deprecated(
        "This method will be removed",
        replaceWith = ReplaceWith("getSubject(context, subjectId, resultLauncher)"),
        DeprecationLevel.WARNING
    )
    fun getSubject(activity: Activity, params: GetSubjectParameters)

    /**
     * Gets a [Subject] for the given [subjectId].
     *
     * @param context Context
     * @param params get subject parameters
     * @param resultLauncher [ActivityResultLauncher<Intent>] fragment or activity that will handle the results .
     */
    fun getSubject(
        context: Context,
        params: GetSubjectParameters,
        resultLauncher: ActivityResultLauncher<Intent>
    )

    /**
     * Adds a [Subject].
     *
     * @param activity [Activity][android.app.Activity] that will handle the results via [onActivityResult][android.app.Activity.onActivityResult].
     * @param params contains instance from [Subject] that will be added in the server.
     */
    @Deprecated(
        "This method will be removed",
        replaceWith = ReplaceWith("addSubject(context, subject, resultLauncher)"),
        DeprecationLevel.WARNING
    )
    fun addSubject(activity: Activity, params: AddSubjectParameters)

    /**
     * Adds a [Subject].
     *
     * @param context Context
     * @param params contains instance from [Subject] that will be added in the server.
     * @param resultLauncher [ActivityResultLauncher<Intent>] fragment or activity that will handle the results .
     */
    fun addSubject(
        context: Context,
        params: AddSubjectParameters,
        resultLauncher: ActivityResultLauncher<Intent>
    )

    /**
     * Updates a [Subject].
     *
     * @param activity [Activity][android.app.Activity] that will handle the results via [onActivityResult][android.app.Activity.onActivityResult].
     * @param params contains instance from [Subject] that will update the one in the server.
     */
    @Deprecated(
        "This method will be removed",
        replaceWith = ReplaceWith("updateSubject(context, subject, resultLauncher)"),
        DeprecationLevel.WARNING
    )
    fun updateSubject(activity: Activity, params: UpdateSubjectParameters)

    /**
     * Updates a [Subject].
     *
     * @param context Context
     * @param params contains instance from [Subject] that will update the one in the server.
     * @param resultLauncher [ActivityResultLauncher<Intent>] fragment or activity that will handle the results .
     */
    fun updateSubject(
        context: Context,
        params: UpdateSubjectParameters,
        resultLauncher: ActivityResultLauncher<Intent>
    )

    /**
     * Deletes the [Subject] with the given [subjectId].
     *
     * @param activity [Activity][android.app.Activity] that will handle the results via [onActivityResult][android.app.Activity.onActivityResult].
     * @param params contains id of the subject to delete.
     */
    @Deprecated(
        "This method will be removed",
        replaceWith = ReplaceWith("deleteSubject(context, subjectId, resultLauncher)"),
        DeprecationLevel.WARNING
    )
    fun deleteSubject(activity: Activity, params: DeleteSubjectParameters)

    /**
     * Deletes the [Subject] with the given [subjectId].
     *
     * @param context Context
     * @param params contains id of the subject to delete.
     * @param resultLauncher [ActivityResultLauncher<Intent>] fragment or activity that will handle the results .
     */
    fun deleteSubject(
        context: Context,
        params: DeleteSubjectParameters,
        resultLauncher: ActivityResultLauncher<Intent>
    )
    ```

=== "iOS"

    ```swift
    
    /// Build a Subject from document data. Can, optionally, receive a boarding pass.
    /// - Parameters:
    ///   - parameters: Parameters for the Building Subject flow.
    ///   - viewController: View controller base from when to present required SDK view controllers.
    ///   - completionHandler: The completion handler to call when the build subject operation is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<Subject, SubjectBuilderError>
    ///     Where `Subject` contains  the subject information and `SubjectBuilderError`
    ///     the possible errors that may occur during the process.
    func buildSubject(parameters: BuildSubjectParameters, viewController: UIViewController, completionHandler: @escaping (Result<Subject, SubjectBuilderError>) -> Void)
    
    /// Gets a Subject from server.
    /// - Parameters:
    ///   - parameters: Parameters for the Get Subject flow.
    ///   - viewController: View controller base from when to present required SDK view controllers.
    ///   - completionHandler: The completion handler to call when the get subject operation is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<Subject, SubjectBuilderError>
    ///     Where `Subject` contains  the subject information and `SubjectBuilderError`
    ///     the possible errors that may occur during the process.
    func getSubject(parameters: GetSubjectParameters, viewController: UIViewController, completionHandler: @escaping (Result<Subject, SubjectError>) -> Void)
    
    /// Saves a Subect to server.
    /// - Parameters:
    ///   - parameters: Parameteres for the Add Subject flow.
    ///   - viewController: View controller base from when to present required SDK view controllers.
    ///   - completionHandler: The completion handler to call when the add subject operation is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<Void, SubjectError>
    ///     Where `SubjectError` contains the possible errors that may occur during the process.
    func addSubject(parameters: AddSubjectParameters, viewController: UIViewController, completionHandler: @escaping (Result<Void, SubjectError>) -> Void)
    
    /// Updates a Subject in server.
    /// - Parameters:
    ///   - parameters: Parameteres for the Updates Subject flow.
    ///   - viewController: View controller base from when to present required SDK view controllers.
    ///   - completionHandler: The completion handler to call when the update subject operation is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<Void, SubjectError>
    ///     Where `SubjectError` contains the possible errors that may occur during the process.
    func updateSubject(parameters: UpdateSubjectParameters, viewController: UIViewController, completionHandler: @escaping (Result<Void, SubjectError>) -> Void)
    
    /// Deletes a subject from server.
    /// - Parameters:
    ///   - parameters: Parameteres for the Delete Subject flow.
    ///   - viewController: View controller base from when to present required SDK view controllers.
    ///   - completionHandler: The completion handler to call when the delete subject operation is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<Void, SubjectError>
    ///     Where `SubjectError` contains the possible errors that may occur during the process.
    func deleteSubject(parameters: DeleteSubjectParameters, viewController: UIViewController, completionHandler: @escaping (Result<Void, SubjectError>) -> Void)
    ```

The GetSubjectParameters will have the following structure:   

=== "Android"

    ```kotlin
    data class GetSubjectParameters(
        val showErrors: Boolean,
        val subjectId: String,
    )
    ```
  
=== "iOS"

    ``` swift 
    public struct GetSubjectParameters {
        public let id: Strin
        public let showErrors: Bool

        public init(id: String, showErrors: Bool)
    }
    ```
    
The AddSubjectParameters will have the following structure:   

=== "Android"

    ```kotlin
    data class AddSubjectParameters(
        val showErrors: Boolean,
        val subject: Subject,
    )
    ```
  
=== "iOS"

    ``` swift 
    public struct AddSubjectParameters {
        public let showErrors: Bool
        public let subject: Subject
    
        public init(subject: Subject, showErrors: Bool)
    }
    ```

The UpdateSubjectParameters will have the following structure:   

=== "Android"

    ```kotlin
    data class UpdateSubjectParameters(
        val showErrors: Boolean,
        val subject: Subject,
    )
    ```
  
=== "iOS"

    ``` swift 
    public struct UpdateSubjectParameters {
        public let showErrors: Bool
        public let subject: Subject

        public init(subject: Subject, showErrors: Bool)
    }
    ```

The DeleteSubjectParameters will have the following structure:   

=== "Android"

    ```kotlin
    data class DeleteSubjectParameters(
        val showErrors: Boolean,
        val subjectId: String,
    )
    ```
  
=== "iOS"

    ``` swift 
    public struct DeleteSubjectParameters {
        public let id: String
        public let showErrors: Bool

        public init(id: String, showErrors: Bool)
    }
    ```
    
## Handle Result

=== "Android"

    Here's how you can get the result by using the result launcher that's passed as the final parameter:
    ```kotlin
    private val addSubjectResultLauncher = registerForActivityResult(AddSubjectResultLauncher())
    { result: GetSubjectActivityResult ->
        when {
            result.success -> {
                val subject = result.subject?.toSubject(this)
                onSubjectReceived(subject)
            }
            else ->
                onSubjectDataError()
        }
    }

    private val deleteSubjectResultLauncher = registerForActivityResult(DeleteSubjectResultLauncher())
    { result: SubjectActivityResult ->
        when {
            result.success ->
                onSubjectDeleted(result.subjectId)
            else ->
                onSubjectDataError()
        }
    }

    private val getSubjectResultLauncher = registerForActivityResult(GetSubjectResultLauncher())
    { result: GetSubjectActivityResult ->
        when {
            result.success -> {
                val subject = result.subject?.toSubject(this)
                onSubjectReceived(subject)
            }
            else ->
                onSubjectDataError()
        }
    }

    private val updateSubjectResultLauncher = registerForActivityResult(UpdateSubjectResultLauncher())
    { result: GetSubjectActivityResult ->
        when {
            result.success -> {
                val subject = result.subject?.toSubject(this)
                onSubjectReceived(subject)
            }
            else ->
                onSubjectDataError()
        }
    }

    private val addSubjectBoardingSubjectResultLauncher = registerForActivityResult(SubjectAddDeleteBoardingPassResultLauncher())
    { result: GetSubjectActivityResult ->
        when {
            result.success -> {
                val subject = result.subject?.toSubject(this)
                onBoardingPassAdded(subject)
            }
            else ->
                onAddingBoardingPassDataError()
        }
    }
    ```
    
    Here is how you can get the report when using the deprecated method and handle the onActivityResult:

    ```kotlin
    private val getSubjectResultHandler by lazy { GetSubjectResultHandler() }
    private val deleteSubjectResultHandler by lazy { DeleteSubjectResultHandler() }
    private val addSubjectResultHandler by lazy { AddSubjectResultHandler() }
    private val updateSubjectResultHandler by lazy { UpdateSubjectResultHandler() }
    private val addSubjectBoardingPassResultHandler by lazy { SubjectAddDeleteBoardingPassResultHandler() }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when (requestCode) {
            EnrolmentSDKRequestCode.ADD_SUBJECT_REQUEST_CODE -> {
                val result = addSubjectResultHandler.parseResult(resultCode, data)
                when {
                    result.success -> {
                        val subject = result.subject?.toSubject(this)
                        onSubjectReceived(subject)
                    }
                    else ->
                        onSubjectDataError()
                }
            }

            EnrolmentSDKRequestCode.GET_SUBJECT_REQUEST_CODE -> {
                val result = getSubjectResultHandler.parseResult(resultCode, data)
                when {
                    result.success -> {
                        val subject = result.subject?.toSubject(this)
                        onSubjectReceived(subject)
                    }
                    else ->
                        onSubjectDataError()
                }
            }

            EnrolmentSDKRequestCode.UPDATE_SUBJECT_REQUEST_CODE -> {
                val result = updateSubjectResultHandler.parseResult(resultCode, data)
                when {
                    result.success -> {
                        val subject = result.subject?.toSubject(this)
                        onSubjectReceived(subject)
                    }
                    else ->
                        onSubjectDataError()
                }
            }

            EnrolmentSDKRequestCode.DELETE_SUBJECT_REQUEST_CODE -> {
                val result = deleteSubjectResultHandler.parseResult(resultCode, data)
                when {
                    result.success ->
                        onSubjectDeleted(result.subjectId)
                    else ->
                        onSubjectDataError()
                }
            }

            EnrolmentSDKRequestCode.ADD_BOARDING_PASS_REQUEST_CODE -> {
                val result = addSubjectBoardingPassResultHandler.parseResult(resultCode, data)
                when {
                    result.success -> {
                        val subject = result.subject?.toSubject(this)
                        onBoardingPassAdded(subject)
                    }
                    else ->
                        onAddingBoardingPassDataError()
                }
            }
        }
    }
    ```
    All subject operations will return a subject, except the "delete" operation that has a different result model. For the other operations you will receive the GetSubjectActivityResult model.

    ```kotlin
    data class GetSubjectActivityResult(
        val subject: SubjectParcelable? = null,
        val subjectError: SubjectError? = null) {
        val success get() = subject != null
    }
    ```
    
    The "delete" operation will return the SubjectActivityResult model.

    ```kotlin
    data class SubjectActivityResult(
        val success: Boolean = false,
        val subjectError: SubjectError? = null
    )
    ```
=== "iOS"

    ```swift
    self.enrolment.addSubject(
        parameters: AddSubjectParameters(subject: subject),
        viewController: vco) { [weak self] result in
            
        switch result {
        case .success:
            print("Add Subject: Success!")
        case .failure(let error):
            print("Add Subject: \(error.localizedDescription)")
        }
    }

    self.enrolment.getSubject(
        id: subjectId,
        viewController: vco) { [weak self] result in
            
        switch result {
        case .success(let subject):
            print("Get Subject: Success!")
            let subjectSummary = subject.toSubjectSummary()
        case .failure(let error):
            print("Get Subject: \(error.localizedDescription)")
            }
        }

    self.enrolment.updateSubject(
        subject,
        viewController: vco) { result in
            
        switch result {
        case .success:
            print("Update Subject: Success!")
        case .failure(let error):
            print("Update Subject: \(error.localizedDescription)")
        }
    }            

    self.enrolment.deleteSubject(
        id: subjectId,
        viewController: vco) { [weak self] result in
        
        switch result {
        case .success:
            print("Delete Subject: Success!")
        case .failure(let error):
            print("Delete Subject: \(error.localizedDescription)")
    }
    ```

The SubjectError has the following structure:

=== "Android"
    ```kotlin
    data class SubjectError(
        val userCanceled: Boolean,
        val termsAndConditionsAccepted: Boolean,
        val featureError: FeatureError?
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
    ```swift
    public enum SubjectError: Error {
        /// [SubjectError] that wraps a message error a controlled error occurs at a Subject service.
        case service(message: String)
        /// [SubjectError] that occurs when a [Subject] is not found by the Subject service.
        case notFound(error: EnrolmentServerError?)
        /// [SubjectError] that occurs when there's an error on the request.
        case client(error: EnrolmentServerError?)
        /// [SubjectError] that occurs when there's an error on the server.
        case server(error: EnrolmentServerError?)
        /// [SubjectError] that occurs when there's an unexpected error.
        case unexpected(message: String)
        /// [SubjectError] that occurs when there's an unreachable error.
        case unreachable(message: String)
        /// [SubjectError] that occurs when there's an error with the pinned certificate.
        case serverCertificatePinning(message: String)
        /// [SubjectError] that occurs when there's an error with pre/pos feature process.
        case feature(error: FeatureError)
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
## SubjectCustomViews
The SDK provides default UI solutions for the Subject Management feature flow, as 
shown in the following images:

![Subject Management Example](Assets/SubjectManagement_Flow.png "Subject Management Flow"){: style="height:600px;width:300px;display: block; margin: 0 auto"}

You can also apply your app’s colors and fonts to these layout solutions, to keep your brand’s image consistent. Check Customization tab to learn more about branding of each view.

=== "Android"

    ```kotlin
    @Parcelize
    class SubjectCustomViews(
        val loadingView: Class<out ICustomSubject.LoadingView>? = null
    ) : Parcelable
    ```
    You can use your own custom views in the subject functionality. Your view must implement the
    SDK view interfaces. For example, if you want to add a custom loading view, your view class must
    implement the ICustomSubject.LoadingView interface.
    
=== "iOS"

    ```swift
    public class EnrolmentViewRegister {
        ...

        // MARK: - Subject Operations
        public func registerSubjectLoadingOverlayView(_ viewType: SubjectLoadingOverlayViewType)
        ...
    }
    ```
    You can use your own custom views in the subject functionality. Your view must implement the
    SDK view protocols. For example, if you want to add a custom loading view, your view class must
    implement the ICustomSubject.LoadingView interface.

