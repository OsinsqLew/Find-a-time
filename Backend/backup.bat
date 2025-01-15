@echo off
SET CONTAINER_NAME=mysql-slave
SET MYSQL_USER=backup_user
SET MYSQL_PASSWORD=backup_pass
SET BACKUP_DIR=C:\Users\lenovo\Documents\Semestr_V\Bazy Danych\friends_app\Find-a-time\backup\dir_of_backups

for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set datetime=%%I
set DATE=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%
set TIME=%datetime:~8,2%-%datetime:~10,2%

set TIMESTAMP=%DATE%_%TIME%

docker exec %CONTAINER_NAME% mysqldump -u %MYSQL_USER% -p%MYSQL_PASSWORD% --all-databases --single-transaction > "%BACKUP_DIR%\backup_%TIMESTAMP%.sql"

IF %ERRORLEVEL% NEQ 0 (
    echo Backup failed!
    exit /b 1
) ELSE (
    echo Backup completed successfully.
)
