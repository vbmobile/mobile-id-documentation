# Migration Guide

## From 7.2.0 to 8.0.0
#### Required Changes
- Developers are now required to specify the provider for the orz/mrz and rfid features. Check the updated [Getting Started](../index.md) page
- Enrolment is now a Singleton, instead of a builder you need to call Enrolment.shared, passing the required parameters to make the Enrolment available anywhere. Check homepage for more details.

## From 7.1.2 to 7.2.0
#### Optional Changes
- faceCaptureTimeout have been added to the [BiometricFaceCaptureParameters](../Features/FaceCapture/FaceCapture_Index.md#initiate-scan), to be able to start the RFID scan automatically
- If you mention the ScanTimeout Error type somewhere, you need to change it to Timeout due to the name change.

## From 7.1.0 to 7.1.1
#### Optional Changes
- showRFIDInstructions have been added to the [ReadDocumentParameters](../Features/DocumentReader/DocumentReader_Index.md#initiate-scan), to be able to start the RFID scan automatically

## From 7.0.0 to 7.1.0
#### Required Changes
- As part of the security improving efforts a `candidateHash` and `referenceHash` have been added to the [BiometricMatchParameters](../Features/BiometricMatch/BiometricMatch_Index.md#initiate-match), these can be found in the generated reports.
- Similarly, the build subject operation needs the generated `ProcessReport` and `DocumentReaderReport` that include the above hashes to verify data integrity. If you already use these parameters on the [BuildSubjectParameters](../Features/SubjectManagement/SubjectManagement_Index.md#subject-operations) you don't need to take any action.
- The package name now needs to be added to the backoffice. You may need to contact Vision-Box for this update.

#### Optional Changes
- Add a public key on the [initial configuration](../index.md#apiconfig) together with a private key setup on the backoffice to ensure encrypted requests.


## From 5.2.3 to 7.0.0
### Required Changes
- Remove the `get`, `update` and `delete` `Subject` operations. You should now save the `Subject` locally if you want to have a copy to check later. Updating a `Subject` is no longer supported as well so, you must create a new one if you want to for example, add a boarding pass;
- Handle errors by new field ErrorType instead of checking every possible errors;
- Filter through Biometrics by their source: Face, Chip or OCR;
- Rename enums to PascalCase, MALE is now Male, etc.

##  From 5.1.0 to 5.2.0

#### Required Changes
- If you are using a value of less than 10 seconds or greater than 60 for the scannerTimeout or rfidTimeout in  **ReadDocumentParameters** you need to change the value.

### Optional Changes
- If you want to continue with the square frame you need to set the frameShape field of the class *BiometricFaceCaptureParameters* to .square
- Refactor any preview custom view that you might be using to be an independent UIViewController in your own flow.
- Refactor any error custom view that you might be using to be an independent UIViewController in your own flow.
- Update remaining custom views with their new protocols.

##  From 5.0.0 to 5.1.0

#### Required Changes
- Removed liveness status parameter from the **BiometricFaceCaptureParameters**.

#### Optional Changes
- If you are using **BiometricFaceCapturePreviewView** custom view, you must remove the property **livenessStatus**.

#### Optional Changes
- Add parameter includeTemplate in BiometricMatchParameters to receive a template.

## From 4.2.4 to 5.0.0

### CocoaPods
- Run pod update & install

#### Required Changes
- Removed BoardingPassScanConfig. The Boarding Pass configuration is now on backend side;
- Removed Vision-Box parameters from the **BiometricFaceCaptureParameters**. These configurations are now on backoffice;
- Removed Vision-Box parameters from the **BiometricMatchParameters**. These configurations are now on backoffice;
- Removed **Subject**'s **validateBiometricQuality** configuration. This configuration is now on backoffice;
- Removed Alamofire lib;
- Removed specific feature loadings and created a generic one, e.g. remove calls for BoardingPassScannerLoadingView & BoardingPassScannerLoadingView and replace it with the new one LoadingOverlayViewType.
- 
#### Optional Changes
- Added new method **startUpdateDatabase** to allow database download. If the method isn't called, then it will be downloaded upon the first usage of our sdk.
- Removed localization support from backend, if you used our screens and our localization definition from backoffice, you must now create your own files.

