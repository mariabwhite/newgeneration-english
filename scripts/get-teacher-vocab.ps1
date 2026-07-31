# Тянет последний teacher-vocab snapshot для урока из Supabase.
# Аргумент — pathname урока (например /lingua-boost-lab/a1/city-speaking/).
# Используется Клодом чтобы видеть Машины teacher-добавки без скринов.

param(
  [Parameter(Mandatory=$true)][string]$LessonPath
)

$SUPABASE_URL  = "https://iqzlphbvmfgoygnozbya.supabase.co"
$SUPABASE_ANON = "sb_publishable_hYhBk3xS90uouUFd_DZWUw_sOv-6JGO"

$encoded = [System.Web.HttpUtility]::UrlEncode($LessonPath)
$url = "$SUPABASE_URL/rest/v1/lab_submissions?lesson_path=eq.$encoded&section_id=eq.teacher-vocab-snapshot&order=created_at.desc&limit=1"

$headers = @{
  "apikey"        = $SUPABASE_ANON
  "Authorization" = "Bearer $SUPABASE_ANON"
}

try {
  $resp = Invoke-RestMethod -Uri $url -Headers $headers -Method Get -TimeoutSec 15
  if ($resp.Count -eq 0) {
    Write-Output "NO SNAPSHOT for $LessonPath"
    return
  }
  $snap = $resp[0]
  Write-Output "Snapshot from $($snap.created_at)"
  Write-Output "Words: $($snap.total)"
  Write-Output "---"
  foreach ($w in $snap.misses) {
    $line = "$($w.word)"
    if ($w.ipa)     { $line += "  $($w.ipa)" }
    if ($w.ru)      { $line += "  →  $($w.ru)" }
    if ($w.example) { $line += "  ·  ex: $($w.example)" }
    Write-Output $line
  }
} catch {
  Write-Output "ERROR: $($_.Exception.Message)"
}
