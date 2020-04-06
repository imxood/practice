# git笔记

## 第一次提交代码

    git init
    git add .

    git remote add origin git@github.com:imxood/MXSpice.git
    git pull origin master --allow-unrelated-histories
    git branch --set-upstream-to=origin/master

    git commit -m "."
    git push


## warning: CRLF will be replaced by LF

git config --global core.autocrlf false