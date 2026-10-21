#!/usr/bin/env bash
# Download the predictable binary that build.yml publishes on release `bin-latest`
# into bin/predictable and verify its checksum.
# Env: GH_TOKEN, GITHUB_REPOSITORY.
set -euo pipefail

repo="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is not set}"
mkdir -p bin
gh release download bin-latest -R "$repo" -p predictable -p predictable.sha256 -D bin --clobber
(cd bin && sha256sum --check --strict predictable.sha256)
chmod +x bin/predictable
bin/predictable --version
