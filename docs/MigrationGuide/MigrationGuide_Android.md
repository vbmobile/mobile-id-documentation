# Migration Guide

## From 7.2.0 to 8.0.0
#### Required Changes
- Developers are now required to specify the provider for the orz/mrz and rfid features. Check the updated [Getting Started](../index.md) page
- The contract for each feature has changed, instead of making use of the Activity Launcher contract, a standard callback has been added. Check each feature page for more details.
- Enrolment is now a Singleton, instead of a builder you need to call Enrolment.initialize() passing the required parameters to make the Enrolment available anywhere. Check homepage for more details.

## From 7.1.1 to 7.2.0
#### Optional Changes
- If you want to activate the Face Capture timeout, then you need to pass a value in milliseconds to faceCaptureTimeout in BiometricFaceCaptureParameters.
- If you mention the ScanTimeout Error type somewhere, you need to change it to Timeout due to the name change.

## From 7.1.0 to 7.1.1
#### Optional Changes
- If you use some resources from VB ImageProcessor, you will have to replace it, as it's now private to the SDK.

## From 7.0.0 to 7.1.0
#### Required Changes
- As part of the security improving efforts a `candidateHash` and `referenceHash` have been added to the [BiometricMatchParameters](../Features/BiometricMatch/BiometricMatch_Index.md#initiate-match), these can be found in the generated reports.
- Similarly, the build subject operation needs the generated `ProcessReport` and `DocumentReaderReport` that include the above hashes to verify data integrity. If you already use these parameters on the [BuildSubjectParameters](../Features/SubjectManagement/SubjectManagement_Index.md#subject-operations) you don't need to take any action.
- The package name now needs to be added to the backoffice. You may need to contact Vision-Box for this update.

#### Optional Changes
- Add a public key on the [initial configuration](../index.md#apiconfig) together with a private key setup on the backoffice to ensure encrypted requests.

## From 5.2.3 to 7.0.0
### Required Changes
- Replace the signatures that do not use the ActivityLauncher contract;
- Remove the `get`, `update` and `delete` `Subject` operations. You should now save the `Subject` locally if you want to have a copy to check later. Updating a `Subject` is no longer supported as well so, you must create a new one if you want to for example, add a boarding pass;
- Handle errors by new field ErrorType instead of checking every possible errors;
- Filter through Biometrics by their source: Face, Chip or OCR;
- Rename enums to PascalCase, MALE is now Male, etc.

## From 5.2.1 to 5.2.2
#### Required Changes
- Contact Vision-Box to update apiKey used before testing new version. (Threshold values changed)

## From 5.1.0 to 5.2.0
#### Required Changes
- Update camera2 library dependency to 1.2.3

#### Optional Changes
- If you are using a value of less than 10 seconds or higher than 60 seconds for either the scanner or rfid reader timeout in  **ReadDocumentParameters** you need to change the value;
- It's no longer possible to disable the scanner or rfid reader timeout in  **ReadDocumentParameters**.
- The default face capture frame is now oval, to keep using the rectangular change the **BiometricFaceCaptureParameters frameFormat**
- Refactor any preview custom view that you might be using to be an independent activity/fragment in your own flow.
- Refactor any error custom view that you might be using to be an independent activity/fragment in your own flow.
- Remove success custom views that you might be using as they no longer exist.
- Remove FaceCapture BiometricProcessView and FaceProcessView as they were merged into the loading view.
- Update remaining custom views with their new contracts.

## From 5.0.3 to 5.1.0
#### Required Changes
- Remove the parameter *showLivenessIcon* from *BiometricFaceCaptureParameters*
#### Optional Changes
- Add parameter includeTemplate in BiometricMatchParameters to receive a template.

## From 5.0.1 to 5.0.3
#### Optional Changes
- Remove the context parameter from the "startDatabaseUpdate" method in the facade
- The error parameter in the **RegulaDatabaseListener**'s unableToPrepareDatabase method is now optional"

## From 4.2.5 to 5.0.1
### Gradle
- Update minSdkVersion from 21 to 23;
- Update compileSdkVersion to 31;

### SDK
#### Required Changes
- The DataResultExtra class and ResultCode class's are now internal and you can handle the feature's result using our ResultHandler created for each feature. This feature ResultHandler will return a model containing the result of the feature. Check the "Handle Results" section of each feature to understand how to handle results.
- Rename BiometricMatchParameters path to "com.visionbox.mobileid.sdk.enrolment.data.biometricFaceMatch.BiometricMatchParameters";
- Rename SubjectBuilderError path to "com.visionbox.mobileid.sdk.enrolment.data.subject.subjectBuilder.error.SubjectBuilderError";
- Rename BuildSubjectParameters path to "com.visionbox.mobileid.sdk.enrolment.data.subject.subjectBuilder.BuildSubjectParameters";
- Rename SubjectPermissionDenied to SubjectPermissionDeniedError and rename SubjectNotFound to SubjectNotFoundError;
- Removed Vision-Box parameters from the **BiometricFaceCaptureParameters**. These configurations are now on backoffice;
- Removed Vision-Box parameters from the **BiometricMatchParameters**. These configurations are now on backoffice;
- Removed **Subject**'s **validateBiometricQuality** configuration. This configuration is now on backoffice;
- Removed BoardingPassScanConfig. The Boarding Pass configuration is now on backend level;
- All Serializable classes changed to Parcelable. Check your onActivityResult methods and change "getSerializableExtra" to "getParcelableExtra";
- Biometric Face Match and Subject features won't return a result, instead the results are obtained using the Android onActivityResult method. Check README for information on how to handle the results for these two features and also how you can use custom views for these features if you need it;
- The methods "addBoardingPass" and "deleteBoardingPass" of the Enrolment won't return direct response, the behavior should be the same of the other Subject Enrolment methods;
- Removed RX module;
- The "buildSubject" enrolment method has a new parameter:
```kotlin
fun buildSubject(activity: Activity, params: BuildSubjectParameters)
```
#### Optional Changes
- If you are using fragments, you can now change to the new Enrolment methods that support Fragments;
```kotlin
// Example:
fun readDocument(context: Context, params: DocumentReaderParameters, resultLauncher: ActivityResultLauncher<Intent>)
```
- Removed localization support from backend, if you used our screens and our localization definition from backoffice, you must now create your own files.
