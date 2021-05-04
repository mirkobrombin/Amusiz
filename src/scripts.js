function DecreaseVolume() {
    var volBar = document.getElementById('volume-range')
    if (volBar === null) {
        document.getElementById('volume-button').click()
        setTimeout(() => {
            DecreaseVolume()
        }, 300)
        return
    }
    var currentVolume = parseFloat(volBar.value)
    var newVolume = currentVolume - 0.05
    if(newVolume < 0) newVolume = 0.0
    volBar.value = newVolume.toString()
    if ("createEvent" in document) {
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", false, true);
        volBar.dispatchEvent(evt);
    }
    else
        volBar.fireEvent("onchange");
}

function IncreaseVolume() {
    var volBar = document.getElementById('volume-range')
    if (volBar === null) {
        document.getElementById('volume-button').click()
        setTimeout(() => {
            DecreaseVolume()
        }, 300)
        return
    }
    var currentVolume = parseFloat(volBar.value)
    var newVolume = currentVolume + 0.05
    if(newVolume > 1) newVolume = 1.0
    volBar.value = newVolume.toString()
    if ("createEvent" in document) {
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", false, true);
        volBar.dispatchEvent(evt);
    }
    else
        volBar.fireEvent("onchange");
}

function fixVolumeBar() {
    var volBar = document.getElementById('volume-range')
    if (volBar === null) return

    volBar.setAttribute('step', '0.05')
}
setInterval(() => fixVolumeBar(), 300)


/*var ready = function () {

  document.getElementById("accountSetting").click();

	if (document.body && document.querySelector("#contextMenuOverlay[aria-label='menu']")) {
    setTimeout(() => {
        user = document.querySelector("#contextMenuOverlay[aria-label='menu'] > div > music-context-menu-header").getAttribute("primary-text");
        alert(user)
    }, 300)
		return;
	}
	window.requestAnimationFrame(ready);
};

window.requestAnimationFrame(ready);*/
