@echo off
title Urdu Novel Bank - Auto Uploader
echo Starting Upload to Google Drive...
echo ---------------------------------------

:: Apne folders ke path yahan set karen
set LOCAL_PATH="D:\audio books"
set REMOTE_NAME=gdrive
set REMOTE_FOLDER=google_drive_novels

:: Rclone command
rclone copy %LOCAL_PATH% %REMOTE_NAME%:%REMOTE_FOLDER% --progress --transfers 10 --checkers 20 --contimeout 60s

echo ---------------------------------------
echo Upload Mukammal Ho Gaya!
pause