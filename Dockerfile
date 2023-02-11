FROM archlinux:latest

RUN pacman --noconfirm -Syu python3 python-requests python-beautifulsoup4 git
RUN mkdir zfsdepends

COPY archzfs_synchronize.py /archzfs_synchronize.py
ENTRYPOINT ["update-repo.sh"]
