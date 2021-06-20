<div align="center">
  <img src="https://raw.githubusercontent.com/mirkobrombin/Amusiz/master/data/pm.mirko.Amusiz.svg" width="64">
  <h1 align="center">Amusiz</h1>
  <p align="center">An Amazon Music client for Linux (unpretentious)</p>
</div>

<br />

<div align="center">
    <img  src="https://raw.githubusercontent.com/mirkobrombin/Amusiz/main/data/screenshot.png">
</div>

## Installation

### AppImage
[Here](https://github.com/mirkobrombin/Amusiz/releases) you can find the latest AppImage build.

### Snap
[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/amusiz)

### Build dependencies
- meson
- ninja
- libhandy
- WebKit2

### Know issues
**Amusiz ask me to re-login each time**  
Choose the correct language from the preferences.

### Build
```bash
meson build
cd build
ninja install
```
