# MobileID SDK - Release Notes

## 8.0.1

### What's new

- Added **deinitialize** method to **Enrolment** to allow for re-initialization with different parameters as needed.

### Improvements

- Fixed crash when wrong timeout parameters are used.
- Small Bug fixes.

## 8.0.0

### What's new

- New, streamlined Face Capture UI.

### Improvements

- Improved Enrolment methods to accept a callback class instead of a result launcher.
- Reduced initialization time for document reader.
- Rotated photo when using the back camera.
- Removed unnecessary screens for a cleaner user experience. Check sample in github for examples with the error and preview screens.

#### Technical Enhancements
- Centralized configuration management.
- Image capture size optimizations.
- Modularized the SDK for better maintainability and scalability.
- Bugs fixes.

### Removed
- Sentry;

#### Warning
- The object DocumentData from the Document Reader feature will is **deprecated and will be removed in the future**, please update to the new object IdDocument.
- The square option from FaceCaptureFrameFormat is **deprecated and will be removed in the future**, please use the oval option.

## 7.3.2

### Improvements

- Updated Regula SDK to version 7.5.

## 7.3.1

### Changes

- Small changes to the face capture animation
- Providing an invalid api key will result in an error when calling any of the SDK's features

## 7.3.0

### Improvements

- Add choice of the scenarios for the [document capture](../Features/DocumentReader/DocumentReader_Index.html#configure)

## 7.2.2

- Remove Sentry has an external dependency

## 7.2.1

### Improvements

- Updated Regula SDK to version 7.4.

## 7.2.0

### Improvements

- Face Capture Timeout: Introduced a configurable timeout for the Face Capture feature. This can be set using the **faceCaptureTimeout** parameter in **BiometricFaceCaptureParameters**. The timeout default is disabled and the minimum allowed timeout is 30 seconds.
- Improved localization support documentation
- Error Handling: Removed the retry button from the default error screen for **InternalError** cases as retries are not effective in these situations.
- Updated Regula SDK to version 7.3.
- Changed the **ScanTimeout** error type to **Timeout**.
- Fixed an infinite loop issue in the Document Reader.

## 7.1.3

### Improvements
- Fix an issue with passive authentication while using Regula version 7.2

## 7.1.2

### Improvements
- Update Regula to 7.2

## 7.1.1

### Improvements
- Handle SubjectDataIntegrityFailed to prevent crashes while building the subject if the data validation fails.
- Change VB ImageProcessor's visibility to private.

## 7.1.0

### Improvements
- Improved security measures:
    - Communications with the backend are now encrypted using hybrid encryption;
    - Data integrity is verified in communications with the backend;
    - Data integrity is verified in the build subject and face match operations;
    - HTTP responses are signed and verifiable

### What's new
- [Form](../Features/Form/Form_Index.md) feature

## 7.0.2

### Improvements
- Fixed an issue with some boarding pass formats

## 7.0.1

### Improvements
- Removed mandatory preview screen in face capture;
- Fixed an issue with regula database listener;
- Changed adding a subject without a boarding pass when it's mandatory error code to it's own error code;
- Clean Regula resources upon document reader finished in order to reduce memory consumption;
- Added a new parameter to **DocumentReaderConfig** called *checkHologram** to enable Regula's hologram scan, to prevent fraudulent documents.

## 7.0.0

### IMPORTANT
- **In Q1 2024, 7.1.0 will be released targeting API 34.**

### What's new
- New subject service (now works asynchronously)
- Removed the `get`, `delete` and `update` subject signatures;
- Clients need to save the subject locally after adding.

### Improvements
- Removed the signatures that use the deprecated `onActivityResult` function that were deprecated;
- Removed some external dependencies to improve SDK size;
- Changed Java compile version to 17;
- Replaced synthetic views with view binding.

### Removed
- Moshi;
- Restring
- kotlin-android-extensions plugin.

## 5.2.3
### Improvements

- Improved frame of face capture drawing by adjusting the ratios.
- Fix issues that subjects couldn't be created with national ID documents and resident cards.

## 5.2.2
### Improvements

- Improved Face capture process by:
  - Fix issue with new mouth open algorithm (requires changes in Backoffice before upgrading)

## 5.2.1
### Improvements

- Improved Face capture process by:
  - Calculate input frame lightning conditions, contrast and sharpness.
  - Improved multiple faces check to focus on the closer face.
  - Changed mouth open algorithm.
  - Fixed switch between frontal and back cameras.
- Added **CameraConfig** to **BiometricFaceCaptureParameters** to control if the toggle camera button should appear and the initial camera facing (Front or back camera)

## 5.2.0
### Improvements
- Added a minimum value of 10 seconds, and a maximum value of 60 seconds for document scanner and rfid reader timeouts.
- Added feature to disable regula passive auth for some documents by their ID.
- Removed preview custom views from every feature, if you don't want our default screen, turn off the showPreview flag in feature parameters.
- Removed error custom views from every feature, if you don't want our default screen, turn off the showErrors flag in feature parameters.
- Removed success custom view interfaces as they were no longer being used by our SDK.
- Improved loading animations.
- Improved image handling process.
- Changed the default face capture frame to Oval shape, but added an option in parameters to use the square option as well.
- Refactor remaining custom views interfaces to make it easier to implement.
- Separated Face Capture Image processing to another SDK in order to increase testability.
- Updated Regula version to 6.8.
- Fix timezone bug on preview screen.

### Warning
- Functions marked with deprecated will be removed in version 6.0.0, please update following their suggestions.

## 5.1.3
### Improvements
- Updated to Regula 6.6;

## 5.1.2
### Improvements
- Fixed bug that Android devices which API level was 9 or less couldn't detect when the user had it's mouth open during real time analysis;
- Calculate intra ocular distance in order to detect proximity to the camera;
- Fixed bug that sometimes final image wouldn't be processed and caused an infinite loading during face capture;
- Fixed bug that RFID custom views were being overlapped.

### Downgrades
- Downgraded regula to 6.3.

## 5.1.1
### Improvements
- Updated to Regula 6.6;

## 5.1.0
### Improvements
- Minor UI/UX improvements.
- Remove Liveness icon from Face Capture preview
- Added *TemplateOption* to *BiometricMatchParameters*

### Downgrades
- Downgraded regula to 6.3.

## 5.0.3
### What's new
- Added a new method to the enrolment facade to remove the database update listener
- New liveness endpoint.

### Improvements
- Improved document reader timeouts functionality, so that it's possible to disable them.
- Improved RFID timeout, now only starts after instruction screen.
- Improved BuildSubjectParameters, If no custom language is provided, use the language defined in the EnrolmentConfig or as last resort the device language.
- Added animations to improve UX.
- Added progress bar to show that the chip is being read.
- Fixed the verification message that checked if the user has it's mouth open while taking the selfie.
- Improved real time analysis of selfie capture to improve feedback on older smartphones.


## 5.0.2
### Improvements
- Updated to Regula 6.6;


## 5.0.1
### What's new
- Added Fragment support to Enrolment methods;
- Added logs to Subject Builder;
- Biometric Face Match has a new workflow. It uses the onActivityResult Android architecture to return results;
- Subject Enrolment methods have a new workflow. They use the onActivityResult Android architecture to return results;
- Biometric Face Capture now has real-time image processing with feedback to increase odds of taking a quality picture for the match service;
- The EnrolmentConfig has a new configuration to set the SDK language;
- Document Reader database download can now be controlled by the client;

### Improvements
- Minimum SDK version changed to 23;
- Upgraded external dependencies;
- Updated to Regula 6.3;
- Migrated from Firebase to MLKit;
- Improved Sentry logs;
- Improved feature logs;
- Improved SDK default UI;
- Simplified SDK configurations by moving some to backoffice;
- New Biometric Match service that improved performance;
- Uses Mobile API 4.0;

### Removed
- OkHttpClient library;
- RX support;
- Localization support from backend;
