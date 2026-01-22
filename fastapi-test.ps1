# Kullanıcı tokenları
$tokens = @{
    "Alice" = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsIm5hbWUiOiJBbGljZSIsInJvbGUiOiJ1c2VyIn0.r3-wK_vwyz3pAkbUfBHr9g7Lq4RUsD1Uc0NZQjvheOE"
    "Bob"   = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsIm5hbWUiOiJCb2IiLCJyb2xlIjoidXNlciJ9.M53d_QcdUIrK9W1fvLxrfVpS6bOjoGaTpj6bRARRqCU"
    "Carol" = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsIm5hbWUiOiJDYXJvbCIsInJvbGUiOiJhZG1pbiJ9.x6STA3t18UUrS9mcxlja6V7kmcv4RxnpcfqJjL9wMHA"
}

$uri = "http://127.0.0.1:8080/messages"

foreach ($user in $tokens.Keys) {
    Write-Host "`n--- Testing $user ---"
    $headers = @{ Authorization = "Bearer $($tokens[$user])" }
    
    try {
        $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method GET
        Write-Host ($response | ConvertTo-Json -Depth 5)
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}
