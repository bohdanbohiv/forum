#! /usr/bin/env bash

set -e
set -x

python -m app.pre_start

alembic upgrade head
