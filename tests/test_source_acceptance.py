import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import accept_ecosystem as acceptance


class SourceAcceptanceTests(unittest.TestCase):
    def test_ignored_build_inputs_are_excluded_and_mutation_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()

            def git(*args):
                return subprocess.check_output(
                    ["git", *args], cwd=repo, text=True
                ).strip()

            git("init", "-q")
            git("config", "user.email", "test@example.invalid")
            git("config", "user.name", "test")
            (repo / ".gitignore").write_text("injected.py\n")
            (repo / "source.py").write_text("original")
            git("add", ".")
            git("commit", "-qm", "fixture")
            commit = git("rev-parse", "HEAD")
            (repo / "injected.py").write_text("ignored input")
            acceptance.clean_commit(repo, commit)
            destination = root / "build"
            snapshot = acceptance.materialize_commit(repo, commit, destination)
            self.assertFalse((destination / "injected.py").exists())
            acceptance.verify_source_snapshot(destination, snapshot)
            (destination / "source.py").write_text("changed by backend")
            with self.assertRaisesRegex(ValueError, "mutated committed source"):
                acceptance.verify_source_snapshot(destination, snapshot)
