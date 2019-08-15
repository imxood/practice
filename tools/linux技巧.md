# Linux技巧

## ssh 免密登录

生成证书:

    ssh-keygen -t rsa

拷贝公钥到服务器上:

    ssh-copy-id USER@HOST
