ARG BASE_IMAGE=i386/debian:buster
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND noninteractive

# Pi-Gen Build Dependencies
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
        git vim parted \
        quilt coreutils qemu-user-static debootstrap zerofree zip dosfstools \
        bsdtar libcap2-bin rsync grep udev xz-utils curl xxd file kmod bc\
        binfmt-support ca-certificates qemu-utils kpartx \
    && rm -rf /var/lib/apt/lists/*

# Python Wrapper Dependencies
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip

RUN pip3 install \
        python-dotenv

WORKDIR /build

COPY . build/pi-gen/

ENTRYPOINT [ "python3", "build/build.py" ]
