import os
import shutil

from nose.tools import istest
import requests
import starboard
import spur


shell = spur.LocalShell()


@istest
def default_installation_serves_default_page():
    nginx_port = starboard.find_local_free_tcp_port()
    install_dir = "_test-install-dir"
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    shell.run(
        ["whack", "install", ".", install_dir],
    )
    conf_path = os.path.join(install_dir, "conf/nginx.conf")
    shell.run([
        "sed", "-ie",
        r"s/listen\s\+80\s*;/listen {0};/g".format(nginx_port),
        conf_path,
    ])
    shell.run([os.path.join(install_dir, "sbin/nginx")])
    response = requests.get("http://localhost:{0}".format(nginx_port))
    assert "Welcome to nginx!" in response.text, "Response text was: \n{0}".format(response.text)
