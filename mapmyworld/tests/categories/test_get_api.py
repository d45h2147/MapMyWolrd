import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

response_categories_schema = {
    "type": "object",
    "properties": {
        "pagination": {
            "type": "object",
            "properties": { }
        },
        "data": {
            "type": "array",
            "items": {}
        },
        "total": {
            "type": "integer"
        },
    },
    "required": ["pagination", "data", "total"]
}


@pytest.mark.parametrize("limit, page, expected_status_code", [
    (1, 1, 200),
    (2, 30, 200),
])
def test_categories_endpoint_parametrized(client, limit, page, expected_status_code):
    url = f'/api/v1/categories?limit={limit}&page={page}'
    response = client.get(url)
    print(response.status_code)
    assert response.status_code == expected_status_code

    try:
        validate(instance=response.json, schema=response_categories_schema)
        # Si no se lanza una excepción, la respuesta es válida
    except ValidationError as e:
        pytest.fail(f"La respuesta no cumple con el esquema esperado: {e}")
