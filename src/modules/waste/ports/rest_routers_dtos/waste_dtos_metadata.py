waste_clasification_req_ex = {"json_schema_extra": {"examples": [{"stateWaste": "solid", "weightInKg": 100, "isotopesNumber": 31}]}}

waste_clasification_res_ex = {"json_schema_extra": {"examples": [{"activityType": 1}]}}

collect_request_classify_req_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "wasteId": "157b3446-52d8-44b7-838e-17575ac63d41",
                "isotopesNumber": 12.2,
                "stateWaste": 1,
                "storeId": 4,
            }
        ]
    }
}

collect_request_classify_res_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "code": 1,
                "message": "Exitoso",
            }
        ]
    }
}