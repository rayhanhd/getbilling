@echo off
setlocal enabledelayedexpansion

set "input_folder=C:\Program Files\hms\smdr\copy"
set "output_extension=txt"

if not exist "!input_folder!" (
    echo Input folder "!input_folder!" not found.
    exit /b 1
)

for %%F in ("!input_folder!\*.txt") do (
    set "input_file=%%~nF"
    set "full_path=%%~fF"
    
    rem Read the content of the input file
    set "content="
    for /f "usebackq delims=" %%a in ("!full_path!") do (
        set "content=!content!%%a"
    )

    rem Write the content to the output file
    set "output_file=!input_file!.!output_extension!"
    echo !content! > "!input_folder!\!output_file!"
    echo Content from "!input_file!.txt" has been stored in "!output_file!".
)

endlocal
