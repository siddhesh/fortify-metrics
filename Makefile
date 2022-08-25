# SPDX-License-Identifier: MIT
DISTVER = 0.1
PROJECT = fortify-metrics
CXX = g++
PLUGINDIR=$(shell $(CXX) -print-file-name=plugin)
CXXFLAGS += -I$(PLUGINDIR)/include -Wall -fPIC -fno-rtti -O2

distfiles = fortify-metrics.py fmetrics.cc README.md LICENSE Makefile tests

all: fmetrics.so

fmetrics.so: fmetrics.o
	$(CXX) $(LDFLAGS) -shared -o $@ $<

fmetrics.o : fmetrics.cc
	$(CXX) $(CXXFLAGS) -fPIC -c -o $@ $<

clean:
	rm -f fmetrics.so fmetrics.o

check:
	make -C tests check

LIBDIR ?= /usr/local/lib
BINDIR ?= /usr/local/bin

install:
	mkdir -p $(DESTDIR)$(LIBDIR)
	cp fmetrics.so $(DESTDIR)$(LIBDIR)/
	mkdir -p $(DESTDIR)$(BINDIR)
	cp fortify-metrics.py $(DESTDIR)$(BINDIR)/

DIR = $(PROJECT)-$(DISTVER)
TAR = $(DIR).tar.gz

dist:
	tar --transform 's,^,$(DIR)/,' -czf $(TAR) $(distfiles)

.PHONY: all clean
