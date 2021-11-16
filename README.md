# Fortify metrics

Parse DSOs to get statistics for how well `_FORTIFY_SOURCE` did with that DSO.
This is different from [OpenOSC](https://github.com/cisco/OpenOSC), which aims
to be more precise at compile time *and* add instrumentation for enhanced
diagnostics.  This project aims to do none of that and as a result, can be
deployed pretty much anywhere and just pointed at a path or a DSO.  Further,
OpenOSC assumes constant object sizes, which makes it unsuitable for
`_FORTIFY_SOURCE=3`.

```
usage: fortify-metrics.py [-h] [-v] [-l] path [path ...]

Get build time statistics of _FORTIFY_SOURCE coverage for ELF files in given
directories.

positional arguments:
  path           Files or directories to analyze

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose mode.
  -l, --list     Prefix results with all fortifiable functions with zero call
                 counts.
```

## Known Limitations

More `_chk` function calls does not necessarily mean better fortification
because calls may have been simplified to their regular variants and in some
cases, inlined or transformed to simpler calls.  One could make reasonable
conclusions from the data though, based on changes in total calls across all
fortifiable functions.
