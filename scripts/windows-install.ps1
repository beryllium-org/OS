echo "Ljinux install script for ljinux.
Why are you doing this in bimbows??"
$a = Get-Volume | ? FileSystemLabel -eq "LJINUX"
$b = Get-Volume | ? FileSystemLabel -eq "CIRCUITPY"
if ( $a -ne $null ){
    $targett = $a
} elseif ($b -ne $null) {
    $targett = $b
} else {
    echo "Board not found."
    exit 1
}
echo "Detected the board in $($targett.DriveLetter):\"
