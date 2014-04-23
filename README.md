BackupperPy (Software for making backups)
===========
Phase 1 finished - Released
===========

Script copies recursively source directories to destination ones.
If directory contains .backup-ignore file this directory will be skipped.

The directory mapping config file is:
./directories.cfg

The logs location:
./logs

Logs directory should contain some performance info, lists of skipped directories and files which are presented at destination directory but missed(skipped) at source.

directories.cfg file format:
/.../source_directory => /.../destination_directory

Script leaves the label at destination directory when was performed last backup
