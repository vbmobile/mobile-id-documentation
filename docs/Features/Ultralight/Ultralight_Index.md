# Ultralight

Ultralight enables **Beamsync**, a proximity-based data transmission mechanism that broadcasts passenger data to nearby airport touchpoints (for example, e-gates or self-service kiosks).
This allows passengers to pass through airport processes without re-scanning their documents at each step.

In the current SDK architecture, Ultralight is integrated through the Enrolment SDK facade.
You provide your own `UltralightProvider` during initialization, and Enrolment exposes two methods to
control the sharing lifecycle: `share()` (sets passengers and starts broadcasting, asynchronous via
`OnShareCompletion` callback) and `stopSharing()`.

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

    !!! warning
        Ultralight is not available when initializing the SDK via `initializeOffline`.

=== "iOS"

    - **Minimum iOS Version: 15** (same as Enrolment SDK)
    - **Required permissions on Info.plist** (brought transitively by the Ultralight provider dependency):

    ``` xml
    <key>NSBluetoothAlwaysUsageDescription</key>
    <string>Bluetooth is used to communicate with nearby UltraLight devices</string>
    ```
    
	``` xml
	<key>NSLocationWhenInUseUsageDescription</key>
	<string>Location is required to detect nearby Bluetooth devices.</string>
	```
        
## How to Import

=== "Android"

    Ultralight is exposed through the Enrolment SDK integration flow.
    
    Add the Ultralight provider dependency to your app's `build.gradle`:

    ```gradle
    dependencies {
        implementation "com.amadeus.mdi.mob.sdk:ama-ultralight:<{{ versions.android_ultralight_provider }}>"
        // ... other dependencies
    }
    ```

=== "iOS"
   
      Ultralight is distributed for iOS via **Swift Package Manager (SPM)**.
   
    __Install using Xcode__
   
    1. Open your project in **Xcode**
    2. Go to **File ▸ Add Packages…**
    3. Enter the package repository URL:
   
    ```
    https://github.com/vbmobile/AmaShareUltralight
    ```
   
    4. Select the desired version (recommended: exact or up to next major)
    5. Add the **AmaShareUltralight** product to your app target

    __Install using `Package.swift`__
   
    If you are managing dependencies manually, add Ultralight to your `Package.swift`:

    ``` swift
    dependencies: [
       .package(
           url: "https://github.com/vbmobile/AmaShareUltralight",
           exact: "{{ versions.ios_ultralight_provider }}"
       )
    ],
    ```

	 > Replace `{{ versions.ios_ultralight_provider }}` with the intended version.
   
    Then include it in your target dependencies:

    ``` swift
    .target(
        name: "YourAppTarget",
        dependencies: [
            .product(name: "AmaShareUltralight", package: "AmaShareUltralight")
        ]
    )
    ```

	> Replace `YourAppTarget ` with the intended app target you wish to use.

    Once added, Ultralight APIs are available to your application through the Enrolment SDK integration flow.

## Configure Ultralight in Enrolment Initialization

### Step 1: Create and Initialize UltralightProvider

Before initializing Enrolment, create and configure your `UltralightProvider` instance.
After `initialiseBeamsync()`, you must call `softStart()`;
report success and errors through `OnSoftStartCompletion`.

=== "Android"

    ```kotlin
    private fun initializeUltralight(): UltralightProvider? {
        val ultralightApiKey = "<your-ultralight-api-key>"

        UltralightSdk.initialize(context = requireContext())
        val provider = UltralightSdk.getInstance()
        provider.initialiseBeamsync(ultralightApiKey)
        provider.softStart(requireContext(), object : OnSoftStartCompletion {
            override fun onProgressChanged(progress: Progress) {
                // Not currently emitted by the provider; override required by the interface.
            }

            override fun onSoftStartSuccess() {
                Log.i("Ultralight", "softStart onSuccess")
            }

            override fun onSoftStartError(error: ProviderError) {
                Log.e("Ultralight", "softStart onError [${error.errorCode}] ${error.description}")
            }
        })
        return provider
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
	func ultralightProvider() -> UltralightProtocol? {
	    let ultralightProvider: AMAShareUltralight.Ultralight = .init()
	    ultralightProvider.initialiseBeamSync(apiKey: "<your-ultralight-api-key>")
	    return ultralightProvider
	}
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
	func initializeEnrolment(provider: UltralightProtocol?) async -> EnrolmentProtocol {
	    let ultralightProvider = provider ?? ultralightProvider()
	    return await withCheckedContinuation { continuation in
	        Enrolment.shared.initWith(enrolmentConfig: nil,
	                                  documentScanProvider: nil,
	                                  documentRFIDProvider: nil,
	                                  ultralightProvider: ultralightProvider,
	                                  viewRegister: nil,
	                                  completionHandler: { result in
	                                      switch result {
	                                      case .success:
	                                          continuation.resume(returning: Enrolment.shared)
	                                      case let .failure(featureError):
	                                          print(featureError.description)
	                                          continuation.resume(returning: Enrolment.shared)
	                                      }
	                                  })
        }
	```

## Share Passenger Data

