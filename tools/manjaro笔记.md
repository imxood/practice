# manjaro笔记

## 下载系统镜像

    https://mirrors.tuna.tsinghua.edu.cn/osdn/storage/g/m/ma/manjaro/xfce/19.0.2/manjaro-xfce-19.0.2-200311-linux54.iso
    
## 写到U盘

    dd if=manjaro-xfce-19.0.2-200311-linux54.iso of=/Dev/sdb bs=16M
    
## 从U盘启动

    换源
    
    sudo pacman -Syy
    sudo pacman-mirrors -i -c China -m rank  #选一个清华源就行
    sudo pacman -Syyu
    
    sudo pacman -S vim
    sudo vim /etc/pacman.conf
    
    [archlinuxcn]
    SigLevel = Optional TrustedOnly
    Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
    
    sudo pacman -Syy && sudo pacman -S archlinuxcn-keyring
    
    安装zsh
    
    sudo pacman -S git
    sudo pacman -S zsh
    sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    chsh -s /bin/zsha
    
    安装输入法
    
    sudo pacman -S fcitx-sogoupinyin
    sudo pacman -S fcitx-im # 全部安装
    sudo pacman -S fcitx-configtool # 图形化配置工具
    
    ~/.xprofile
    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS="@im=fcitx"
    
    必要软件
    
    sudo pacman -S visual-studio-code-bin
    sudo pacman -S make
    sudo pacman -S screenfetch
    sudo pacman -S electronic-wechat-git
    sudo pacman -S deepin.com.qq.office
    sudo pacman -S clang gdb
    sudo pacman -S flameshot-git
    sudo pacman -S wps-office
