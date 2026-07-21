#!/usr/bin/env bash
# Check sibling layout for efficient cabal 1.0 + AI tooling workflow.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PARENT="$(cd "$ROOT/.." && pwd)"
ok=0; warn=0; bad=0
check() {
  local path="$1" role="$2" need="${3:-warn}"
  if [[ -d "$path" ]]; then
    printf 'OK   %s  (%s)\n' "$role" "$path"
    ok=$((ok+1))
  else
    if [[ "$need" == "must" ]]; then
      printf 'MISS %s  expected %s\n' "$role" "$path"
      bad=$((bad+1))
    else
      printf 'opt  %s  missing %s\n' "$role" "$path"
      warn=$((warn+1))
    fi
  fi
}
echo "compose-doctor: parent=$PARENT"
check "$ROOT" "cabal-devmelopner" must
check "$PARENT/tg-agent-relay" "tg-agent-relay" must
check "$PARENT/gha-runner-ctl" "gha-runner-ctl" must
check "$PARENT/agent-harness" "agent-harness" warn
check "$PARENT/tero-mcp" "tero-mcp" warn
check "$PARENT/tero-rs" "tero-rs" warn
check "$PARENT/tz-forge" "tz-forge" warn
check "$PARENT/security-mcp" "security-mcp" warn
check "$PARENT/dev-shell" "dev-shell" warn
# versions
if [[ -f "$ROOT/VERSION" ]]; then echo "cabal VERSION=$(cat "$ROOT/VERSION")"; fi
if [[ -f "$PARENT/tg-agent-relay/VERSION" ]]; then echo "relay VERSION=$(cat "$PARENT/tg-agent-relay/VERSION")"; fi
if [[ -f "$PARENT/gha-runner-ctl/VERSION" ]]; then echo "gha-runner-ctl VERSION=$(cat "$PARENT/gha-runner-ctl/VERSION")"; fi
# docs presence
for f in docs/V1_0_0_GAP_ANALYSIS.md docs/V1_0_0_JOINT_EXECUTION.md docs/TOOLING_STACK_READINESS.md; do
  if [[ -f "$ROOT/$f" ]]; then echo "OK   $f"; else echo "MISS $f"; bad=$((bad+1)); fi
done
echo "summary: ok=$ok warn=$warn bad=$bad"
[[ "$bad" -eq 0 ]]
