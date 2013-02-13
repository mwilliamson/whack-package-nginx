import os

from nose.tools import istest
import peachtree
import requests


@istest
def default_installation_serves_default_page():
    with _start_virtual_machine() as machine:
        _install_whack(machine)
        
        working_dir = _upload_source(machine)
        shell = machine.shell()
        install_dir = shell.run(["sh", "-c", "echo ~/install-dir"]).output.strip()
        shell.run(
            ["whack", "install", working_dir, install_dir],
        )
        conf_path = os.path.join(install_dir, "conf/nginx.conf")
        shell.run([
            "sed", "-ie",
            r"s/listen\s\+80\s*;/listen {0};/g".format(_nginx_port),
            conf_path,
        ])
        shell.run([os.path.join(install_dir, "sbin/nginx")])
        response = requests.get("http://localhost:{0}".format(machine.public_port(_nginx_port)))
        assert "Welcome to nginx!" in response.text
        
        

def _start_virtual_machine():
    return peachtree.qemu_provider().start(
        "ubuntu-precise-amd64-whack",
        public_ports=[_nginx_port]
    )


def _install_whack(machine):
    whack_rooter_path = "/usr/local/bin/whack-run-with-whack-root"
    with open(whack_rooter_path, "rb") as whack_rooter_file:
        whack_rooter_contents = whack_rooter_file.read()
        
    root_shell = machine.root_shell()
    
    with root_shell.open(whack_rooter_path, "wb") as remote_whack_rooter_file:
        remote_whack_rooter_file.write(whack_rooter_contents)
    root_shell.run(["chmod", "+xs", whack_rooter_path])
        
    root_shell.run(["pip", "install", "whack"])


def _package_source_root():
    return os.path.dirname(os.path.dirname(__file__))


def _upload_source(machine):
    shell = machine.shell()
    working_dir = shell.run(["sh", "-c", "echo ~/working-dir"]).output.strip()
    # TODO: should only copy across source files that are specified
    shell.upload_dir(_package_source_root(), working_dir, ignore=[])
    return working_dir
    

_nginx_port = 8080
