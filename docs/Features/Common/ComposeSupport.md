# Jetpack Compose Custom Views

In Android, there's a new way to create the layouts programmatically using Jetpack compose library.
Our layouts are currently in traditional XML files but we also want to give the option to use compose when needed.
This page will briefly explain how you can wrap a composable in a xml layout to use it as a custom view.

## Create a Composable Wrapper layout file

First we are going to need a layout file that contains a compose view.

Since we want to make the whole screen a composable, then it's as simple as adding a Compose View that takes the whole space.
Create a new layout file, call it, for example, composable_wrapper.xml and paste the following code there:

```xml
<?xml version="1.0" encoding="utf-8"?>
<merge
xmlns:android="http://schemas.android.com/apk/res/android"
xmlns:tools="http://schemas.android.com/tools"
android:layout_width="match_parent"
android:layout_height="match_parent"
tools:parentTag="androidx.constraintlayout.widget.ConstraintLayout">

    <androidx.compose.ui.platform.ComposeView
        android:id="@+id/compose_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent">

    </androidx.compose.ui.platform.ComposeView>

</merge>
```

Now that we have the composable wrapper, this layout file can be used for all the custom views you want to implement.

For example, let's implement the document reader loading as a composable custom view.

## Create the custom view class
Create a new class, let's call it CustomLoadingView that's going to extend a ConstraintLayout.

Paste the following code and make sure to import everything you need.

```kotlin
class CustomLoadingView(context: Context) : ConstraintLayout(context), ICustomDocumentReader.LoadingView { 
    private val binding: ComposeWrapperBinding
    private var isLoading by mutableStateOf(false)
    private var title by mutableStateOf("")
    private var message by mutableStateOf("")
    
    init {
        binding = ComposeWrapperBinding.inflate(
            LayoutInflater.from(context),
            this
        )
        binding.composeView.setContent {
            LoadingViewCompose()
        }
    }

    override fun onPreFeatureLoading(message: String) {
        isLoading = true
        title = "Loading..."
        this.message = message
    }

    override fun onPostFeatureLoading() {
        isLoading = false
        title = ""
        this.message = ""
    }

    override fun onDownloadProgressChanged(progress: Int) {
        isLoading = true
        title = "Downloading Resources"
        this.message = "Progress: $progress%"
    }

    override fun hideLoading() {
        isLoading = false
        title = ""
        this.message = ""
    }

    @Composable
    fun LoadingViewCompose() {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (isLoading) {
                // Show loading progress indicator
                CircularProgressIndicator()
            }
            // Show title and message
            Text(
                text = title,
                color = Color.Black,
                fontSize = 20.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            Text(
                text = message,
                color = Color.Gray,
                fontSize = 16.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(bottom = 16.dp)
            )
        }
    }
}
```

Breaking this code down, we have a constraint layout, that implements the loading view contract, changing the values of the spinner, title and message according to what is happening in the moment. 
Basically the same we would have with a traditional xml custom view.

The difference comes in the composable function, that's a very simple UI to serve as an example. 
It contains a spinner which visibility is controlled by a state variable.
And two text fields which value will also change during the execution.

In the constructor of this class, we make sure to inflate the composable wrapper we added in the first place and pass the composable into the ComposeView.

## Pass the custom view into the builder
After this class is created and configured, we need to inject it to the custom views list as we do with regular custom views as well.

```kotlin
val enrolmentModule = module {
    single<IEnrolment> {
        EnrolmentBuilder.of(
            context = this@ComposeApp,
            config = enrolmentConfig
        ).withDocumentReaderConfig(documentReaderConfig)
            .withDocumentReaderCustomViews(
                DocumentReaderCustomViews(
                    loadingView = CustomLoadingView::class.java
                )
            ).build()
    }
}
```

And that's it, when you run the document reader feature, the loading screen will show up using the UI defined in the composable.