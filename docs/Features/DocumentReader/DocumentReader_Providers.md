# Custom Providers

This page contains all available providers for the **Document Reader** feature, as well as instructions on how to import and implement them in a project using the SeamlessMobile SDK.

- [Regula Provider](#regula-provider)
- [Amadeus DocScanMrz Provider](#amadeus-docscanmrz-provider)
- [Amadeus Doc RFID Read Provider](#amadeus-doc-rfid-read-provider)

## Regula Provider

This provider uses Regula services and supports both OCR Document Reading and RFID scanning functionalities.

### How to Import: 

=== "Android"

    Work in progress...

=== "iOS"
    
	### Install using Xcode
	
	1.  Open your project in **Xcode**.
	
	2.  Navigate to **File ▸ Add Packages…**
	
	3.  In the dialog that appears, enter the package repository URL for the SDK you want to add:
	
	    **AMADocScanRegulaiOS**
	
	        https://github.com/vbmobile/AMADocScanRegulaiOS
	
	4.  Select the version to integrate. For new projects, we recommend using the latest available release (for example: **`2.0.2`**).
	
	5.  Choose the project and target to which the package should be added.
	
	6.  Click **Add Package**.
	
	Once completed, Xcode will download the package and resolve all required dependencies automatically.
	
	***
	
	### Install Using `Package.swift`
	
	If you manage dependencies manually, add the SDKs to your `Package.swift` file.
	
	#### 1. Add the dependency
	
	```swift
	dependencies: [
	    .package(
	        url: "https://github.com/vbmobile/AMADocScanRegulaiOS",
	        exact: "2.0.2"
	    )
	]
	```
	
	> Replace `2.0.2` with the intended version you wish to use.
	
	***
	
	#### 2. Link the product to your target
	
	```swift
	.target(
	    name: "YourAppTarget",
	    dependencies: [
	        .product(name: "AMADocScanRegulaiOS", package: "AMADocScanRegulaiOS")
	    ]
	)
	```
	
	> Replace `YourAppTarget` with the intended target you wish to use.

### How to Instantiate: 

=== "Android"

    Work in progress...
    
=== "iOS"
    
    Creates a `DocumentReaderScanProtocol` using `AMADocScanRegulaiOS ` provider
    
    ```swift
    func amaDocScanRegulaiOSProviderSetup() {
        var enrolmentConfig: EnrolmentConfig! // Not relevant for this example

        func amaDocScanRegulaiOS() -> DocumentReaderScanProtocol {
            guard
                let licensePath = Bundle.main.path(
                    forResource: "<YOUR_REGULA_LICENCE_FILE>",
                    ofType: "license"
                ),
                (try? Data(contentsOf: URL(fileURLWithPath: licensePath))) != nil
            else {
                fatalError("Unable to read Regula License")
            }
            let documentReaderConfig: mdi_mob_sdk_doc_mrz_regula_ios.DocumentReaderConfig = DocumentReaderConfig(
                multipageProcessing: false, // Single-page scanning
                databaseID: "<YOUR_DATA_BASE_ID>", // Database id
                scenario: .mrz // MRZ scanning scenario
            )
            return RegulaDocumentReaderScan(config: documentReaderConfig)
        }

        Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                                  documentScanProvider: amaDocScanRegulaiOS(),
                                  documentRFIDProvider: nil, // Not relevant for this example
                                  ultralightProvider: nil, // Not relevant for this example
                                  viewRegister: nil,
                                  completionHandler: { result in
                                      switch result {
                                      case .success:
                                          print("SDK is ready to use")

                                      case let .failure(error):
                                          print("Failure: \(error)")
                                      }
                                  })
    }
	```
    
    
### How to Use:

=== "Android"

    Work in progress...
    
=== "iOS"

	```swift
     func readDocumentSampleUsage() {
         // The view controller responsible for presenting the document scanner camera interface
         var viewController: UIViewController!
         
         Enrolment.shared.readDocument(
            parameters: .init(readRFID: false),
             viewController: viewController
         ) { result in
             switch result {
             case let .success(report):
                 print("Document Read: Success!")
                 print(report)
                 print(report.idDocument)
                 print(report.documentStatuses)
             case let .failure(error):
                 print(error.featureError.description)
             }
         }
     }
	```

    Once both providers are initialized, simply pass them as parameters to the Enrolment initialization as shown below. For more information on initializing, see [Enrolment](../../index.md#how-to-initialize-the-sdk).

    ``` swift
    var documentReaderConfig = DocumentReaderConfig(multipageProcessing: false, databaseID: "Passports", checkHologram: false)
    
    var regulaDocumentReaderScan = RegulaDocumentReaderScan(config: documentReaderConfig)
    var regulaDocumentReaderRFID = RegulaDocumentReaderRFID()
    
    Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                              documentScanProvider: regulaDocumentReaderScan,
                              documentRFIDProvider: regulaDocumentReaderRFID,
                              viewRegister: viewRegister,
                              completionHandler: completionHandler)
    
    ```
    
## Amadeus DocScanMrz Provider

This provider uses Amadeus services and supports MRZ Document Reading functionalities.

### How to Import: 

=== "Android"

    ```kotlin
    implementation("com.amadeus.mdi.mob.sdk:ama-doc-scan-mrz:<2.0.x>")
    ```

=== "iOS"

	### Install using Xcode
	
	1.  Open your project in **Xcode**.
	
	2.  Navigate to **File ▸ Add Packages…**
	
	3.  In the dialog that appears, enter the package repository URL for the SDK you want to add:
	
	    **AMADocScanMrziOS**
	
	        https://github.com/vbmobile/AMADocScanMrziOS
	
	4.  Select the version to integrate.  
	    For new projects, we recommend using the latest available release (for example: **`2.0.2`**).
	
	5.  Choose the project and target to which the package should be added.
	
	6.  Click **Add Package**.
	
	Once completed, Xcode will download the package and resolve all required dependencies automatically.
	
	***
	
	### Install Using `Package.swift`
	
	If you manage dependencies manually, add the SDKs to your `Package.swift` file.
	
	#### 1. Add the dependency
	
	```swift
	dependencies: [
	    .package(
	        url: "https://github.com/vbmobile/AMADocScanMrziOS",
	        exact: "2.0.2"
	    )
	]
	```
	
	> Replace `2.0.2` with the intended version you wish to use.
	
	***
	
	#### 2. Link the product to your target
	
	```swift
	.target(
	    name: "YourAppTarget",
	    dependencies: [
	        .product(name: "AMADocScanMrziOS", package: "AMADocScanMrziOS")
	    ]
	)
	```

	> Replace `YourAppTarget` with the intended target you wish to use.

### How to Instantiate: 


=== "Android"

    To initialize the Enrolment with the **DocScanMrz**. It can be done as follows.

    ```kotlin

    val docScanMrzConfig = DocScanMrzConfig(
        enableLogs = <true>,
        docScanMrzKey: <YOUR DOC SCAN MRZ KEY>,
    )

    DocScanMrz.initialize(
        context = this,
        docScanMrzConfig = docScanMrzConfig
    )

    val context = ...
    val enrolmentConfig = ...
    val callback = ...
    val documentReaderProvider = DocScanMrz.getInstance()

    // Soft-start the provider before passing it to Enrolment.
    documentReaderProvider.softStart(context, object : OnSoftStartCompletion {
        override fun onProgressChanged(progress: Progress) { /* not emitted by DocScanMrz */ }

        override fun onSoftStartSuccess() {
            Log.i("DocScanMrz", "softStart onSuccess")
        }

        override fun onSoftStartError(error: ProviderError) {
            Log.e("DocScanMrz", "softStart onError [${error.errorCode}] ${error.description}")
        }
    })

    Enrolment.initialize(
        context = context, 
        enrolmentConfig = enrolmentConfig,
        documentReaderProvider = documentReaderProvider,
        callback = callback
    )
    ```
    
=== "iOS"

    Creates a `DocumentReaderScanProtocol` using `AMADocScanMrziOS ` provider

	```swift
    func docScanMrziOSProviderSetup() {
        var enrolmentConfig: EnrolmentConfig! // Not relevant for this example

        func amaDocScanMrziOS() -> DocumentReaderScanProtocol {
            /// Specifies the expected document type (e.g. passport)
            let documentType: DSDocumentType = .td3

            /// Uses screen size to configure capture resolution
            let bounds = UIScreen.main.bounds

            /// Returns a PSS-based document scanner
            return DocumentReaderScan(
                documentType: documentType,
                apiKey: "<YOUR_KEY>",
                pixelWidth: Int(bounds.width),
                pixelHeight: Int(bounds.height)
            )
        }

        Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                                  documentScanProvider: amaDocScanMrziOS(),
                                  documentRFIDProvider: nil, // Not relevant for this example
                                  ultralightProvider: nil, // Not relevant for this example
                                  viewRegister: nil,
                                  completionHandler: { result in
                                      switch result {
                                      case .success:
                                          print("SDK is ready to use")

                                      case let .failure(error):
                                          print("Failure: \(error)")
                                      }
                                  })
    }
    ```

### How to Use:

=== "Android"

    ```kotlin
    Enrolment.getInstance().readDocument(
        activity = activity,
        params = DocumentReaderParameters(
            rfidRead = true,
            mrzReadTimeout = TimeUnit.SECONDS.toMillis(30),
            rfidReadTimeout = TimeUnit.SECONDS.toMillis(30),
            showRFIDInstructions = true,
        ),
        mode = DocumentReaderMode.SCAN,
        onReadDocumentCompletion = object : OnReadDocumentCompletion {
            override fun onReadDocumentSuccess(documentReaderReport: DocumentReaderReport) {

            }

            override fun onReadDocumentError(documentReaderError: DocumentReaderError) {

            }
        }
    )
    ```
    
=== "iOS"

	```swift
     // The view controller responsible for presenting the document scanner camera interface
     var viewController: UIViewController!
     
     Enrolment.shared.readDocument(
        parameters: .init(readRFID: false),
         viewController: viewController
     ) { result in
         switch result {
         case let .success(report):
             print("Document Read: Success!")
             print(report)
             print(report.idDocument)
             print(report.documentStatuses)
         case let .failure(error):
             print(error.featureError.description)
         }
     }
	```

## Amadeus Doc RFID Read Provider

This provider uses Amadeus services and supports RFID scanning functionalities.

### How to Import:

=== "Android"

    ```kotlin
    implementation("com.amadeus.mdi.mob.sdk:ama-doc-rfid-read:<2.0.x>")
    ```

=== "iOS"

	### Install using Xcode
	
	1.  Open your project in **Xcode**.
	
	2.  Navigate to **File ▸ Add Packages…**
	
	3.  In the dialog that appears, enter the package repository URL for the SDK you want to add:
	
	    **AMADocScanRegulaiOS**
	
	        https://github.com/vbmobile/AMADocRfid
	
	4.  Select the version to integrate. For new projects, we recommend using the latest available release (for example: **`2.0.1`**).
	
	5.  Choose the project and target to which the package should be added.
	
	6.  Click **Add Package**.
	
	Once completed, Xcode will download the package and resolve all required dependencies automatically.
	
	***
	
	### Install Using `Package.swift`
	
	If you manage dependencies manually, add the SDKs to your `Package.swift` file.
	
	#### 1. Add the dependency
	
	```swift
	dependencies: [
	    .package(
	        url: "https://github.com/vbmobile/AMADocRfid",
	        exact: "2.0.1"
	    )
	]
	```
	
	> Replace `2.0.1` with the intended version you wish to use.
	
	***
	
	#### 2. Link the product to your target
	
	```swift
	.target(
	    name: "YourAppTarget",
	    dependencies: [
	        .product(name: "AMADocRfid", package: "AMADocRfid")
	    ]
	)
	```
	
	> Replace `YourAppTarget` with the intended target you wish to use.

### How to Instantiate:

=== "Android"

    To initialize the Enrolment with the **DocRfidRead**. It can be done as follows.

    ```kotlin

    val docRfidReadConfig = DocRfidReadConfig(
            apiConfig = DocRfidReadApiConfig(
                baseUrl = <YOUR DOC RFID READ BASE URL>,
                apiKey = <YOUR DOC RFID READ API KEY>,
                publicKey = Base64.encodeToString("YOUR PUBLIC KEY", Base64.DEFAULT),
            ),
            enableLogs = <ENABLE LOGS>,
        )

    DocRfidRead.initialize(
        context = this,
        docRfidReadConfig = docRfidReadConfig
    )

    val context = ...
    val enrolmentConfig = ...
    val callback = ...
    val documentRfidReaderProvider = DocRfidRead.getInstance()

    // Soft-start the provider before passing it to Enrolment.
    documentRfidReaderProvider.softStart(context, object : OnSoftStartCompletion {
        override fun onProgressChanged(progress: Progress) { /* not emitted by DocRfidRead */ }

        override fun onSoftStartSuccess() {
            Log.i("DocRfidRead", "softStart onSuccess")
        }

        override fun onSoftStartError(error: ProviderError) {
            Log.w("DocRfidRead", "softStart onError [${error.errorCode}] ${error.description}")
        }
    })

    Enrolment.initialize(
        context = context, 
        enrolmentConfig = enrolmentConfig,
        rfidReaderProvider = documentRfidReaderProvider,
        callback = callback
    )
    ```

=== "iOS"

    
    ```swift
	 import AMADocModeliOS
	 import AMADocRFIDReadiOS
	 import MobileIdSDKiOS

    func docScanRfidProviderSetup() {
        var enrolmentConfig: EnrolmentConfig! // Not relevant for this example
        func documentRFIDProvider() -> DocumentReaderRFIDProtocol {
            let apiConfig = APIConfig(
                baseURL: "<YOUR_BASE_URL>",
                apiKey: "<YOUR_API_KEY>",
                publicKey: "")
            return  AMADocRFIDRead( config: DocRfidReadConfig( apiConfig: apiConfig, enableLogs: true))
        }

        Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                                  documentScanProvider: nil, // Not relevant for this example
                                  documentRFIDProvider: documentRFIDProvider(),
                                  ultralightProvider: nil, // Not relevant for this example
                                  viewRegister: nil,
                                  completionHandler: { result in
                                      switch result {
                                      case .success:
                                          print("SDK is ready to use")

                                      case let .failure(error):
                                          print("Failure: \(error)")
                                      }
                                  })
    }
    ```

### How to Use:

=== "Android"

    Enrolment.getInstance().readDocumentRFID(
        activity = requireActivity(),
        params = DocumentReaderRFIDParameters(
            rfidReadTimeout = docReaderRFIDParams.rfidReadTimeout,
            showRFIDInstructions = docReaderRFIDParams.showRFIDInstructions,
            mrzString = docReaderRFIDParams.mrzString
        ),
        onReadDocumentCompletion = object : OnReadDocumentCompletion {
            override fun onReadDocumentSuccess(documentReaderReport: DocumentReaderReport) {
                
            }

            override fun onReadDocumentError(documentReaderError: DocumentReaderError) {
                
            }
        }
    )
    
=== "iOS"

	```swift
    func readRFIDDocumentSampleUsage() {
        // The view controller responsible for presenting the document scanner camera interface
        var viewController: UIViewController!
        
        let formatter = DateFormatter()
        formatter.timeZone = TimeZone(identifier: "UTC")
        formatter.dateFormat = "YY-MM-dd"
        let parameters = ReadRFIDDocumentParameters(
            documentNumber: "<DOCUMENT_NUMBER>",
            documentMRZ: "<DOCUMENT_MRZ>", //
            dateOfExpiry: formatter.date(from: "<DATE_OF_EXPIRY>") ?? Date(),
            dateOfBirth: formatter.date(from: "<DATE_OF_BIRTH>") ?? Date(),
            showRFIDStatus: false,
            rfidTimeout: 30)
        
        Enrolment.shared.readRFIDDocument(
            parameters: parameters,
            viewController: viewController
        ) { result in
            switch result {
            case let .success(report):
                print("Document Read: Success!")
                print(report.idDocument)
            case let .failure(error):
                print(error.featureError.description)
            }
        }
    }
    
    ```
