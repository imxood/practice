#!/bin/bash

set -e -x

export LFS=/mnt/lfs

echo "LFS: $LFS"

# 挂载"/"文件系统
mkdir -pv $LFS
mkfs -v -t ext4 /dev/sda1
mount -v -t ext4 /dev/sda1 $LFS

# 内存交换分区
mkswap /dev/sda2
swapon -v /dev/sda2

# 挂载"boot"文件系统
mkdir -pv $LFS/boot
mkfs -v -t ext4 /dev/sda3
mount -v -t ext4 /dev/sda3 $LFS/boot

# 挂载"/usr/local"文件系统
mkdir -pv $LFS/usr/local
mkfs -v -t ext4 /dev/sda5
mount -v -t ext4 /dev/sda5 $LFS/usr/local

# 挂载"/tmp"文件系统
mkdir -pv $LFS/tmp
mkfs -v -t ext4 /dev/sda6
mount -v -t ext4 /dev/sda6 $LFS/tmp

# 挂载"/usr/src"文件系统
mkdir -pv $LFS/usr/src
mkfs -v -t ext4 /dev/sda7
mount -v -t ext4 /dev/sda7 $LFS/usr/src

# 挂载"/home"文件系统
mkdir -pv $LFS/home
mkfs -v -t ext4 /dev/sda8
mount -v -t ext4 /dev/sda8 $LFS/home
