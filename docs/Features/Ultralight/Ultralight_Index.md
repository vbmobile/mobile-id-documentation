# Ultralight Integration

Ultralight enables **Beamsync**, a proximity-based data transmission mechanism that broadcasts
passenger data to nearby airport touchpoints (for example, e-gates or self-service kiosks).
This allows passengers to pass through airport processes without re-scanning their documents at each step.

In the current SDK architecture, Ultralight is integrated through the Enrolment SDK facade.
You provide your own `UltralightProvider` during initialization, and Enrolment exposes two methods to
control the sharing lifecycle: `share()` (sets passengers and starts broadcasting) and `stopSharing()`.

## Prerequisites

Before integrating Ultralight, ensure you have:

- **Ultralight API key** — Contact your Amadeus liaison to obtain one
- **Ultralight provider dependency** — Added to your project (see import instructions below)

=== "Android"

    - **Minimum SDK level 26** (same as Enrolment SDK)
    - **Required permissions** (brought transitively by the Ultralight provider dependency):
        - `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` (Bluetooth Low Energy)
        - `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION` (required for BLE scanning)
    - **Runtime requirements:**
        - Bluetooth must be enabled on the device
        - Location services must be enabled on the device

    !!! note
        The SDK validates that Bluetooth and Location are enabled before starting Beamsync
        and returns a descriptive `FeatureError` if either is disabled.

=== "iOS"

    - **Minimum iOS Verion: 15** (same as Enrolment SDK)
    - **Required permissions on Info.plist** (brought transitively by the Ultralight provider dependency):

```xml
<key>NSBluetoothAlwaysUsageDescription</key>
<string>We need access BT (UltraLight)</string>
```
        
## How to Import

=== "Android"

    Ultralight is exposed through the Enrolment SDK integration flow.
    
    Add the Ultralight provider dependency to your app's `build.gradle`:

    ```gradle
    dependencies {
        implementation "com.amadeus.mdi.mob.sdk:ama-ultralight:1.0.0-rc02"
        // ... other dependencies
    }
    ```

