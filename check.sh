#!/usr/bin/env bash
# Health check for the deliberate-practice repo.
#
# Confirms the virtual environment, the dsakit package, every Python file,
# the full test suite, and that your work is committed and in sync with
# GitHub. Run it from anywhere inside the repo:
#
#     ./check.sh
#
# Exits 0 when nothing failed. "note" lines are reminders, not failures.

set -u

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "Run this from inside the repo."; exit 1; }
cd "$ROOT" || exit 1
PY="$ROOT/.venv/bin/python"
failures=0

ok()   { printf '  ok    %s\n' "$*"; }
note() { printf '  note  %s\n' "$*"; }
fail() { printf '  FAIL  %s\n' "$*"; failures=$((failures + 1)); }

echo "Environment"
if [ ! -x "$PY" ]; then
  fail "no virtual environment: run python3 -m venv .venv"
  echo; echo "Create the environment first, then run this again."; exit 1
fi
ok "$("$PY" --version) in .venv"
if version=$("$PY" -m pytest --version 2>&1); then
  ok "$version"
else
  fail "pytest is missing: run pip install -e \".[dev]\""
fi

echo "Package"
location=$("$PY" -c 'import dsakit, os; print(os.path.relpath(dsakit.__file__))' 2>/dev/null)
if [ "$location" = "src/dsakit/__init__.py" ]; then
  ok "dsakit imports from src/dsakit"
else
  fail "dsakit isn't installed from this repo: run pip install -e \".[dev]\""
fi

echo "Code"
if "$PY" -m compileall -q -x '/\.venv/' . >/dev/null; then
  ok "every Python file compiles"
else
  "$PY" -m compileall -q -x '/\.venv/' .
  fail "syntax errors (details above)"
fi

benchmarks=0
broken=0
while IFS= read -r file; do
  benchmarks=$((benchmarks + 1))
  if ! (cd "$(dirname "$file")" && "$PY" -c "import $(basename "$file" .py)") >/dev/null 2>&1; then
    fail "benchmark won't load: $file"
    broken=$((broken + 1))
  fi
done < <(find algorithms data-science sql -name 'benchmark_*.py' 2>/dev/null)
[ "$broken" -eq 0 ] && ok "benchmarks load ($benchmarks found)"

if results=$("$PY" -m pytest -q 2>&1); then
  ok "tests: $(printf '%s\n' "$results" | tail -n 1 | tr -d '=' | xargs)"
else
  printf '%s\n' "$results" | tail -n 30
  fail "tests failed (details above)"
fi

echo "Git"
if git ls-files | grep -qE '(^|/)(\.venv|__pycache__|\.pytest_cache)/|\.egg-info/'; then
  fail "generated files are committed: check .gitignore"
else
  ok "no generated files committed"
fi

if [ -z "$(git status --porcelain)" ]; then
  ok "no uncommitted changes"
else
  note "uncommitted changes: run git status"
fi

if git fetch --quiet 2>/dev/null; then
  upstream=$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null)
  if [ -z "$upstream" ]; then
    note "this branch isn't linked to GitHub yet"
  else
    read -r behind ahead < <(git rev-list --left-right --count '@{u}...HEAD')
    if [ "$behind" -eq 0 ] && [ "$ahead" -eq 0 ]; then
      ok "in sync with $upstream"
    else
      note "$ahead commit(s) to push and $behind to pull: run git pull, then git push"
    fi
  fi
else
  note "couldn't reach GitHub to check sync"
fi

echo
if [ "$failures" -eq 0 ]; then
  echo "All checks passed."
else
  echo "$failures check(s) failed."
fi
exit $((failures > 0))
