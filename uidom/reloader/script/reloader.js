
function reloader_connect(isReconnect = false) {
  const reconnectInterval = parseFloat("$reloader::reconnect_interval");
  let endPointURL = "$reloader::url";
  let url = new URL(document.location);
  const wsHostPort = `${url.protocol.replace('http', 'ws')}//${url.hostname}:${url.port}`;
  if (!endPointURL.includes(wsHostPort)){
    endPointURL = `${wsHostPort}${endPointURL}`;
  }
  const ws = new WebSocket(endPointURL);
  
  function log_info(msg) {
    console.info(`[reloader] ${msg}`);
  }

  // https://stackoverflow.com/a/76892302

  const clearCacheAndReload =  () => {
    if('caches' in window){
        log_info("Clearing cache.");
        caches.keys().then((names) => {
            names.forEach(async (name) => {
                await caches.delete(name)
            })
          log_info("Cache cleared.");
        })
    }
    log_info("Reloading.");
    window.location.reload();
  }


  ws.onopen = function () {
    if (isReconnect) {
      // The server may have disconnected while it was reloading itself,
      // e.g. because the app Python source code has changed.
      // The page content may have changed because of this, so we don't
      // just want to reconnect, but also get that new page content.
      // A simple way to do this is to reload the page.
      clearCacheAndReload();
      return;
    }

    log_info("Connected.");
  };

  ws.onmessage = function (event) {
    if (event.data === "reload") {
      clearCacheAndReload();
    }
  };

  // Cleanly close the WebSocket before the page closes (1).
  window.addEventListener("beforeunload", function () {
    ws.close(1000);
  });

  ws.onclose = function (event) {
    if (event.code === 1000) {
      // Side-effect of (1). Ignore.
      return;
    }

    log_info(
      `WebSocket is closed. Will attempt reconnecting in ${reconnectInterval} seconds...`
    );

    setTimeout(function () {
      const isReconnect = true;
      reloader_connect(isReconnect);
    }, reconnectInterval * 1000);
  };
}

reloader_connect();
