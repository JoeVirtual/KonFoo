@ECHO OFF

REM Command file
if "%1" == "" goto help

if "%1" == "help" (
    :help
    echo.Please use `make ^<target^>` where ^<target^> is one of
    echo.  docs       to build the html documentation of the package
    echo.  doctest    to run all tests for the documentation
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

if "%1" == "doctest" (
    cd docs
    make doctest -o +NORMALIZE_WHITESPACE
    cd ..
    goto end
)

if "%1" == "test" (
    cd tests
    pytest
    cd ..
    goto end
)

if "%1" == "build" (
    python setup.py sdist
    python setup.py bdist_wheel
    goto end
)

if "%1" == "release" (
    set HOME=.
    python setup.py sdist
    python setup.py bdist_wheel
    twine upload dist/*
    goto end
)

:end
