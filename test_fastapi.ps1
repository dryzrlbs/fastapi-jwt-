# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Start server in background
Start-Process python -ArgumentList '-m uvicorn app.main:app --reload --port 8080'

# Wait a few seconds for the server to start
Start-Sleep -Seconds 5

# Test the protected endpoint with Carol's token
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsIm5hbWUiOiJDYXJvbCIsInJvbGUiOiJhZG1pbiJ9.x6STA3t18UUrS9mcxlja6V7kmcv4RxnpcfqJjL9wMHA"
$headers = @{ Authorization = "Bearer $token" }

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8080/protected" -Headers $headers -Method GET
    Write-Output "Response from /protected:`n$response"
} catch {
    Write-Output "Error:`n$($_.Exception.Message)"
}
