const { app, BrowserWindow } = require('electron')

function createWindow () {
  // Cria uma janela de navegação.
  let win = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true
    }
  })

  // e carregar o index.html do aplicativo.
  win.loadFile('index.html')
  win.show()
}

app.on('ready', createWindow)