=== "iOS"

    Ultralight is exposed through Swift Package Manager at [https://github.com/vbmobile/AmaShareUltralight](https://github.com/vbmobile/AmaShareUltralight)

## Configure Ultralight in Enrolment Initialization

### Step 1: Create and Initialize UltralightProvider

Before initializing Enrolment, create and configure your `UltralightProvider` instance:

=== "Android"

    ```kotlin
    private fun initializeUltralight(): UltralightProvider? {
        val ultralightApiKey = "<your-ultralight-api-key>"
        
        // Initialize UltralightSdk
        UltralightSdk.initialize(context = requireContext())
        UltralightSdk.getInstance().initialiseBeamSync(ultralightApiKey)
        
        return UltralightSdk.getInstance()
    }
    ```

    If you don't want to enable Ultralight, simply return `null`:

    ```kotlin
    private fun initializeUltralight(): UltralightProvider? {
        val enabled = false // Your configuration flag
        if (!enabled) return null
        
        // ... initialization code
    }
    ```

=== "iOS"

    ```swift
    let ultralightProvider: AMAShareUltralight.Ultralight = .init()
    ultralightProvider.initialise(apiKey: "<your-ultralight-api-key>")
    ```


                                  
### Step 2: Pass Provider to Enrolment Initialization

Pass the `UltralightProvider` to `Enrolment.initialize()`:

=== "Android"

    ```kotlin
    val ultralightProvider = initializeUltralight()
    
    Enrolment.initialize(
        context = requireContext().applicationContext,
        enrolmentConfig = enrolmentConfig,
        enrolmentCustomViews = enrolmentCustomViews,
        documentReaderProvider = documentReaderProvider,
        ultralightProvider = ultralightProvider, // Pass the provider
        rfidReaderProvider = null,
        enrolmentInitializerCallback = callback
    )
    ```


=== "iOS"

    ```swift
    Enrolment.shared.initWith(enrolmentConfig: <your-enrolment-config>,
                             documentScanProvider: <your-document-scan-provider>,
                             documentRFIDProvider: <your-rfid-scanner-provider>,
                             ultralightProvider: ultralightProvider,
                             viewRegister: EnrolmentViewRegister(),
                             completionHandler: completionHandler)
    ```

## Share Passenger Data

The `share()` method sets the passenger list **and** starts sharing in a single call.
It returns a `Pair<Boolean, FeatureError>`

=== "Android"

    ```kotlin

    val passengers = listOf(
        Passenger(
            language = "en",
            mrz = "<mrz-line-1>\n<mrz-line-2>",
            boardingPasses = listOf("<bcbp-barcode-string>"),
            docPhotoBase64 = "<base64-encoded-document-photo>",
            selfieBase64 = "<base64-encoded-selfie>",
            ePassport = true,
            eBagTagId = null,
            tag = null
        )
    )

    val (success, featureError) = Enrolment.getInstance().share(passengers)
    
    if (success) {
        // Passengers set and Beamsync started successfully
    } else {
        // Check featureError.description for details
        Log.e("Ultralight", "Error: ${featureError.description}")
    }
    ```

    **Passenger model:**

    | Field             | Type           | Description                              |
    |-------------------|----------------|------------------------------------------|
    | `language`        | `String`       | Language code (e.g., `"en"`, `"fr"`)     |
    | `mrz`             | `String`       | MRZ string (`\n` separating lines)       |
    | `boardingPasses`  | `List<String>` | Raw BCBP barcode strings                 |
    | `docPhotoBase64`  | `String`       | Base64-encoded document holder photo     |
    | `selfieBase64`    | `String`       | Base64-encoded selfie                    |
    | `ePassport`       | `Boolean`      | Whether the document is an e-Passport    |
    | `eBagTagId`       | `String?`      | Optional electronic bag tag ID           |
    | `tag`             | `String?`      | Optional custom tag                      |


=== "iOS"


```swift
let passenger = Passenger(language: "en",
             mrz: "<mrz-line-1>\n<mrz-line-2>",
             boardingPasses: ["<bcbp-barcode-string>"],
             docPhotoBase64: "<base64-encoded-document-photo>",
             selfieBase64: "<base64-encoded-selfie>",
             ePassport: true,
             tag: nil,
             ebagtagId: nil)
guard let shareResult = await enrolment?.share(passengers: [passenger]) else {
    print("Precondition failed: nil shareResult")
    return
}
if shareResult.result ?? false {
    // Passengers set and Beamsync started successfully
} else {
    // Check featureError.description for details
    print(shareResult.error ?? "")
}
```

Given a document (`IdDocument`), a selfie (`UIImage`) and the boarding passe (`BoardingPassFull`) we can use the following extension to create a `Passanger`


```swift
import UIKit
import MobileIdSDKiOS
import AMADocModeliOS

extension IdDocument {
    
    func mapToPassenger(faceCapture: UIImage, boardingPassesFull: [BoardingPassFull]) -> Passenger {
        mapToPassenger(faceCapture: faceCapture,
                       boardingPasses: boardingPassesFull.compactMap({ $0.raw })
        )
    }
    
    func mapToPassenger(faceCapture: UIImage, boardingPasses: [String]) -> Passenger {
        guard let holderImage = data?.holderImage else {
            fatalError("Invalid holderImage")
        }
        let docPhotoBase64 = Data(holderImage).base64EncodedString()
        guard !docPhotoBase64.isEmpty else {
            fatalError("Invalid docPhotoBase64")
        }
        guard let faceCaptureBase64 = faceCapture.resized?.base64 else {
            fatalError("Invalid selfieBase64")
        }
        guard let mrz = mrz?.mrzString, !mrz.isEmpty else {
            fatalError("Invalid mrz")
        }
        return .init(language: "en",
                     mrz: mrz,
                     boardingPasses: boardingPasses,
                     docPhotoBase64: docPhotoBase64,
                     selfieBase64: faceCaptureBase64,
                     ePassport: info?.isElectronic == .electronic,
                     tag: nil,
                     ebagtagId: nil)
    }
}

extension UIImage {

    var resized: UIImage? {
        let maxDimension: CGFloat = 500
        let width = size.width
        let height = size.height
        let maxCurrent = max(width, height)
        if maxCurrent <= maxDimension { return self }
        let scale = maxDimension / maxCurrent
        let newSize = CGSize(width: width * scale, height: height * scale)
        let format = UIGraphicsImageRendererFormat.default()
        format.scale = scale
        format.opaque = false
        let renderer = UIGraphicsImageRenderer(size: newSize, format: format)
        return renderer.image { _ in
            self.draw(in: CGRect(origin: .zero, size: newSize))
        }
    }
  
    var base64: String? {
        if let jpegData = self.jpegData(compressionQuality: 1) {
            return jpegData.base64EncodedString()
        }
        if let jpegData = self.jpegData(compressionQuality: 0.9) {
            return jpegData.base64EncodedString()
        }
        if let jpegData = self.jpegData(compressionQuality: 0.8) {
            return jpegData.base64EncodedString()
        }
        if let pngData = self.pngData() {
            return pngData.base64EncodedString()
        }
        return nil
    }
}
```

## Stop Beamsync

Stop Beamsync when the flow ends (for example, when leaving the screen or destroying the view):

=== "Android"

    ```kotlin
    Enrolment.getInstance().stopSharing()
    ```

    It's recommended to call `stopSharing()` in your fragment/activity lifecycle:

    ```kotlin
    override fun onDestroyView() {
        super.onDestroyView()
        Enrolment.getInstance().stopSharing()
    }
    ```

=== "iOS"


It's recommended to call `stopSharing()` in your view lifecycle:


```swift
deinit {
   presenter.unbind()
   presenter.shouldStopSharing { _ in } // MVP Arquitecture
}
```

or call it ha hoc 

```swift
enrolment?.stopSharing()
```

## Complete Example

Here's a complete example integrating Ultralight with the Enrolment SDK:

=== "Android"

    ```kotlin
    class UltralightFragment : Fragment() {
        
        // Initialize Ultralight provider
        private fun initializeUltralight(): UltralightProvider? {
            val ultralightApiKey = "<your-api-key>"
            
            UltralightSdk.initialize(context = requireContext())
            UltralightSdk.getInstance().initialiseBeamSync(ultralightApiKey)
            return UltralightSdk.getInstance()
        }
        
        // Initialize Enrolment with Ultralight
        private fun initializeEnrolment() {
            val ultralightProvider = initializeUltralight()
            
            Enrolment.initialize(
                context = requireContext().applicationContext,
                enrolmentConfig = enrolmentConfig,
                enrolmentCustomViews = enrolmentCustomViews,
                documentReaderProvider = documentReaderProvider,
                ultralightProvider = ultralightProvider,
                rfidReaderProvider = null,
                enrolmentInitializerCallback = object : EnrolmentInitializerCallback {
                    override fun onEnrolmentInitialized() {
                        Log.d(TAG, "Enrolment initialized successfully")
                    }
                    
                    override fun onEnrolmentInitializationError(error: FeatureError) {
                        Log.e(TAG, "Initialization error: ${error.description}")
                    }
                }
            )
        }
        
        // Prepare and share passenger data
        private fun prepareAndSharePassenger(): Pair<Boolean, String?> {
            try {
                val idDocument = EnrolmentData.documentReaderReport?.idDocument
                    ?: return false to "No ID document"
                val boardingPass = EnrolmentData.boardingPass
                val selfieBitmap = readPhotoFromInternalStorage(
                    requireContext(),
                    EnrolmentData.faceCapturePhotoFilename ?: ""
                )

                // Build passenger from collected enrolment data
                val passenger = Passenger(
                    language = "en",
                    mrz = idDocument.mrz,
                    boardingPasses = listOf(boardingPass.rawBoardingPass),
                    docPhotoBase64 = documentPhoto,
                    selfieBase64 = selfiePhoto,
                    ePassport = idDocument.isElectronic
                )

                val (success, featureError) = Enrolment.getInstance()
                    .share(listOf(passenger))

                return if (success) {
                    true to null
                } else {
                    false to featureError.description.ifBlank {
                        featureError.publicMessage.ifBlank { "Unknown error" }
                    }
                }
            } catch (e: Exception) {
                Log.e(TAG, "Error preparing passenger", e)
                return false to e.message
            }
        }
        
        // Stop Beamsync
        private fun stopBeamsync() {
            Enrolment.getInstance().stopSharing()
            Log.d(TAG, "Beamsync stopped")
        }
        
        override fun onDestroyView() {
            super.onDestroyView()
            Enrolment.getInstance().stopSharing()
        }
    }
    ```

=== "iOS"

```swift
import MobileIdSDKiOS
import AMADocModeliOS
import AMAShareUltralight

class UltralightSample {

    func initializeUltralight() -> UltralightProtocol? {
        let ultralightProvider: AMAShareUltralight.Ultralight = .init()
        ultralightProvider.initialise(apiKey: "<your-ultralight-api-key>")
        return ultralightProvider
      }
    
    func initializeEnrolment() async -> EnrolmentProtocol {
        return await withCheckedContinuation { continuation in
            let enrolmentConfig = EnrolmentConfig(
                apiConfig: APIConfig(
                    baseURL: "<your-url>",
                    timeout: 30,
                    logLevel: .basic,
                    apiKey: "<your-enrolment-api-key>"
                ))
            Enrolment.shared.initWith(enrolmentConfig: enrolmentConfig,
                                      documentScanProvider: nil,
                                      documentRFIDProvider: nil,
                                      ultralightProvider: initializeUltralight(),
                                      viewRegister: nil,
                                      completionHandler:  { result in
                switch result {
                case .success:
                    continuation.resume(returning: Enrolment.shared)
                case .failure(let featureError):
                    print(featureError.description)
                    continuation.resume(returning: Enrolment.shared)
                }
            })
        }
    }
    
    func stopSharing(enrolment: EnrolmentProtocol?) {
        enrolment?.stopSharing()
    }
    
    func prepareAndSharePassenger(enrolment: EnrolmentProtocol?) {
        guard EnrolmentData.idDocument != nil else {
            print("Precondition failed: Have not read document")
            return
        }
        guard let faceCapture = EnrolmentData.biometricFaceCaptureReport?.photo else {
            print("Precondition failed: Have not read face")
            return
        }
        guard EnrolmentData.boardingPass != nil else {
            print("Precondition failed: Have not read boarding pass")
            return
        }
        guard let idDocument = EnrolmentData.idDocument else {
            print("Precondition failed: idDocument missing")
            return
        }
        let boardPass = EnrolmentData.boardingPass?.raw ?? ""
        let passenger = idDocument.mapToPassenger(faceCapture: faceCapture, boardingPasses: [boardPass])
        Task {
            guard let shareResult = await enrolment?.share(passengers: [passenger]) else {
                print("Precondition failed: nil shareResult")
                return
            }
            if shareResult.result ?? false {
                // Passengers set and Beamsync started successfully
            } else {
                // Check featureError.description for details
                print(shareResult.error ?? "")
            }
        }
    }
}
```

## Notes

- The `UltralightProvider` must be initialized **before** passing it to `Enrolment.initialize()`
- Ultralight is **not available** in offline mode (`initializeOffline`)
- `share()` is a **blocking** call — always invoke it from a background thread
- `share()` both sets the passenger data **and** starts Beamsync (there is no separate `startSharing()` step)
- The SDK performs pre-flight checks for Bluetooth and Location before starting Beamsync
- Always call `stopSharing()` when cleaning up (e.g., in `onDestroyView()`)
