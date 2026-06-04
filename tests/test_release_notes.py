import unittest

from maintainerkit.release_notes import build_release_notes, parse_commit_line, parse_commit_lines


class ReleaseNotesTests(unittest.TestCase):
    def test_parse_conventional_commit(self):
        entry = parse_commit_line("feat(cli): add triage command")

        self.assertIsNotNone(entry)
        self.assertEqual(entry.kind, "feat")
        self.assertEqual(entry.scope, "cli")
        self.assertEqual(entry.description, "add triage command")
        self.assertEqual(entry.section, "Added")

    def test_parse_breaking_change_marker(self):
        entry = parse_commit_line("refactor!: rename configuration keys")

        self.assertIsNotNone(entry)
        self.assertTrue(entry.breaking)
        self.assertEqual(entry.section, "Changed")

    def test_build_release_notes_groups_sections(self):
        entries = parse_commit_lines(
            [
                "feat: add checklist command",
                "fix: preserve unknown commits",
                "docs: update readme",
            ]
        )

        notes = build_release_notes(entries, "v0.1.0")

        self.assertIn("# v0.1.0", notes)
        self.assertIn("## Added", notes)
        self.assertIn("## Fixed", notes)
        self.assertIn("## Documentation", notes)


if __name__ == "__main__":
    unittest.main()

