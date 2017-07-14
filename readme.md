## Install

## SD Card Fresh Install

Assuming OS X install. Based upon the [Official Installation Guide](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md).

1. [Download](https://www.raspberrypi.org/downloads/raspbian/) latest Raspbian Lite Distro
2. Insert SD Card into the Mac
3. Find the SD Card's dev diskID with ```df -h```
4. Unmount the correct disk ```sudo diskutil unmount /dev/disk2s1```
5. Copy the .img file downloaded (and unzipped if needed). Ensure that you are targeting the correct .img file, the correct /dev/disk (s does not matter) ```sudo dd if=/Users/cchapman/Downloads/2017-07-05-raspbian-jessie-lite.img of=/dev/disk2 bs=1m```
6. Load SD Card into Pi
7. Login 'pi'
8. pwd 'raspberry'
9. Localization Options - US Keyboard
10. Advanced Options - Expand File System
11. Enable SSH
12. Enable Remote GPIO
13. reboot


Edit the wpa file.

```sudo nano /etc/wpa_supplicant/wpa_supplicant.conf```

Configure the file to your network specification

```shell
country=US

network={
    ssid="NetworkName"
    psk="NetworkPassword"
}
```

Install git

```
sudo apt-get update && sudo apt-get install git-all -y
```

Install Docker

```
curl -sSL https://get.docker.com | sh
```

Add the docker user to the pi group

```
sudo usermod -aG docker pi
```


### Install Docker Compose on the RPI
 
Based upon the guide defined on the [Getting Docker Compose on RPI](https://www.berthon.eu/2017/getting-docker-compose-on-raspberry-pi-arm-the-easy-way/)

```
git clone https://github.com/docker/compose.git
cd compose
git checkout release
```

```
sudo docker build -t docker-compose:armhf -f Dockerfile.armhf .
```

```
sudo docker run --rm --entrypoint="script/build/linux-entrypoint" -v $(pwd)/dist:/code/dist -v $(pwd)/.git:/code/.git "docker-compose:armhf"
```