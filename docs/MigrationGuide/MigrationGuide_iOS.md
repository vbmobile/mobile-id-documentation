# Migration Guide

## From 5.2.0 to 5.2.1
#### Optional Changes
- Add **CameraConfig** to **BiometricFaceCaptureParameters**

##  From 5.1.0 to 5.2.0

#### Required Changes
- if you are using a value of less than 10 seconds or greater than 60 for the scannerTimeout or rfidTimeout in  **ReadDocumentParameters** you need to change the value.

#### Optional Changes
- if you want to continue with the square frame you need to set the frameShape field of the class *BiometricFaceCaptureParameters* to .square
- Refactor any preview custom view that you might be using to be an independent UIViewController in your own flow.
- Refactor any error custom view that you might be using to be an independent UIViewController in your own flow.
- Update remaining custom views with their new protocols.

##  From 5.0.0 to 5.1.0

#### Required Changes
- Removed liveness status parameter from the **BiometricFaceCaptureParameters**.

#### Optional Changes
- If you are using **BiometricFaceCapturePreviewView** custom view, you must remove the property **livenessStatus**.
- Add parameter includeTemplate in BiometricMatchParameters to receive a template.

## From 4.2.4 to 5.0.0

### CocoaPods
- run pod update & install

#### Required Changes
- Removed BoardingPassScanConfig. The Boarding Pass configuration is now on backend side;
- Removed Vision-Box parameters from the **BiometricFaceCaptureParameters**. These configurations are now on backoffice;
- Removed Vision-Box parameters from the **BiometricMatchParameters**. These configurations are now on backoffice;
- Removed **Subject**'s **validateBiometricQuality** configuration. This configuration is now on backoffice;
- Removed Alamofire lib;
- Removed specific feature loadings and created a generic one, e.g. remove calls for BoardingPassScannerLoadingView & BoardingPassScannerLoadingView and replace it with the new one LoadingOverlayViewType.
- 
#### Optional Changes
- Added new method **startUpdateDatabase** to allow database download. If the method isn't called, then it will be downloaded uppon the first usage of our sdk.
- Removed localization support from backend, if you used our screens and our localization definition from backoffice, you must now create your own files.

