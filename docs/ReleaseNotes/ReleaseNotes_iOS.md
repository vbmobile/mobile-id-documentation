# MobileID SDK - Release Notes

## 8.0.0

### What's new

- New, streamlined Face Capture UI.

### Improvements

- Reduced initialization time for document reader.
- Mirror photo when using the front camera.
- Removed unnecessary screens for a cleaner user experience. Check sample in github for examples with the error and preview screens.

#### Technical Enhancements
- Centralized configuration management.
- Modularized the SDK for better maintainability and scalability.
- Bugs fixes.

#### Warning
- The object DocumentData from the Document Reader feature will is **deprecated and will be removed in the future**, please update to the new object IdDocument.
- The square option from BiometricFaceCaptureFrameOptions is **deprecated and will be removed in the future**, please use the oval option.  

## 7.3.3

### Improvements

- Updated Regula SDK to version 7.5.

## 7.3.2

### Improvements

- Fix issues with Camera permissions.
- Updated Lottie SDK to version 4.4.1.
- Fix face capture animation bug, where the face selection frame was moved to top left corner.

## 7.3.1

### Improvements

- Updated VBDependencyInjector SDK to version 1.0.5.

## 7.3.0

### Improvements

- Add choice of the scenarios for the [document capture](../Features/DocumentReader/DocumentReader_Index.html#configure)
- Remove Sentry has an external dependency

## 7.2.2

### Improvements

- Updated Sentry SDK to version 8.33.

## 7.2.1

### Improvements

- Updated Regula SDK to version 7.4.
- Support to SPM 

## 7.2.0

### Improvements

- Face Capture Timeout: Introduced a configurable timeout for the Face Capture feature. This can be set using the **faceCaptureTimeout** parameter in **BiometricFaceCaptureParameters**. The timeout default is disabled and the minimum allowed timeout is 30 seconds. 
- Improved localization support documentation
- Error Handling: Removed the retry button from the default error screen for **InternalError** cases as retries are not effective in these situations.
- Updated Regula SDK to version 7.3.
- Changed the **ScanTimeout** error type to **Timeout**.
- Fixed an infinite loop issue in the Document Reader.
- Resolved layout inconsistencies in the Face Capture UI.
- Prevented simultaneous pressing of RFID skip and start buttons in the Document Reader.

## 7.1.2

### Improvements
- Update Regula to 7.2
- Improvements in **BiometricFaceCapture** feature.

## 7.1.1
### Improvements
- Added a new parameter to **ReadDocumentParameters** called **showRFIDInstructions**  that allows you to skip the RFID scan instruction screen

## 7.1.0
### Improvements
- Improved security measures:
    - Communications with the backend are now encrypted using hybrid encryption;
    - Data integrity is verified in communications with the backend;
    - Data integrity is verified in the build subject and face match operations;
    - HTTP responses are signed and verifiable

### What's new
- [Form](../Features/Form/Form_Index.md) feature

## 7.0.1

### Improvements
- Fixed an issue with Boarding Pass Preview clickable rows 
- Added a new parameter to **DocumentReaderConfig** called *checkHologram** to enable Regula's hologram scan, to prevent fraudulent documents.
- Removed mandatory preview screen in face capture;
- Changed adding a subject without a boarding pass when it's mandatory error code to it's own error code;
- Fix id 215 and 224 to appear as IDCard in Document Reader 
- Fix issues with oval drawing in Face Capture

## 7.0.0

### What's new
- New subject service (now works asynchronously)
  - Removed the `get`, `delete` and `update` subject signatures;
  - Clients need to save the subject locally after adding.
- Improve error handling
- The boarding pass can be read from an image

### Improvements
- Fix issues with Loading Screen Animations
- Add Camera permissions messages in Boarding Pass Scanner and Face Capture 

## 5.2.3
### Improvements

- Updated to Lottie 4.3.3


## 5.2.2
### Improvements

- Improved the fetching of needed resources in the **DocumentReader** feature.

## 5.2.1
### Improvements

- Improved Face capture process by:
  - Improved multiple faces check to focus on the closer face.
- Added **CameraConfig** to **BiometricFaceCaptureParameters** to control if the toggle camera button should appear and the initial camera facing (Front or back camera)

## 5.2.0
### Improvements
- The frameShape field of the class *BiometricFaceCaptureParameters* can now be set to choose between an oval or square shape, default is oval
- The scannerTimeout and rfidTimeout field of the class *ReadDocumentParameters* has a maximum and minimum value (maximum 60, minimum 10)
- The scannerTimeout field of the class *ReadDocumentParameters* can now be set to nil to be disabled
- Removed preview custom views from every feature, if you don't want our default screen, turn off the showPreview flag in feature parameters.
- Removed error custom views from every feature, if you don't want our default screen, turn off the showErrors flag in feature parameters.
- Refactor remaining custom views protocols to make it easier to implement.
- Added feature to disable regula passive auth for some documents by their ID.
- Improved loading animations.
- Improved image handling process.
- Updated Regula version to 6.8

## 5.1.1
### Improvements
- Updated to Lottie 3.4;

## 5.1.0
### Improvements
- Minor UI/UX improvements.
- Added *TemplateOption* to *BiometricMatchParameters*

### Removed
- Liveness icon from Face Capture preview screen

## 5.0.3
### Improvements
- Improved RFID timeout, now only starts after instruction screen.
- Improved error and timeout messages. 
- Improved UI
- Added animations to improve UX.

## 5.0.2
### Improvements
- Updated to Regula 6.6;

## 5.0.1
### What's new
- Biometric Face Capture now has real-time image processing with more feedback to increase odds of taking a quality picture for the match service;
- The EnrolmentConfig has a new configuration to set the SDK language;
- Document Reader database download can now be controlled by the client;
- Added logs to Subject Builder;

### Improvements
- Upgraded external dependencies;
- Migrated to Vision framework for image processing;
- Improved Sentry logs;
- Improved feature logs;
- Improved SDK default UI;
- Simplified SDK configurations by moving some to backoffice;
- New Biometric Match service that improved performance;
- Uses Mobile API 4.0;
- Updated to Regula 6.3; 

### Removed
- Alamofire library;
- Localization support from backend;
