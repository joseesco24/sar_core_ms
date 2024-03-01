collect_request_creation_req_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "request": {"productionCenterId": 123456789, "collectDate": "12/12/2024"},
                "waste": [
                    {
                        "type": 1,
                        "weightInKg": 18.2,
                        "volumeInL": 19.0,
                        "packaging": 1,
                        "description": "nuclear wastes",
                        "note": "this is a note",
                    },
                    {"type": 2, "weightInKg": 18.9, "volumeInL": 18.4, "packaging": 4, "description": "bone scan wastes"},
                ],
            }
        ]
    }
}

collect_request_creation_res_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "request": {"productionCenterId": 123456789, "collectDate": "12/12/2024", "id": "e1899fe3-2ebf-4fcd-b168-922f75a34253"},
                "waste": [
                    {
                        "weightInKg": 18.2,
                        "volumeInL": 19.0,
                        "description": "nuclear wastes",
                        "packaging": 1,
                        "requestId": "e1899fe3-2ebf-4fcd-b168-922f75a34253",
                        "note": "this is  a note",
                        "type": 1,
                        "id": "fa1934fa-56a8-4397-80d6-28913ff2927b",
                    },
                    {
                        "weightInKg": 18.9,
                        "volumeInL": 18.4,
                        "description": "bone scan wastes",
                        "packaging": 4,
                        "requestId": "e1899fe3-2ebf-4fcd-b168-922f75a34253",
                        "note": None,
                        "type": 2,
                        "id": "ea16dbfd-44a4-4ecb-adb4-dcad64b9f23e",
                    },
                ],
            }
        ]
    }
}
