# MobileID SDK - Release Notes

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
