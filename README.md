# Video to WebM Converter

A simple yet powerful Python script for bulk conversion of video files to the `.webm` format. Ideal for archiving and saving disk space, for example, with video collections.

## Key Features

-   **WebM Format Conversion**: Utilizes modern and efficient codecs (video **VP9** and audio **Opus**).
-   **Disk Space Saving**: Optimizes video files, significantly reducing their size while maintaining good quality.
-   **Optional Original File Removal**: After successful conversion, the script can automatically delete the original, larger file (`--autoremove`).
-   **Two Scanning Modes**:
    -   **Default**: Scans only files in the current directory.
    -   **Optional**: Recursively scans all subdirectories (`--recursive`).
-   **Intelligent Skipping**: Does not convert files if the `.webm` version already exists.
-   **Detailed Summary**: At the end, it displays a report with the number of converted files and the amount of space saved.

## Installation

#### 1. Prerequisites

Before running the script, ensure you have the following installed:

-   **Python 3**: Usually available on most systems.
-   **FFmpeg**: A powerful tool for multimedia operations.

**FFmpeg Installation:**
-   **On Debian/Ubuntu/Mint systems:**
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
-   **On Windows:**
    Download from the official website [ffmpeg.org](https://ffmpeg.org/download.html) and add `ffmpeg.exe` to your system's PATH.
-   **On macOS (using Homebrew):**
    ```bash
    brew install ffmpeg
    ```

#### 2. Getting the script

Clone this repository or download the files manually.

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER_NAME>
```

The script does not require any external Python libraries (the `requirements.txt` file is empty).

## Usage

To run the script, use your terminal or command prompt.

#### Displaying Help
```bash
python3 konwerter_wideo.py --help
```

#### Usage Examples

**1. Convert files only in the current directory (default mode)**
```bash
python3 konwerter_wideo.py
```

**2. Convert in the current directory with automatic original file removal**
> **Warning:** Use with caution! Original files will be permanently deleted.
```bash
python3 konwerter_wideo.py --autoremove
```

**3. Convert in all subdirectories (recursively)**
```bash
python3 konwerter_wideo.py --recursive
```

**4. Recursive conversion with automatic original file removal**
```bash
python3 konwerter_wideo.py --recursive --autoremove
```

## Available Arguments

-   `--autoremove`: Deletes the original file after successful conversion to `.webm`.
-   `--recursive`: Enables recursive scanning of subdirectories for video files.
