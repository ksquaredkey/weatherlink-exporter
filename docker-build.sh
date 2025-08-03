#!/bin/sh

VERSION=0.0.0

docker buildx build \
  --push \
  --platform linux/amd64,linux/arm64 \
  --tag "ghcr.io/ksquaredkey/weatherlink-exporter:${VERSION}"  .
