tests = vararray mult
PLUGIN_CFLAGS = -fplugin=../fmetrics.so -fplugin-arg-fmetrics-project=fmetrics -O2

V ?= @

check: $(patsubst %,check-%,$(tests))

check-%:%.c
	$(V)echo -n "Testing $(subst %.c,%,$^): "
	$(V)op=$$(diff -u $<.expected \
		          <(gcc -o /dev/null -S $(PLUGIN_CFLAGS) $< \
			    3>&1 1>&2 2>&3 3>&- | grep "^fmetrics:: ")) \
	&& echo -e "\e[32mPASSED\e[0m" || echo -e "\e[31mFAILED\e[0m:\n$$op"
