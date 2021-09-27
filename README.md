# Fortify metrics

Parse DSOs to get statistics for how well `_FORTIFY_SOURCE` did with that DSO.
This is different from [OpenOSC](https://github.com/cisco/OpenOSC), which aims
to be more precise at compile time *and* add instrumentation for enhanced
diagnostics.  This project aims to do none of that and as a result, can be
deployed pretty much anywhere and just pointed at a path or a DSO.

```
usage: fortify-metrics.py [-h] [-v] [-l] path [path ...]

Get build time statistics of _FORTIFY_SOURCE coverage for ELF files in given
directories.

positional arguments:
  path           Directories to analyze

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose mode.
  -l, --list     Prefix results with all fortifiable functions with zero call
                 counts.
```
