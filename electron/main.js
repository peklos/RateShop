const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

// Fix black screen on machines with old/incompatible GPU drivers
app.disableHardwareAcceleration();
app.commandLine.appendSwitch('disable-gpu');
app.commandLine.appendSwitch('disable-software-rasterizer');

let mainWindow = null;
let pythonProcess = null;

const BACKEND_PORT = 8000;
const BACKEND_URL = `http://127.0.0.1:${BACKEND_PORT}`;

function getBackendPath() {
  const isPackaged = app.isPackaged;

  if (isPackaged) {
    const platform = process.platform;
    const exeName = platform === 'win32' ? 'RateShopBackend.exe' : 'RateShopBackend';
    // In packaged app, backend is in resources/backend/
    return path.join(process.resourcesPath, 'backend', exeName);
  } else {
    // Development mode - run Python directly
    return null;
  }
}

function startBackend() {
  return new Promise((resolve, reject) => {
    const backendPath = getBackendPath();

    if (backendPath) {
      // Production: run packaged backend executable
      console.log('Starting packaged backend:', backendPath);
      pythonProcess = spawn(backendPath, [], {
        cwd: path.dirname(backendPath),
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    } else {
      // Development: run Python directly
      const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
      const backendDir = path.join(__dirname, '..', 'backend');
      console.log('Starting dev backend from:', backendDir);
      pythonProcess = spawn(pythonCmd, ['-u', 'main.py'], {
        cwd: backendDir,
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    }

    pythonProcess.stdout.on('data', (data) => {
      console.log(`[backend] ${data.toString().trim()}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`[backend] ${data.toString().trim()}`);
    });

    pythonProcess.on('error', (err) => {
      console.error('Failed to start backend:', err);
      reject(err);
    });

    pythonProcess.on('exit', (code) => {
      console.log(`Backend exited with code ${code}`);
    });

    // Poll until backend is ready
    let attempts = 0;
    const maxAttempts = 30;
    const pollInterval = setInterval(() => {
      attempts++;
      const req = http.get(BACKEND_URL, (res) => {
        clearInterval(pollInterval);
        console.log('Backend is ready');
        resolve();
      });
      req.on('error', () => {
        if (attempts >= maxAttempts) {
          clearInterval(pollInterval);
          reject(new Error('Backend failed to start'));
        }
      });
      req.setTimeout(1000, () => req.destroy());
    }, 500);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    title: 'RateShop',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.loadURL(BACKEND_URL);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function killBackend() {
  if (pythonProcess) {
    if (process.platform === 'win32') {
      spawn('taskkill', ['/pid', pythonProcess.pid.toString(), '/f', '/t']);
    } else {
      pythonProcess.kill('SIGTERM');
    }
    pythonProcess = null;
  }
}

app.whenReady().then(async () => {
  try {
    await startBackend();
    createWindow();
  } catch (err) {
    console.error('Failed to start application:', err);
    app.quit();
  }
});

app.on('window-all-closed', () => {
  killBackend();
  app.quit();
});

app.on('before-quit', () => {
  killBackend();
});
