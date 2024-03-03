waste_clasification_req_ex = {"json_schema_extra": {"examples": [{"stateWaste": "solid", "weightInKg": 100, "isotopesNumber": 31}]}}

waste_clasification_res_ex = {"json_schema_extra": {"examples": [{"storeType": 4}]}}

collect_request_classify_req_ex = {"json_schema_extra": {"examples": [{"isotopesNumber": 1942, "stateWaste": 7, "storeId": 4, "wasteId": "97ed79c5-eb28-4f80-93b1-1d5800c95bc9"}]}}

collect_request_classify_res_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "id": "97ed79c5-eb28-4f80-93b1-1d5800c95bc9",
                "requestId": "4c9b6703-3b9b-402e-8930-d765bcc03586",
                "type": 1,
                "packaging": 4,
                "processStatus": 9,
                "weightInKg": 18.2,
                "volumeInL": 19.0,
                "isotopesNumber": 1942.0,
                "stateWaste": 7,
                "storeType": 4,
                "description": "nuclear wastes",
                "note": "this is a note",
                "create": "2024-03-02 23:22:57.000000",
                "update": "2024-03-02 23:22:57.000000",
            }
        ]
    }
}
