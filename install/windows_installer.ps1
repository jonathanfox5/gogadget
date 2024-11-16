# Define the path to the .local\bin directory within the user's home directory
$tool_install_path = "$env:USERPROFILE\.local\bin"
$local_tools_path = "tools"

Write-Output "~~~Starting Installer~~~"
Write-Output "~~~Setting system paths~~~"

# Ensure the .local\bin directory exists
if (-not (Test-Path -Path $tool_install_path)) {
    New-Item -ItemType Directory -Path $tool_install_path -Force
}

# Get the current user PATH environment variable
$user_path = [System.Environment]::GetEnvironmentVariable("PATH", "User")

# Check if the new path is already in the PATH
if ($user_path -notlike "*$tool_install_path*") {
    # Append the new path to the user PATH environment variable
    $new_user_path = "$user_path;$tool_install_path"
    [System.Environment]::SetEnvironmentVariable("PATH", $new_user_path, "User")
    Write-Output "Status: The path $tool_install_path has been added to the user PATH variable."
} else {
    Write-Output "Status: The path $tool_install_path has been detected in the user PATH variable."
}

Write-Output "~~~Copying support tools (FFMPEG / uv)~~~"
# Ensure the local tools folder exists
if (-not (Test-Path -Path $local_tools_path)) {
    Write-Output "### Error ### The local tools folder does not exist. Please re-download the .zip file from https://github.com/jonathanfox5/gogadget/releases/ and try again ###"
    exit
}

# Function to check if a file exists in the system PATH
function Test-ToolInPath {
    param (
        [string]$toolName
    )
    $paths = $env:PATH -split ';'
    foreach ($path in $paths) {
        if (Test-Path -Path (Join-Path -Path $path -ChildPath $toolName)) {
            return $true
        }
    }
    return $false
}

# Copy files only if they are not already available in the system PATH
Get-ChildItem -Path $local_tools_path -File | ForEach-Object {
    $toolName = $_.Name
    if (-not (Test-ToolInPath -toolName $toolName)) {
        Copy-Item -Path $_.FullName -Destination $tool_install_path -Force
        Write-Output "Status: The tool $toolName has been copied to $tool_install_path."
    } else {
        Write-Output "Status: The tool $toolName already exists in the system PATH. Skipping copy."
    }
}


Write-Output "~~~Installing gogadget ~~~"
uv tool install gogadget --python 3.12

Write-Output "~~~Making gogadget accessible to the user~~~"
uv tool update-shell

# Write success
Write-Output "~~~INSTALLATION COMPLETE! You can now run the program by opening command prompt and typing gogadget ~~~"
Write-Output "In command prompt / powershell, you can optionally run `gogadget install` (without quotes) to install all of the required models for your chosen language."
Read-Host -Prompt "Press Enter to close this window"
