# !/bin/zsh

/usr/sbin/networksetup -setwebproxystate Wi-Fi off
/usr/sbin/networksetup -setproxybypassdomains Wi-Fi ""
/usr/sbin/networksetup -setautoproxystate Wi-Fi off
