# remarkable-obsidian-sync

Sync
```sh
rsync -av root@10.11.99.1:/home/root/.local/share/remarkable/xochitl/ <path_to_remarkables>
```

Build:

```sh
docker build -t ros .
```

Run:

```sh
docker run  -v <path_to_remarkables>:/app/remarkables:ro -v <path_to_dir_in_vault>:/app/vault ros
```
