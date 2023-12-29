@echo off
setlocal enabledelayedexpansion

set "input_folder=C:\Program Files\hms\smdr\copy"
set "output_file=output_combined.txt"

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

    rem Append the content to the output file
    echo !content! >> "%~dp0\!output_file!"
)

echo Combined content from all .txt files has been stored in "!output_file!".

endlocal
