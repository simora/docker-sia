FROM lsiobase/ubuntu:bionic

ENV DEBIAN_FRONTEND="noninteractive" \
SIA_DIR="/sia" \
SIA_DATA_DIR="/sia-data"

RUN apt-get update
RUN apt-get install -y \
      python3 \
      python3-requests \
      python3-bs4 \
      unzip \
      socat

# Workaround for backwards compatibility with old images, which hardcoded the
# Sia data directory as /mnt/sia. Creates a symbolic link so that any previous
# path references stored in the Sia host config still work.
RUN ln --symbolic "$SIA_DATA_DIR" /mnt/sia

EXPOSE 9980 9981 9982

# add local files
COPY root/ /
