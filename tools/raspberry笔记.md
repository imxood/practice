# raspberry笔记

## 使用imager烧写TF卡

    https://mirrors.tuna.tsinghua.edu.cn/raspbian-images/raspbian_lite/images/raspbian_lite-2020-02-14/2020-02-13-raspbian-buster-lite.zip

## 烧写后, 先在boot分区中,添加一个文件名是"ssh"的文件, 无后缀, 空文件, 这样会默认开启ssh, 这样可以不用显示屏

## 修改软件源

    /etc/apt/sources.list
    
    # deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
    deb http://mirrors.aliyun.com/raspbian/raspbian/ buster main contrib non-free rpi
    
    /etc/apt/sources.list.d/raspi.list
    
    # deb http://archive.raspberrypi.org/debian/ buster main
    deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ buster main
    
## 修改密码, reboot

## 安装OMV

    在树莓派上安装OMV:
    https://github.com/OpenMediaVault-Plugin-Developers/docs
    
## issues

    --2020-04-18 04:01:08--  https://github.com/OpenMediaVault-Plugin-Developers/installScript/raw/master/install
    Resolving github.com (github.com)... 13.250.177.223
    Connecting to github.com (github.com)|13.250.177.223|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/install [following]
    --2020-04-18 04:01:09--  https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/install
    Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 0.0.0.0, ::
    Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|0.0.0.0|:443... failed: Connection refused.
    Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|::|:443... failed: Connection refused.
    
    
    
    
