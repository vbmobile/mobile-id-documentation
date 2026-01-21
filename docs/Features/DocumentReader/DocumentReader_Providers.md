# Custom Providers

This page contains all available providers for the **Document Reader** feature, as well as instructions on how to import and implement them in a project using the SeamlessMobile SDK.

- [Regula Provider](#regula-provider)
- [Amadeus Provider](#amadeus-provider)

## Regula Provider

This provider uses Regula services and supports both OCR Document Reading and RFID scanning functionalities.

### How to Import: 

=== "Android"

    ```kotlin
    implementation("com.visionbox.mobileid.sdk:vb-ocrmrzrfid-regula:<2.0.2>")
    ```
    Or declare Mobile ID SDK and document reader provider following the BOM pattern instead:

    ```kotlin
    implementation(platform('com.visionbox.mobileid.sdk:mobileid-bom:8.1.4'))
    implementation("com.visionbox.mobileid.sdk:vb-ocrmrzrfid-regula")
    ```

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

    The **RegulaProvider** requires a **DocumentReaderConfig** to initialize. It can be done as follows. For more information, see [DocumentReaderConfig](./DocumentReader_Index.md#configure).

    ```kotlin
    val regulaDocumentRfidProvider = RegulaProvider.getInstance(
        DocumentReaderConfig(
            multipageProcessing = true,
            databaseId = "Passports"
        )
    )
    ```
    
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

    After initializing the provider, simply pass it as a parameter to the Enrolment initialization as shown below. For more information on initializing, see [Enrolment](../../index.md#how-to-initialize-the-sdk).

    ```kotlin
    val context = ...
    val enrolmentConfig = ...
    val callback = ...
    val regulaDocumentRfidProvider = RegulaProvider.getInstance(
        DocumentReaderConfig(
            multipageProcessing = true,
            databaseId = "Passports"
        )
    )

    Enrolment.initialize(
        context = context, 
        enrolmentConfig = enrolmentConfig,
        documentReaderProvider = regulaDocumentRfidProvider,
        rfidReaderProvider = regulaDocumentRfidProvider,
        callbackcallback
    )
    ```
    
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
    
## Amadeus Provider

This provider uses Amadeus services and supports both OCR Document Reading and RFID scanning functionalities.

### How to Import: 

=== "Android"

    It will be available soon.

=== "iOS"

    **CocoaPods**
   
    It will be available soon.

    **SPM**

    It will be available soon.

### How to Instantiate: 


=== "Android"

    To initialize the **VBProvider**. It can be done as follows. For more information, see [DocumentReaderConfig](./DocumentReader_Index.md#configure).

    ```kotlin
    val vbProvider = VBProvider.getInstance()
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

### How to Use: 

Once both providers are initialized, simply pass them as parameters to the Enrolment initialization as shown below. For more information on initializing, see [Enrolment](../../index.md#how-to-initialize-the-sdk).

=== "Android"

    ```kotlin
    val context = ...
    val enrolmentConfig = ...
    val callback = ...
    val vbDocumentReaderProvider = VBProvider.getInstance()

    Enrolment.initialize(
        context = context, 
        enrolmentConfig = enrolmentConfig,
        documentReaderProvider = vbDocumentReaderProvider,
        rfidReaderProvider = vbDocumentReaderProvider,
        callbackcallback
    )
    ```
    
=== "iOS"

    ``` swift
    var documentReaderConfig = DocumentReaderConfig(multipageProcessing: false, databaseID: "Passports", checkHologram: false)
    
    var documentReaderScan = DocumentReaderScan(config: documentReaderConfig)
    var documentReaderRFID = DocumentReaderRFID()
    
    Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                              documentScanProvider: documentReaderScan,
                              documentRFIDProvider: documentReaderRFID,
                              viewRegister: viewRegister,
                              completionHandler: completionHandler)
    
    ```
 
