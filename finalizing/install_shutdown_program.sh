while true; do
    read -p "This script will add sleep/wake external button capability. You must run this as root. Continue?" yn
    case $yn in
        [Yy]* ) sudo cp listen-for-shutdown.py /usr/local/bin/; sudo chmod +x /usr/local/bin/listen-for-shutdown.py; sudo cp listen-for-shutdown.sh /etc/init.d/; sudo chmod +x /etc/init.d/listen-for-shutdown.sh; sudo update-rc.d listen-for-shutdown.sh defaults; sudo /etc/init.d/listen-for-shutdown.sh start; echo "successfuly installed"; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
