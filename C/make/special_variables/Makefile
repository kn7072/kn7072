# Query the default goal.
ifeq ($(.DEFAULT_GOAL),)
$(warning no default goal is set)
endif

.PHONY: foo
foo:
	@echo $@
	@echo "end of foo"
	@echo $(.INCLUDE_DIRS)

$(warning default goal is $(.DEFAULT_GOAL))

# Reset the default goal.
.DEFAULT_GOAL :=
.PHONY: bar
bar: ; @echo $@

$(warning default goal is $(.DEFAULT_GOAL))
# Set our own.
.DEFAULT_GOAL := foo
