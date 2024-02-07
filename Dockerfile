FROM docker.io/python:3.12.1-slim-bookworm

COPY --from=docker.io/fnndsc/malpem:1.3 /opt/malpem-1.3 /opt/malpem-1.3

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="MALPEM Brain Segmentation" \
      org.opencontainers.image.description="Brain MRI bias correction, extraction, and segmentation pipeline"

ARG SRCDIR=/usr/local/src/pl-malpem
WORKDIR ${SRCDIR}

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["malpem_chris_wrapper"]
