# 🎵 Spotify Controller with Hand Gesture

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-API-1DB954?style=for-the-badge&logo=spotify&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Control your Spotify playback using hand gestures — No more mouse clicks or keyboard shortcuts, just move your hand and let the music obey.**

</div>

---

## 🌟 Overview

This innovative project leverages **real-time hand tracking technology** to create an intuitive, touchless Spotify controller. Using advanced computer vision and machine learning, it detects hand gestures through your webcam and translates them into Spotify playback commands via the official Spotify Web API.

Perfect for:
- 🎧 Music enthusiasts who want a futuristic listening experience
- 🖥️ Developers exploring computer vision applications
- 🎮 Anyone looking for hands-free device control

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎚️ **Play/Pause Control** | Toggle playback with a simple fist gesture |
| ⏭️ **Track Navigation** | Skip forward/backward through your playlist |
| 🔊 **Volume Control** | Adjust volume levels with palm gestures |
| 📷 **Real-time Detection** | Instant gesture recognition via webcam |
| ⚡ **Lightweight Performance** | Optimized for smooth, responsive operation |
| 🎯 **High Accuracy** | Precise gesture detection in various lighting conditions |

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core programming language | 3.9+ |
| **OpenCV** | Video capture & image processing | 4.x |
| **MediaPipe** | Hand tracking & gesture recognition | Latest |
| **Spotipy** | Spotify Web API client | Latest |

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Webcam/Camera access
- Spotify Premium account
- Active internet connection

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/arizzira/Spotify-Controller-with-hand-gesture.git
   cd Spotify-Controller-with-hand-gesture
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Linux/macOS:
   source venv/bin/activate
   
   # On Windows:
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Spotify API Configuration

1. **Create Spotify Application**
   - Navigate to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Click "Create App"
   - Fill in app name and description
   - Set redirect URI: `http://localhost:8888/callback`
   - Save your **Client ID** and **Client Secret**

2. **Environment Setup**
   
   Create a `.env` file in the project root:
   ```env
   CLIENT_ID=your_spotify_client_id_here
   CLIENT_SECRET=your_spotify_client_secret_here
   REDIRECT_URI=http://localhost:8888/callback
   ```

3. **Launch the Application**
   ```bash
   python gesture_spotify.py
   ```

---

## ✋ Gesture Controls

<div align="center">

| Gesture | Visual | Action | Description |
|---------|--------|--------|-------------|
| **Closed Fist** | ✊ | Play/Pause | Toggle music playback |
| **Index Finger** | 👉 | Next Track | Skip to next song |
| **Peace Sign** | ✌️ | Previous Track | Go back to previous song |
| **Open Palm** | 🖐️ | Volume Up | Increase volume level |
| **Palm Down** | 🤚 | Volume Down | Decrease volume level |

</div>

### Customization

You can modify gesture mappings and add new controls by editing the gesture detection logic in `gesture_spotify.py`. The modular design makes it easy to:
- Add new gestures
- Change existing mappings  
- Adjust sensitivity settings
- Implement custom actions

---

## 🔧 Configuration & Troubleshooting

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: Minimum 4GB recommended
- **Camera**: Built-in webcam or external USB camera
- **Python**: Version 3.9 or higher

### Common Issues

<details>
<summary><strong>🔍 Camera not detected</strong></summary>

- Ensure camera permissions are granted
- Check if other applications are using the camera
- Try different camera indices in the code (0, 1, 2, etc.)
</details>

<details>
<summary><strong>🔍 Spotify authentication failed</strong></summary>

- Verify Client ID and Client Secret in `.env` file
- Ensure redirect URI matches exactly
- Check if Spotify app has necessary permissions
</details>

<details>
<summary><strong>🔍 Poor gesture recognition</strong></summary>

- Ensure adequate lighting
- Position hand within camera frame
- Avoid busy backgrounds
- Calibrate gesture sensitivity in settings
</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

---

## 📋 Roadmap

- [ ] **Multi-hand gesture support**
- [ ] **Custom gesture training interface**
- [ ] **Mobile app companion**
- [ ] **Integration with other music platforms**
- [ ] **Voice command backup**
- [ ] **Gesture recording and playback**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 arizzira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- **Google MediaPipe** team for the excellent hand tracking solution
- **Spotify** for providing the comprehensive Web API
- **OpenCV** community for computer vision tools
- All contributors and testers who helped improve this project

---

## 📞 Contact & Support
Email : arizgg@gmail.com
Instagram : @arizzira
Tiktok : @arizzira
<div align="center">

**Made with ❤️ by [arizzira](https://github.com/arizzira)**

[![GitHub](https://img.shields.io/badge/GitHub-arizzira-black?style=for-the-badge&logo=github)](https://github.com/arizzira)
[![Issues](https://img.shields.io/github/issues/arizzira/Spotify-Controller-with-hand-gesture?style=for-the-badge)](https://github.com/arizzira/Spotify-Controller-with-hand-gesture/issues)
[![Stars](https://img.shields.io/github/stars/arizzira/Spotify-Controller-with-hand-gesture?style=for-the-badge)](https://github.com/arizzira/Spotify-Controller-with-hand-gesture/stargazers)

</div>

---

<div align="center">
<sub>⭐ If this project helped you, please consider giving it a star! ⭐</sub>
</div>