The `share()` method sets the passenger list **and** starts sharing in a single call.
It is asynchronous — pass an `OnShareCompletion` callback to receive the result.

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

    Enrolment.getInstance().share(passengers, object : OnShareCompletion {
        override fun onShareSuccess() {
            // Passengers set and Beamsync started successfully
        }

        override fun onShareError(error: FeatureError) {
            // Check error.description for details
            Log.e("Ultralight", "Error: ${error.description}")
        }
    })
    ```

=== "iOS"


	```swift
    func sampleShare(enrolment: EnrolmentProtocol?) {
        let passenger = Passenger(language: "en",
                                  mrz: "<mrz-line-1>\n<mrz-line-2>",
                                  boardingPasses: ["<bcbp-barcode-string>"],
                                  docPhotoBase64: "<base64-encoded-document-photo>",
                                  selfieBase64: "<base64-encoded-selfie>",
                                  ePassport: true,
                                  tag: nil,
                                  ebagtagId: nil)
        enrolment?.share(passengers: [passenger], completionHandler: { result, error in
            if result {
                // Passengers set and Beamsync started successfully
            } else {
                // Check error.for details
                print(error ?? "")
            }
        })
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
	    presenter?.shouldStopSharing() // MVP Design Pattern
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
            val provider = UltralightSdk.getInstance()
            provider.initialiseBeamsync(ultralightApiKey)
            provider.softStart(requireContext(), object : OnSoftStartCompletion {
                override fun onProgressChanged(progress: Progress) {
                    // Not currently emitted by the provider; override required by the interface.
                }

                override fun onSoftStartSuccess() {
                    Log.i(TAG, "softStart onSuccess")
                }

                override fun onSoftStartError(error: ProviderError) {
                    Log.e(TAG, "softStart onError [${error.errorCode}] ${error.description}")
                }
            })
            return provider
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
        private fun prepareAndSharePassenger() {
            try {
                val idDocument = EnrolmentData.documentReaderReport?.idDocument ?: return
                val boardingPass = EnrolmentData.boardingPass
                val selfieBitmap = readPhotoFromInternalStorage(
                    requireContext(),
                    EnrolmentData.faceCapturePhotoFilename ?: ""
                )

                val passenger = Passenger(
                    language = "en",
                    mrz = idDocument.mrz,
                    boardingPasses = listOf(boardingPass.rawBoardingPass),
                    docPhotoBase64 = documentPhoto,
                    selfieBase64 = selfiePhoto,
                    ePassport = idDocument.isElectronic
                )

                Enrolment.getInstance().share(listOf(passenger), object : OnShareCompletion {
                    override fun onShareSuccess() {
                        Log.d(TAG, "Beamsync started")
                    }

                    override fun onShareError(error: FeatureError) {
                        val message = error.description.ifBlank {
                            error.publicMessage.ifBlank { "Unknown error" }
                        }
                        Log.e(TAG, "Share failed: $message")
                    }
                })
            } catch (e: Exception) {
                Log.e(TAG, "Error preparing passenger", e)
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

	### Notes
	
	- The `UltralightProvider` must be initialized **before** passing it to `Enrolment.initialize()`
	- Ultralight is **not available** in offline mode (`initializeOffline`)
	- `share()` is **asynchronous** — results are delivered via `OnShareCompletion`; safe to call from the main thread
	- `share()` both sets the passenger data **and** starts Beamsync (there is no separate `startSharing()` step)
	- The SDK performs pre-flight checks for Bluetooth and Location before starting Beamsync
	- Always call `stopSharing()` when cleaning up (e.g., in `onDestroyView()`)

=== "iOS"

	```swift
	import AMADocModeliOS
	import AMAShareUltralight
	import MobileIdSDKiOS
	
	class UltralightProviderSample {
	    func ultralightProvider() -> UltralightProtocol? {
	        let ultralightProvider: AMAShareUltralight.Ultralight = .init()
	        ultralightProvider.initialiseBeamSync(apiKey: "<your-ultralight-api-key>")
	        return ultralightProvider
	    }
	
	    func initializeEnrolment(provider: UltralightProtocol?) async -> EnrolmentProtocol {
	        let ultralightProvider = provider ?? ultralightProvider()
	        return await withCheckedContinuation { continuation in
	            Enrolment.shared.initWith(enrolmentConfig: nil,
	                                      documentScanProvider: nil,
	                                      documentRFIDProvider: nil,
	                                      ultralightProvider: ultralightProvider,
	                                      viewRegister: nil,
	                                      completionHandler: { result in
	                                          switch result {
	                                          case .success:
	                                              continuation.resume(returning: Enrolment.shared)
	                                          case let .failure(featureError):
	                                              print(featureError.description)
	                                              continuation.resume(returning: Enrolment.shared)
	                                          }
	                                      })
	        }
	    }
	
	    func sampleShare(enrolment: EnrolmentProtocol?) {
	        let passenger = Passenger(language: "en",
	                                  mrz: "<mrz-line-1>\n<mrz-line-2>",
	                                  boardingPasses: ["<bcbp-barcode-string>"],
	                                  docPhotoBase64: "<base64-encoded-document-photo>",
	                                  selfieBase64: "<base64-encoded-selfie>",
	                                  ePassport: true,
	                                  tag: nil,
	                                  ebagtagId: nil)
	        enrolment?.share(passengers: [passenger], completionHandler: { result, error in
	            if result {
	                // Passengers set and Beamsync started successfully
	            } else {
	                // Check error.for details
	                print(error ?? "")
	            }
	        })
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
	        enrolment?.share(passengers: [passenger], completionHandler: { result, error in
	            if result {
	                // Passengers set and Beamsync started successfully
	            } else {
	                // Check error.for details
	                print(error ?? "")
	            }
	        })
	    }
	}	
	```

	### Notes
	
	- The `UltralightProvider` must be initialized **before** passing it to `Enrolment.initialize()`
	- Ultralight is **not available** in offline mode (`initializeOffline`)
	- `share()` is **asynchronous** — results are delivered through the `OnShareCompletion` callback
	- `share()` both sets the passenger data **and** starts Beamsync (there is no separate `startSharing()` step)
	- The SDK performs pre-flight checks for Bluetooth and Location before starting Beamsync
	- Always call `stopSharing()` when cleaning up (e.g., in `deinit()`)
