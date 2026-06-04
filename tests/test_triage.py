import unittest

from maintainerkit.triage import WorkItem, analyze_item


class TriageTests(unittest.TestCase):
    def test_security_issue_routes_to_private_review(self):
        result = analyze_item(
            WorkItem(
                number=7,
                title="Possible token leak in logs",
                body="Verbose logs expose a secret token.",
            )
        )

        self.assertEqual(result.priority, "P0")
        self.assertIn("security", result.suggested_labels)
        self.assertEqual(result.route, "security review")
        self.assertIn("private security process", result.next_action)

    def test_bug_without_reproduction_gets_needs_repro(self):
        result = analyze_item(
            WorkItem(
                number=9,
                title="Crash when opening settings",
                body="The settings page crashes.",
            )
        )

        self.assertIn("bug", result.suggested_labels)
        self.assertIn("needs-repro", result.suggested_labels)
        self.assertIn("minimal reproduction", result.next_action)

    def test_regression_gets_specific_next_action(self):
        result = analyze_item(
            WorkItem(
                number=10,
                title="Regression after upgrading",
                body="Expected login to work. Actual result is a 500 error.",
            )
        )

        self.assertEqual(result.priority, "P1")
        self.assertIn("last known good version", result.next_action)

    def test_debug_does_not_match_bug_keyword(self):
        result = analyze_item(
            WorkItem(
                number=11,
                title="Possible token leak in debug logs",
                body="Verbose logs expose a secret token.",
            )
        )

        self.assertIn("security", result.suggested_labels)
        self.assertNotIn("bug", result.suggested_labels)
        self.assertNotIn("needs-repro", result.suggested_labels)

    def test_large_pr_gets_review_planning(self):
        result = analyze_item(
            WorkItem(
                number=11,
                title="feat: import workspace data",
                body="Adds import flow.",
                item_type="pr",
                changed_files=20,
                additions=900,
                deletions=40,
            )
        )

        self.assertEqual(result.priority, "P2")
        self.assertIn("needs-split", result.suggested_labels)
        self.assertEqual(result.route, "maintainer review planning")


if __name__ == "__main__":
    unittest.main()
