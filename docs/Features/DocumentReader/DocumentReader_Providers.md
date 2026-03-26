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

    **CocoaPods**
   
    Add the following to your Podfile, with the latest version:
    ```
    pod 'VBOcrMrzRfidRegula', '1.1.0'
    ```
    
    Run in Terminal the command below to install pods in your project:
    ```
    pod install
    ```

    **SPM**

    Enter the package URL:
    ```
    https://github.com/vbmobile/VBOcrMrzRfidRegula
    ```

### How to Instantiate: 

=== "Android"

    Work in progress...
    
=== "iOS"
    
    This provider allows you to create both a **RegulaDocumentReaderScan** and a **RegulaDocumentReaderRFID** instance.

    The **RegulaDocumentReaderScan** requires a **DocumentReaderConfig** to initialize. It can be done as follows. For more information, see [DocumentReaderConfig](./DocumentReader_Index.md#configure).

    ``` swift
    var documentReaderConfig = DocumentReaderConfig(multipageProcessing: false, databaseID: "Passports", checkHologram: false)
    
    RegulaDocumentReaderScan(config: documentReaderConfig)
    ```

    The **RegulaDocumentReaderRFID** has no initialization requirements and can be instantiated as follows:

    ``` swift
    RegulaDocumentReaderRFID()
    
    ```
    
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
