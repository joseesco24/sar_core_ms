collect_request_modify_state_by_id_req_dto = {
    "json_schema_extra": {"examples": [{"collectReqId": "97ed79c5-eb28-4f80-93b1-1d5800c95bc9", "processStatus": 10, "note": "this is a note"}]}
}

collect_request_modify_state_by_id_res_dto = {
    "json_schema_extra": {
        "examples": [
            {
                "id": "09fe7cbc-8acf-4147-9b45-d3d79f19ceda",
                "processStatus": 10,
                "collectDate": "2024/03/03",
                "productionCenterId": 123456789,
                "note": "this is a note",
                "create": "2024-03-03 02:54:12.000000",
                "update": "2024-03-05 12:35:18.000000",
            }
        ]
    }
}

collect_request_id_note_dto = {"json_schema_extra": {"examples": [{"id": "09fe7cbc-8acf-4147-9b45-d3d79f19ceda", "note": "this is a note"}]}}

collect_request_find_by_status_req_dto = {"json_schema_extra": {"examples": [{"processStatus": 9}]}}

collect_request_find_by_status_res_dto = {
    "json_schema_extra": {
        "examples": [
            {
                "values": [
                    {
                        "id": "09fe7cbc-8acf-4147-9b45-d3d79f19ceda",
                        "processStatus": 9,
                        "collectDate": "2024/03/03",
                        "productionCenterId": 123456789,
                        "note": "this is a note",
                        "create": "2024-03-03 02:54:12.000000",
                        "update": "2024-03-03 02:54:12.000000",
                    },
                    {
                        "id": "097d0fd7-847f-4a1c-8f37-0cde338aeaef",
                        "processStatus": 9,
                        "collectDate": "2024/03/08",
                        "productionCenterId": 15,
                        "note": "this is a note",
                        "create": "2024-03-03 22:54:12.000000",
                        "update": "2024-03-03 22:54:12.000000",
                    },
                ]
            }
        ]
    }
}

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
                    "note": "this is a note",
                    "create": "2024-03-03 02:54:12.000000",
                    "update": "2024-03-03 02:54:12.000000",
                },
            }
        ]
    }
}
