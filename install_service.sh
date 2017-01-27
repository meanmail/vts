#! /bin/sh
#debian 6 stable or later

echo "Installing VTS-bot as a Debian service"

# coping script
echo "Coping vts.example.sh --> vts.sh"
cp vts.example.sh vts.sh

# path script
dir=$(pwd)
echo "Setting path to vts.py: ${dir}"
sed -i "s%/path/to/vts%${dir}%" vts.sh

# setting as executable
chmod +x vts.sh

# install service
sudo insserv -v -r /etc/init.d/vts.sh
sudo cp -f vts.sh /etc/init.d/vts.sh
sudo insserv -v -f /etc/init.d/vts.sh
sudo systemctl daemon-reload