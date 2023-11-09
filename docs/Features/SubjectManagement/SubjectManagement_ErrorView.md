# Error View

When the showErrors flag is set to true in one of the Subject parameters classes, then any error that happens in this feature will show a default screen with some information.
You can either customize this screen to your branding or set the flag to false and handle the error in your own activity.

[//]: # (TODO - DELETE COMMENT AFTER INSERTING IMAGE)
[//]: # (![Biometric Face Capture Example]&#40;Assets/SM_Error.PNG "Subject Management Default Error Screen"&#41;{: style="height:600px;width:300px;display: block; margin: 0 auto"})

It contains a title(1), a message(2), an image(3), a warning icon(4), a list item layout(5), a retry button(6) and a background that can be customized. 

## Branding

You can apply your own branding to our screens by overriding the resources we use.

### Text resources

=== "Android"

    You can add your own texts and localization by overriding the following string resources:
    ```xml
    <string name="feature_failure_title_sdk_enrolment">There\'s something wrong</string>
    <string name="feature_failure_subtitle_sdk_enrolment">Check the items below:</string>
    ```

=== "iOS"

    ``` swift
    // TODO
    ```

### Colors
=== "Android"

    You can change the text colors by overriding the following color resource (It affects all texts):
    ```xml
    <color name="colorOverlayInvalidTxtSdkEnrolment">#1A1C1E</color>
    ```

    You can change the background color by overriding the following color resource:
    ```xml
    <color name="colorOverlayInvalidBgSdkEnrolment">#F1F0F4</color>
    ```

=== "iOS"

    ``` swift
    // TODO
    ```

### Styles
=== "Android"

    You can extend the styles we use and override any properties (textColor, textSize, fontFamily, etc...) you want.
    ```xml
    <style name="Theme.Sdk.Enrolment.TextView.Dark.Title.Centered">
    <style name="Theme.Sdk.Enrolment.TextView.Dark.Subtitle.Centered">
    ```
    Note: It will affect every component that uses the same style.

=== "iOS"

    ``` swift
    // TODO
    ```

### Image

=== "Android"

    You can change the loading image by adding a drawable with this name:
    ```xml
    ic_subject_loading.xml
    ```
    The image we are using is 232x232dp.

=== "iOS"
    
    ``` swift
    // TODO
    ```
