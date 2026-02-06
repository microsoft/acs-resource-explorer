# Convert Markdown to Word Document using PowerShell
param(
    [string]$InputFile = "C:\Users\jameelaesa\ACS-Transition-Agent-v0\migration-guides\email\email-service-migration.md",
    [string]$OutputFile = "C:\Users\jameelaesa\ACS-Transition-Agent-v0\email-service-migration.docx"
)

# Read markdown content
$content = Get-Content $InputFile -Raw -Encoding UTF8

# Create Word Application
$word = New-Object -ComObject Word.Application
$word.Visible = $false

# Create new document
$doc = $word.Documents.Add()

# Process content line by line
$lines = $content -split "`n"
$inCodeBlock = $false
$codeContent = @()

foreach ($line in $lines) {
    # Handle code blocks
    if ($line -match '^```') {
        if (-not $inCodeBlock) {
            $inCodeBlock = $true
            $codeContent = @()
        } else {
            $inCodeBlock = $false
            if ($codeContent.Count -gt 0) {
                $para = $doc.Content.Paragraphs.Add()
                $para.Range.Text = ($codeContent -join "`n")
                $para.Range.Font.Name = "Courier New"
                $para.Range.Font.Size = 9
                $para.Range.InsertParagraphAfter()
            }
            $codeContent = @()
        }
        continue
    }

    if ($inCodeBlock) {
        $codeContent += $line
        continue
    }

    # Handle headings
    if ($line -match '^# (.+)$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $matches[1]
        $para.Style = "Heading 1"
        $para.Range.InsertParagraphAfter()
    }
    elseif ($line -match '^## (.+)$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $matches[1]
        $para.Style = "Heading 2"
        $para.Range.InsertParagraphAfter()
    }
    elseif ($line -match '^### (.+)$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $matches[1]
        $para.Style = "Heading 3"
        $para.Range.InsertParagraphAfter()
    }
    elseif ($line -match '^#### (.+)$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $matches[1]
        $para.Style = "Heading 4"
        $para.Range.InsertParagraphAfter()
    }
    # Handle horizontal rules
    elseif ($line -match '^---+$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = "_" * 60
        $para.Range.InsertParagraphAfter()
    }
    # Handle bullet points
    elseif ($line -match '^[-*]\s+(.+)$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $matches[1]
        $para.Style = "List Bullet"
        $para.Range.InsertParagraphAfter()
    }
    # Handle numbered lists
    elseif ($line -match '^\d+\.\s+(.+)$') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $matches[1]
        $para.Style = "List Number"
        $para.Range.InsertParagraphAfter()
    }
    # Regular text
    elseif ($line.Trim() -ne '') {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.Text = $line
        $para.Range.InsertParagraphAfter()
    }
    # Empty line
    else {
        $para = $doc.Content.Paragraphs.Add()
        $para.Range.InsertParagraphAfter()
    }
}

# Save document
$doc.SaveAs([ref]$OutputFile, [ref]16) # 16 = wdFormatDocumentDefault (.docx)

# Close document and quit Word
$doc.Close()
$word.Quit()

# Release COM objects
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Host "Conversion complete! Document saved to: $OutputFile" -ForegroundColor Green
