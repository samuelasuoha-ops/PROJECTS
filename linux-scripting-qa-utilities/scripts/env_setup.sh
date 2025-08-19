#!/usr/bin/env bash
set -euo pipefail

DRY_RUN="${DRY_RUN:-1}"

run() {
  echo "+ $*"
  if [[ "$DRY_RUN" == "0" ]]; then
    eval "$@"
  fi
}

echo "Ubuntu environment setup (DRY_RUN=$DRY_RUN)"
run "sudo apt-get update -y"
run "sudo apt-get upgrade -y"
run "sudo apt-get install -y git curl jq ufw"

echo "Optionally configure UFW (allow OpenSSH)"
run "sudo ufw allow OpenSSH"
run "sudo ufw --force enable"

echo "Add handy aliases"
mkdir -p "$HOME/.bashrc.d"
cat <<'EOF' > "$HOME/.bashrc.d/qa_aliases.sh"
alias ll='ls -alF'
alias gs='git status'
alias gd='git diff'
EOF

if ! grep -q '.bashrc.d' "$HOME/.bashrc"; then
  echo 'for f in ~/.bashrc.d/*.sh; do [ -r "$f" ] && . "$f"; done' >> "$HOME/.bashrc"
fi

echo "Done. Re-run with DRY_RUN=0 to apply changes."
