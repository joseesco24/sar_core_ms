user_creation_req_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "email": "pedro.perez@correo.com",
                "name": "Pedro Alejandro",
                "lastName": "Perez Sarmiento",
            }
        ]
    }
}

user_by_email_req_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "email": "pedro.perez@correo.com",
            }
        ]
    }
}

user_creation_res_ex = {
    "json_schema_extra": {
        "examples": [
            {
                "id": "97ed79c5-eb28-4f80-93b1-1d5800c95bc9",
                "active": True,
                "email": "pedro.perez@correo.com",
                "name": "Pedro Alejandro",
                "lastName": "Perez Sarmiento",
                "create": "2024-03-02 23:22:57.000000",
                "update": "2024-03-02 23:22:57.000000",
            }
        ]
    }
}
