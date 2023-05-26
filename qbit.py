import qbittorrentapi
import shutil

qbt_client = qbittorrentapi.Client(
    host='YOUR QBITTORRENT IP HERE',
    port=8080,
    username='USERNAME',
    password='PASSWORD'
 )

# retrieve and show all torrents
for torrent in qbt_client.torrents_info():
        if torrent.state_enum.is_uploading or torrent.state_enum.is_complete: 
          if not torrent.properties.is_private:
                shutil.copyfile(f'/var/lib/docker/volumes/qbittorrent/config/qBittorrent/BT_backup/{torrent.hash}.torrent', f'/mnt/PUBLIC_WATCHED_TRANSMISSION_DIR/{torrent.name}.torrent') # Change /var/lib/docker/volumes/qbittorrent/BT_backup to your according location if needed.
                qbt_client.torrents_delete(torrent_hashes={torrent.hash})
          elif torrent.properties.is_private:
                shutil.copyfile(f'/var/lib/docker/volumes/qbittorrent/config/qBittorrent/BT_backup/{torrent.hash}.torrent', f'/mnt/PRIVATE_WATCHED_TRANSMISSION_DIR/{torrent.name}.torrent') # Change /var/lib/docker/volumes/qbittorrent/BT_backup to your according location if needed.
                qbt_client.torrents_delete(torrent_hashes={torrent.hash})
