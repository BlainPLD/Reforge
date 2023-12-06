@echo off
setlocal enabledelayedexpansion

rem Create a folder with the current date and time
set datetime=%date:/=-%_%time::=-%
set datetime=%datetime:.=%
set datetime=!datetime: =!

md " ..\Output\!datetime!"

rem Move the output files to the new folder
move /Y ..\Input\Input.csv " ..\Output\!datetime!"
move /Y ..\Package\DAT_output.csv " ..\Output%\!datetime!"
move /Y ..\Package\item_mod.txt " ..\Output\!datetime!"
move /Y ..\Package\Needs_ModID.csv "%outputFolder%\!datetime!"


pause
