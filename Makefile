# SPDX-License-Identifier: MIT

CXX = g++
PLUGINDIR=$(shell $(CXX) -print-file-name=plugin)
CXXFLAGS += -I$(PLUGINDIR)/include -Wall -fPIC -fno-rtti -O2

all: fmetrics.so

fmetrics.so: fmetrics.o
	$(CXX) $(LDFLAGS) -shared -o $@ $<

fmetrics.o : fmetrics.cc
	$(CXX) $(CXXFLAGS) -fPIC -c -o $@ $<

clean:
	rm -f fmetrics.so fmetrics.o

check:
	make -C tests check

.PHONY: all clean
