# Custom Providers

This page contains all available providers for the **Document Reader** feature, as well as instructions on how to import and implement them in a project using the SeamlessMobile SDK.

- [Regula Provider](#regula-provider)
- [Amadeus DocScanMrz Provider](#amadeus-docscanmrz-provider)

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
	
	4.  Select the version to integrate.  
	    For new projects, we recommend using the latest available release (for example: **`1.0.0-rc24`**).
	
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
	        exact: "1.0.0-rc24"
	    )
	]
	```
	
	> Replace `1.0.0-rc24` with the intended version you wish to use.
	
	
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

### How to Instantiate: 

=== "Android"

    Work in progress...
    
=== "iOS"
    
    ```swift
        let bounds = UIScreen.main.bounds
        let documentScanProvider = DocumentReaderScan(
            documentType: .td3,
            apiKey: "YOUR KEY",
            pixelWidth: Int(bounds.width),
            pixelHeight: Int(bounds.height)
        )

        Enrolment.shared.initWith(enrolmentConfig: nil,
                                  documentScanProvider: documentScanProvider,
                                  documentRFIDProvider: nil,
                                  ultralightProvider: nil,
                                  viewRegister: EnrolmentViewRegister(),
                                  completionHandler: { result in
                                      switch result {
                                      case .success:
                                          print("SDK is ready to use")
                                      case let .failure(error):
                                          print("Failure: \(error)")
                                      }
                                  })
	```
    
<!--
    This provider allows you to create both a **RegulaDocumentReaderScan** and a **RegulaDocumentReaderRFID** instance.

    The **RegulaDocumentReaderScan** requires a **DocumentReaderConfig** to initialize. It can be done as follows. For more information, see [DocumentReaderConfig](./DocumentReader_Index.md#configure).

    ``` swift
        let bounds = UIScreen.main.bounds
        let documentScanProvider = DocumentReaderScan(
            documentType: .td3,
            apiKey: "YOUR KEY",
            pixelWidth: Int(bounds.width),
            pixelHeight: Int(bounds.height)
    ```

    The **RegulaDocumentReaderRFID** has no initialization requirements and can be instantiated as follows:

    ``` swift
    RegulaDocumentReaderRFID()
    
    ```
-->
    
### How to Use:

=== "Android"

    Work in progress...
    
=== "iOS"

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
    implementation("com.amadeus.mdi.mob.sdk:ama-doc-scan-mrz:<1.0.0-rc01>")
    ```

=== "iOS"

    **CocoaPods**
   
    It will be available soon.

    **SPM**

    It will be available soon.

### How to Instantiate: 


=== "Android"

    To initialize the Enrolment with the **DocScanMrz**. It can be done as follows.

    ```kotlin

    val docScanMrzConfig = DocScanMrzConfig(
        enableLogs = <true>,
        docScanMrzKey: <YOUR DOC SCAN MRZ KEY>,
    )

    DocScanMrz.softStart(
        context = this,
        docScanMrzConfig = docScanMrzConfig
    )

    val context = ...
    val enrolmentConfig = ...
    val callback = ...
    val documentReaderProvider = DocScanMrz.getInstance()

    Enrolment.initialize(
        context = context, 
        enrolmentConfig = enrolmentConfig,
        documentReaderProvider = documentReaderProvider,
        callback = callback
    )
    ```
    
=== "iOS"

    This provider allows you to create both a **DocumentReaderScan** and a **DocumentReaderRFID** instance.
    
    The **DocumentReaderScan** requires a **DocumentReaderConfig** to initialize. It can be done as follows. For more information, see [DocumentReaderConfig](./DocumentReader_Index.md#configure).

    ``` swift
    var documentReaderConfig = DocumentReaderConfig(multipageProcessing: false, databaseID: "Passports", checkHologram: false)
    
    DocumentReaderScan(config: documentReaderConfig)
    ```

    The **DocumentReaderRFID** has no initialization requirements and can be instantiated as follows:

    ``` swift
    DocumentReaderRFID()
    
    ```
