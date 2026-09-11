#!/usr/bin/env python3
"""Cross-platform verification and formatting utility for Django student projects.

Usage:
  python check_submission.py           # Check PEP-8, Django, HTML templates, and CSS/JS
  python check_submission.py --format  # Auto-format Python, HTML templates, and CSS/JS
"""

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

# Enable ANSI escape sequences on Windows console
if sys.platform == "win32":
    os.system("")

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "migrations",
    "staticfiles",
    "node_modules",
    ".ruff_cache",
    ".mypy_cache",
}


def check_prerequisites() -> bool:
    """Verify that required tools are installed in current Python environment."""
    required = {
        "ruff": "ruff",
        "djlint": "djlint",
        "cssbeautifier": "cssbeautifier",
        "jsbeautifier": "jsbeautifier",
    }
    missing = [
        pkg_name
        for mod, pkg_name in required.items()
        if importlib.util.find_spec(mod) is None
    ]
    if missing:
        print(f"{RED}{BOLD}[ERROR] Missing required dependencies:{RESET}")
        for pkg in missing:
            print(f"  - {pkg}")
        print(
            f"\n{YELLOW}Please install dev dependencies with:{RESET}\n"
            f"  {BOLD}{sys.executable} -m pip install -r requirements-dev.txt{RESET}\n"
        )
        return False
    return True


def run_command(title: str, cmd: list[str]) -> bool:
    print(f"\n{CYAN}{BOLD}▶ {title}...{RESET}")
    result = subprocess.run(cmd, text=True)
    if result.returncode == 0:
        print(f"{GREEN}✓ {title} passed.{RESET}")
        return True
    else:
        print(f"{RED}✗ {title} found issues.{RESET}")
        return False


def process_html_templates(format_mode: bool) -> bool:
    """Run djLint only if HTML files exist, avoiding non-zero exit codes on empty repos."""
    root = Path(".")
    html_files = [
        p
        for p in root.rglob("*.html")
        if not any(part in IGNORE_DIRS for part in p.parts)
    ]
    if not html_files:
        print(f"\n{CYAN}{BOLD}▶ Django HTML Templates (djLint)...{RESET}")
        print(f"{YELLOW}No HTML template files found to check.{RESET}")
        return True

    if format_mode:
        cmd = [
            sys.executable,
            "-m",
            "djlint",
            ".",
            "--reformat",
            "--profile=django",
        ]
        return run_command("djLint Template Reformat", cmd)
    else:
        cmd = [
            sys.executable,
            "-m",
            "djlint",
            ".",
            "--check",
            "--profile=django",
        ]
        return run_command("Django HTML Template Linting (djLint)", cmd)


def process_static_file(file_path: Path, beautifier, opts, format_mode: bool) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8")
        formatted = beautifier.beautify(content, opts)
        if content != formatted:
            if format_mode:
                file_path.write_text(formatted, encoding="utf-8")
                print(f"  {GREEN}[FORMATTED]{RESET} {file_path}")
                return True
            else:
                print(f"  {RED}[UNFORMATTED]{RESET} {file_path}")
                return False
        return True
    except Exception as e:
        print(f"  {RED}[ERROR] {file_path}: {e}{RESET}")
        return False


def process_static_files(format_mode: bool) -> bool:
    import cssbeautifier
    import jsbeautifier

    css_opts = cssbeautifier.default_options()
    css_opts.indent_size = 2

    js_opts = jsbeautifier.default_options()
    js_opts.indent_size = 2

    title = (
        "Auto-Formatting Static Files (CSS/JS)"
        if format_mode
        else "Checking Static Files Formatting (CSS/JS)"
    )
    print(f"\n{CYAN}{BOLD}▶ {title}...{RESET}")

    root = Path(".")
    all_files = [
        p
        for p in root.rglob("*")
        if p.is_file()
        and p.suffix in (".css", ".js")
        and not any(part in IGNORE_DIRS for part in p.parts)
    ]

    if not all_files:
        print(f"{YELLOW}No standalone .css or .js files found to check.{RESET}")
        return True

    all_passed = True
    for p in all_files:
        if p.suffix == ".css":
            ok = process_static_file(p, cssbeautifier, css_opts, format_mode)
        elif p.suffix == ".js":
            ok = process_static_file(p, jsbeautifier, js_opts, format_mode)
        else:
            ok = True
        all_passed = all_passed and ok

    if all_passed:
        print(f"{GREEN}✓ Static files check passed.{RESET}")
    else:
        print(
            f"{RED}✗ Static files have formatting issues. Run with --format to fix.{RESET}"
        )

    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Verify or format Django student submissions."
    )
    parser.add_argument(
        "--format",
        "-f",
        action="store_true",
        help="Automatically format Python, HTML templates, CSS, and JS files.",
    )
    args = parser.parse_args()

    if not check_prerequisites():
        sys.exit(1)

    format_mode = args.format

    if format_mode:
        print(f"{BOLD}{GREEN}=== AUTO-FORMATTING PROJECT ==={RESET}")

        # 1. Format Python code
        run_command("Ruff Format", [sys.executable, "-m", "ruff", "format", "."])

        # 2. Auto-fix safe PEP-8 and Django lint rules
        run_command(
            "Ruff Lint Auto-Fix",
            [sys.executable, "-m", "ruff", "check", "--fix", "."],
        )

        # 3. Format Django HTML templates (and embedded styles/scripts)
        process_html_templates(format_mode=True)

        # 4. Format standalone static CSS & JS
        process_static_files(format_mode=True)

        print(
            f"\n{GREEN}{BOLD}Formatting complete! Run `python check_submission.py` to verify.{RESET}"
        )
        sys.exit(0)

    # CHECK / GRADING MODE
    print(f"{BOLD}{CYAN}=== VERIFYING PROJECT COMPLIANCE ==={RESET}")
    all_passed = True

    # 1. PEP-8, PEP-8 naming, and Django rules
    all_passed &= run_command(
        "Python PEP-8 Linting (Ruff)",
        [sys.executable, "-m", "ruff", "check", "."],
    )

    # 2. Python code formatting check
    all_passed &= run_command(
        "Python Code Formatting (Ruff Format)",
        [sys.executable, "-m", "ruff", "format", "--check", "."],
    )

    # 3. Django HTML templates check
    all_passed &= process_html_templates(format_mode=False)

    # 4. Standalone CSS & JS files check
    all_passed &= process_static_files(format_mode=False)

    print("\n" + "=" * 45)
    if not all_passed:
        print(
            f"{RED}{BOLD}VERIFICATION FAILED:{RESET} One or more checks reported issues.\n"
            f"Run {BOLD}python check_submission.py --format{RESET} to fix formatting issues automatically."
        )
        sys.exit(1)

    print(
        f"{GREEN}{BOLD}ALL CHECKS PASSED:{RESET} Project conforms to grading standards."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
