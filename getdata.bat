@echo off
setlocal enabledelayedexpansion

set "input_folder=C:\Program Files\hms\smdr\copy"
set "output_file=output_combined.txt"
set "regex=(\d{2}.\d{2}.\d{2})(\d{2}:\d{2}:\d{2})\s+(\d+)\s+(\d+)\s+(\d{2}:\d{2}:\d{2})(\d+)(\d)\s+(\d)\s+(\d)"

if not exist "!input_folder!" (
    echo Input folder "!input_folder!" not found.
    exit /b 1
)

rem Create or clear the output file
type nul > "%~dp0\!output_file!"

for %%F in ("!input_folder!\*.txt") do (
    set "full_path=%%~fF"
    
    rem Read the content of the input file
    set "content="
    for /f "usebackq delims=" %%a in ("!full_path!") do (
        set "content=!content!%%a"
    )

    rem Split the content based on the specified regular expression
    for /f "tokens=*" %%s in ('echo !content! ^| findstr /r /c:"%regex%"') do (
        rem Append each part to the output file
        echo %%s >> "%~dp0\!output_file!"
    )
)

echo Content from all .txt files has been split based on the regex and stored in "!output_file!".

endlocal
