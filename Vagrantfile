$name = "ubuntu-20-networklab"

# ------------------------------------------------------------
# Description
# ------------------------------------------------------------
$description = <<'EOS'
mininet lab

user: vagrant
password: vagrant
EOS

# ------------------------------------------------------------
# install Lubutu Desktop
# ------------------------------------------------------------
$lubuntu_desktop = <<SCRIPT
sudo apt install -y --no-install-recommends lubuntu-desktop
SCRIPT

# ------------------------------------------------------------
# install FRR
# ------------------------------------------------------------
$FRR = <<SCRIPT
sudo apt install -y frr
SCRIPT


# ------------------------------------------------------------
# install basic package
# ------------------------------------------------------------
$install_package = <<SCRIPT
# install package
sudo apt -y update
sudo apt -y upgrade
sudo apt -y install python3-pip
sudo apt -y install sshpass
sudo apt -y install python3.8-dev python3.8

python3.8 -m pip install -U pip
sudo apt -y remove python-pexpect python3-pexpect

sudo apt -y install libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
sudo apt -y install git
sudo apt -y install curl
sudo apt -y install wireshark-dev

#NOTE: Should is used venv???
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade pexpect
sudo pip3 install --upgrade lxml
sudo pip3 install grpcio-tools
sudo pip3 install pyshark
sudo pip3 install scapy
sudo pip3 install mininet
sudo pip3 install aiohttp
sudo pip3 install python-socketio
sudo pip3 install nest_asyncio
sudo pip3 install python-openflow
sudo pip3 install flask
sudo pip3 install flask_socketio
sudo pip3 install macaddress
SCRIPT

# ------------------------------------------------------------
# install Vue 3
#
# References:
#    - https://linuxize.com/post/how-to-install-node-js-on-ubuntu-20-04/
# ------------------------------------------------------------
$install_vue = <<SCRIPT
sudo curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install -y nodejs

sudo chown -R vagrant /usr/lib/node_modules/
sudo npm install -g n
sudo npm install -g @vue/cli

sudo n install 10.16.0
SCRIPT


# ------------------------------------------------------------
# install mininet with bofuss
# ------------------------------------------------------------
$install_mininet = <<SCRIPT
git clone git://github.com/mininet/mininet
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
# install ryu
# Libraries dependent on ryu are added here as required
# ------------------------------------------------------------
$install_ryu = <<SCRIPT
sudo apt install -y python3-ryu
SCRIPT

# ------------------------------------------------------------
# vagrant configure version 2
# ------------------------------------------------------------
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    # vm name
    config.vm.hostname = $name + '.localhost'
    # ubuntu image
    config.vm.box = "bento/ubuntu-20.04"

    # network
    config.vm.network 'private_network', ip: '10.0.0.123'

    # install package
    config.vm.provision 'shell', inline: $install_package
    config.vm.provision 'shell', inline: $install_mininet
    config.vm.provision 'shell', inline: $install_ryu
    config.vm.provision 'shell', inline: $lubuntu_desktop
    config.vm.provision 'shell', inline: $FRR

    config.vm.synced_folder '.', '/vagrant', disabled: true
    config.vm.synced_folder './', '/home/vagrant/netwarkLab'

    # ssh config
    # config.ssh.username = 'vagrant'
    # config.ssh.password = 'vagrant'
    # config.ssh.insert_key = false

    # config virtual box
    config.vm.provider "virtualbox" do |vb|
        vb.name = $name
        vb.gui = true

        vb.cpus = 2
        vb.memory = "4096"

        vb.customize [
            "modifyvm", :id,
            "--vram", "128", # full screen
            "--clipboard", "bidirectional", # clip board
            "--draganddrop", "bidirectional", # drag and drop
            "--ioapic", "on", # enable I/O APIC
            "--accelerate3d", "on",
            "--hwvirtex", "on",
            "--nestedpaging", "on",
            "--largepages", "on",
            "--pae", "on",
            "--description", $description
        ]
    end
end