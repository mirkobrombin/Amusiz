function fixVolumeBar() {
    var volBar = document.getElementById('volume-range')
    if (volBar === null) return

    volBar.setAttribute('step', '0.05')
}
setInterval(() => fixVolumeBar(), 300)
