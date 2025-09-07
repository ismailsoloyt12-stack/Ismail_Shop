<?php
/**
 * Secure File Download Handler for App Store
 * This script handles secure file downloads from the Apps_Link folder
 */

// Configuration
$APPS_LINK_DIR = __DIR__ . '/Apps_Link/';
$APPS_DATA_FILE = __DIR__ . '/apps_data.json';

// Security headers
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');

// Function to send JSON response
function sendJsonResponse($data, $statusCode = 200) {
    http_response_code($statusCode);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

// Function to load apps data
function loadApps() {
    global $APPS_DATA_FILE;
    if (!file_exists($APPS_DATA_FILE)) {
        return [];
    }
    $content = file_get_contents($APPS_DATA_FILE);
    return json_decode($content, true) ?: [];
}

// Function to save apps data
function saveApps($apps) {
    global $APPS_DATA_FILE;
    file_put_contents($APPS_DATA_FILE, json_encode($apps, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

// Check if app_id is provided
if (!isset($_GET['app_id'])) {
    sendJsonResponse(['error' => 'App ID is required'], 400);
}

$appId = $_GET['app_id'];

// Load apps data
$apps = loadApps();

// Find the app
$app = null;
foreach ($apps as &$appItem) {
    if ($appItem['id'] === $appId) {
        $app = &$appItem;
        break;
    }
}

if (!$app) {
    sendJsonResponse(['error' => 'App not found'], 404);
}

// Handle API request (POST for download counter)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Increment download counter
    $app['downloads'] = isset($app['downloads']) ? $app['downloads'] + 1 : 1;
    saveApps($apps);
    
    // Check if app has a real file
    $hasFile = !empty($app['app_file']);
    
    sendJsonResponse([
        'success' => true,
        'downloads' => $app['downloads'],
        'message' => 'Download started!',
        'has_file' => $hasFile,
        'file_url' => $hasFile ? "/download.php?app_id={$appId}&action=file" : null
    ]);
}

// Handle file download (GET request with action=file)
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'file') {
    // Get the file name from app data
    $appFile = isset($app['app_file']) ? $app['app_file'] : null;
    
    if (!$appFile) {
        header('HTTP/1.1 404 Not Found');
        die('No file available for this app');
    }
    
    // Construct file path
    $filePath = $APPS_LINK_DIR . $appFile;
    
    // Check if file exists
    if (!file_exists($filePath)) {
        // Try with app_file_path if available
        if (isset($app['app_file_path']) && file_exists($app['app_file_path'])) {
            $filePath = $app['app_file_path'];
        } else {
            header('HTTP/1.1 404 Not Found');
            die('File not found on server');
        }
    }
    
    // Security check - ensure file is within Apps_Link directory
    $realPath = realpath($filePath);
    $realAppsDir = realpath($APPS_LINK_DIR);
    if (strpos($realPath, $realAppsDir) !== 0 && !isset($app['app_file_path'])) {
        header('HTTP/1.1 403 Forbidden');
        die('Access denied');
    }
    
    // Get file info
    $fileSize = filesize($filePath);
    $fileName = basename($filePath);
    $fileMime = mime_content_type($filePath);
    
    // If mime type cannot be determined, use a generic one
    if (!$fileMime) {
        $ext = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
        $mimeTypes = [
            'apk' => 'application/vnd.android.package-archive',
            'exe' => 'application/x-msdownload',
            'msi' => 'application/x-msi',
            'dmg' => 'application/x-apple-diskimage',
            'deb' => 'application/x-debian-package',
            'pkg' => 'application/x-newton-compatible-pkg',
            'zip' => 'application/zip',
            'rar' => 'application/x-rar-compressed'
        ];
        $fileMime = isset($mimeTypes[$ext]) ? $mimeTypes[$ext] : 'application/octet-stream';
    }
    
    // Set download headers
    header('Content-Type: ' . $fileMime);
    header('Content-Disposition: attachment; filename="' . $fileName . '"');
    header('Content-Length: ' . $fileSize);
    header('Cache-Control: no-cache, must-revalidate');
    header('Expires: 0');
    header('Pragma: public');
    
    // Clear output buffer
    if (ob_get_level()) {
        ob_end_clean();
    }
    
    // Output file
    readfile($filePath);
    exit;
}

// If no valid action, show download page
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download - <?php echo htmlspecialchars($app['name']); ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .download-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        .app-icon {
            width: 80px;
            height: 80px;
            border-radius: 16px;
            margin: 0 auto 20px;
            display: block;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .developer {
            color: #666;
            margin-bottom: 30px;
        }
        .download-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .download-btn:hover {
            transform: translateY(-2px);
        }
        .file-info {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="download-container">
        <?php if (file_exists(__DIR__ . '/static/images/app_icons/' . $app['icon'])): ?>
            <img src="/static/images/app_icons/<?php echo htmlspecialchars($app['icon']); ?>" 
                 alt="<?php echo htmlspecialchars($app['name']); ?>" 
                 class="app-icon">
        <?php endif; ?>
        
        <h1><?php echo htmlspecialchars($app['name']); ?></h1>
        <p class="developer">by <?php echo htmlspecialchars($app['developer']); ?></p>
        
        <?php if (!empty($app['app_file'])): ?>
            <button class="download-btn" onclick="downloadFile()">
                Download Now
            </button>
            
            <div class="file-info">
                <p>Version: <?php echo htmlspecialchars($app['version'] ?? '1.0.0'); ?></p>
                <p>Size: <?php echo htmlspecialchars($app['size'] ?? 'Unknown'); ?></p>
                <?php if (!empty($app['app_file'])): ?>
                    <p>File: <?php echo htmlspecialchars($app['app_file']); ?></p>
                <?php endif; ?>
            </div>
        <?php else: ?>
            <p style="color: #666;">No download file available for this app yet.</p>
        <?php endif; ?>
    </div>
    
    <script>
        function downloadFile() {
            // Trigger the file download
            window.location.href = '/download.php?app_id=<?php echo urlencode($appId); ?>&action=file';
        }
    </script>
</body>
</html>
