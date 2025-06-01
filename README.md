# Introduction to MayOS_GUI built-in applications

MayOS_GUI currently includes multiple practical built-in applications, each of which has been carefully designed and deeply integrated with the system to provide users with a smooth user experience. The following are the main built-in applications and their functions in the current version:

## 1. Music player (MayPlayer 2.0)

### Core functions
- **Multi-format support**: Perfectly play mainstream audio formats such as MP3, WAV, FLAC

- **Smart playlist**: Automatically record recent playback and history

- **High-precision progress control**: Support dragging the progress bar to jump to the specified position

### Special functions
- **Album cover display**: Automatically extract and display cover art from audio files

### Technical features
- Use pygame for underlying audio processing
- Adopt multi-threaded design to avoid interface freezes
- Memory usage optimization, suitable for long-term playback

## 2. Wallpaper manager (MayWallpaper) (0.0.4 planned function)

### Core functions
- **Dual-source wallpaper**: Support local wallpapers and Bing daily wallpapers
- **Smart cache**: Automatically manage wallpaper cache to avoid repeated downloads
- **Slideshow mode**: Timely switch wallpapers

### Special functions
- ** Wallpaper metadata display **: Display information such as photographer, shooting location, etc.
- ** Dynamic effect **: Support parallax scrolling effect
- ** Collection system **: You can mark your favorite wallpapers

### Technical features
- Use requests to efficiently obtain network resources
- Image processing pipeline based on Pillow
- Adapt to various screen resolutions

The built-in applications of MayOS_GUI are continuously updated, and each version will bring performance improvements and new features. We welcome user feedback and suggestions to jointly create a more complete application ecosystem.
