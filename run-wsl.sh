#!/usr/bin/env bash
set -euo pipefail

# Always run relative to the repository, even when launched from elsewhere.
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

# Avoid hitting RubyGems on every launch when the bundle is already installed.
bundle check >/dev/null 2>&1 || bundle install

exec bundle exec jekyll serve --force_polling --livereload --incremental "$@"
