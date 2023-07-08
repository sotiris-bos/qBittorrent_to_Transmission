import qbittorrentapi

#This script is used with 3 torrent clients. One is the main qbittorrent client where everything is downloaded, then torrents are separated to public and private and their .torrent files are exported to a second and a third torrent client, one used for public torrents and one used for private. After the .torrent files have been created to the respective "watched" directory of each client, they are deleted from the first qbittorrent client. Thus, the first qbittorrent client has no torrents active, while the second and third can continue seeding the already downloaded torrents, with different speed and peer settings depending on if they are seeding public or private torrents. I use cron for running this python script once a day.

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
    host='_YOUR QBITTORRENT IP OR HOSTNAME HERE_',
    port=8080,
    username='_YOUR QBITTORRENT USERNAME HERE_',
    password='_YOUR QBITTORRENT PASSWORD HERE_'
 )

#Find completed/uploading public and private torrents and export their .torrent files to their respective location to be picked up by the "public" or "private" torrent client.
for torrent in qbt_client.torrents_info():
        if torrent.state_enum.is_uploading or torrent.state_enum.is_complete: 
          if not torrent.properties.is_private:
              with open(f'/mnt/media/torrents/watched/{torrent.name}.torrent', "wb") as file:  #change /mnt/media/torrents/watched/  to your second (public) torrent client's watched folder
               file.write(qbt_client.torrents_export(torrent_hash={torrent.hash}))
               qbt_client.torrents_delete(torrent_hashes={torrent.hash})
          elif torrent.properties.is_private:
              with open(f'/mnt/media/torrents/private_watched/{torrent.name}.torrent', "wb") as file:  #change /mnt/edia/torrents/watched/  to your third (private) torrent client's watched folder
               file.write(qbt_client.torrents_export(torrent_hash={torrent.hash}))
               qbt_client.torrents_delete(torrent_hashes={torrent.hash})
