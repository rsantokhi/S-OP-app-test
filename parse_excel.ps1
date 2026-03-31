Add-Type -AssemblyName System.IO.Compression.FileSystem

$zipPath = $args[0]
$sheetFile = $args[1]

$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)

# Get shared strings
$ssEntry = $zip.GetEntry('xl/sharedStrings.xml')
$reader = New-Object System.IO.StreamReader($ssEntry.Open())
$ssContent = $reader.ReadToEnd()
$reader.Close()
$strings = [regex]::Matches($ssContent, '<t[^>]*>([^<]*)</t>') | ForEach-Object { [System.Net.WebUtility]::HtmlDecode($_.Groups[1].Value) }

# Read sheet
$sheetEntry = $zip.GetEntry($sheetFile)
$reader = New-Object System.IO.StreamReader($sheetEntry.Open())
$sheetContent = $reader.ReadToEnd()
$reader.Close()
$zip.Dispose()

# Use XmlDocument to parse properly
$xml = New-Object System.Xml.XmlDocument
$xml.LoadXml($sheetContent)

$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace("x", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")

$rows = $xml.SelectNodes("//x:row", $ns)
$count = 0
foreach ($row in $rows) {
    if ($count -gt 80) { break }
    $cells = $row.SelectNodes("x:c", $ns)
    $rowData = @()
    foreach ($cell in $cells) {
        $ref = $cell.GetAttribute("r")
        $type = $cell.GetAttribute("t")
        $vNode = $cell.SelectSingleNode("x:v", $ns)
        if ($vNode -ne $null) {
            $val = $vNode.InnerText
            if ($type -eq "s") {
                $idx = [int]$val
                if ($idx -lt $strings.Count) {
                    $rowData += "$ref=[$($strings[$idx])]"
                }
            } elseif ($type -eq "str") {
                $fNode = $cell.SelectSingleNode("x:f", $ns)
                $rowData += "$ref=[formula:$val]"
            } else {
                $rowData += "$ref=$val"
            }
        }
    }
    if ($rowData.Count -gt 0) {
        Write-Host ($rowData -join " | ")
        $count++
    }
}
