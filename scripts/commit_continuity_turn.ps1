param([Parameter(Mandatory=$true)][string]$Message,[switch]$Push)
$ErrorActionPreference='Stop'
$root=(git rev-parse --show-toplevel).Trim(); Set-Location $root
$forbidden = git status --porcelain | Select-String -Pattern '(\.env|credentials|secrets|\.pem|\.key|\.safetensors|\.gguf|\.zip)$'
if ($forbidden) { throw "Refusing continuity commit: forbidden/heavy asset appears in Git status: $forbidden" }
git add continuity state docs policy reincarnation doctrine transcript scripts archive_manifests README.md .gitignore .gitattributes
if (-not (git diff --cached --quiet)) {
  git -c user.name='CFE Continuity Runtime' -c user.email='cfe-continuity@users.noreply.github.com' commit -m $Message
}
if ($Push) { git push origin HEAD }
git status --short --branch
