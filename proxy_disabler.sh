# !/bin/zsh

/usr/sbin/networksetup -setwebproxystate "$1" off
/usr/sbin/networksetup -setproxybypassdomains "$1" ""
/usr/sbin/networksetup -setautoproxystate "$1" off
