@echo off
cls

REM CONSTANTS
set DIRECTORY=bin
set COMPRESSOR=%DIRECTORY%\upx.exe
set MAC=macos-agent
set LINUX=linux-agent
set WIN=windows-agent.exe
set RASP=rasp-agent
set BSD=bsd-agent
set FLAGS=-ldflags "-s -w"

REM CHECK FOR UPX COMPRESSION TOOL
if exist %COMPRESSOR% (
    set COMPRESS=1
    echo [+] UPX was found in the bin directory. Enabling compression...
    echo.
) else (
    set COMPRESS=0
    echo [!] UPX not found in the bin directory. Skipping compression...
    echo.
)

REM COMPILATION CALL STACK
call :agent-mac
call :agent-linux
call :agent-windows
call :agent-raspberrypi
call :agent-freebsd
goto :EOF

:agent-mac
	echo [1/5] Compiling MacOS binary...
	set GOOS=darwin
	set GOARCH=amd64
	go build %FLAGS% -o %DIRECTORY%\%MAC% cmd\agent\main.go

	if "%COMPRESS%"=="1" (
        echo [1/5] Compressing MacOS binary...
		%COMPRESSOR% %DIRECTORY%\%MAC%
    )
	goto :EOF

:agent-linux
    cls
	echo [2/5] Compiling Linux binary...
	set GOOS=linux
	set GOARCH=amd64
	go build %FLAGS% -o %DIRECTORY%\%LINUX% cmd\agent\main.go

	if "%COMPRESS%"=="1" (
        echo [2/5] Compressing Linux binary...
		%COMPRESSOR% %DIRECTORY%\%LINUX%
	)
	goto :EOF

:agent-windows
    cls
	echo [3/5] Compiling Windows binary...
	set GOOS=windows
	set GOARCH=amd64
	go build %FLAGS% -o %DIRECTORY%\%WIN% cmd\agent\main.go

	if "%COMPRESS%"=="1" (
        echo [3/5] Compressing Windows binary...
		%COMPRESSOR% %DIRECTORY%\%WIN%
	)
	goto :EOF

:agent-raspberrypi
    cls
	echo [4/5] Compiling Raspberry Pi binary...
	set GOOS=linux
	set GOARCH=arm
	set GOARM=7
	go build %FLAGS% -o %DIRECTORY%\%RASP% cmd\agent\main.go

	if "%COMPRESS%"=="1" (
        echo [4/5] Compressing Raspberry Pi binary...
		%COMPRESSOR% %DIRECTORY%\%RASP%
	)
	goto :EOF

:agent-freebsd
    cls
	echo [5/5] Compiling FreeBSD binary...
	set GOOS=freebsd
	set GOARCH=amd64
	go build %FLAGS% -o %DIRECTORY%\%BSD% cmd\agent\main.go

	if "%COMPRESS%"=="1" (
        echo [5/5] Compression for FreeBSD binaries is off...
	)
	goto :EOF
