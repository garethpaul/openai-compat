import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryPolicyTests(unittest.TestCase):
    def run_checker(self, mutate=None):
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repo"
            repository.mkdir()
            tracked = subprocess.run(
                ["git", "ls-files"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            for relative_path in tracked:
                source = ROOT / relative_path
                destination = repository / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                if source.is_symlink():
                    destination.symlink_to(os.readlink(source))
                else:
                    shutil.copy2(source, destination)
            subprocess.run(["git", "init", "--quiet"], cwd=repository, check=True)
            subprocess.run(["git", "add", "--all"], cwd=repository, check=True)
            if mutate:
                mutate(repository)
            return subprocess.run(
                ["python3", "scripts/check-baseline.py"],
                cwd=repository,
                text=True,
                capture_output=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

    def test_secure_composed_repository_passes(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_symlinked_required_policy(self):
        def mutate(repository):
            policy = repository / "SECURITY.md"
            policy.unlink()
            policy.symlink_to("README.md")

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("regular file", result.stderr)

    def test_rejects_oversized_tracked_document(self):
        def mutate(repository):
            readme = repository / "README.md"
            readme.write_bytes(readme.read_bytes() + b"x" * (1024 * 1024))

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("size limit", result.stderr)

    def test_rejects_nested_untracked_implementation_artifact(self):
        def mutate(repository):
            source = repository / "src" / "server.py"
            source.parent.mkdir()
            source.write_text("print('runtime')\n", encoding="utf-8")

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("implementation artifact", result.stderr)

    def test_rejects_tracked_runtime_file(self):
        def mutate(repository):
            source = repository / "server.py"
            source.write_text("print('runtime')\n", encoding="utf-8")
            subprocess.run(["git", "add", "server.py"], cwd=repository, check=True)

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("new tracked surfaces", result.stderr)

    def test_rejects_workflow_write_permission(self):
        def mutate(repository):
            workflow = repository / ".github" / "workflows" / "check.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "contents: read", "contents: write"
                ),
                encoding="utf-8",
            )

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Python matrix", result.stderr)

    def test_rejects_live_network_workflow_step(self):
        def mutate(repository):
            workflow = repository / ".github" / "workflows" / "check.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "run: make check", "run: curl https://api.openai.com/v1/models"
                ),
                encoding="utf-8",
            )

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Python matrix", result.stderr)

    def test_rejects_missing_openai_route_contract(self):
        def mutate(repository):
            contract = repository / "docs" / "compatibility-contract.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "exact `/v1/...` path", "generic endpoint path"
                ),
                encoding="utf-8",
            )

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exact `/v1/...` path", result.stderr)

    def test_rejects_missing_openai_error_envelope_contract(self):
        def mutate(repository):
            contract = repository / "docs" / "compatibility-contract.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "`error.message`, `error.type`, `error.param`, and `error.code`",
                    "documented error fields",
                ),
                encoding="utf-8",
            )

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error.message", result.stderr)

    def test_rejects_missing_stream_done_contract(self):
        def mutate(repository):
            contract = repository / "docs" / "compatibility-contract.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "`data: [DONE]`", "a terminal event"
                ),
                encoding="utf-8",
            )

        result = self.run_checker(mutate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("data: [DONE]", result.stderr)


if __name__ == "__main__":
    unittest.main()
