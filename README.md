# img2movie

A Python script to create a video from a sequence of images in a folder.

## Description

`img2movie.py` takes a folder containing image files and converts them into a video file. The images are sorted naturally (handling numbered sequences correctly) and combined into an MP4 video at the specified frame rate.

## Features

- Supports multiple image formats: JPG, JPEG, PNG, BMP, TIF, TIFF
- Natural sorting of image files (e.g., frame1.jpg, frame2.jpg, frame10.jpg)
- Automatic output path generation when not specified
- Handles existing output files by adding numbered suffixes
- Resizes images to match the first image's dimensions if necessary

## Dependencies

- Python 3.6+
- OpenCV (`opencv-python`)

Install dependencies with:
```bash
pip install opencv-python
```

## License

This project is licensed under the MIT License.

## Usage

### Basic Usage

```bash
python img2movie.py /path/to/image/folder
```

This will create a video file named after the input folder (e.g., `imagefolder.mp4`) in the same directory as the input folder.

### Advanced Usage

```bash
python img2movie.py /path/to/image/folder -o output.mp4 -r 24 -c avc1
```

### Command Line Options

- `folder`: Path to the folder containing image frames (required)
- `-o, --output`: Output video file path (optional)
  - If not specified, saves alongside the input folder using the folder name
  - If the file exists, appends a 4-digit number suffix (e.g., `foldername0001.mp4`)
- `-r, --fps`: Frames per second for the output video (default: 30.0)
- `-c, --codec`: FourCC codec for the output video (default: mp4v)
  - Common options: mp4v, avc1, XVID, MJPG

## Examples

### Example 1: Default output
```bash
python img2movie.py images/
```
Creates `images.mp4` in the parent directory of `images/`.

### Example 2: Custom output
```bash
python img2movie.py images/ -o myvideo.mp4 -r 60
```
Creates `myvideo.mp4` with 60 FPS.

### Example 3: Different codec
```bash
python img2movie.py images/ -c XVID
```
Creates video using XVID codec.

## Notes

- Images are sorted naturally, so files like `frame001.jpg`, `frame002.jpg`, etc., will be in correct order.
- All images should have the same dimensions; if not, they will be resized to match the first image.
- The script will skip any files that are not recognized image formats.</content>
<parameter name="filePath">d:\Marc\Misc\img2movie\README.md