import importlib.util
import pathlib
import unittest


SCRIPT = (
    pathlib.Path(__file__).resolve().parents[1]
    / "skills_tutorial"
    / "database-schema-validator"
    / "scripts"
    / "validate_schema.py"
)
SPEC = importlib.util.spec_from_file_location("validate_schema", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class SchemaValidatorTests(unittest.TestCase):
    def test_valid_schema_passes(self):
        sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);"
        self.assertEqual(module.validate_schema_text(sql), [])

    def test_drop_table_is_rejected(self):
        errors = module.validate_schema_text("DROP TABLE users;")
        self.assertTrue(any("DROP TABLE" in error for error in errors))

    def test_non_snake_case_table_is_rejected(self):
        errors = module.validate_schema_text(
            "CREATE TABLE UserAccounts (id INTEGER PRIMARY KEY);"
        )
        self.assertTrue(any("snake_case" in error for error in errors))

    def test_missing_id_primary_key_is_rejected(self):
        errors = module.validate_schema_text(
            "CREATE TABLE users (user_id INTEGER PRIMARY KEY);"
        )
        self.assertTrue(any("primary key named 'id'" in error for error in errors))

    def test_empty_schema_is_rejected(self):
        errors = module.validate_schema_text("-- no schema here")
        self.assertTrue(any("No CREATE TABLE" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
