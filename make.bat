@ECHO OFF

REM Command file
if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  clean      to clean up the repository
	echo.  doctest    to run all doctests embedded in the source files
	goto end
)

if "%1" == "clean" (
	goto end
)

if "%1" == "doctest" (
    cd tests
    doctests.bat
    cd ..
	goto end
)

:end