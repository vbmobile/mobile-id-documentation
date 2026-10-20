VERSIONS = {
    "android_enrolment_sdk": "9.2.4",
    "android_doc_scan_mrz_provider": "2.0.11",
    "android_doc_rfid_read_provider": "2.0.11",
    "android_ultralight_provider": "2.0.11",
    "ios_enrolment_sdk": "9.2.8",
    "ios_doc_scan_regula_provider": "2.0.2",
    "ios_doc_scan_mrz_provider": "2.0.8",
    "ios_doc_rfid_read_provider": "2.0.8",
    "ios_ultralight_provider": "2.0.17",
}

def define_env(env):
    env.variables["versions"] = VERSIONS
