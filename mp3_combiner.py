#!/usr/bin/env python3

# ===================================================================
# MP3 Combiner - A tool for combining multiple MP3 files into one
# ===================================================================
# Before running this script, please install the required dependency:
#   pip install pydub
# 
# Note: pydub also requires ffmpeg or libav to be installed on your system.
# For more information, visit: https://github.com/jiaaro/pydub#dependencies
# ===================================================================

import argparse
import os
import sys
import tty
import termios
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def list_mp3_files(folder_path):
    """
    Lists all MP3 files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing MP3 files
        
    Returns:
        A sorted list of MP3 filenames
    """
    # Get all files and directories in the folder
    all_items = os.listdir(folder_path)
    
    # Filter to only include files with .mp3 extension
    mp3_files = [file for file in all_items if file.lower().endswith('.mp3')]
    
    # Sort the list alphabetically
    sorted_mp3_files = sorted(mp3_files)
    
    return sorted_mp3_files

def generate_silence(duration_ms):
    """
    Generate a silent AudioSegment with the specified duration.
    
    Args:
        duration_ms: Duration of silence in milliseconds
        
    Returns:
        An AudioSegment object representing silence
    """
    return AudioSegment.silent(duration=duration_ms)

def read_mp3_file(file_path):
    """
    Read an MP3 file and load it into an AudioSegment object.
    
    Args:
        file_path: Path to the MP3 file to read
        
    Returns:
        An AudioSegment object containing the audio from the MP3 file
    """
    return AudioSegment.from_mp3(file_path)

def parse_arguments():
    """Parse command line arguments for the MP3 combiner."""
    parser = argparse.ArgumentParser(description='Combine multiple MP3 files into a single file.')
    
    # Add positional arguments
    parser.add_argument('input_folder', 
                        help='Path to the folder containing the MP3 files to combine')
    parser.add_argument('output_file', 
                        help='Path where the combined MP3 file will be saved')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Store the argument values in variables
    input_folder_path = args.input_folder
    output_file_path = args.output_file
    
    return input_folder_path, output_file_path

def clear_screen():
    """Clear the terminal screen."""
    # ANSI escape code to clear screen and move cursor to home position
    print("\033[2J\033[H", end="", flush=True)

def display_mp3_files(mp3_files, focused_index, selected_index, input_folder_path, output_file_path):
    """Display the MP3 files with the focused file highlighted."""
    clear_screen()
    
    # Print info with proper line endings
    print(f"Input folder: {input_folder_path}\r")
    print(f"Output file: {output_file_path}\r")
    
    print("\nMP3 files found:\r")
    for idx, file in enumerate(mp3_files):
        if idx == focused_index and idx == selected_index:
            # Both focused and selected
            print(f"- *> SELECTED >*{file}\r")
        elif idx == focused_index:
            # Only focused
            print(f"- *> {file} <*\r")
        elif idx == selected_index:
            # Only selected
            print(f"- *> SELECTED >*{file}\r")
        else:
            # Neither focused nor selected
            print(f"- {file}\r")
    
    print("\nUse up/down arrow keys to navigate, Enter to select/deselect, 'q' to quit\r")
    print("When an item is selected, up/down arrows will reorder it in the list\r")
    print("Press 'c' to combine files in the current order\r")
    sys.stdout.flush()

