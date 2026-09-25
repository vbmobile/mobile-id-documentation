VERSIONS = {
    "android_enrolment_sdk": "9.2.1",
    "android_doc_scan_mrz_provider": "2.0.9",
    "android_doc_rfid_read_provider": "2.0.9",
    "android_ultralight_provider": "2.0.9",
    "ios_enrolment_sdk": "9.2.4",
    "ios_doc_scan_regula_provider": "2.0.2",
    "ios_doc_scan_mrz_provider": "2.0.6",
    "ios_doc_rfid_read_provider": "2.0.8",
    "ios_ultralight_provider": "2.0.17",
}

def define_env(env):
    env.variables["versions"] = VERSIONS
