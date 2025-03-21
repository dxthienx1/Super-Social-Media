from common_function import requests, os
from common_function import get_txt_data, remove_file

def download_videos_form_playhh3dhay_by_txt_file(id_file_txt, download_folder=None):
    def download_video_by_url(url, output_path):
        try:
            headers = {
                'Referer': 'https://playhh3dhay.xyz',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, stream=True)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"Video downloaded successfully to {output_path}")
                return True
            else:
                print(f"Failed to download video. Status code: {response.status_code}")
                return False
        except:
            return False
        
    file_data = get_txt_data(id_file_txt)
    if file_data is None:
        print(f"File {id_file_txt} không tồn tại.")
        return
    lines = file_data.splitlines()
    index = 1938
    temp_list_file = f"{download_folder}\\temp_list.txt"
    remove_file(temp_list_file)
    for line in lines:
        no_video_downloaded = False
        line = line.split(',')
        if len(line) == 1:
            server, video_id, end_url = 's1', line[0], '1080p/1080p_003.html'
        elif len(line) == 2:
            server, video_id, end_url = line[0], line[1], '1080p/1080p_003.html'
        else:
            server, video_id, end_url = line[0], line[1], line[2] #dạng s1,81ff33517ddda537c8858780626cfc12,1080p/1080p_003.html
        resolution = end_url.split('_')[0]
        exp = end_url.split('_')[1].split('.')[-1]
        print("-----------------------------------------")
        print(f"Bắt đầu tải tập phim với id {video_id} - Độ phân giải {resolution}")
        output_folder = os.path.join(download_folder, video_id)
        os.makedirs(output_folder, exist_ok=True)
        for j in range(1, 2000):
            if no_video_downloaded:
                break
            if j < 1000:
                j_str = f"{j:03}"
            else:
                j_str = f"{j:04}"
            for i in range(1, 6):
                video_url = f"https://{server}.playhh3dhay{i}.com/cdn/down/{video_id}/Video/{resolution}_{j_str}.{exp}"
                segment_path = os.path.join(output_folder, f"video_{index}.mp4")
                
                if download_video_by_url(video_url, segment_path):
                    no_video_downloaded = False  # Đặt lại cờ vì đã tải được video
                    index += 1
                    break
            else:
                no_video_downloaded = True








    # def schedule_videos(self):
    #     try:
    #         videos_folder = self.youtube_config['template'][self.channel_name]['upload_folder']
    #         if not videos_folder or not os.path.isdir(videos_folder):
    #             print(f"Thư mục chứa video của channel {self.channel_name} không tồn tại")
    #             return
    #         videos = os.listdir(videos_folder)
    #         videos = [k for k in videos if k.endswith('.mp4')]      
    #         if len(videos) == 0:
    #             print(f"Không có video nào trong thư mục {videos_folder}")
    #             return
    #         videos = natsorted(videos)

    #         if self.is_schedule:
    #             number_of_days = get_number_of_days(self.youtube_config['template'][self.channel_name]['number_of_days'])
    #             day_gap = get_day_gap(self.youtube_config['template'][self.channel_name]['day_gap'])
    #             upload_date_str = self.youtube_config['template'][self.channel_name]['upload_date']
    #             if not upload_date_str:
    #                 return
    #             publish_times = self.youtube_config['template'][self.channel_name]['publish_times'].split(',')
    #             if not publish_times:
    #                 return
    #             if self.is_auto_upload:
    #                 number_of_days = 10
    #                 upload_date_str = add_date_into_string(upload_date_str, day_gap)
    #             upload_date = convert_date_string_to_datetime(upload_date_str)
    #             if not upload_date:
    #                 return False

    #         upload_count = 0
    #         date_cnt = 0
    #         for i, video_file in enumerate(videos):
    #             if self.is_stop_upload:
    #                 break
    #             video_name = os.path.splitext(video_file)[0] #lấy tên
    #             title = self.youtube_config['template'][self.channel_name]['title']
    #             if self.youtube_config['template'][self.channel_name]['is_title_plus_video_name']:
    #                 self.full_title = f"{title}{video_name}"
    #             else:
    #                 self.full_title = title
    #             if len(self.full_title) > 100:
    #                 if not self.is_auto_upload:
    #                     notification(self.root, f"Chiều dài tối đa của tiêu đề là 100 ký tự:\n{self.full_title}: có tổng {len(self.full_title)} ký tự")
    #                 return False
    #             video_path = os.path.join(videos_folder, video_file)
    #             if self.is_schedule:
    #                 publish_time_hh_mm = publish_times[upload_count % len(publish_times)]
    #                 try:
    #                     publish_time_hh_mm = get_pushlish_time_hh_mm(publish_time_hh_mm)
    #                     if publish_time_hh_mm:
    #                         publish_time_str = f'{publish_time_hh_mm}:00'
    #                         publish_time = datetime.strptime(publish_time_str, '%H:%M:%S').time()
    #                     else:
    #                         print(f"Dừng đăng video vì {publish_time_hh_mm} có định dạng thời gian không phải là hh:mm")
    #                         break
    #                 except:
    #                     getlog()
    #                     if not self.is_auto_upload:
    #                         print(f"Dừng đăng video vì {publish_time_hh_mm} có định dạng thời gian không phải là hh:mm")
    #                         break
    #                 publish_datetime = datetime.combine(upload_date, publish_time)
    #                 publish_at = convert_time_to_UTC(publish_datetime.year, publish_datetime.month, publish_datetime.day, publish_datetime.hour, publish_datetime.minute, publish_datetime.second)
    #             else:
    #                 publish_at=None
                
    #             if self.upload_video(video_path, publish_at=publish_at):
    #                 remove_or_move_after_upload(video_path, self.youtube_config['template'][self.channel_name]['is_delete_after_upload'], finish_folder_name='youtube_upload_finished')
    #                 upload_count += 1
    #                 if self.is_schedule:
    #                     self.youtube_config['template'][self.channel_name]['upload_date'] = convert_datetime_to_string(upload_date)
    #                 else:
    #                     self.youtube_config['template'][self.channel_name]['upload_date'] = convert_datetime_to_string(datetime.now().date())
    #                 self.save_youtube_config()
    #                 print(f"Đăng thành công video '{video_file}'")
    #                 if self.is_schedule:
    #                     if (i + 1) % len(publish_times) == 0:
    #                         upload_date += timedelta(days=day_gap)
    #                         date_cnt += 1
    #                         if date_cnt == number_of_days:
    #                             break
    #                 else:
    #                     break
    #             else:
    #                 print("uploaded fail")
    #                 return False
    #         if upload_count > 0:
    #             self.save_youtube_config()
    #         if not self.is_auto_upload:
    #             notification(self.root, f"Đăng thành công {upload_count} video")
    #         else:
    #             print(f"Đăng thành công {upload_count} video")

    #         return True
    #     except:
    #         getlog()
    #         return False

    # def upload_video(self, video_file, publish_at=None):
    #     try:
    #         category_name = self.youtube_config['template'][self.channel_name]['category_id']
    #         category_id = int(youtube_category[category_name])
    #         body = {
    #             "snippet": {
    #                 "title": self.full_title,
    #                 "description": self.youtube_config['template'][self.channel_name]['description'],
    #                 "tags": self.youtube_config['template'][self.channel_name]['tags'],
    #                 "categoryId": category_id,
    #                 "defaultLanguage": "en",  # Thêm ngôn ngữ tiếng Anh
    #                 "automaticChapters": False  # Tắt tự động chương và khoảnh khắc chính
    #             },
    #             "status": {
    #                 "privacyStatus": self.youtube_config['template'][self.channel_name]['privacy_status'],
    #                 "selfDeclaredMadeForKids": False,
    #                 'license': self.youtube_config['template'][self.channel_name]['license'],
    #                 'notifySubscribers': False,   # Disable notifications to subscribers
    #             }
    #         }
    #         if publish_at:
    #             body['status']['publishAt'] = publish_at
    #             body['status']['privacyStatus'] = 'private'
    #         insert_request = self.youtube.videos().insert(
    #             part=",".join(body.keys()),
    #             body=body,
    #             media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True),
    #         )
    #         video_id = self.resumable_upload(insert_request)
    #         if video_id:
    #             sleep(2)
    #             return True
    #         return False
    #     except:
    #         getlog()
    #         return False

    # def resumable_upload(self, insert_request):
    #     response = None
    #     while response is None:
    #         try:
    #             if self.is_stop_upload:
    #                 return None
    #             self.save_youtube_config()
    #             print ("Đang đăng video...")
    #             try:
    #                 status, response = insert_request.next_chunk()
    #             except:
    #                 remove_file(self.curent_oath_path)
    #                 # self.get_authenticated_service()
    #                 status, response = insert_request.next_chunk()

    #             if response is not None and 'id' in response:
    #                 video_id = response['id']
    #                 print(f"Video id '{video_id}' was successfully uploaded.")
    #                 sleep(2)
    #                 return video_id
    #         except HttpError as e:
    #             if e.resp.status == 403:
    #                 error_details = e._get_reason()
    #                 if 'quota' in error_details:
    #                     print("Mỗi ngày chỉ được đăng tối đa 6 video bằng api --> Vui lòng đợi ngày tiếp theo !!!")
    #                 else:
    #                     print(f"HTTP error occurred: {error_details}")
    #             else:
    #                 print(f"An error occurred when resumable_upload: {e}")
    #             return None
    #         except:
    #             getlog()
    #             return None

# def convert_time_to_UTC(year, month, day, hour, minute, second=0, iso8601=True):
#     local_tz = get_localzone()
#     local_time = datetime(year, month, day, hour, minute, second, tzinfo=local_tz)
#     utc_time = local_time.astimezone(timezone.utc)
#     # Định dạng thời gian theo ISO 8601
#     if iso8601:
#         iso8601_time = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
#         return iso8601_time
#     return utc_time