if __name__ == "__main__":
    # Parse command-line arguments
    input_folder_path, output_file_path = parse_arguments()
    
    # Verify that the input folder exists and is a directory
    if not os.path.exists(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isdir(input_folder_path):
        print(f"Error: '{input_folder_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    # Get list of MP3 files
    mp3_files = list_mp3_files(input_folder_path)
    
    if not mp3_files:
        print("No MP3 files found in the specified folder.")
        sys.exit(1)
    
    # Initialize focused and selected indices
    focused_index = 0
    selected_index = None
    
    # Save original terminal settings
    original_settings = termios.tcgetattr(sys.stdin.fileno())
    
    try:
        # Set terminal to raw mode
        tty.setraw(sys.stdin.fileno())
        
        # Display initial file list
        display_mp3_files(mp3_files, focused_index, selected_index, input_folder_path, output_file_path)
        
        # Interactive loop for navigation
        while True:
            # Read a single character from input
            char = sys.stdin.read(1)
            
            # Check for arrow key sequences
            if char == '\x1b':
                # It could be an escape sequence
                next_char = sys.stdin.read(1)
                if next_char == '[':
                    # It's definitely an arrow key
                    arrow_key = sys.stdin.read(1)
                    
                    if arrow_key == 'A':  # Up arrow
                        if selected_index is not None:
                            # An item is selected, so move it up in the list
                            if selected_index > 0:
                                # Swap with the item above
                                mp3_files[selected_index], mp3_files[selected_index - 1] = \
                                mp3_files[selected_index - 1], mp3_files[selected_index]
                                # Move the selection up
                                selected_index -= 1
                                # Also move the focus
                                focused_index = selected_index
                        else:
                            # No item selected, just move the focus up
                            focused_index = max(0, focused_index - 1)
                    elif arrow_key == 'B':  # Down arrow
                        if selected_index is not None:
                            # An item is selected, so move it down in the list
                            if selected_index < len(mp3_files) - 1:
                                # Swap with the item below
                                mp3_files[selected_index], mp3_files[selected_index + 1] = \
                                mp3_files[selected_index + 1], mp3_files[selected_index]
                                # Move the selection down
                                selected_index += 1
                                # Also move the focus
                                focused_index = selected_index
                        else:
                            # No item selected, just move the focus down
                            focused_index = min(len(mp3_files) - 1, focused_index + 1)
            
            # Check for Enter key (selection)
            elif char == '\r' or char == '\n':
                if selected_index is None:
                    # No item is selected, so select the focused item
                    selected_index = focused_index
                else:
                    # An item is already selected, so deselect it
                    selected_index = None
            
            # Check for combine command
            elif char == 'c':
                # Restore terminal settings before printing
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, original_settings)
                clear_screen()
                print("Combining files...\n")
                break
            
            # Check for quit command
            elif char == 'q':
                break
            
            # Redraw the file list with updated focus and selection
            display_mp3_files(mp3_files, focused_index, selected_index, input_folder_path, output_file_path)
        
        # If we exited by pressing 'c', show the final ordered list
        if char == 'c':
            print("Files will be combined in this order:")
            for idx, file in enumerate(mp3_files):
                print(f"{idx+1}. {file}")
            print(f"\nOutput will be saved to: {output_file_path}")
            
            # Initialize an empty AudioSegment for the combined audio
            combined_audio = AudioSegment.empty()
            
            # Iterate through the MP3 files and combine them
            for i, filename in enumerate(mp3_files):
                # Construct full file path
                full_path = os.path.join(input_folder_path, filename)
                
                print(f"Processing: {filename}")
                
                # Read the MP3 file with error handling
                try:
                    audio = read_mp3_file(full_path)
                    
                    # Append the audio to the combined audio
                    combined_audio += audio
                    
                    # Add silence between tracks (except after the last file)
                    if i < len(mp3_files) - 1:
                        silence = generate_silence(3000)  # 3 seconds of silence
                        combined_audio += silence
                        print(f"Added 3 seconds of silence after {filename}")
                except (CouldntDecodeError, IOError, OSError) as e:
                    print(f"Warning: Could not process file '{filename}'. Skipping. Error: {str(e)}")
                    continue
            
            # Only export if we have audio to export
            if len(combined_audio) > 0:
                print(f"\nSaving combined audio to {output_file_path}...")
                # Export the combined audio to the output file
                try:
                    combined_audio.export(output_file_path, format="mp3", bitrate="320k")
                    print(f"Successfully saved combined audio to {output_file_path}")
                    print(f"Total duration: {len(combined_audio)/1000:.2f} seconds")
                except IOError:
                    print(f"Error: Could not write to the specified output file '{output_file_path}'.", file=sys.stderr)
                    sys.exit(1)
            else:
                print("Error: No valid MP3 files could be processed.", file=sys.stderr)
                sys.exit(1)
    
    finally:
        # Restore original terminal settings
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, original_settings)
        if char != 'c':  # Only clear and print exit message if we didn't already handle 'c'
            clear_screen()
            print("Exiting MP3 combiner.\n")
    
    # Future code to combine MP3 files will go here 