FROM archlinux:latest

RUN pacman -Syu
RUN pacman --noconfirm -S python3 python-requests python-beautifulsoup4
RUN mkdir zfsdepends

COPY archzfs_synchronize.py /archzfs_synchronize.py
ENTRYPOINT ["/archzfs_synchronize.py"]