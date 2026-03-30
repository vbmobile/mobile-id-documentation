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

    - Requirements will be available soon

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

    It will be available soon.

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

    It will be available soon.

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

    It will be available soon.

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

    It will be available soon.

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

    It will be available soon.

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

    It will be available soon.

## Notes

- The `UltralightProvider` must be initialized **before** passing it to `Enrolment.initialize()`
- Ultralight is **not available** in offline mode (`initializeOffline`)
- `share()` is a **blocking** call — always invoke it from a background thread
- `share()` both sets the passenger data **and** starts Beamsync (there is no separate `startSharing()` step)
- The SDK performs pre-flight checks for Bluetooth and Location before starting Beamsync
- Always call `stopSharing()` when cleaning up (e.g., in `onDestroyView()`)
