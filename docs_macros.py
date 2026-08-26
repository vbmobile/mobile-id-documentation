VERSIONS = {
    "android_enrolment_sdk": "9.2.0",
    "android_doc_scan_mrz_provider": "2.0.7",
    "android_doc_rfid_read_provider": "2.0.7",
    "android_ultralight_provider": "2.0.7",
    "ios_enrolment_sdk": "9.2.3",
    "ios_doc_scan_regula_provider": "2.0.2",
    "ios_doc_scan_mrz_provider": "2.0.5",
    "ios_doc_rfid_read_provider": "2.0.2",
    "ios_ultralight_provider": "2.0.17",
}

def define_env(env):
    env.variables["versions"] = VERSIONS
