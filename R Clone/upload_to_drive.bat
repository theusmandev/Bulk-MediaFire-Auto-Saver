@echo off
title Urdu Novel Bank - Auto Uploader
echo Starting Upload to Google Drive...
echo ---------------------------------------

:: Apne folders ke path yahan set karen
set LOCAL_PATH="C:\Users\PCS\Downloads\Documents"
set REMOTE_NAME=gdrive
set REMOTE_FOLDER=mediafire_novels_backup

:: Rclone command
rclone copy %LOCAL_PATH% %REMOTE_NAME%:%REMOTE_FOLDER% --progress --transfers 10 --checkers 20 --contimeout 60s

echo ---------------------------------------
echo Upload Mukammal Ho Gaya!
pause