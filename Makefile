clean: clean-pyc

# Remove *.pyc files, ignoring dotfiles
clean-pyc: log
	find . \( ! -regex '.*/\..*' \) -type f -name '*.pyc' -print0 \
		| xargs -0 rm -f -v > log/clean-pyc.log
	wc -l log/clean-pyc.log

log:
	mkdir -p log
