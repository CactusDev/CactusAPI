import sys
import pytest
from app.util import helpers

VALID_LOOKUP_DATA = {
    "token": "paradigmshift3d",
    "name": "spam"
}


@pytest.mark.parametrize("table_name,lookup,result,code", [
    ("commands", VALID_LOOKUP_DATA, {}, 200),
    ("comands", VALID_LOOKUP_DATA, None, 404),  # Should 404, nonexistant table
])
def test_delete_soft(table_name, lookup, result, code):
    # NOTE: Requires commands for multiple users added to the testing DB
    response, res_code = helpers.delete_soft(table_name, **lookup)
    assert response == result
    assert res_code == code
