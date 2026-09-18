# hackspain-maferai

| Folder | Contents |
| --- | --- |
| [`simulation/`](simulation/README.md) | MuJoCo install, 3D viewer, and the AutoBio lab scene with the GC-MS, UV-Vis-NIR and tube spawner |
| `assets/` | Source 3D models of the lab instruments (zips) |

Quick start:

```bash
cd simulation
./install.sh          # MuJoCo + viewer in .venv
./setup_autobio.sh    # AutoBio lab scenes in .venv-autobio
.venv-autobio/bin/python scripts/view_autobio.py
```
