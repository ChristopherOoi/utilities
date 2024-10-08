#!/usr/bin/env python3
import os
import argparse
import cv2
from glob import glob


def extract_frames(filename: str) -> list:
    frames = []
    cap = cv2.VideoCapture(filename)
    while cap.isOpened():
        ret, frame = cap.read()
        frames.append(frame)
    cap.release()
    return frames


def save_frames(
    frames: list,
    output_dir: str,
) -> bool:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    success = True
    for i, frame in enumerate(frames):
        try:
            cv2.imwrite(os.path.join(output_dir, f"frame_{i}.jpg"), frame)
        except Exception as e:
            print(f"Error saving frame {i}: {e}")
            success = False
    return success


def get_frames_from_video(
    path: str = None,
    patterns: list[str] = None,
    start: int = 0,
    end: int = -1,
    step: int = 1,
):
    if not path:
        print("No path specified, defaulting to current directory...")
        path = os.getcwd()
    if not patterns:
        print("No patterns specified, defaulting to all *.mp4...")
        patterns = ["*.mp4"]
    if end != -1 and end < start:
        print("End frame cannot be less than start frame, defaulting to -1...")
        end = -1
    for pattern in patterns:
        for file in glob(os.path.join(path, pattern)):
            frames = extract_frames(file)
            if end == -1:
                end = len(frames)
            elif end > len(frames):
                print(
                    f"End frame {end} exceeds total frames {len(frames)}, defaulting to {len(frames)}..."
                )
                end = len(frames)
            if step > len(frames):
                print(
                    f"Step {step} exceeds total frames {len(frames)}, defaulting to 1..."
                )
                step = 1
            save_frames(frames[start:end:step], os.path.join(path, "frames"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video files.")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to video files.",
    )
    parser.add_argument(
        "-pat",
        "--patterns",
        type=str,
        nargs="+",
        help="Patterns to match video files.",
    )
    parser.add_argument(
        "--start",
        type=int,
        help="Start frame index.",
    )
    parser.add_argument(
        "--end",
        type=int,
        help="End frame index.",
    )
    parser.add_argument(
        "--step",
        type=int,
        help="Step between frames.",
    )
    args = parser.parse_args()
    get_frames_from_video(args.path, args.patterns, args.start, args.end, args.step)
