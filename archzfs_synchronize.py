import tarfile
import tempfile
import requests
import os
import sys
from bs4 import BeautifulSoup

KERNELS = ["linux", "linux-headers", "linux-zen", "linux-zen-headers"]
WORKING_DIR = tempfile.mkdtemp(suffix=".archzfs_synchronize.py")

REPO_NAME = "zfsdepends"
REPO_DIR = f"./{REPO_NAME}"
REPO_DBS = set([f"{REPO_NAME}.db", f"{REPO_NAME}.db.tar.zst", f"{REPO_NAME}.files", f"{REPO_NAME}.files.tar.zst", f"{REPO_NAME}.db.tar.zst.old", f"{REPO_NAME}.files.tar.zst.old"])

ARCHZFS_DB = f"{WORKING_DIR}/archzfs.db"

ARCHIVE_REPO_URL = "https://archive.archlinux.org/packages"
ARCHZFS_REPO_URL = "http://archzfs.com/archzfs/x86_64"

KERNEL_TO_MODULE = lambda package: "zfs-" + package

def archzfs_package_version(package):
    if not os.path.isfile(ARCHZFS_DB):
        download_file(f"{ARCHZFS_REPO_URL}/archzfs.db", ARCHZFS_DB)
    
    module = KERNEL_TO_MODULE(package)

    with tarfile.open(ARCHZFS_DB) as tar:
        files = tar.getnames()
        files.sort()
        
        # assumes that the package name does not contain numbers
        package_dir = next(file for file in files if file.startswith(module))
        desc = tar.extractfile(f"{package_dir}/desc").read()
    
    desc = desc.decode("utf-8")

    # either check dependencies or make dependencies, depending on if the package is a kernel or a header
    if package.endswith("-headers"):
        section = "%MAKEDEPENDS%"
    else:
        section = "%DEPENDS%"

    deps = desc.split(section)[-1].split("\n\n")[0].split("\n")
    package_version = next(dep.split('=')[1] for dep in deps if dep.split('=')[0] == package)

    return package + '-' + package_version

def archive_package_url(package):
    return f"{ARCHIVE_REPO_URL}/{package[0]}/{package}"

def download_file(url, destination):
    response = requests.get(url, stream = True)

    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size = 1024):
            if chunk: # filter out keep-alive new chunks
                file.write(chunk)

def archive_package_versions(package):
    response = requests.get(archive_package_url(package))
    html = BeautifulSoup(response.text, 'html.parser')
    packages = []

    for anchor in html.pre.find_all("a"):
        href = anchor.get("href")
        file_type = href.split('.')[-1]

        if file_type == "zst" or file_type == "xz":
            packages.append(href)

    return packages

def execute(command):
    with os.popen(command) as pipe:
        # stdout = ANSI_ESCAPE.sub("", pipe.read())
        for line in pipe.read().split('\n'):
            # consider better logging than just print
            print(f"{command}: {line}", file=sys.stderr)

def main():
    if not os.path.isdir(REPO_DIR):
        print(f"Error: REPO_DIR={REPO_DIR} does not exist", file=sys.stderr)
        exit(1)

    new_packages = set()
    unused_packages = set(os.listdir(REPO_DIR))

    for kernel in KERNELS:
        target_package = archzfs_package_version(kernel)
        available_packages = archive_package_versions(kernel)

        package = next(pkg for pkg in available_packages if pkg.startswith(target_package))
        new_packages.add(package)
    
        url = archive_package_url(package)
        download_file(url, f"{REPO_DIR}/{package}")
    
    unused_packages -= new_packages.union(REPO_DBS)

    for pkg in unused_packages:
        # print(f"would run os.remove(f\"{REPO_DIR}/{pkg}\")")
        os.remove(f"{REPO_DIR}/{pkg}")
    
    unused_packages = ' '.join(f"{REPO_DIR}/{pkg}" for pkg in unused_packages)
    execute(f"repo-remove -n {REPO_DIR}/{REPO_NAME}.db.tar.zst {unused_packages}")   

    packages = ' '.join(f"{REPO_DIR}/{pkg}" for pkg in new_packages)

    if packages:
        execute(f"repo-add -n {REPO_DIR}/{REPO_NAME}.db.tar.zst {packages}")   

if __name__ == "__main__":
    main()
