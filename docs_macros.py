VERSIONS = {
    "android_enrolment_sdk": "9.2.x",
    "android_doc_scan_mrz_provider": "2.0.x",
    "android_doc_rfid_read_provider": "2.0.x",
    "android_ultralight_provider": "2.0.x",
    "ios_enrolment_sdk": "9.2.0",
    "ios_doc_scan_regula_provider": "2.0.2",
    "ios_doc_scan_mrz_provider": "2.0.3",
    "ios_doc_rfid_read_provider": "2.0.2",
    "ios_ultralight_provider": "2.0.4",
}

def define_env(env):
    env.variables["versions"] = VERSIONS
