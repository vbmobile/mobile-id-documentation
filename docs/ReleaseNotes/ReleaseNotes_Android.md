# MobileID SDK - Release Notes

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
- Functions marked with deprecated will be removed in version 6.0.0, please update following their sugestions.

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