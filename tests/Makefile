tests = vararray mult
PLUGIN_CFLAGS = -fplugin=../fmetrics.so -fplugin-arg-fmetrics-project=fmetrics -O2

check: $(patsubst %,check-%,$(tests))

check-%:%.c
	diff -u $<.expected <(gcc -o /dev/null -S $(PLUGIN_CFLAGS) $< 3>&1 1>&2 2>&3 3>&- | grep "^fmetrics:: ")
