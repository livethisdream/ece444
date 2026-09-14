@echo off
rem nec_lab -- double-click launcher for Windows.
rem
rem The lowest-barrier path on a managed PC is a URL to a shared copy, which
rem needs nothing here at all. This is the next one down: no install, no admin,
rem no command line -- double-click, and the browser opens on the tool. It uses
rem whatever Python the machine already has, and the NEC engine inside 4nec2 if
rem that is what is installed.

setlocal
title ECE 444 -- nec_lab

set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY (python --version >nul 2>&1 && set "PY=python")
if not defined PY (python3 --version >nul 2>&1 && set "PY=python3")

if not defined PY (
  echo.
  echo   Python was not found on this computer.
  echo.
  echo   Two ways forward:
  echo     1. Use the shared copy your instructor is running -- open the
  echo        address given in class in any browser. Nothing to install.
  echo     2. Install Python from the Software Center, or python.org, and
  echo        double-click this file again. No admin rights are needed for a
  echo        per-user install.
  echo.
  pause
  exit /b 1
)

echo.
echo   Starting nec_lab. A browser window will open in a moment.
echo   Leave this window open while you work; close it to stop the tool.
echo.

%PY% "%~dp0run.py" serve %*

echo.
echo   nec_lab has stopped.
pause
