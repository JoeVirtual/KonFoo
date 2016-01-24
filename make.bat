@ECHO OFF

REM Command file
if "%1" == "" goto help

if "%1" == "help" (
    :help
    echo.Please use `make ^<target^>` where ^<target^> is one of
    echo.  docs       to build the html documentation of the package
    echo.  test       to run all tests for the package
    echo.  build      to build the package
    echo.  release    to release the package on PyPi
    goto end
)

if "%1" == "docs" (
    cd docs
    make html
    cd ..
    goto end
)

if "%1" == "test" (
    cd tests
    py.test
    cd ..
    goto end
)

if "%1" == "build" (
    python setup.py sdist bdist_wheel
    goto end
)

if "%1" == "release" (
    python setup.py sdist bdist_wheel upload
    goto end
)

:end
