#!/usr/bin/python
# SPDX-License-Identifier: MIT

import sys, argparse, magic, subprocess, os, re
from stat import *

# TODO: Handle static binaries too someday.
scan_mimes = ['application/x-executable', 'application/x-pie-executable',
              'application/x-sharedlib']
scan_exclude = [r'\.debug$']

functions = ["asprintf", "confstr", "dprintf", "explicit_bzero", "fdelt",
             "fgets", "fgets_unlocked", "fgetws", "fgetws_unlocked", "fprintf",
             "fread", "fread_unlocked", "fwprintf", "getcwd", "getdomainname",
             "getgroups", "gethostname", "getlogin_r", "gets", "getwd",
             "longjmp", "mbsnrtowcs", "mbsrtowcs", "mbstowcs", "memcpy",
             "memmove", "mempcpy", "memset", "obstack_printf",
             "obstack_vprintf", "poll", "ppoll", "pread", "pread64", "printf",
             "ptsname_r", "read", "readlink", "readlinkat", "realpath", "recv",
             "recvfrom", "snprintf", "sprintf", "stpcpy", "stpncpy", "strcat",
             "strcpy", "strncat", "strncpy", "swprintf", "syslog", "ttyname_r",
             "vasprintf", "vdprintf", "vfprintf", "vfwprintf", "vprintf",
             "vsnprintf", "vsprintf", "vswprintf", "vsyslog", "vwprintf",
             "wcpcpy", "wcpncpy", "wcrtomb", "wcscat", "wcscpy", "wcsncat",
             "wcsncpy", "wcsnrtombs", "wcsrtombs", "wcstombs", "wctomb",
             "wmemcpy", "wmemmove", "wmempcpy", "wmemset", "wprintf" ]

listall = None
fullpath = None

def maybe_fullpath(f):
    if fullpath:
        return f
    else:
        return os.path.basename(f)

def get_calls(line):
    m = re.search(r'.*<([^>]+)@plt>$', line.decode().strip())

    if not m or not m.group(1):
        return None

    func = m.group(1)
    if [f for f in functions if func == f or func == '__' + f + '_chk']:
        return func
    return None

def analyze_dso(f):
    args = ['objdump', '-d', '--no-addresses', f]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    pltcalls = [get_calls(x) for x in proc.stdout]
    m = re.compile(r'__(.+)_chk')
    protected_calls = [re.search(m, x).group(1) for x in pltcalls \
                       if x and re.search(m, x)]
    protected_calls = {x:protected_calls.count(x) for x in protected_calls}
    unprotected_calls = [x for x in pltcalls if x and x in functions]
    unprotected_calls = {x:unprotected_calls.count(x) for x in unprotected_calls}

    if listall:
        keys = functions
    else:
        keys = set(list(protected_calls.keys()) + list(unprotected_calls.keys()))

    for k in sorted(keys):
        if k not in protected_calls.keys():
            p = 0
        else:
            p = protected_calls[k]
        if k not in unprotected_calls.keys():
            u = 0
        else:
            u = unprotected_calls[k]
        print('%s, %s, %d, %d' % (maybe_fullpath(f), k, p, u))

def should_read(f):
    # Fast check, just the file name.
    if [e for e in scan_exclude if re.search(e, f)]:
        return (False, "excluded file")

    m = magic.detect_from_filename(f)
    # Slower check, mime type.
    if not 'application/' in m.mime_type or m.mime_type not in scan_mimes:
        return (False, "unsupported mime %s" % m.mime_type)

    return (True, None)

# Get file text and feed into analyze_text.
def analyze_file(f):
    eprint('%s: Reading file' % f)
    (result, reason) = should_read(f)
    if result:
        analyze_dso(f)
    else:
        eprint('%s: SKIPPED: %s' % (f, reason))

# Actual implementation of the recursive descent into directories.
def analyze_any(p):
    try:
        mode = os.stat(p).st_mode
        if S_ISDIR(mode):
            analyze_dir(p)
        elif S_ISREG(mode) and not S_ISLNK(mode):
            analyze_file(p)
        else:
            eprint('%s: UNREADABLE' % p)
    except IOError as e:
        eprint('%s: stat failed: %s' % (p, str(e)))

# Recursively analyze files in the directory.
def analyze_dir(d):
    for f in os.listdir(d):
        analyze_any(os.path.join(d, f))

def analyze_paths(paths):
    for p in paths:
        analyze_any(p)

verbose_mode = False

def list_fortifiable():
    for f in functions:
        print(', %s, 0, 0' % f)

# Print to stderr in verbose mode.
def eprint(*args, **kwargs):
    if verbose_mode:
        print(*args, file=sys.stderr, **kwargs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get build time statistics of _FORTIFY_SOURCE coverage for ELF files in given directories.')
    parser.add_argument('path', metavar='path', nargs='+',
            help='Files or directories to analyze')
    parser.add_argument('-v', '--verbose', required=False, action='store_true',
        help='Verbose mode.')
    parser.add_argument('-l', '--listall', required=False, action='store_true',
        help='Include fortifiable functions with zero call counts.')
    parser.add_argument('-f', '--fullpath', required=False, action='store_true',
        help='Show full path in binary names.')

    args = parser.parse_args()
    listall = args.listall
    fullpath = args.fullpath

    verbose_mode = args.verbose
    analyze_paths(args.path)
