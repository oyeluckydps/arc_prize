Get-ChildItem -Filter *.txt | 
    Where-Object { $_.Name -ne "combined.txt" } | 
    ForEach-Object { 
        Get-Content $_.FullName
        "`n`n"
    } | Set-Content combined.txt