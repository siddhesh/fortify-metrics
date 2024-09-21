SHELL = /bin/bash

tests = \
	builtin-dynamic-object-size-0 \
	builtin-object-size-1 \
	builtin-object-size-2 \
	builtin-object-size-3 \
	builtin-object-size-4 \
	builtin-object-size-5 \
	builtin-object-size-6 \
	builtin-object-size-7 \
	builtin-object-size-8 \
	builtin-object-size-9 \
	builtin-object-size-10 \
	builtin-object-size-11 \
	builtin-object-size-12 \
	builtin-object-size-13 \
	builtin-object-size-14 \
	builtin-object-size-15 \
	builtin-object-size-16 \
	builtin-object-size-17 \
	builtin-object-size-18 \
	builtin-object-size-19 \
	builtin-object-size-20 \
	builtin-object-size-22 \
	mult \
	min \
	vararray

PLUGIN_CFLAGS = -fplugin=../fmetrics.so -fplugin-arg-fmetrics-project=fmetrics -O2

V ?= @

check: $(patsubst %,check-%,$(tests))

check-%:%.c
	$(V)echo -n "Testing $(subst %.c,%,$^): "
	$(V)op=$$(gcc -o /dev/null -S $(PLUGIN_CFLAGS) $< 2>&1); \
	if [ $$? -eq 0 ]; then \
		op=$$(echo "$$op" | grep "^fmetrics:: "); \
		op=$$(diff -u $<.expected <(echo $$op)); \
	fi; \
	if [ "x" = "x$$op" ]; then \
		echo -e "\e[32mPASSED\e[0m"; \
	else \
		echo -e "\e[31mFAILED\e[0m:\n$$op"; \
		exit 1; \
	fi

gencheck: $(patsubst %,gencheck-%,$(tests))

gencheck-%:%.c
	$(V)echo "Generating expected result for $(subst %.c,%,$^)"
	$(V)gcc -o /dev/null -S $(PLUGIN_CFLAGS) $< \
		3>&1 1>&2 2>&3 3>&- | grep "^fmetrics:: " > $<.expected
