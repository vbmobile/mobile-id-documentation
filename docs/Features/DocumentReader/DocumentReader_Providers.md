# Custom Providers

This page contains all available providers for the **Document Reader** feature, as well as instructions on how to import and implement them in a project using the SeamlessMobile SDK.

- [Regula Provider](#regula-provider)

## Regula Provider

This provider uses Regula services and supports both OCR Document Reading and RFID scanning functionalities.

### How to Import: 

=== "Android"

    ```kotlin
    //TODO:
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

This provider allows you to create both a **RegulaDocumentReaderScan** and a **RegulaDocumentReaderRFID** instance.

The **RegulaDocumentReaderScan** requires a **DocumentReaderConfig** to initialize. It can be done as follows. For more information, see [DocumentReaderConfig](./DocumentReader_Index.html#Configure).

=== "Android"

    ```kotlin
    //TODO:
    ```
    
=== "iOS"

    ``` swift
    var documentReaderConfig = DocumentReaderConfig(multipageProcessing: false, databaseID: "Full_id_passport", checkHologram: false)
    
    RegulaDocumentReaderScan(config: documentReaderConfig)
    
    ```

The **RegulaDocumentReaderRFID** has no initialization requirements and can be instantiated as follows:

=== "Android"

    ```kotlin
    //TODO:
    ```
    
=== "iOS"

    ``` swift
    RegulaDocumentReaderRFID()
    
    ```
    
### How to Use: 

Once both providers are initialized, simply pass them as parameters to the Enrolment initialization as shown below. For more information on initializing, see [Enrolment](../../index.html#how-to-initialize-the-sdk).

=== "Android"

    ```kotlin
    //TODO:
    ```
    
=== "iOS"

    ``` swift
    var documentReaderConfig = DocumentReaderConfig(multipageProcessing: false, databaseID: "Full_id_passport", checkHologram: false)
    
    var regulaDocumentReaderScan = RegulaDocumentReaderScan(config: documentReaderConfig)
    var regulaDocumentReaderRFID = RegulaDocumentReaderRFID()
    
    Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                              documentScanProvider: regulaDocumentReaderScan,
                              documentRFIDProvider: regulaDocumentReaderRFID,
                              viewRegister: viewRegister,
                              completionHandler: completionHandler)
    
    ```
