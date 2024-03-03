collect_request_creation_req_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "request": {"collectDate": "12/12/2024", "productionCenterId": 123456789},
                "waste": [
                    {"description": "nuclear wastes", "note": "this is a note", "packaging": 4, "type": 1, "volumeInL": 19, "weightInKg": 18.2},
                    {"description": "bone scan wastes", "packaging": 4, "type": 2, "volumeInL": 18.4, "weightInKg": 18.9},
                ],
            }
        ]
    }
}

collect_request_creation_res_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "waste": [
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
                        "create": "2024-03-03 02:54:12.000000",
                        "update": "2024-03-03 02:54:12.000000",
                    },
                    {
                        "id": "a654077f-c7b3-426d-baa6-c9c251006f48",
                        "requestId": "f4cd1133-00ce-460a-a81c-e298a804a860",
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
                        "create": "2024-03-03 02:54:12.000000",
                        "update": "2024-03-03 02:54:12.000000",
                    },
                ],
                "request": {
                    "id": "f4cd1133-00ce-460a-a81c-e298a804a860",
                    "collectDate": "12/12/2024",
                    "processStatus": 9,
                    "productionCenterId": 123456789,
                    "create": "2024-03-03 02:54:12.000000",
                    "update": "2024-03-03 02:54:12.000000",
                },
            }
        ]
    }
}
