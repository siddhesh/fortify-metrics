# Fortify metrics

This project is a couple of tools that does source or binary analysis to get an
estimate of how much of a program or project is fortified as a result of
building with the `_FORTIFY_SOURCE` macro.

## fmetrics GCC plugin

This plugin helps get source level statistics on object size computation in
source code.  Specifically, when a source file is built with this plugin
invoked, it will print the number of times that the `__builtin_object_size`
builtin was computed successfully along with the number of times it would have
been computed successfully if it were replaced with
`__builtin_dynamic_object_size`.

### Building

`make` to build and `make check` to run tests.

### Running

Add `-fplugin=$PATH_TO/fmetrics.so -fplugin-arg-fmetrics-project=SOMENAME` to
`CFLAGS` or `CXXFLAGS` of the project you intend to analyze and then build it.
The output for every source file is written out to stderr in the form:

```
SOMENAME:: TOTAL:BOS:BDOS
```

Where `SOMENAME` is what you passed in the `CFLAGS` above, TOTAL is the number
of `__builtin_object_size` encountered, `BOS` is the number of
`__builtin_object_size` that the compiler successfully resolved to something
other than `(size_t) -1` and `BDOS` is the corresponding success count if the
builtin were replaced with `__builtin_dynamic_object_size`.

### Known limitations of fmetrics.so

The `__builtin_object_size` builtin may get folded away early in some cases,
thus eluding the plugin.  These cases however are successes or failures (e.g.
in handling of volatile expressions) in both `__builtin_object_size` and
`__builtin_dynamic_object_size`, so the meaning of the metrics should not
change.  The percentage changes however may look different from the ideal
case.

## fortify-metrics.py

Parse DSOs to get statistics for how well `_FORTIFY_SOURCE` did with that DSO.
This is different from [OpenOSC](https://github.com/cisco/OpenOSC), which aims
to be more precise at compile time *and* add instrumentation for enhanced
diagnostics.  This project aims to do none of that and as a result, can be
deployed pretty much anywhere and just pointed at a path or a DSO.  Further,
OpenOSC assumes constant object sizes, which makes it unsuitable for
`_FORTIFY_SOURCE=3`.

```
usage: fortify-metrics.py [-h] [-v] [-l] [-f] path [path ...]

Get build time statistics of _FORTIFY_SOURCE coverage for ELF files in given
directories.

positional arguments:
  path            Files or directories to analyze

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   Verbose mode.
  -l, --listall   Include fortifiable functions with zero call counts.
  -f, --fullpath  Show full path in binary names.
```

### Known Limitations of fortify-metrics.py

More `_chk` function calls does not necessarily mean better fortification
because calls may have been simplified to their regular variants and in some
cases, inlined or transformed to simpler calls.  One could make reasonable
conclusions from the data though, based on changes in total calls across all
fortifiable functions.

## Contributing

Submit a pull request or file an issue!
