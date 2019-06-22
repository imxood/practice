
# find your device
lsblk

# first make three partions: / /boot /home
# ...


# mount point: /mnt /mnt/boot /mnt/home
# ...

sudo pacstrap /mnt base base-devel

# need to check the fstab's correctness
sudo genfstab -U /mnt | sudo tee /mnt/etc/fstab

sudo arch-chroot /mnt

ls -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

hwclock --systohc

pacman -S vim

pacman -S bash-completion
. /etc/bash.bashrc

pacman -S networkmanager
systemctl enable NetworkManager.service

# en_US.UTF-8 UTF-8
# zh_CN.UTF-8 UTF-8
vim /etc/locale.gen

locale-gen

echo 'LANG=en_US.UTF-8' > /etc/locale.cfg

echo 'YourPcName' > /etc/hostname

cat - > /etc/hosts << eof
127.0.0.1       localhost
::1             localhost
127.0.0.1       maxu-pc.localdomain maxu-pc
eof

pacman -S grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchLinux --boot-directory=/boot --debug

passwd

# add new user
useradd -m -g wheel -s /bin/bash UserName
passwd UserName

# search: wheel, add sudo authority to wheel group
visudo

# Chinese font
pacman -S ttf-dejavu ttf-liberation wqy-microhei

# install desktop

pacman -S xorg-server

# video driver
pacman -S xf86-video-intel nvidia

# input device
pacman -S xf86-input-libinput xf86-input-synaptics

# display manager
pacman -S lightdm lightdm-gtk-greeter
systemctl enable lightdm.service

# add greeter-session=lightdm-gtk-greeter
vim /etc/lightdm/lightdm.conf

# kde desktop
pacman -S plasma-desktop kdebase

exit