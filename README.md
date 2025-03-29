# ini sections copier
This small script, entirely AI generated, allows to copy INI sections from one input INI file to another. INI files are processed as windows-1252, as this script has been created specifically to sync Total Commander INI files, before I found out that there's some level of support of this feature in TC itself. The intent here is to preserve the target INI file in its structure, order and formatting, as by using some INI libraries this was not the case.

From TC's help file, section **Settings in the file wincmd.ini: Overview**
*Warning: Windows functions do NOT support UTF-8-encoded INI files. Newer notepad versions will sometimes save INI files as UTF-8 without byte order mark (BOM). This will not work and result in scrambled accents. Please save INI files either as ANSI (plain text) or as UTF-16 LE (little endian).*

Edit `conf.toml` for settings, and review the `runIT.cmd` to run it.
