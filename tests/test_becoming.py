import unittest
from becoming import runner

class TestBecomingPrototype(unittest.TestCase):
    def test_rejects_incomplete_record(self):
        with self.assertRaises(ValueError):
            runner.validate_output({"chosen_question": "not enough"})
        with self.assertRaises(ValueError):
            runner.validate_output({key: "" for key in runner.FIELDS})
        complete = {key: "A carefully considered thought" for key in runner.FIELDS}
        self.assertEqual(runner.validate_output(complete), complete)

    def test_rejects_incomplete_model_call(self):
        with self.assertRaises(ValueError):
            runner.extract_output({"status": "incomplete", "output": []})
        with self.assertRaises(ValueError):
            runner.extract_output({"status": "completed", "output": []})

    def test_stateless_has_no_inherited_history(self):
        self.assertEqual(runner.packet_for("stateless")["approved_prior_public_sessions"], [])

    def test_dry_run_requires_no_credentials(self):
        self.assertEqual(runner.main(["--dry-run", "--condition", "stateless"]), 0)

if __name__ == "__main__":
    unittest.main()
