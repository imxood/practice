# manjaro笔记

## 下载系统镜像

    https://mirrors.tuna.tsinghua.edu.cn/osdn/storage/g/m/ma/manjaro/xfce/19.0.2/manjaro-xfce-19.0.2-200311-linux54.iso
    
## 写到U盘

    dd if=manjaro-xfce-19.0.2-200311-linux54.iso of=/Dev/sdb bs=16M
    
## 从U盘启动

    换源
    
    sudo pacman-mirrors -c China
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
    
    # google输入法
    sudo pacman -S kcm-fcitx fcitx-googlepinyin
    
    搜狗输入法
    sudo pacman -S fcitx-lilydjwg-git fcitx-configtool fcitx-sogoupinyin
    
    ~/.xprofile
    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS="@im=fcitx"
    
    如果搜狗有问题，卸载搜狗输入法
    sudo pacman -Rs fcitx-lilydjwg-git fcitx-configtool fcitx-sogoupinyin
    cd ~/.config
    rm -rf SogouPY SogouPY.users sogou-qimpanel fcitx
    
    必要软件
    
    sudo pacman -S docker docker-compose
    sudo pacman -S visual-studio-code-bin
    sudo pacman -S make
    sudo pacman -S screenfetch
    sudo pacman -S electronic-wechat-git
    sudo pacman -S deepin.com.qq.office
    sudo pacman -S clang gdb
    sudo pacman -S flameshot-git
    sudo pacman -S wps-office ttf-wps-fonts
    sudo pacman -S netease-cloud-music
