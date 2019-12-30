# wine笔记

## LinuxMint19 安装wine

    ps: https://www.youtube.com/watch?v=R9B-tCznSDY

    sudo dpkg --add-architecture i386
    wget -nc https://dl.winehq.org/wine-builds/winehq.key
    sudo apt-key add winehq.key
    sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'

    # audio
    sudo add-apt-repository ppa:cybermax-dexter/sdl2-backport

    sudo apt update
    sudo apt install --install-recommends winehq-stable

    # 记得执行这一行, 在命令行中执行, 可以使用代理, 有利于后面的下载
    winecfg

    # 系统配了代理, 安装速度还是很快的
    mono install --> install
    gecko installer -->  install
    gecko installer -->  install



## wine 设置中文

```
sudo apt install ttf-wqy-zenhei

cp /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc ~/.wine/drive_c/windows/Fonts



zh.reg:


REGEDIT4

[HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\FontLink\SystemLink]
"Lucida Sans Unicode"="wqy-zenhei.ttc"
"Microsoft Sans Serif"="wqy-zenhei.ttc"
"Microsoft YaHei"="wqy-zenhei.ttc"
"微软雅黑"="wqy-zenhei.ttc"
"MS Sans Serif"="wqy-zenhei.ttc"
"Tahoma"="wqy-zenhei.ttc" 
"Tahoma Bold"="wqy-zenhei.ttc"
"SimSun"="wqy-zenhei.ttc"
"Arial"="wqy-zenhei.ttc"
"Arial Black"="wqy-zenhei.ttc"
"宋体"="wqy-zenhei.ttc"
"新細明體"="wqy-zenhei.ttc"

```

wine regedit zh.reg

LC_ALL=zh_CN.UTF-8 wine ProgramName
