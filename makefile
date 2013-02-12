.PHONY: test bootstrap

virtualenv_dir = _virtualenv
package_tarball = whack-package-nginx.tar.gz

build: $(package_tarball)

$(package_tarball): whack/*
	rm -rf _package
	mkdir -p _package
	$(virtualenv_dir)/bin/whack build . `pwd`/_package --no-cache
	tar czf $(package_tarball) _package

test: bootstrap
	sh -c '. $(virtualenv_dir)/bin/activate; nosetests -m'\''^$$'\'' `find tests -name '\''*.py'\''`'

bootstrap: _virtualenv
	$(virtualenv_dir)/bin/pip install -r requirements.txt
	
_virtualenv:
	virtualenv $(virtualenv_dir)
