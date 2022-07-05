import pytest
from db_helper import parse_json_to_compounds


class TestParse:
    def generate_object(self, id):
        return {f"test_compound_{id}": [
            {"name": f"test_name_{id}",
             "formula": f"test_formula_{id}",
             "inchi": f"test_inchi_{id}",
             "inchi_key": f"test_inchi_key_{id}",
             "smiles": f"test_smiles_{id}",
             "cross_links": [
                 {"resource": "test_resource1",
                  "resource_id": "test_resource_id1"},
                 {"resource": "test_resource2",
                  "resource_id": "test_resource_id2"},
                 {"resource": "test_resource3",
                  "resource_id": "test_resource_id3"}
             ]
             }
        ]}

    def generate_data(self, n=1):
        result = {}
        for i in range(n):
            result.update(self.generate_object(i))
        return result

    def test_empty_json_input(self):
        assert [] == parse_json_to_compounds({})

    def test_parse_to_object(self):
        json = self.generate_data()
        result = parse_json_to_compounds(json)
        number_of_objects = len(result)
        assert number_of_objects == 1
        assert result[0].cross_links_count == 3

    def test_parse_to_objects5(self):
        json = self.generate_data(5)
        result = parse_json_to_compounds(json)
        number_of_objects = len(result)
        assert number_of_objects == 5
        assert result[0].cross_links_count == 3
