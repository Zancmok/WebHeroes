FROM ubuntu:24.04

WORKDIR /build

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    liblua5.4-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN gcc -O3 -Wall -fPIC -shared \
    $(python3-config --cflags) \
    $(pkg-config --cflags lua5.4) \
    lua_bridge.c base_prototype.c lua_sandbox.c prototype_definition.c \
    $(pkg-config --libs lua5.4) \
    $(python3-config --ldflags) \
    -o /build/LuaBridge.so
