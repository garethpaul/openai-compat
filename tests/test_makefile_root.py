import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakefileRootTests(unittest.TestCase):
    def run_make(self, *arguments, environment=None, prefix="OpenAI Compat's [gate] "):
        with tempfile.TemporaryDirectory(prefix=prefix) as directory:
            checkout = Path(directory)
            makefile = checkout / "Makefile"
            makefile.write_text(
                (ROOT / "Makefile").read_text(encoding="utf-8"), encoding="utf-8"
            )
            env = {"PATH": os.environ.get("PATH", "")}
            if environment:
                env.update(environment)
            return subprocess.run(
                ["make", "--no-print-directory", "-f", str(makefile), *arguments],
                cwd=checkout.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                env=env,
            )

    def run_live_make(self, target, prefix, arguments=(), environment=None):
        with tempfile.TemporaryDirectory() as parent_directory:
            parent = Path(parent_directory)
            checkout = parent / prefix
            checkout.mkdir()
            shutil.copy2(ROOT / "Makefile", checkout / "Makefile")
            (checkout / "scripts").mkdir()
            (checkout / "tests").mkdir()
            for relative_path in (
                "scripts/check-baseline.py",
                "tests/test_repository_policy.py",
                "tests/test_makefile_root.py",
            ):
                (checkout / relative_path).touch()

            bin_directory = parent / "bin"
            bin_directory.mkdir()
            log = parent / "commands.log"
            sentinel = parent / "command-substitution-ran"
            python = bin_directory / "python3"
            python.write_text(
                "#!/bin/sh\nprintf '%s\\t%s\\n' \"$PWD\" \"$*\" >> \"$COMMAND_LOG\"\n",
                encoding="utf-8",
            )
            python.chmod(0o755)
            attacker = bin_directory / "root_attack"
            attacker.write_text(
                "#!/bin/sh\n: > \"$ATTACK_SENTINEL\"\n",
                encoding="utf-8",
            )
            attacker.chmod(0o755)
            env = {
                "ATTACK_SENTINEL": str(sentinel),
                "COMMAND_LOG": str(log),
                "PATH": f"{bin_directory}:{os.environ.get('PATH', '')}",
            }
            if environment:
                env.update(environment)
            result = subprocess.run(
                [
                    "make",
                    "--no-print-directory",
                    "-f",
                    str(checkout / "Makefile"),
                    target,
                    *arguments,
                ],
                cwd=parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                env=env,
            )
            command_log = log.read_text(encoding="utf-8") if log.exists() else ""
            return result, checkout, command_log, sentinel.exists()

    def test_all_targets_preserve_spaced_absolute_makefile_path(self):
        targets = (
            "build",
            "check",
            "lint",
            "root-test",
            "static-check",
            "test",
            "verify",
        )
        for target in targets:
            for name, arguments, environment in (
                ("none", (target,), None),
                ("command", (target, "REPO_ROOT=/tmp/attacker-root"), None),
                ("environment", (target,), {"REPO_ROOT": "/tmp/attacker-root"}),
            ):
                with self.subTest(target=target, override=name):
                    result, checkout, log, attacked = self.run_live_make(
                        target,
                        "OpenAI Compat's [gate] ",
                        arguments=arguments[1:],
                        environment=environment,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertNotIn("/tmp/attacker-root", result.stdout)
                    self.assertFalse(attacked, result.stdout)
                    self.assertIn(str(checkout), log)

    def test_command_line_makefile_list_override_fails_closed(self):
        result = self.run_make("verify", "MAKEFILE_LIST=/tmp/untrusted")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stdout)

    def test_environment_makefile_list_override_fails_closed(self):
        result = self.run_make(
            "-e", "verify", environment={"MAKEFILE_LIST": "/tmp/untrusted"}
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stdout)

    def test_make_invocation_variable_overrides_fail_closed(self):
        for variable, diagnostic in (
            ("MAKEFLAGS=-n", "MAKEFLAGS must not be overridden"),
            (
                "MAKEFILES=/tmp/untrusted",
                "MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone",
            ),
        ):
            with self.subTest(variable=variable):
                result = self.run_make("check", variable)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(diagnostic, result.stdout)

    def test_later_makefile_cannot_replace_or_append_public_recipes(self):
        for separator in (":", "::"):
            with self.subTest(separator=separator), tempfile.TemporaryDirectory() as directory:
                checkout = Path(directory) / "checkout"
                checkout.mkdir()
                makefile = checkout / "Makefile"
                makefile.write_text(
                    (ROOT / "Makefile").read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
                later_makefile = checkout / "later.mk"
                marker = checkout / "later-recipe-ran"
                later_makefile.write_text(
                    (
                        "build check lint root-test static-check test "
                        f"verify{separator}\n\t@touch '{marker}'\n"
                    ),
                    encoding="utf-8",
                )
                result = subprocess.run(
                    [
                        "make",
                        "--no-print-directory",
                        "-f",
                        str(makefile),
                        "-f",
                        str(later_makefile),
                        "check",
                    ],
                    cwd=checkout.parent,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                    env={"PATH": os.environ.get("PATH", "")},
                )

                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertFalse(marker.exists(), result.stdout)

    def test_non_executing_and_error_ignoring_modes_fail_closed(self):
        for flag in (
            "-n",
            "--just-print",
            "--dry-run",
            "--recon",
            "-t",
            "--touch",
            "-q",
            "--question",
            "-i",
            "--ignore-errors",
        ):
            with self.subTest(flag=flag):
                result = self.run_make(flag, "check")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(
                    "non-executing or error-ignoring MAKEFLAGS are not supported",
                    result.stdout,
                )

    def test_root_overrides_do_not_redirect_targets(self):
        for variable in ("ROOT", "REPO_ROOT"):
            for name, arguments, environment in (
                ("command", ("verify", f"{variable}=/tmp/attacker-root"), None),
                ("environment", ("verify",), {variable: "/tmp/attacker-root"}),
            ):
                with self.subTest(variable=variable, override=name):
                    result, checkout, log, attacked = self.run_live_make(
                        "verify",
                        "OpenAI Compat's [gate] ",
                        arguments=arguments[1:],
                        environment=environment,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertNotIn("/tmp/attacker-root", result.stdout)
                    self.assertFalse(attacked, result.stdout)
                    self.assertIn(str(checkout), log)

    def test_live_recipes_treat_hostile_checkout_path_as_data(self):
        hostile_path = " OpenAI Compat's [gate] `root_attack` "
        targets = ("build", "check", "lint", "root-test", "static-check", "test", "verify")
        for target in targets:
            with self.subTest(target=target):
                result, checkout, log, attacked = self.run_live_make(target, hostile_path)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertFalse(attacked, result.stdout)
                self.assertIn(str(checkout), log)


if __name__ == "__main__":
    unittest.main()
