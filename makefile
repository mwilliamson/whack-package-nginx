.PHONY: test bootstrap

virtualenv_dir = _virtualenv
package_tarball = whack-package-nginx.tar.gz

build: $(package_tarball)

$(package_tarball): whack/*
	$(virtualenv_dir)/bin/whack get-package-tarball . .

test: bootstrap
	sh -c '. $(virtualenv_dir)/bin/activate; nosetests -m'\''^$$'\'' `find tests -name '\''*.py'\''`'

bootstrap: _virtualenv
	$(virtualenv_dir)/bin/pip install -r requirements.txt
	
_virtualenv:
	virtualenv $(virtualenv_dir)
