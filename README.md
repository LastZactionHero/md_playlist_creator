# MP3 Combiner

A command-line tool for combining multiple MP3 files into a single file with a simple interactive interface.

## Features

- Interactive text-based UI for selecting and reordering MP3 files
- Combine multiple MP3 files into a single high-quality MP3
- Automatically adds silence between tracks
- Graceful error handling for corrupted or inaccessible files
- High-quality output (320kbps bitrate)

## Requirements

- Python 3.6 or higher
- [pydub](https://github.com/jiaaro/pydub) library
- FFmpeg or libav (required by pydub for MP3 processing)

## Installation

1. Clone this repository or download the `mp3_combiner.py` script.

2. Install the required Python library:
   ```
   pip install pydub
   ```

3. Install FFmpeg:
   - **macOS** (using Homebrew):
     ```
     brew install ffmpeg
     ```
   - **Linux** (Debian/Ubuntu):
     ```
     sudo apt-get install ffmpeg
     ```
   - **Windows**:
     Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add it to your PATH.

## Usage

Run the script from the command line with two arguments:

```
python mp3_combiner.py input_folder output_file.mp3
```

Where:
- `input_folder` is the path to the folder containing your MP3 files
- `output_file.mp3` is the path where the combined MP3 should be saved

### Interactive Controls

Once the script is running, you'll see a list of MP3 files found in the input folder.
You can use the following controls:

- **↑/↓** (Up/Down Arrow keys): Navigate through the list
- **Enter**: Select/deselect a file
- When a file is selected:
  - **↑** (Up Arrow): Move the selected file up in the list
  - **↓** (Down Arrow): Move the selected file down in the list
- **c**: Combine the files in the current order
- **q**: Quit without combining

## Example

```
$ python mp3_combiner.py ~/Music/tracks ~/combined_playlist.mp3

Input folder: /home/user/Music/tracks
Output file: /home/user/combined_playlist.mp3

MP3 files found:
- *> track01.mp3 <*
- track02.mp3
- track03.mp3
- track04.mp3

Use up/down arrow keys to navigate, Enter to select/deselect, 'q' to quit
When an item is selected, up/down arrows will reorder it in the list
Press 'c' to combine files in the current order
```

After pressing 'c' to combine:

```
Files will be combined in this order:
1. track01.mp3
2. track02.mp3
3. track03.mp3
4. track04.mp3

Output will be saved to: /home/user/combined_playlist.mp3

Processing: track01.mp3
Added 3 seconds of silence after track01.mp3
Processing: track02.mp3
Added 3 seconds of silence after track02.mp3
Processing: track03.mp3
Added 3 seconds of silence after track03.mp3
Processing: track04.mp3

Saving combined audio to /home/user/combined_playlist.mp3...
Successfully saved combined audio to /home/user/combined_playlist.mp3
Total duration: 843.21 seconds
```

## Troubleshooting

### FFmpeg Not Found

If you get an error about FFmpeg not being found, make sure:
1. FFmpeg is installed on your system
2. FFmpeg is available in your system PATH

### File Cannot Be Processed

If a specific MP3 file is skipped with a "Could not process file" warning:
1. Check if the file is a valid MP3
2. Verify you have read permissions for the file
3. Try re-encoding the file with another tool

## Error Handling

The script handles several types of errors:
- Invalid input folder path
- No MP3 files in the folder
- Corrupted or invalid MP3 files
- Permission issues when writing the output file

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 