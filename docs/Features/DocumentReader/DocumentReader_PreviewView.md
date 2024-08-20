# Preview View

**From version 8 onwards, the preview management changed in the SDK to make it easier to integrate.**

To improve flexibility in the preview screen, the optional preview screen has been removed.

To add a preview feature to your app you can follow the example from our sample app, where we provide an example with the same user interface.

=== "Android"

    Example can be found here: [FaceCapturePreview](https://github.com/vbmobile/mobileid-android-sample/tree/main/app/src/main/java/com/example/sample_app_android/presentation/readDocument/preview/DocumentPreviewActivity.kt)
    ```kotlin
    private fun showDocumentDetails(documentPreviewViewModel: DocumentPreviewViewModel) {
        binding.documentHeader.setup(
            DocumentHeaderViewModel(
                surname = documentPreviewViewModel.documentHeader.surname,
                givenName = documentPreviewViewModel.documentHeader.givenNames,
                genderAndAge = "${documentPreviewViewModel.documentHeader.sex}, ${documentPreviewViewModel.documentHeader.age}",
                portrait = documentPreviewViewModel.getPortraitImage(this),
                status = documentPreviewViewModel.documentData.rfidStatusRes,
                statusText = documentPreviewViewModel.documentData.rfidStatusTextRes
            )
        )

        val hasErrorsBesidesExpiration = if(documentReaderReport.status.contains(DocumentDataStatus.EXPIRED_DOCUMENT)) {
            documentReaderReport.status.any { it != DocumentDataStatus.EXPIRED_DOCUMENT && it != DocumentDataStatus.RFID_PASSIVE_AUTHENTICATION }
        } else {
            documentReaderReport.status.any()
        }

        if (documentReaderReport.status.contains(DocumentDataStatus.USER_SKIPPED_RFID)
            || documentReaderReport.status.contains(DocumentDataStatus.RFID_NFC_NOT_SUPPORTED)
            || documentReaderReport.status.contains(DocumentDataStatus.RFID_PERMISSION_NOT_GRANTED)
        ) {
            binding.txtDocumentPreviewTitle.text =
                getString(R.string.document_preview_rfid_skipped_title)
            binding.txtDocumentPreviewSubtitle.text =
                getString(R.string.document_preview_rfid_undefined_subtitle)
        } else if (documentReaderReport.rfidStatus == RFIDStatus.ERROR && hasErrorsBesidesExpiration) {
            binding.txtDocumentPreviewTitle.text =
                getString(R.string.document_preview_rfid_error_title)
            binding.txtDocumentPreviewSubtitle.text =
                getString(R.string.document_preview_rfid_error_subtitle)
        } else {
            if (documentReaderReport.rfidStatus == RFIDStatus.SUCCESS) {
                binding.txtDocumentPreviewTitle.text =
                    getString(R.string.document_preview_rfid_success_title)
                binding.btnRepeat.visibility = GONE
            } else {
                binding.txtDocumentPreviewTitle.text =
                    getString(R.string.document_preview_rfid_undefined_title)
            }
            binding.txtDocumentPreviewSubtitle.visibility = GONE
        }

        when (documentPreviewViewModel.documentData.documentType) {
            DocumentType.Passport -> {
                binding.ppvPassportView.setDocumentData(documentPreviewViewModel.documentData)
                binding.ppvPassportView.visibility = VISIBLE
                binding.pvvVisaView.visibility = GONE
                binding.pidcvIdCardView.visibility = GONE
                binding.pdlvDriverLicenseView.visibility = GONE
                binding.podvOtherDocsView.visibility = GONE
            }

            DocumentType.Visa -> {
                binding.pvvVisaView.setDocumentData(documentPreviewViewModel.documentData)
                binding.ppvPassportView.visibility = GONE
                binding.pvvVisaView.visibility = VISIBLE
                binding.pidcvIdCardView.visibility = GONE
                binding.pdlvDriverLicenseView.visibility = GONE
                binding.podvOtherDocsView.visibility = GONE
            }

            DocumentType.IdCard -> {
                binding.pidcvIdCardView.setDocumentData(documentPreviewViewModel.documentData)
                binding.ppvPassportView.visibility = GONE
                binding.pvvVisaView.visibility = GONE
                binding.pidcvIdCardView.visibility = VISIBLE
                binding.pdlvDriverLicenseView.visibility = GONE
                binding.podvOtherDocsView.visibility = GONE
            }

            DocumentType.DrivingLicense -> {
                binding.pdlvDriverLicenseView.setDocumentData(documentPreviewViewModel.documentData)
                binding.ppvPassportView.visibility = GONE
                binding.pvvVisaView.visibility = GONE
                binding.pidcvIdCardView.visibility = GONE
                binding.pdlvDriverLicenseView.visibility = VISIBLE
                binding.podvOtherDocsView.visibility = GONE
            }

            else -> {
                binding.podvOtherDocsView.setDocumentData(documentPreviewViewModel.documentData)
                binding.ppvPassportView.visibility = GONE
                binding.pvvVisaView.visibility = GONE
                binding.pidcvIdCardView.visibility = GONE
                binding.pdlvDriverLicenseView.visibility = GONE
                binding.podvOtherDocsView.visibility = VISIBLE
            }
        }

        documentPreviewViewModel.documentDataRowItems?.let {
            binding.documentDetails.setup(it)
        }
    }
    ```

=== "iOS"

    // TODO
