FROM archlinux:latest

RUN pacman -Syu
RUN pacman --noconfirm -S python3 python-requests python-beautifulsoup4 git
RUN mkdir zfsdepends

COPY archzfs_synchronize.py /archzfs_synchronize.py
ENTRYPOINT ["python3", "/archzfs_synchronize.py"]
