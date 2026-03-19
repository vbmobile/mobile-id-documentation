# Ultralight Integration

Ultralight enables **Beamsync**, a proximity-based data transmission mechanism that sends passenger
data to nearby touchpoints (for example, gates or kiosks).

In the current SDK architecture, Ultralight is integrated through the **Enrolment SDK** facade.
You provide your own `UltralightProvider` during initialization, and Enrolment exposes methods to control sharing.

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

Before initializing Enrolment, create and configure your UltralightProvider instance:

=== "Android"

    ```kotlin
    private fun initializeUltralight(): UltralightProvider? {
        val ultralightApiKey = "<your-ultralight-api-key>"
        
        // Initialize UltralightSdk
        UltralightSdk.softStart(context = requireContext())
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

Pass the UltralightProvider to Enrolment during initialization:

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

    Offline mode follows the same pattern:

    ```kotlin
    val ultralightProvider = initializeUltralight()
    
    Enrolment.initializeOffline(
        context = requireContext().applicationContext,
        enrolmentConfig = enrolmentConfig,
        enrolmentCustomViews = enrolmentCustomViews,
        documentReaderProvider = documentReaderProvider,
        ultralightProvider = ultralightProvider, // Pass the provider
        rfidReaderProvider = null,
        enrolmentInitializerCallback = callback,
        license = token
    )
    ```

=== "iOS"

    It will be available soon.

## Start Beamsync

Start Beamsync using the Enrolment facade method `startSharing()`:

=== "Android"

    ```kotlin
    val result = Enrolment.getInstance().startSharing()
    
    when (result) {
        "SUCCESS" -> {
            // Beamsync initialized successfully
        }
        "ERROR" -> {
            // Initialization failed
        }
    }
    ```

    The method returns:
    - `"SUCCESS"` if Beamsync started successfully or was already running
    - `"ERROR"` if initialization failed or provider is not available

=== "iOS"

    It will be available soon.

## Share Passenger Data

Set the list of passengers to be broadcast through Beamsync using the `share()` method:

=== "Android"

    ```kotlin
    import com.amadeus.mdi.mob.sdk.doc_model.api.models.Ultralight.Passenger
    
    val passengers = listOf(
        Passenger(
            language = "en",
            mrz = "<mrz-line-1>\\n<mrz-line-2>",
            boardingPasses = listOf("<bcbp-barcode-string>"),
            docPhotoBase64 = "<base64-encoded-document-photo>",
            selfieBase64 = "<base64-encoded-selfie>",
            ePassport = true,
            eBagTagId = null,
            tag = null
        )
    )
    
    Enrolment.getInstance().share(passengers) { result, error ->
        if (result == true) {
            // Passengers data set successfully
        } else {
            // Failed to set passenger data
            Log.e("Ultralight", "Error: $error")
        }
    }
    ```

    Passenger model:

    ```kotlin
    data class Passenger(
        val language: String,
        val mrz: String,
        val boardingPasses: List<String>,
        val docPhotoBase64: String,
        val selfieBase64: String,
        val ePassport: Boolean,
        val eBagTagId: String? = null,
        val tag: String? = null
    )
    ```

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
        try {
            Enrolment.getInstance().stopSharing()
        } catch (e: Exception) {
            Log.e(TAG, "Error stopping beamsync", e)
        }
    }
    ```

=== "iOS"

    It will be available soon.

## Complete Example

Here's a complete example integrating Ultralight with Enrolment:

=== "Android"

    ```kotlin
    class UltralightFragment : Fragment() {
        
        // Initialize Ultralight provider
        private fun initializeUltralight(): UltralightProvider? {
            val ultralightApiKey = "<your-api-key>"
            if (ultralightApiKey.isNullOrEmpty()) return null
            
            UltralightSdk.softStart(context = requireContext())
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
        
        // Start Beamsync
        private fun startBeamsync() {
            val result = Enrolment.getInstance().startSharing()
            
            if (result == "SUCCESS") {
                Log.d(TAG, "Beamsync started successfully")
                prepareAndSharePassenger()
            } else {
                Log.e(TAG, "Failed to start Beamsync")
            }
        }
        
        // Prepare and share passenger data
        private fun prepareAndSharePassenger() {
            // Build passenger from collected data
            val passenger = Passenger(
                language = "en",
                mrz = idDocument.mrz,
                boardingPasses = listOf(boardingPass.rawBoardingPass),
                docPhotoBase64 = documentPhoto,
                selfieBase64 = selfiePhoto,
                ePassport = idDocument.isElectronic
            )
            
            // Share passengers
            Enrolment.getInstance().share(listOf(passenger)) { result, error ->
                activity?.runOnUiThread {
                    if (result == true) {
                        Log.d(TAG, "Passenger data set successfully")
                    } else {
                        Log.e(TAG, "Failed to set passenger: $error")
                    }
                }
            }
        }
        
        // Stop Beamsync
        private fun stopBeamsync() {
            Enrolment.getInstance().stopSharing()
            Log.d(TAG, "Beamsync stopped")
        }
        
        override fun onDestroyView() {
            super.onDestroyView()
            // Always stop beamsync when leaving
            try {
                Enrolment.getInstance().stopSharing()
            } catch (e: Exception) {
                Log.e(TAG, "Error stopping beamsync", e)
            }
        }
    }
    ```

=== "iOS"

    It will be available soon.



## Notes

- The `UltralightProvider` must be initialized before passing it to Enrolment
- All sharing operations are handled through the Enrolment facade methods
- `share()` uses a callback for async result notification
- Always call `stopSharing()` when cleaning up (e.g., in `onDestroyView()`)
