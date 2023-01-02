This is the documentation for AutomaticBackup's configuration file.
At this moment, it only support a single user. All the fields must have a valid 
value.

- **backup_dir**: Path to the directory the backup will be stored.
- **include_media**: Indicates if you want to include the collection.media 
  directory. Its value is either `true` or `false`.
- **compress_colpkg**: Indicates if you want to compress the colpkg file. Its 
- value is either `true` or `false`.
- **compress_media**: Indicates if you want to compress the collection.med

Example:
```json
{
  "backup_dir": "/home/geromt/.local/share/AnkiBackup",
  "include_media": true,
  "compress_colpkg": true,
  "compress_media": false,
  "upload_to_cloud": true,
  "remote": "backup-anki:"
}
```