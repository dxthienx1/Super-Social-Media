
from common_function import *

# from scenedetect import VideoManager, SceneManager
# from scenedetect.detectors import ContentDetector

# def detect_scene_changes(video_path, threshold=30.0):
#     """Phát hiện các đoạn chuyển cảnh trong video bằng PySceneDetect"""
#     video_manager = VideoManager([video_path])
#     scene_manager = SceneManager()
#     scene_manager.add_detector(ContentDetector(threshold=threshold))

#     video_manager.start()
#     scene_manager.detect_scenes(frame_source=video_manager)
#     scene_list = scene_manager.get_scene_list()

#     # Chỉ lấy timestamp của từng cảnh
#     timestamps = [scene[0].get_seconds() for scene in scene_list]

#     # Bỏ cảnh đầu tiên và lọc khoảng cách >= 5s
#     filtered_timestamps = [timestamps[0]]
#     for t in timestamps[1:]:
#         if t - filtered_timestamps[-1] >= 5:
#             filtered_timestamps.append(t)

#     return filtered_timestamps

# def run_command_ffmpeg(cmd, hide=True):
#     """Chạy lệnh ffmpeg"""
#     stderr_option = subprocess.DEVNULL if hide else None
#     subprocess.run(cmd, stderr=stderr_option, stdout=subprocess.DEVNULL, text=True)

# def apply_transitions(input_video, output_video, timestamps):
#     """Cắt video và thêm hiệu ứng chuyển cảnh"""
#     temp_clips = []
#     transitions = ['fade', 'wipeleft', 'wiperight', 'wipeup', 'wipedown']

#     # Cắt các đoạn video
#     start_time = 0
#     for i in range(len(timestamps) - 1):
#         start_time = timestamps[i]
#         end_time = timestamps[i + 1]
#         temp_clip = f"temp_{i}.mp4"
#         temp_clips.append(temp_clip)

#         command = [
#             'ffmpeg', '-progress', 'pipe:1', '-accurate_seek', '-ss', str(start_time), '-i', input_video,
#             '-to', str(end_time - start_time), '-c:v', 'copy', '-c:a', 'copy', '-fps_mode', 'cfr',
#             '-y', temp_clip, '-loglevel', 'quiet'
#         ]
#         run_command_ffmpeg(command, hide=False)

#     # Ghép video với hiệu ứng chuyển cảnh
#     concat_file = "concat_list.txt"
#     with open(concat_file, "w") as f:
#         for i, clip in enumerate(temp_clips):
#             f.write(f"file '{clip}'\n")

#             # Thêm hiệu ứng vào điểm ghép
#             if i < len(temp_clips) - 1:
#                 transition = random.choice(transitions)
#                 f.write(f"file 'transition_{i}.mp4'\n")

#                 cmd_transition = [
#                     "ffmpeg", "-i", temp_clips[i], "-i", temp_clips[i + 1],
#                     "-filter_complex", f"[0:v][1:v]xfade=transition={transition}:duration=1:offset=0",
#                     "-c:v", "libx264", "-preset", "fast", f"transition_{i}.mp4", "-y"
#                 ]
#                 run_command_ffmpeg(cmd_transition, hide=False)

#     cmd_concat = [
#         "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_file,
#         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-y", output_video
#     ]
#     run_command_ffmpeg(cmd_concat, hide=False)

#     # Xóa file tạm
#     os.remove(concat_file)
#     for clip in temp_clips:
#         os.remove(clip)
#     for i in range(len(temp_clips) - 1):
#         os.remove(f"transition_{i}.mp4")

# if __name__ == "__main__":
#     input_video = "E:\\tiktok\\test edit video\\1.mp4"
#     output_video = "E:\\tiktok\\test edit video\\1_out.mp4"

#     # Phát hiện cảnh và lọc theo điều kiện
#     scene_changes = detect_scene_changes(input_video)
#     print("Chuyển cảnh áp dụng tại:", scene_changes)

#     # Áp dụng hiệu ứng chuyển cảnh
#     if scene_changes:
#         apply_transitions(input_video, output_video, scene_changes)

import cv2
import numpy as np
import subprocess

def process_video(input_path, temp_video_path):
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("Không thể mở video!")
        return
    
    # Lấy thông tin video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec hỗ trợ MP4
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

    frame_count = 0  # Biến đếm frame để tạo hiệu ứng động

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Thêm hiệu ứng
        edited_frame = add_effects(frame, frame_count)

        # Ghi frame đã chỉnh sửa vào video đầu ra
        out.write(edited_frame)

        frame_count += 1  # Cập nhật frame count để tạo hiệu ứng động

    cap.release()
    out.release()
    print("Xử lý video hoàn tất!")

def add_effects(frame, frame_count):
    """ Thêm nhiễu, đường vạch ngang dày hơn và hiệu ứng gợn sóng động """
    height, width, _ = frame.shape
    
    # Thêm nhiễu nhẹ
    noise = np.random.randint(0, 30, frame.shape, dtype='uint8')
    noisy_frame = cv2.add(frame, noise)

    # Thêm đường vạch ngang dày hơn (mỗi 50px)
    overlay = noisy_frame.copy()
    for i in range(25, height, 50):  # Khoảng cách 50px giữa các đường
        cv2.line(overlay, (0, i), (width, i), (128, 128, 128), 2)  # Màu xám

    # Áp dụng hiệu ứng mờ dần cho đường kẻ
    alpha = 0.3  # Độ trong suốt của đường kẻ
    cv2.addWeighted(overlay, alpha, noisy_frame, 1 - alpha, 0, noisy_frame)

    # Áp dụng hiệu ứng gợn sóng động
    distorted_frame = apply_wave_effect(noisy_frame, frame_count)

    return distorted_frame

def apply_wave_effect(frame, frame_count):
    """ Tạo hiệu ứng gợn sóng động (dịch pixel theo sóng sin thay đổi theo thời gian) """
    height, width, _ = frame.shape
    wave_frame = np.zeros_like(frame)

    for i in range(height):
        shift_x = int(5 * np.sin(2 * np.pi * (i / 100) + frame_count * 0.1))  
        # Biên độ: 5px, thay đổi theo thời gian (frame_count * 0.1)
        wave_frame[i] = np.roll(frame[i], shift_x, axis=0)

    return wave_frame

def merge_audio(video_path, original_video, output_video):
    """ Ghép âm thanh từ video gốc vào video đã chỉnh sửa """
    command = [
        "ffmpeg", "-y",
        "-i", video_path,    # Video đã chỉnh sửa
        "-i", original_video, # Video gốc (chứa âm thanh)
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        "-map", "0:v:0",  # Lấy video từ file đã chỉnh sửa
        "-map", "1:a:0",  # Lấy âm thanh từ file gốc
        output_video
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Đã ghép âm thanh vào video!")

if __name__ == "__main__":
    input_video = "E:\\tiktok\\test edit video\\1.mp4"
    temp_video = "E:\\tiktok\\test edit video\\temp.mp4"  # Video tạm không có âm thanh
    output_video = "E:\\tiktok\\test edit video\\1_out.mp4"

    # Xử lý video
    process_video(input_video, temp_video)

    # Ghép âm thanh lại với video đã chỉnh sửa
    merge_audio(temp_video, input_video, output_video)
