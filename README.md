# qBittorrent_to_Transmission
Automatically moving qBittorrent torrents to Transmission


 My use case: I use qBittorrent to download torrent files because of its superior speed, but I like the Transmission GUI and way of handling things. I wanted to find a way to download stuff through qBittorrent, then move them to my Transmission torrent clients depending on if they are public or private torrents. This is source agnostic, aka you can use this with Sonarr and Radarr as I am, to manage torrents. However, any Indexer settings set in Sonarr or Radarr will not work with this script.
 
 I have a public Transmission torrent client that has an upload bandwidth limit of ~15% of my ISP's upload bandwidth. I also have a private Transmission client that has unlimited upload speed for torrents that are provided by private trackers in order to increase my ratio and uploaded data.
 
 
 My concept is as such: have a shared folder where everything is moved after download. I call this /mnt/torrents.  Have a watched folder for each Transmission client, e.g. /mnt/transmission_public and /mnt/transmission_private. Optional: have separate folders as temporary download locations for each client, e.g. /mnt/qbittorrent_temp, /mnt/transmission_private_temp, /mnt/transmission_public/temp. These are used as "scratchdisks" to download torrents (hosted on an enterprise-grade SSD), then the torrents are moved to their final location at /mnt/torrents, this is done in order to avoid fragmentation because I use ZFS as a filesystem and ZFS cannot be defragged.
 
 I use docker for all my torrent clients and I have a single host for all containers. This guide should work for regular installs as well.
 
 You will need to install the qbittorentapi and shutil python packages on your linux host.
 
 The script provided that makes all of this happen is a python script. It queries the qBittorrent client for uploading or completed downloads, checks to see if they are private or public torrents, then copies the .torrent files to the respective "watched" directory of the public or private (transmission) client. It just copies the .torrent files to directories, so it should be usable with other torrent clients that have "watched" directories. The Transmission clients automatically recognize the downloaded files and instantly begin to seed them, instead of re-downloading them. It is crucial that all download clients are running under a user that has a group access to the files. E.g., I have separate users for each download client, qbittorent user runs the qbittorent docker container, transmission_public runs the transmission_public container and transmission_private runs the transmission_private container (all provided by linuxserver.io). All 3 users are part of the media group and the qBittorrent client is set to change the permissions of all the downloaded torrens to 770. You can do this by setting: ``` Tools-> Options-> Run External Program -> Run external program on torrent finished: chmod -R 770 "%F/" ``` in the qBittorrent Web UI. This gives all the required permissions to the media group, so all clients are able to access and modify the data stored under /mnt/torrents. All you need to do is edit the qBittorrent host, (port), username and password, and the temporary and permanent download file locations according to your application. The script will search for private or public torrent files on the qBittorrent client, copy the torrent files to the respective watch folders, then delete the torrents from the qBittorrent client.
 
  The script runs on the host, I run it through cron. You can set a specific time of day to run the script. My crontab looks like this:
  ```
  0 5 * * * /usr/bin/python3 /root/.scripts/qbit.py
  ```
  
  It runs on 05:00am every day. You might need to change the python directory depending on your distro and you might need to set your qbit.py script as executable (chmod +x qbit.py).
