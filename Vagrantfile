$name = "ubuntu-20-networklab"

# ------------------------------------------------------------
# Description
# ------------------------------------------------------------
$description = <<'EOS'
# Mininet Lab

user: vagrant
password: vagrant
EOS


# ------------------------------------------------------------
# install basic package
# ------------------------------------------------------------
$install_package = <<SCRIPT
sudo apt -y update
sudo apt -y upgrade

sudo apt -y install build-essential
sudo apt -y install sshpass
sudo apt -y install python3
sudo apt -y install python3-pip

python3 -m pip install -U pip

sudo apt -y install libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
sudo apt -y install git
sudo apt -y install curl
sudo apt -y install wireshark-dev

sudo pip3 install --upgrade pip

sudo apt install -y golang

# sudo timedatectl set-timezone Asia/Tokyo
# sudo cat << 'EOF' | sudo tee /etc/default/keyboard
# # KEYBOARD CONFIGURATION FILE

# # Consult the keyboard(5) manual page.

# XKBMODEL="pc105"
# XKBLAYOUT="jp"
# XKBVARIANT=""
# XKBOPTIONS=""

# BACKSPACE="guess"
# EOF
SCRIPT


# ------------------------------------------------------------
# install mininet
# ------------------------------------------------------------
$install_mininet = <<SCRIPT
git clone https://github.com/mininet/mininet
cd mininet
# git tag  # list available versions
git checkout -b mininet-2.3.0 2.3.0  # or whatever version you wish to install
cd ..
# mininet/util/install.sh -n3fw
mininet/util/install.sh -a

sudo apt -y install openvswitch-switch
sudo service openvswitch-switch start
SCRIPT


# ------------------------------------------------------------
# install Lubutu Desktop
# ------------------------------------------------------------
$install_lubuntu = <<SCRIPT
sudo apt install -y --no-install-recommends lubuntu-desktop
SCRIPT


# ------------------------------------------------------------
# install FRR
# ------------------------------------------------------------
$install_frr = <<SCRIPT
# sudo apt install -y frr

## installing Dependencies
sudo apt update -y
sudo apt-get install -y \
   git autoconf automake libtool make libreadline-dev texinfo \
   pkg-config libpam0g-dev libjson-c-dev bison flex \
   libc-ares-dev python3-dev python3-sphinx \
   install-info build-essential libsnmp-dev perl \
   libcap-dev python2 libelf-dev libunwind-dev

## install libyang
sudo apt install -y cmake
git clone https://github.com/CESNET/libyang.git
cd libyang
git checkout v2.0.0
mkdir build; cd build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr \
      -D CMAKE_BUILD_TYPE:String="Release" ..
make
sudo make install
cd ../../
rm -rf libyang

## install Protobuf
sudo apt-get install -y protobuf-c-compiler libprotobuf-c-dev

## install ZeroMQ
sudo apt-get install -y libzmq5 libzmq3-dev

## Add FRR user and groups
sudo groupadd -r -g 92 frr
sudo groupadd -r -g 85 frrvty
sudo adduser --system --ingroup frr --home /var/run/frr/ \
   --gecos "FRR suite" --shell /sbin/nologin frr
sudo usermod -a -G frrvty frr

## install FRR
git clone https://github.com/frrouting/frr.git frr
cd frr
./bootstrap.sh
./configure \
    --prefix=/usr \
    --includedir=\${prefix}/include \
    --bindir=\${prefix}/bin \
    --sbindir=\${prefix}/lib/frr \
    --libdir=\${prefix}/lib/frr \
    --libexecdir=\${prefix}/lib/frr \
    --localstatedir=/var/run/frr \
    --sysconfdir=/etc/frr \
    --with-moduledir=\${prefix}/lib/frr/modules \
    --with-libyang-pluginsdir=\${prefix}/lib/frr/libyang_plugins \
    --enable-configfile-mask=0640 \
    --enable-logfile-mask=0640 \
    --enable-snmp=agentx \
    --enable-multipath=64 \
    --enable-user=frr \
    --enable-group=frr \
    --enable-vty-group=frrvty \
    --with-pkg-git-version 
make
sudo make install
cd ..
rm -rf frr/
SCRIPT

# ------------------------------------------------------------
# vagrant configure version 2
# ------------------------------------------------------------
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    # vm name
    config.vm.hostname = $name + '.localhost'
    # ubuntu image
    # config.vm.box = 'bento/ubuntu-18.04'
    # config.vm.box = 'bento/ubuntu-20.04'
    config.vm.box = "ubuntu/jammy64"

    # share directory
    config.vm.synced_folder './', '/home/vagrant/share'

    # install package
    config.vm.provision 'shell', inline: $install_package
    config.vm.provision 'shell', inline: $install_mininet
    # config.vm.provision 'shell', inline: $install_lubuntu
    config.vm.provision 'shell', inline: $install_frr

    # config virtual box
    config.vm.provider "virtualbox" do |vb|
        vb.name = $name
        vb.gui = true

        vb.cpus = 6
        vb.memory = "4096"
    
        vb.customize [
            "modifyvm", :id,
            "--vram", "32", 
            "--clipboard", "bidirectional", # clip board
            "--draganddrop", "bidirectional", # drag and drop
            "--ioapic", "on", # enable I/O APIC
            '--graphicscontroller', 'vmsvga',
            "--accelerate3d", "off",
            "--hwvirtex", "on",
            "--nestedpaging", "on",
            "--largepages", "on",
            "--pae", "on",
            '--audio', 'none',
            "--uartmode1", "disconnected",
            "--description", $description
        ]
    end
end
