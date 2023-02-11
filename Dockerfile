FROM archlinux:latest

RUN pacman -Syu
RUN pacman --noconfirm -S python3

COPY archzfs_synchronize.py /archzfs_synchronize.py
ENTRYPOINT ["/archzfs_synchronize.py"]
