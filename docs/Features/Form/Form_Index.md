# Form

Form is a feature that allows you to collect additional data and attach it to created subjects. The supported built-in data is currently:

- Email
- Text

You can then submit this data, alongside your subject, through the [AddSubjectParameters](../SubjectManagement/SubjectManagement_Index.md#subject-operations).

To start the form feature, you can use the enrolment method

=== "Android"

    ```kotlin
       /**
     * @param activity [Activity] that will launch the face capture feature
     * @param onFormCompletion [OnFormCompletion] callback to handle Success and Error scenarios
     */
    fun startForm(
        activity: Activity,
        onFormCompletion: OnFormCompletion,
    )
    ```

=== "iOS"

    ```swift
    // MARK: - FormFeature
    /// - Parameters:
    ///   - parameters: Parameters for Form feature flow.
    ///   - viewController: The view controller that will present the FormFeature.
    ///   - completionHandler: The completion handler to call when the boarding pass parser feature is finished.
    ///     This completion handler takes the following parameter:
    ///
    ///     Result<FormReport, FormError>
    ///     Where `FormReport` contains  the form data and
    ///     `FeatureError` the possible errors that may occur during the process.
    func startForm(parameters: FormParameters, viewController: UIViewController, completionHandler: @escaping (Result<FormReport, FormError>) -> Void)
    ```

## Handle Result

=== "Android"

    Here's how you can get the result by using the form callback:

    ```kotlin
    interface OnFormCompletion {
        fun onFormSuccess(formAnswer: FormAnswer)
        fun onFormError(formError: FormError)
    }

    ```

    FormAmswer on the success callback is defined as:

    ```kotlin
    data class FormAnswer(
        val formId: String,
        val answers: List<Answer>
    )
    ```

=== "iOS"

    Here's how you can get the report by calling the startForm function.
    
    ```swift
    enrolment?.startForm(parameters: params, viewController: view, completionHandler: { result in
        switch result {
        case .success(let report):
            // save report 
            completion(.success(()))
        case .failure(let error):
            completion(.failure(error))
        }
    })
    ```
    
    The FormReport has the following structure:
    
    ```swift
    public struct FormReport {
        let answer: [FormAnswer]

        init(answer: [FormAnswer]) {
            self.answer = answer
        }
    }  
    ```
    
    The FormAnswer has the following structure:
    
    ```swift
    public class FormAnswer: Codable {
        var formId: String
        var answers: [Answer]
    
        init(formId: String, answers: [Answer]) {
            self.formId = formId
            self.answers = answers
        }
    }
    ```
        
    The Answer has the following structure:
    
    ```swift
    public class Answer: Codable{
        var questionId: String
        var value: String

        init(questionId: String, value: String) {
            self.questionId = questionId
            self.value = value
        }
    }
    ```

The FormError has the following structure:

=== "Android"

    ```kotlin
    data class FormError(
        val userCanceled: Boolean = false,
        val termsAndConditionsAccepted: Boolean = true,
        val featureError: FeatureError? = null
    )
    ```

=== "iOS"

    ```swift
    public class FormError: Error {
        public var userCanceled: Bool
        public var termsAndConditionsAccepted: Bool
        public var featureError: FeatureError
    }
    ```
