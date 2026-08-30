param(
  [switch]$ResearchArchive,
  [string]$Repo = "SEng-Kitathas/Cognitive-Field-Engineering",
  [string]$Tag = "cfe-reincarnation-latest"
)
if (-not $ResearchArchive) {
  Write-Host "Runtime/project clone is already complete. Heavy R&D assets are opt-in."
  Write-Host "Re-run with -ResearchArchive to fetch release assets."
  exit 0
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "GitHub CLI required for release-asset fetch." }
gh release download $Tag --repo $Repo --dir .\research_archive
