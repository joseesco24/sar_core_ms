waste_clasification_req_ex = {"json_schema_extra": {"examples": [{"stateWaste": "solid", "weightInKg": 100, "isotopesNumber": 31}]}}

waste_clasification_res_ex = {"json_schema_extra": {"examples": [{"storeType": 4}]}}

waste_filter_by_status_request_dto = {"json_schema_extra": {"examples": [{"processStatus": 9}]}}

waste_update_status_req = {"json_schema_extra": {"examples": [{"id": "97ed79c5-eb28-4f80-93b1-1d5800c95bc9", "processStatus": 9}]}}

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
                "storeId": 1,
                "create": "2024-03-02 23:22:57.000000",
                "update": "2024-03-02 23:22:57.000000",
            }
        ]
    }
}

waste_full_data_response_list_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "values": [
                    {
                        "id": "09fe7cbc-8acf-4147-9b45-d3d79f19ceda",
                        "requestId": "f064c86e-25da-476b-ba71-956c434be4c0",
                        "type": 2,
                        "packaging": 4,
                        "processStatus": 9,
                        "weightInKg": 18.9,
                        "volumeInL": 18.4,
                        "isotopesNumber": None,
                        "stateWaste": None,
                        "storeType": None,
                        "description": "bone scan wastes",
                        "note": None,
                        "storeId": 1,
                        "create": "2024-03-03 05:08:30.000000",
                        "update": "2024-03-03 05:08:30.000000",
                    },
                    {
                        "id": "1bf4296e-4ad9-49d9-96b0-4ca4af9a7fcb",
                        "requestId": "f4cd1133-00ce-460a-a81c-e298a804a860",
                        "type": 1,
                        "packaging": 4,
                        "processStatus": 9,
                        "weightInKg": 18.2,
                        "volumeInL": 19.0,
                        "isotopesNumber": None,
                        "stateWaste": None,
                        "storeType": None,
                        "description": "nuclear wastes",
                        "note": "this is a note",
                        "storeId": 1,
                        "create": "2024-03-03 02:54:12.000000",
                        "update": "2024-03-03 02:54:12.000000",
                    },
                ]
            }
        ]
    }
}
