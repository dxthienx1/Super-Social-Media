from common_function import *
from tiktok import TikTokManager
from facebook import FacebookManager
from youtube import YouTubeManager

class MainApp:
    def __init__(self):
        try:
            self.root = ctk.CTk()
            self.root.title("SSM App")
            self.width = 500
            serial = get_disk_and_mainboard_serial()
            serial = serial.strip()
            is_ok = True
            if serial in ban_serials:
                print("bạn không thể dùng ứng dụng !!!")
                return
            if serial not in serials.keys():
                if serial in already_serial:
                    print("bạn đã hết lượt dùng thử --> liên hệ admin để đăng ký gói mới.")
                else:
                    print("bạn chưa đăng ký --> gửi mã đăng ký riêng cho admin để đăng ký dùng thử")
                is_ok = False
            else:
                if not is_date_greater_than_current_day(serials[serial]):
                    print(f"hết hạn sử dụng --> liên hệ admin để gia hạn")
                    is_ok = False
            
            if not is_ok:
                self.serial = create_frame_label_and_input(self.root, text="mã đăng ký", width=self.width, left=0.25, right=0.75)
                self.serial.delete(0, ctk.END)
                self.serial.insert(0, serial)
                return
            print(f'Ngày hết hạn sử dụng: {serials[serial]}')

            if not os.path.exists(ico_path):
                if os.path.exists(icon_path):
                    image = Image.open(icon_path)
                    image.save(ico_path, format='ICO')
                    image.close()
            
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)

            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.download_thread = threading.Thread()
            self.upload_thread = threading.Thread()
            self.edit_thread = threading.Thread()
            self.edit_audio_thread = threading.Thread()
            self.config = load_config()
            self.tiktok_config = load_tiktok_config()
            self.youtube_config = load_youtube_config()
            self.facebook_config = load_facebook_config()
            self.youtube = None
            self.is_youtube_window = False
            self.is_sign_up_youtube = False
            self.tiktok = None
            self.is_tiktok_window = False
            self.is_interact_setting_window = False
            self.is_auto_upload_tiktok_window = False
            self.is_sign_up_tiktok = False
            self.facebook = None
            self.is_sign_up_facebook = False
            self.is_facebook_window = False
            remove_file("log.txt")
            self.thread_main = None
            self.max_threads = 1
            self.icon = None
            self.convert_multiple_record = False
            self.load_download_info()
            self.is_start_app = True
            self.is_start_window = False
            self.is_edit_video_window = False
            self.is_edit_audio_option = False
            self.is_extract_audio_option = False
            self.is_open_edit_video_menu = False
            self.is_open_common_setting = False
            self.is_other_window = False
            self.is_other_download_window = False
            self.is_download_douyin_video_window = False
            self.is_download_douyin_channel = False
            self.is_open_auto_process_window = False
            self.is_text_to_mp3_window = False
            self.is_edit_audio_window = False
            self.is_169_to_916 = True
            self.is_combine_video_window = False
            self.is_increse_video_quality_window = False
            self.is_rename_file_by_index_window = False
            self.is_remove_char_in_file_name_window = False
            self.is_open_change_mac_addres_window = False
            self.is_extract_image_from_video_window = False
            self.is_editing_video = False
            self.is_add_new_channel = False
            self.is_remove_channel = False
            self.pre_time_check_status_video_youtube = 0
            self.first_check_status_video = True
            self.first_check_upload_video_youtube = True
            self.first_check_upload_video_tiktok = True
            self.first_check_upload_video_facebook = True
            self.is_stop_edit = False
            self.is_stop_download = False
            self.is_stop_upload = False
            self.driver = None
            self.new_name=None
            self.index = 1

            self.setting_window_size()
            self.create_icon()
            self.get_start_window()
            # self.start_main_check_thread()
            if self.config["auto_start"]:
                set_autostart()
            else:
                unset_autostart()
            self.is_start_app = False
        except:
            getlog()

#------------------------------------------------main thread----------------------------------------------------
    def start_main_check_thread(self):
            if self.is_start_app:
                self.config['time_check_auto_upload'] = "0"
                self.config['time_check_status_video'] = "0"
                self.save_config()
            self.thread_main = threading.Thread(target=self.main_check_thread)
            self.thread_main.daemon = True
            self.thread_main.start()

    def main_check_thread(self):
        while True:
            try:
                if not self.upload_thread.is_alive() and not self.download_thread.is_alive() and not self.edit_thread.is_alive():
                    self.auto_check_status_video_youtube()
                    self.auto_upload_youtube()
                    self.auto_upload_facebook()
                    self.auto_upload_tiktok()
                sleep(30)
            except:
                getlog()
                sleep(500)

    def check_status_process(self):
        status = False
        if self.upload_thread.is_alive() or self.download_thread.is_alive() or self.edit_thread.is_alive():
            return True

    def auto_upload_youtube(self):
        try:
            auto_channel_name = self.youtube_config['registered_account']
            for channel_name in auto_channel_name:
                try:
                    acc_config = load_youtube_config(channel_name)
                    if self.is_stop_upload:
                        return
                    videos_folder = acc_config.get('upload_folder')
                    videos = get_file_in_folder_by_type(videos_folder, ".mp4", False)   
                    if not videos:
                        return
                    print(f"đang thực hiện đăng video tự động cho kênh {channel_name} ...")
                    if self.is_stop_upload:
                        return
                    self.youtube= YouTubeManager(channel_name, is_auto_upload=True, upload_thread=self.upload_thread, download_thread=self.download_thread)
                    self.youtube.schedule_videos_by_selenium()
                except:
                    getlog()
                    print(f"Có lỗi trong quá trình đăng video tự động cho kênh {channel_name} !!!")
                sleep(2)

        except:
            getlog()

    def auto_check_status_video_youtube(self):
        print(f'Đang tạm dừng...')
        return
        try:
            time_check_cycle = get_time_check_cycle(self.config['time_check_status_video'])
            if time_check_cycle == 0:
                return
            if (self.first_check_status_video and time_check_cycle > 0) or (time() - self.pre_time_check_status_video_youtube >= time_check_cycle):
                self.pre_time_check_status_video_youtube = time()
                auto_channel_name = []
                for channel_name in auto_channel_name:
                    try:
                        time_check_cycle = get_time_check_cycle(self.config['time_check_status_video'])
                        if time_check_cycle == 0:
                            return
                        print(f"đang thực hiện kiểm tra tình trạng video cho kênh {channel_name} ...")
                        auto_youtube= YouTubeManager(channel_name, is_auto_upload=True, upload_thread=self.upload_thread, download_thread=self.download_thread)
                        auto_youtube.check_status_videos_by_selenium()
                    except:
                        getlog()
                        print(f"Có lỗi trong quá trình đăng video tự động cho kênh {channel_name} !!!")
                    sleep(2)
                self.first_check_status_video = False
        except:
            getlog()

    def auto_upload_facebook(self):
        try:
            time_check_cycle = get_time_check_cycle(self.config['time_check_auto_upload'])
            if time_check_cycle == 0:
                return
            if self.config['auto_upload_facebook']:
                if (self.first_check_upload_video_facebook and time_check_cycle > 0) or (time() - self.pre_time_check_auto_upload_facebook >= time_check_cycle):
                    self.pre_time_check_auto_upload_facebook = time()
                    auto_page_name = [page for page in self.facebook_config['registered_account']]
                    for page_name in auto_page_name:
                        try:
                            if self.is_stop_upload:
                                return
                            acc_config = load_facebook_config(page_name)
                            videos_folder = acc_config.get('upload_folder')
                            videos = get_file_in_folder_by_type(videos_folder, ".mp4", False)   
                            if not videos:
                                return
                            print(f"đang thực hiện đăng video tự động cho trang {page_name} ...")
                            if self.is_stop_upload:
                                return
                            auto_facebook= FacebookManager(page_name, self.download_thread, self.upload_thread, is_auto_upload=True)
                            auto_facebook.upload_video()
                        except:
                            getlog()
                            print(f"Có lỗi trong quá trình đăng video tự động cho trang {page_name} !!!")
                        sleep(2)
                    self.first_check_upload_video_facebook = False
        except:
            getlog()

    def auto_upload_tiktok(self):  
        try:
            
            auto_tiktok_othernames = self.tiktok_config['registered_account']
            print(f'Tổng số acc đã đăng ký: {len(auto_tiktok_othernames)}')
            is_auto_and_schedule = self.config['is_auto_and_schedule']
            # Giới hạn số luồng tối đa chạy cùng lúc
            try:
                max_threads = int(self.config['max_threads'])
            except:
                max_threads = 1
            
            semaphore = threading.Semaphore(max_threads)
            account_queue = queue.Queue()
            # Đẩy tất cả tài khoản vào hàng đợi
            for other_name in auto_tiktok_othernames:
                account_queue.put(other_name)
            # Tạo số luồng tối đa theo giới hạn
            self.upload_threads = []
            for _ in range(max_threads):
                thread = threading.Thread(target=self.worker_upload_task, args=(account_queue, semaphore, is_auto_and_schedule))
                thread.start()
                self.upload_threads.append(thread)
                sleep_random(5,10)
            # Chờ tất cả các luồng hoàn thành
            for thread in self.upload_threads:
                thread.join()
            self.first_check_upload_video_tiktok = False
        except Exception as e:
            getlog()
            print(f"{other_name} Lỗi trong auto_upload_tiktok: {e}")

    def worker_upload_task(self, account_queue, semaphore, is_auto_and_schedule):
        """Luồng xử lý upload video từ hàng đợi, chạy đến khi hàng đợi hết tài khoản"""
        while not account_queue.empty():
            other_name = account_queue.get()  # Lấy tài khoản từ hàng đợi
            with semaphore:  # Giới hạn số luồng tối đa
                try:
                    if self.is_stop_upload:
                        return
                    acc_config = load_tiktok_config(other_name)
                    videos_folder = acc_config.get('upload_folder')
                    if not videos_folder or not os.path.isdir(videos_folder):
                        videos_folder = self.videos_edit_folder_var.get().strip()
                        if not videos_folder or not os.path.isdir(videos_folder):
                            print(f'{thatbai} {other_name} Không tìm thấy thư mục chứa video!')
                            return
                    videos = get_file_in_folder_by_type(videos_folder, ".mp4", False)
                    if not videos:
                        return  # Không có video thì bỏ qua
                    print(f"Đang thực hiện đăng video tự động cho tài khoản TikTok {other_name} ...")
                    # Khởi tạo quá trình upload video
                    auto_tiktok = TikTokManager(other_name, self.download_thread, None, is_auto_upload=True, is_auto_and_schedule=is_auto_and_schedule)
                    auto_tiktok.upload_video(videos_folder)
                except:
                    getlog()

            account_queue.task_done()  # Đánh dấu tài khoản đã được xử lý

#-------------------------------------------Điều hướng window--------------------------------------------

    def get_start_window(self):
        if not self.is_start_app:
            self.reset()
            self.is_start_window=True
            self.show_window()
            self.setting_window_size()
        else:
            self.show_window()
        create_button(frame=self.root, text="Quản lý Youtube", command=self.open_youtube_window)
        create_button(frame=self.root, text="Quản lý Tiktok", command=self.open_tiktok_window)
        create_button(frame=self.root, text="Quản lý Facebook", command=self.open_facebook_window)
        create_button(frame=self.root, text="Tải video từ link/các nền tảng khác", command=self.open_other_download_video_window)
        create_button(frame=self.root, text="Xử lý video", command=self.open_edit_video_menu)
        create_button(frame=self.root, text="Xử lý audio", command=self.open_edit_audio_window)
        create_button(frame=self.root, text="Thiết lập tự động tải - edit - đăng", command=self.open_auto_process_window)
        create_button(frame=self.root, text="Chức năng khác", command=self.other_function)
        create_button(frame=self.root, text="Tắt proxy hệ thống", command=disable_system_proxy)
        create_button(frame=self.root, text="Cài đặt chung", command=self.open_common_settings)
    
    def open_auto_process_window(self):
        self.reset()
        self.is_open_auto_process_window = True
        self.show_window()
        self.setting_window_size()

        def start_thread_auto_process():
            auto_thread = threading.Thread(target=self.start_auto_process)
            auto_thread.start()
        self.download_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục lưu video", command=self.choose_folder_to_save, width=self.width, left=left, right=right)
        self.download_video_from_url_var = create_frame_label_and_input(self.root, text="Link tải hàng loạt video", width=self.width, left=left, right=right)
        self.quantity_download_var = self.create_settings_input("Số video muốn tải", values=["20", "50", "100"], left=left, right=right)
        self.filter_by_views_var = self.create_settings_input("Lọc theo số lượt xem", values=["100000", "200000", "300000", "500000", "1000000"], left=left, right=right)
        self.edit_video_var = self.create_settings_input("Chỉnh sửa video", values=['Yes', 'No'], left=left, right=right)
        self.index_file_name_var, self.file_name_var = create_frame_label_input_input(self.root, text="Đổi tên video - Số thứ tự", place_holder2="Nhập tên có chứa chuỗi \"<index>\" là vị trí số thứ tự", place_holder1="Số TT", width=self.width, left=left, mid=0.1, right=0.6)
        self.image_position_var = create_frame_label_and_input(self.root, text="Trích xuất ảnh làm thumbnail", width=self.width, left=left, right=right, place_holder='Vd: 5(5 giây cuối) hoặc 00:01:30(giây thứ 90)')
        youtube_channels = [key for key in self.youtube_config['registered_account']]
        self.youtube_channel_var = self.create_settings_input("Đăng lên youtube", values=youtube_channels, left=left, right=right)
        tiktok_channels = [key for key in self.tiktok_config['registered_account']]
        self.tiktok_channel_var = self.create_settings_input("Đăng lên tiktok", values=tiktok_channels, left=left, right=right)
        facebook_channels = [key for key in self.facebook_config['registered_account']]
        self.facebook_channel_var = self.create_settings_input("Đăng lên facebook", values=facebook_channels, left=left, right=right)
        self.delete_after_edit_var = self.create_settings_input("Xóa video gốc sau khi chỉnh sửa", values=['Yes', 'No'], left=left, right=right)
        self.delete_after_upload_var = self.create_settings_input("Xóa video sau khi đăng", values=['Yes', 'No'], left=left, right=right)
        create_button(frame=self.root, text="Bắt đầu tiến trình tự động", command=start_thread_auto_process, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)

    def start_auto_process(self):
        try:
            download_platform = ['youtube', 'tiktok', 'facebook']
            youtube_channel = self.youtube_channel_var.get().strip()
            tiktok_channel = self.tiktok_channel_var.get().strip()
            facebook_page = self.facebook_channel_var.get().strip()
            thumbnail = self.image_position_var.get().strip()
            if (not self.download_thread or not self.download_thread.is_alive()) and (not self.edit_thread or not self.edit_thread.is_alive()) and (not self.upload_thread or not self.upload_thread.is_alive()):
                download_folder = self.download_folder_var.get().strip()
                if not check_folder(download_folder):
                    return
                download_url = self.download_video_from_url_var.get().strip()
                if not download_url:
                    print("Hãy nhập link tải video !!!")
                    return
                download_from, web = get_download_flatform(download_url)
                if download_from not in download_platform:
                    print(f"Chưa hỗ trợ nền tảng {download_from} !!!")
                    return
                filter_by_views = self.filter_by_views_var.get().strip() or "0"
                quantity_download = self.quantity_download_var.get().strip() or "2000"
                if not quantity_download:
                    quantity_download = "2000"
                is_edit_video = self.edit_video_var.get().strip() == "Yes"
                self.new_name = self.file_name_var.get().strip()
                try:
                    self.index = int(self.index_file_name_var.get().strip())
                except:
                    self.index = 1
                if download_from == 'youtube':
                    self.youtube_config['download_folder'] = download_folder
                    self.youtube_config['download_url'] = download_url
                    self.youtube_config['filter_by_views'] = filter_by_views
                    self.youtube_config['quantity_download'] = quantity_download
                    self.youtube_config['show_browser'] = False
                    save_youtube_config(youtube_channel, self.youtube_config)
                    self.youtube = YouTubeManager(self.config['current_channel'], is_auto_upload=False, upload_thread=self.upload_thread, download_thread=self.download_thread)
                    self.download_thread = threading.Thread(target=self.youtube.download_videos_by_channel_id_selenium)
                    self.download_thread.start()
                elif download_from == 'tiktok':
                    self.tiktok_config['download_folder'] = download_folder
                    self.tiktok_config['download_url'] = download_url
                    self.tiktok_config['filter_by_views'] = filter_by_views
                    self.tiktok_config['quantity_download'] = quantity_download
                    self.tiktok_config['show_browser'] = True
                    account_download = self.config['current_tiktok_account']
                    save_tiktok_config(account_download, self.tiktok_config)
                    tiktok = TikTokManager(account_download, self.download_thread, self.upload_thread)
                    self.download_thread = threading.Thread(target=tiktok.get_tiktok_videos_by_channel_url)
                    self.download_thread.start()
                elif download_from == 'facebook':
                    self.facebook_config['download_folder'] = download_folder
                    self.facebook_config['download_url'] = download_url
                    self.facebook_config['filter_by_views'] = filter_by_views
                    self.facebook_config['quantity_download'] = quantity_download
                    self.facebook_config['show_browser'] = True
                    page_name = self.config['current_page']
                    save_facebook_config(page_name, self.facebook_config)
                    facebook = FacebookManager(page_name, self.download_thread, self.upload_thread)
                    self.download_thread = threading.Thread(target=facebook.download_page_videos_now)
                    self.download_thread.start()
                else:
                    print("Nơi tải video không phù hợp !!!")
            else:
                print("Hãy đảm bảo các tiến trình tải, edit và đăng video đã dừng !!!")
                return
            upload_folder = download_folder
            if is_edit_video:
                upload_folder = os.path.join(download_folder, 'upload_folder')
            def start_edit_videos():
                if thumbnail:
                    extract_folder = upload_folder
                cnt_err_edit = 0
                err_video_folder = os.path.join(download_folder, 'error_videos')
                os.makedirs(err_video_folder, exist_ok=True)
                while True:
                    try:
                        edit_videos = get_file_in_folder_by_type(download_folder, noti=False) or []
                        if len(edit_videos) > 0:
                            print("Đang kiểm tra và chỉnh sửa video ...")
                            sleep(30)
                            for video in edit_videos:
                                video_path = os.path.join(download_folder, video)
                                if not self.fast_edit_video(video_path, upload_folder=upload_folder):
                                    err_video_path = os.path.join(err_video_folder, video)
                                    try:
                                        shutil.move(video_path, err_video_path)
                                    except:
                                        print(f'Không thể chuyển video {video_path} vào thư mục {err_video_folder}')
                                if thumbnail:
                                    self.extract_image_from_video(extract_folder)
                                    
                        if (not self.download_thread or not self.download_thread.is_alive()) and len(edit_videos) == 0:
                            print("Thoát quá trình chỉnh sửa video tự động")
                            self.config['is_delete_video'] = False
                            break
                    except:
                        cnt_err_edit += 1
                        print(f"Có lỗi khi chỉnh sửa video, thử lại lần {cnt_err_edit}")
                    sleep(10)
                    if cnt_err_edit > 10:
                        break
            def start_upload_videos():
                is_delete_after_upload = self.delete_after_upload_var.get() == "Yes"
                upload_folder = download_folder
                if is_edit_video:
                    upload_folder = os.path.join(download_folder, 'upload_folder')
                youtube_folder = tiktok_folder = face_folder = None
                if youtube_channel:
                    youtube_folder = upload_folder
                    upload_folder = os.path.join(youtube_folder, 'youtube_upload_finished')
                if tiktok_channel:
                    tiktok_folder = upload_folder
                    upload_folder = os.path.join(tiktok_folder, 'tiktok_upload_finished')
                if facebook_page:
                    face_folder = upload_folder
                    upload_folder = os.path.join(face_folder, 'facebook_upload_finished')
                cnt_err_upload = 0
                cnt = 0
                is_stop = False
                while True:
                    try:
                        is_ok = True
                        if youtube_channel:
                            youtube_videos = get_file_in_folder_by_type(youtube_folder, ".mp4") or []
                            if len(youtube_videos) > 0:
                                print(f"Đang kiểm tra và đăng video cho kênh youtube: {youtube_channel}...")
                                self.youtube = YouTubeManager(youtube_channel, is_auto_upload=True, upload_thread=self.upload_thread, download_thread=self.download_thread)
                                if not self.youtube.schedule_videos_by_selenium(youtube_folder):
                                    is_ok = False
                                    cnt += 1
                        if tiktok_channel and not is_stop:
                            tiktok_videos = get_file_in_folder_by_type(tiktok_folder, ".mp4") or []
                            if len(tiktok_videos) > 0:
                                print(f"Đang kiểm tra và đăng video cho kênh tiktok: {tiktok_channel}...")
                                auto_tiktok= TikTokManager(tiktok_channel, self.download_thread, self.upload_thread, is_auto_upload=True)
                                status, is_stop = auto_tiktok.upload_video(tiktok_folder)
                                if not status:
                                    if is_stop:
                                        move_file_from_folder_to_folder(face_folder, tiktok_folder)
                                        face_folder = tiktok_folder
                                        upload_folder = os.path.join(face_folder, 'facebook_upload_finished')
                                        tiktok_folder = None
                                        is_delete_after_upload = False
                                    else:
                                        is_ok = False
                                        cnt += 1
                        if facebook_page:
                            face_videos = get_file_in_folder_by_type(face_folder, ".mp4") or []
                            if len(face_videos) > 0:
                                print(f"Đang kiểm tra và đăng video cho trang facebook: {facebook_page}...")
                                auto_facebook= FacebookManager(facebook_page, self.download_thread, self.upload_thread, is_auto_upload=True)
                                if not auto_facebook.upload_video(face_folder):
                                    is_ok = False
                                    cnt += 1
                        if is_delete_after_upload and is_ok:
                            dele_videos = get_file_in_folder_by_type(upload_folder, noti=False)
                            for dele_video in dele_videos:
                                file_path = os.path.join(upload_folder, dele_video)
                                remove_file(file_path)
                        youtube_videos = get_file_in_folder_by_type(youtube_folder, noti=False) or []
                        tiktok_videos = get_file_in_folder_by_type(tiktok_folder, noti=False) or []
                        face_videos = get_file_in_folder_by_type(face_folder, noti=False) or []
                        if (not self.download_thread or not self.download_thread.is_alive()) and (not self.edit_thread or not self.edit_thread.is_alive()) and len(youtube_videos) == 0 and len(tiktok_videos) == 0 and len(face_videos) == 0:
                            print("Thoát quá trình đăng video tự động")
                            break
                        if cnt > 10:
                            break
                    except:
                        cnt_err_upload += 1
                        print(f"Có lỗi khi đăng video, thử lại lần {cnt_err_upload}")
                    sleep(10)
                    if cnt_err_upload > 5:
                        break
            if is_edit_video:
                while True:
                    edit_videos = get_file_in_folder_by_type(download_folder, noti=False) or []
                    if len(edit_videos) > 0:
                        break
                    sleep(10)
                if not self.edit_thread or not self.edit_thread.is_alive():
                    self.edit_thread = threading.Thread(target=start_edit_videos)
                    self.edit_thread.start()

            while True:
                upload_videos = get_file_in_folder_by_type(upload_folder, noti=False) or []
                if len(upload_videos) > 0:
                    if not youtube_channel or not self.download_thread or not self.download_thread.is_alive():
                        break
                sleep(10)
            if not self.upload_thread or not self.upload_thread.is_alive():
                self.upload_thread = threading.Thread(target=start_upload_videos)
                self.upload_thread.start()
        except:
            getlog()
            print("Có lỗi trong quá trình tự động tải - chỉnh sửa - đăng video !!!")

    def open_other_download_video_window(self):
        def start_download_by_video_url():
            download_url = self.download_by_video_url.get()
            if not download_url:
                self.noti("Hãy nhập link video muốn tải trước.")
                return
            if not self.download_thread or not self.download_thread.is_alive():
                self.is_stop_download = False
                self.download_thread = threading.Thread(target=self.download_video_by_video_url)
                self.download_thread.start()
        
        self.reset()
        self.is_other_download_window = True
        self.show_window()
        self.setting_window_size()
        self.is_start_app = False
        self.download_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục lưu video", command=self.choose_folder_to_save, width=self.width, left=0.4, right=0.6)
        self.download_by_video_url = create_frame_button_and_input(self.root,text="Tải video từ URL", command=start_download_by_video_url, width=self.width, left=0.4, right=0.6)
        create_button(frame=self.root, text="Tải video từ Douyin", command=self.open_download_douyin_video_window)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)

    def choose_folder_to_save(self):
        download_folder = filedialog.askdirectory()
        if download_folder:
            self.download_folder_var.delete(0, ctk.END)
            self.download_folder_var.insert(0, download_folder)
            self.config['download_folder'] = download_folder
            self.save_config()

    def download_video_by_video_url(self):
        download_folder = self.config['download_folder']
        video_url = self.download_by_video_url.get()
        video_urls = [video_url]
        try:
            if not download_video_by_url(video_url, download_folder):
                download_video_by_bravedown(video_urls, download_folder)
        except:
            download_video_by_bravedown(video_urls, download_folder)


    def open_download_douyin_video_window(self):
        self.reset()
        self.is_download_douyin_video_window = True
        self.show_window()
        self.setting_window_size()
        
        def start_thread_download_douyin_video_by_url():
            if not self.download_thread or not self.download_thread.is_alive():
                self.is_download_douyin_channel = False
                self.download_thread = threading.Thread(target=start_download_douyin_video)
                self.download_thread.start()
            else:
                self.noti("Đang tải video ở một luồng khác.")

        def start_thread_download_douyin_channel():
            if not self.download_thread or not self.download_thread.is_alive():
                self.is_download_douyin_channel = True
                self.download_thread = threading.Thread(target=start_download_douyin_video)
                self.download_thread.start()
            else:
                self.noti("Đang tải video ở một luồng khác.")

        def start_download_douyin_video():
            try:
                def check_quang_cao():
                    xpath = get_xpath_by_multi_attribute('div', ['id="dismiss-button"'])
                    ele = get_element_by_xpath(self.driver, xpath)
                    if ele:
                        ele.click()

                def download_douyin_video_by_tikvideoapp(url):

                    try:
                        file_name = f"{url.split('/')[-1]}.mp4"
                        output_path = os.path.join(self.config['download_folder'], file_name)
                        self.driver.get('https://tikvideo.app/vi/download-douyin-video')
                        sleep(2)
                        check_quang_cao()
                        input_xpath = get_xpath_by_multi_attribute('input', ['id="s_input"'])
                        input_ele = get_element_by_xpath(self.driver, input_xpath)
                        if input_ele:
                            input_ele.send_keys(url)
                            input_ele.send_keys(Keys.ENTER)
                            check_quang_cao()
                            video_link_xpath = "//a[contains(text(),'Tải xuống MP4 HD')]"
                            video_link_ele = get_element_by_xpath(self.driver, video_link_xpath)
                            if video_link_ele:
                                url = video_link_ele.get_attribute('href')
                                response = requests.get(url, stream=True)

                                # Lưu video vào file
                                with open(output_path, 'wb') as file:
                                    for chunk in response.iter_content(chunk_size=1024):
                                        if chunk:
                                            file.write(chunk)
                                if not os.path.exists(output_path):
                                    if download_douyin_video_by_snaptikapp(url):
                                        return True
                                    else:
                                        return False
                                else:
                                    return True
                        return False
                    except:
                        return False

                def download_douyin_video_by_snaptikapp(url):
                    try:
                        file_name = f"{url.split('/')[-1]}.mp4"
                        output_path = os.path.join(self.config['download_folder'], file_name)
                        self.driver.get('https://snaptik.app/vn/douyin-downloader')
                        sleep(2)
                        check_quang_cao()
                        input_xpath = get_xpath_by_multi_attribute('input', ['id="url"', 'name="url"'])
                        input_ele = get_element_by_xpath(self.driver, input_xpath)
                        if input_ele:
                            input_ele.send_keys(url)
                            ele.send_keys(Keys.ENTER)
                            check_quang_cao()
                            video_link_xpath = "//a[contains(text(),'Tải xuống MP4 HD')]"
                            video_link_ele = get_element_by_xpath(self.driver, video_link_xpath)
                            if video_link_ele:
                                url = video_link_ele.get_attribute('href')
                                response = requests.get(url, stream=True)
                                with open(output_path, 'wb') as file:
                                    for chunk in response.iter_content(chunk_size=1024):
                                        if chunk:
                                            file.write(chunk)
                                if os.path.exists(output_path):
                                    return True
                        return False
                    except:
                        return False

                video_urls = []
                cnt_download = 0
                if self.is_download_douyin_channel:
                    cnt_search = 0
                    channel_link = self.download_by_channel_link.get()
                    if not channel_link:
                        self.noti("Hãy nhập link kênh muốn tải video trước.")
                        return
                    self.driver = get_driver(show=False)
                    self.driver.get(channel_link)
                    self.check_noti_login_douyin(self.driver)
                    if self.is_stop_download:
                        return
                    last_height = self.driver.execute_script("return document.body.scrollHeight")
                    k = False
                    print(f"Bắt đầu quét video trong kênh theo link {channel_link} ...")
                    while True:
                        if self.is_stop_download:
                            return
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Cuộn xuống cuối trang
                        sleep(2)
                        new_height = self.driver.execute_script("return document.body.scrollHeight") # Tính chiều cao mới của trang
                        if new_height == last_height: # Kiểm tra nếu không có thêm nội dung mới
                            if k:
                                break
                            else:
                                k = True
                                sleep(2)
                                continue
                        k = False
                        last_height = new_height
                        cnt_search += 1
                        if cnt_search > 100:
                            break

                    xpath = get_xpath('a', 'uz1VJwFY TyuBARdT IdxE71f8')
                    eles = self.driver.find_elements(By.XPATH, xpath)
                    if len(eles) > 0:
                        for ele in eles:
                            if self.is_stop_download:
                                return
                            video_link = ele.get_attribute('href')
                            if video_link not in video_urls:
                                video_urls.append(video_link)
                    else:
                        xpath = "//div[starts-with(@id, 'waterfall_item_')]"
                        eles = self.driver.find_elements(By.XPATH, xpath)
                        if eles:
                            for ele in eles:
                                if self.is_stop_download:
                                    return
                                ele_id = ele.get_attribute('id')
                                video_id = ele_id.split('waterfall_item_')[-1]
                                video_link = f'https://www.douyin.com/video/{video_id}'
                                if video_link not in video_urls:
                                    video_urls.append(video_link)
                else:
                    video_url = self.download_by_video_url.get().strip()
                    video_urls.append(video_url)
                if len(video_urls) > 0:
                    print(f'Đã tìm thấy {len(video_urls)} video')
                    print("Bắt đầu tải video ...")
                    for url in video_urls.copy():
                        if self.is_stop_download:
                            break
                        print(f'Bắt đầu tải video {url}')
                        if download_douyin_video_by_tikvideoapp(url):
                            print(f"Tải thành công video {url}")
                            video_urls.remove(url)
                            cnt_download += 1
                        else:
                            print(f"Tải video không thành công: {url}!!!")
                    if cnt_download > 0:
                        print(f'Đã tải thành công {cnt_download} video')
                    else:
                        self.close_driver()
                        if len(video_urls) > 0:
                            download_video_by_bravedown(video_urls, self.config['download_folder'])
                else:
                    print("Không tìm thấy video phù hợp !!!")
            except:
                print("Có lỗi trong quá trình tải video từ douyin")
            finally:
                self.close_driver()

        self.download_by_video_url = create_frame_button_and_input(self.root, text="Tải video từ link video", command=start_thread_download_douyin_video_by_url, width=self.width, left=0.45, right=0.55)
        self.download_by_channel_link = create_frame_button_and_input(self.root, text="Tải video từ link kênh/ link tìm kiếm", command=start_thread_download_douyin_channel, width=self.width, left=0.45, right=0.55)
        create_button(self.root, text="Lùi lại", command=self.open_other_download_video_window, width=self.width)



        

    def check_noti_login_douyin(self, driver):
        xpath = get_xpath('div', 'douyin-login__close dy-account-close')
        ele = get_element_by_xpath(driver, xpath)
        if ele:
            ele.click()
        
    def open_edit_audio_window(self):
        self.reset()
        self.is_edit_audio_window = True
        self.show_window()
        self.setting_window_size()
        create_button(frame=self.root, text="Thay đổi thông tin audio", command=self.open_edit_audio_option)
        create_button(frame=self.root, text="Trích xuất audio", command=self.open_extract_audio_option)
        create_button(frame=self.root, text="Gộp audio", command=self.open_combine_audio_window)
        create_button(frame=self.root, text="Chuyển đổi văn bản sang giọng nói", command=self.open_text_to_mp3_window)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)

    def other_function(self):
        self.reset()
        self.is_other_window = True
        self.show_window()
        self.setting_window_size()
        create_button(self.root, text="Đặt tên file theo chỉ số", command=self.open_rename_file_by_index_window, width=self.width)
        create_button(self.root, text="Xóa ký tự trong file", command=self.open_remove_char_in_file_name_window, width=self.width)
        create_button(self.root, text="Trích xuất ảnh từ video", command=self.extract_image_from_video_window, width=self.width)
        create_button(frame=self.root, text="Đổi thông tin mã máy", command= self.change_mac_address_window, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)

    def change_mac_address_window(self):
        def change_mac_address_now():
            CHANGE_MAC_URL = 'http://127.0.0.1:5000/api/change_mac'
            data = {}
            data['old_mac_address'] = self.old_mac_address_var.get().strip()
            data['password'] = self.pass_mac_var.get().strip()
            data['new_mac_address'] = self.new_mac_address_var.get().strip()
            if not data['old_mac_address'] or not data['password'] or not data['new_mac_address']:
                print("Hãy nhập đầy đủ thông tin !!!")
                return
            response = requests.post(CHANGE_MAC_URL, json=data)
            print(response)
            return response
            
        self.reset()
        self.is_open_change_mac_addres_window = True
        self.show_window()
        self.setting_window_size()
        self.old_mac_address_var = create_frame_label_and_input(self.root, text="Nhập mã máy cũ",  width=self.width, left=0.4, right=0.6)
        self.pass_mac_var = create_frame_label_and_input(self.root, text="Nhập mật mã xác nhận", width=self.width, left=0.4, right=0.6)
        self.new_mac_address_var = create_frame_label_and_input(self.root, text="Nhập mã máy mới",  width=self.width, left=0.4, right=0.6)
        create_button(frame=self.root, text="Đổi thông tin mã máy", command= change_mac_address_now, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.other_function, width=self.width)

    def open_youtube_window(self):
        self.reset()
        self.is_youtube_window = True
        self.show_window()
        self.setting_window_size()
        values = self.youtube_config['registered_account']
        if not values:
            values = ['--------------------']
        self.input_current_channel_name = self.create_settings_input("Chọn tên kênh", "current_channel" ,values=values, left=0.4, right=0.6)
        self.input_current_channel_name.set(self.config['current_channel'])
        create_button(self.root, text="Mở cửa sổ quản lý kênh Youtube", command=self.start_youtube_management)
        create_button(self.root, text="Đăng ký kênh youtube mới", command=self.add_new_channel)
        create_button(self.root, text="Xóa thông tin kênh youtube", command=self.remove_youtube_channel_window)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)

    def remove_youtube_channel_window(self):
        def remove_channel_now():
            try:
                channel_name = self.channel_remove_var.get()
                if not channel_name:
                    self.noti("Hãy chọn channel muốn xóa.")
                    return
                if channel_name in self.youtube_config['registered_account']:
                    self.youtube_config['registered_account'].remove(channel_name)
                    save_youtube_config(data=self.youtube_config)
                    self.noti(f'Xóa kênh [{channel_name}] thành công.')
                    self.remove_youtube_channel_window()
                else:
                    self.noti(f"Kênh {channel_name} không tồn tại trong cơ sở dữ liệu")
            except:
                self.noti(f"Xóa kênh [{channel_name}] thất bại !!!")
            
        self.reset()
        self.is_remove_channel = True
        self.setting_window_size()
        self.show_window()
        self.channel_remove_var = self.create_settings_input(text="Nhập tên kênh youtube", config_key='current_channel', values=self.youtube_config['registered_account'], left=left, right=right)
        create_button(frame=self.root, text="Bắt đầu xóa thông tin kênh youtube", command=remove_channel_now)
        create_button(self.root, text="Lùi lại", command=self.open_youtube_window, width=self.width)

    def add_new_channel(self):
        self.reset()
        self.is_add_new_channel = True
        self.setting_window_size()
        self.show_window()
        self.input_email = self.create_settings_input(text="Tài khoản gmail", values=self.youtube_config['registered_account'], left=left, right=right)
        self.input_current_channel_name = create_frame_label_and_input(self.root, text="Nhập tên kênh")
        create_button(frame=self.root, text="Đăng ký ngay", command=self.sign_up_youtube_channel)
        create_button(self.root, text="Lùi lại", command=self.open_youtube_window, width=self.width)
    
    def sign_up_youtube_channel(self):
        self.is_add_new_channel = True
        email = self.input_email.get().strip()
        channel_name = self.input_current_channel_name.get().strip()
        if not email or not channel_name:
            self.noti("Hãy nhập đầy đủ thông tin!")
            return
        if '@gmail.com' not in email:
            self.noti("Định dạng email là abc@gmail.com.")
            return
        acc_config = load_youtube_config(channel_name)
        acc_config['email'] = email
        if channel_name not in self.youtube_config['registered_account']:
            self.youtube_config['registered_account'].append(channel_name)
        self.config['current_channel'] = channel_name
        save_youtube_config(channel_name, acc_config)
        save_youtube_config(data=self.youtube_config)
        self.save_config()
        self.start_youtube_management(channel_name)

    def start_youtube_management(self, channel_name=None):
        if self.is_add_new_channel:
            self.is_add_new_channel = False
            if channel_name not in self.youtube_config['registered_account']:
                self.youtube_config['registered_account'].append(channel_name)
        else:
            channel_name = self.input_current_channel_name.get().strip()
            if not channel_name:
                self.noti("Hãy chọn kênh!")
                return
            if channel_name not in self.youtube_config['registered_account']: 
                self.noti(f"tài khoản email {channel_name} chưa được đăng ký!")
                return
        self.youtube = YouTubeManager(channel_name, is_auto_upload=False, download_thread=self.download_thread, upload_thread=self.upload_thread)
        self.reset()
        self.config['current_channel'] = channel_name
        self.save_config()
        save_youtube_config(data=self.youtube_config)
        self.youtube.get_start_youtube()

    def open_tiktok_window(self, other_name=None):
        self.reset()
        self.is_tiktok_window = True
        self.show_window()
        self.setting_window_size()
        self.tiktok_account_var = self.create_settings_input(text="Chọn tài khoản", config_key="current_tiktok_account", values=self.tiktok_config['registered_account'])
        if other_name:
            self.tiktok_account_var.set(other_name)
        create_button(self.root, text="Mở cửa sổ quản lý kênh tiktok", command=self.start_tiktok_management)
        create_button(self.root, text="Đăng ký tài khoản tiktok mới", command=self.sign_up_tiktok_window)
        create_button(self.root, text="Xóa thông tin kênh tiktok", command=self.remove_tiktok_channel_window)
        create_button(self.root, text="Thiết lập tự dộng đăng", command=self.auto_upload_tiktok_window)
        create_button(self.root, text="Thiết lập tương tác cho các kênh tiktok", command=self.interact_setting_window)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)


    def auto_upload_tiktok_window(self):
        def start_auto_upload_tiktok_thread():
            is_auto_and_schedule = self.is_auto_and_schedule_var.get() == 'Yes'
            max_threads = self.max_threads_var.get().strip()
            self.config['is_auto_and_schedule'] = is_auto_and_schedule
            self.config['max_threads'] = max_threads
            self.save_config()
            auto_upload_thread = threading.Thread(target=self.auto_upload_tiktok)
            auto_upload_thread.start()

        self.reset()
        self.is_auto_upload_tiktok_window = True
        self.show_window()
        self.setting_window_size()
        self.is_auto_and_schedule_var = self.create_settings_input("Lên lịch", "is_auto_and_schedule", values=["Yes", "No"], left=0.4, right=0.6)
        self.max_threads_var = self.create_settings_input("Số account đăng video tối đa", "max_threads", values=["1", "3", "5"], left=0.4, right=0.6)
        self.videos_edit_folder_var = create_frame_button_and_input(self.root,text="Chọn Thư Mục Chứa Video", command= self.choose_videos_edit_folder, left=0.4, right=0.6, width=self.width)
        create_button(self.root, text="Bắt đầu", command=start_auto_upload_tiktok_thread, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.open_tiktok_window, width=self.width)


    def interact_setting_window(self):
        self.reset()
        self.is_interact_setting_window = True
        self.show_window()
        self.setting_window_size()
        self.insteract_now_var = self.create_settings_input(text="Tương tác ngay", config_key='insteract_now', values=['Yes', 'No'], left=left, right=right)
        self.max_threads_var = self.create_settings_input(text="Số acc chạy cùng lúc", config_key='max_threads', values=['1', '2', '3', '4'], left=left, right=right)
        self.video_number_interact_var = self.create_settings_input(text="Số video tương tác(min-max)", config_key='video_number_interact', values=['5-10', '10-20'], left=left, right=right)
        self.watch_time_var = self.create_settings_input(text="Thời gian xem(min-max) (giây)", config_key='watch_time', values=['5-30', '10-40'], left=left, right=right)
        self.watch_percent_var = self.create_settings_input(text="Xác suất tiến hành tương tác (%)", config_key='watch_percent', values=['50', '60', '70'], left=left, right=right)
        self.like_percent_var = self.create_settings_input(text="Xác suất bấm like (%)", config_key='like_percent', values=['30', '40', '50'], left=left, right=right)
        self.comment_percent_var = self.create_settings_input(text="Xác suất comment (%)", config_key='comment_percent', values=['20', '30', '40'], left=left, right=right)
        self.follow_percent_var = self.create_settings_input(text="Xác suất bấm follow so với xs comment (%)", config_key='follow_percent', values=['30', '40', '50'], left=left, right=right)
        self.comments_texts_var = create_frame_label_and_input(self.root, 'Các lời commnet', 'hay lắm,tuyệt vời,...', width=self.width, left=left, right=right)
        create_button(self.root, text="Lưu thiết lập tương tác", command=self.save_insteract_tiktok_thread, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.open_tiktok_window, width=self.width)

    def start_thread_insteract_tiktok(self):
        active_threads = []
        try:
            max_threads = int(self.config['max_threads'])
        except:
            max_threads = 1
        othernames = self.tiktok_config['registered_account']
        for othername in othernames:
            acc_config = load_tiktok_config(othername)
            if acc_config['auto_interact']:
                while len(active_threads) >= max_threads:
                    # Nếu đã đạt giới hạn, chờ một chút trước khi kiểm tra lại
                    active_threads = [t for t in active_threads if t.is_alive()]
                    sleep_random(5,10)

                print(f'Bắt đầu tương tác cho kênh {othername} ...')
                Tiktok = TikTokManager(othername, is_auto_upload=True)
                Tiktok.acc_config['use_profile_type'] = "Không dùng"
                # Tạo và lưu thread vào danh sách
                thread = threading.Thread(target=Tiktok.interact_with_tiktok, args=(self.config['video_number_interact'],))
                thread.start()
                active_threads.append(thread)
            sleep(10)


    def save_insteract_tiktok_thread(self):
        try:
            self.config['insteract_now'] = self.insteract_now_var.get().strip() == 'Yes'
            self.config['video_number_interact'] = self.video_number_interact_var.get().strip()
            self.config['max_threads'] = self.max_threads_var.get().strip()
            self.config['watch_time'] = self.watch_time_var.get().strip()
            self.config['watch_percent'] = self.watch_percent_var.get().strip()
            self.config['like_percent'] = self.like_percent_var.get().strip()
            self.config['comment_percent'] = self.comment_percent_var.get().strip()
            self.config['follow_percent'] = self.follow_percent_var.get().strip()
            self.config['comments_texts'] = self.comments_texts_var.get().strip()
            self.save_config()
            print(f'Thiết lập đã lưu.')
            if self.config['insteract_now']:
                self.config['insteract_now'] = False
                self.save_config()
                thread = threading.Thread(target=self.start_thread_insteract_tiktok)
                thread.start()
            else:
                self.open_tiktok_window()
        except:
            getlog()

    def remove_tiktok_channel_window(self):
        def remove_channel_now():
            try:
                other_name = self.tiktok_channel_remove_var.get()
                if not other_name:
                    self.noti("Hãy chọn channel muốn xóa.")
                    return
                acc_config = load_tiktok_config(other_name)
                if other_name not in self.tiktok_config['registered_account']:
                    self.noti(f"Kênh {other_name} không tồn tại")
                    return
                if other_name in self.tiktok_config['registered_account']:
                    self.tiktok_config['registered_account'].remove(other_name)
                if self.config['current_tiktok_account'] == other_name:
                    self.config['current_tiktok_account'] = ""
                self.save_config()
                save_tiktok_config(other_name, acc_config)
                save_tiktok_config(data=self.tiktok_config)
                self.noti(f'Xóa kênh [{other_name}] thành công.')
                self.remove_tiktok_channel_window()

            except:
                self.noti(f"Xóa kênh [{other_name}] thất bại !!!")
        self.reset()
        self.is_remove_channel = True
        self.setting_window_size()
        self.show_window()
        self.tiktok_channel_remove_var = self.create_settings_input(text="Nhập tên kênh tiktok", config_key='current_tiktok_account', values=self.tiktok_config['registered_account'], left=left, right=right)
        create_button(frame=self.root, text="Bắt đầu xóa thông tin kênh tiktok", command=remove_channel_now)
        create_button(self.root, text="Lùi lại", command=self.open_tiktok_window, width=self.width)

    def sign_up_tiktok_window(self):
        self.reset()
        self.is_sign_up_tiktok = True
        self.show_window()
        self.setting_window_size()
        def sign_up_tiktok():
            self.is_sign_up_tiktok = True
            account_txt_path = self.chose_account_txt_file_var.get().strip()
            if account_txt_path:
                acc_data = get_json_data(account_txt_path)
                if not acc_data:
                    print(f"Không tìm thấy thông tin tài khoản trong file {account_txt_path}")
                    return
                for line in acc_data:
                    tiktok_account = tiktok_password = other_name = proxy = ""
                    acc_info = [fff.strip() for fff in line.split(',')]
                    try:
                        if len(acc_info) == 4:
                            tiktok_account, tiktok_password, other_name, proxy = acc_info
                        elif len(acc_info) == 3:
                            if ":" in acc_info[2]:
                                tiktok_account, tiktok_password, proxy = acc_info
                            else:
                                tiktok_account, tiktok_password, other_name = acc_info
                        elif len(acc_info) == 2:
                            tiktok_account, tiktok_password = acc_info
                        else:
                            print(f'{thatbai} Tài khoản phải có ít nhất 2 thông tin account,password: \n<{line}>')
                            continue
                        if not other_name or other_name == 'none':
                            other_name = tiktok_account
                    except:
                        print(f'{thatbai} Tài khoản phải có ít nhất 2 thông tin account,password: \n<{line}>')
                        continue
                    if not tiktok_account or not tiktok_password or not other_name:
                        self.noti("Hãy nhập đầy đủ thông tin!")
                        continue
                    acc_config = load_tiktok_config(other_name)
                    acc_config['email'] = tiktok_account
                    acc_config['password'] = tiktok_password
                    acc_config['proxy'] = proxy
                    
                    if other_name not in self.tiktok_config['registered_account']:
                        self.tiktok_config['registered_account'].append(other_name)
                        print(f'{thanhcong} Đăng ký tài khoản <{other_name}> thành công')
                    else:
                        print(f'{thanhcong} Cập nhật thành công cho tài khoản: <{line}>')
                    save_tiktok_config(other_name, acc_config)
                    save_tiktok_config(data=self.tiktok_config)
            else:
                other_name = self.other_name_var.get().strip()
                tiktok_account = self.tiktok_account_var.get().strip()
                tiktok_password = self.tiktok_password_var.get().strip()
                proxy = self.proxy_var.get().strip()
                if not tiktok_account or not tiktok_password:
                    self.noti("Hãy nhập đầy đủ thông tin!")
                    return
                if not other_name or other_name == 'none':
                    other_name = tiktok_account

                acc_config = load_tiktok_config(other_name)
                acc_config['email'] = tiktok_account
                acc_config['password'] = tiktok_password
                acc_config['proxy'] = proxy

                if other_name not in self.tiktok_config['registered_account']:
                    self.tiktok_config['registered_account'].append(other_name)
                    print(f'{thanhcong} Đăng ký tài khoản <{other_name}> thành công')
                else:
                    print(f'{thanhcong} Cập nhật thành công cho tài khoản: <{other_name}>')
                save_tiktok_config(other_name, acc_config)
                save_tiktok_config(data=self.tiktok_config)
            self.open_tiktok_window(other_name)

        self.other_name_var = create_frame_label_and_input(self.root, text="Tên hiển thị")
        self.tiktok_account_var = create_frame_label_and_input(self.root, text="Nhập tài khoản tiktok")
        self.tiktok_password_var = create_frame_label_and_input(self.root, text="Nhập mật khẩu", is_password=True)
        self.proxy_var = create_frame_label_and_input(self.root, text="Nhập proxy")
        self.chose_account_txt_file_var = create_frame_button_and_input(self.root, "Lấy tài khoản từ file .txt", command=self.chose_account_txt_file, width=self.width, left=left, right=right)
        create_button(self.root, text="Đăng ký ngay", command=sign_up_tiktok)
        create_button(self.root, text="Lùi lại", command=self.open_tiktok_window, width=self.width)

    def start_tiktok_management(self, other_name=None):
        if self.is_sign_up_tiktok:
            if not other_name:
                other_name = self.other_name_var.get()
        else:
            other_name = self.tiktok_account_var.get()
        if not other_name:
            return
        if not self.is_sign_up_tiktok:
            if other_name not in self.tiktok_config['registered_account']:
                self.noti(f"tài khoản {other_name} chưa được đăng ký")
                return
        self.config['current_tiktok_account'] = other_name
        self.save_config()
        self.reset()
        self.setting_window_size()
        self.tiktok = TikTokManager(other_name)
        self.tiktok.get_start_tiktok()



    def open_facebook_window(self):
        self.reset()
        self.is_facebook_window = True
        self.show_window()
        self.setting_window_size()
        self.facebook_page_name_var = self.create_settings_input(text="Chọn trang facebook", config_key="current_page", values=self.facebook_config['registered_account'])
        create_button(self.root, text="Mở cửa sổ quản lý trang facebook", command=self.start_facebook_management)
        create_button(self.root, text="Đăng ký trang facebook mới", command=self.sign_up_facebook_window)
        create_button(self.root, text="Xóa thông tin trang facebook", command=self.remove_facebook_page_window)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)

    def sign_up_facebook_window(self):
        self.reset()
        self.is_sign_up_facebook = True
        self.show_window()
        self.setting_window_size()
        def sign_up_facebook():
            facebook_account = self.facebook_account_var.get().strip()
            facebook_password = self.facebook_password_var.get().strip()
            facebook_page_name = self.facebook_page_name_var.get().strip()
            if not facebook_account or not facebook_password or not facebook_page_name:
                self.noti("Hãy nhập đầy đủ thông tin!")
                return
            acc_config = load_facebook_config(facebook_page_name)

            acc_config['email'] = facebook_account
            acc_config['password'] = facebook_password

            self.config['current_page'] = facebook_page_name
            self.facebook_config['registered_account'].append(facebook_page_name)
            save_facebook_config(data=self.facebook_config)
            save_facebook_config(facebook_page_name, acc_config)
            self.start_facebook_management(facebook_page_name)

        self.facebook_account_var = self.create_settings_input(text="Tài khoản Facebook", values=self.facebook_config['registered_account'], left=left, right=right)
        self.facebook_password_var = create_frame_label_and_input(self.root, text="Nhập mật khẩu", is_password=True)
        self.facebook_page_name_var = create_frame_label_and_input(self.root, text="Nhập tên trang")
        create_button(self.root, text="Đăng ký ngay", command=sign_up_facebook)
        create_button(self.root, text="Lùi lại", command=self.open_facebook_window, width=self.width)

    def remove_facebook_page_window(self):
        def remove_channel_now():
            try:
                page_name = self.page_remove_var.get()
                if not page_name:
                    self.noti("Hãy chọn trang facebook muốn xóa.")
                    return
                if page_name in self.facebook_config['registered_account']:
                    self.facebook_config['registered_account'].remove(page_name)
                    self.noti(f'Xóa trang [{page_name}] thành công.')
                    save_facebook_config(data=self.facebook_config)
                    self.remove_facebook_page_window()
                else:
                    self.noti(f"Trang {page_name} không tồn tại trong cơ sở dữ liệu")
            except:
                self.noti(f"Xóa trang [{page_name}] thất bại !!!")
            
        self.reset()
        self.is_remove_channel = True
        self.setting_window_size()
        self.show_window()
        self.page_remove_var = self.create_settings_input(text="Nhập tên trang facebook", config_key='current_page', values=self.facebook_config['registered_account'], left=left, right=right)
        create_button(frame=self.root, text="Bắt đầu xóa thông tin trang facebook", command=remove_channel_now)
        create_button(self.root, text="Lùi lại", command=self.open_facebook_window, width=self.width)

    def start_facebook_management(self, facebook_page_name=None):
        if not facebook_page_name:
            facebook_page_name = self.facebook_page_name_var.get()
            if not facebook_page_name:
                self.noti("Hãy chọn trang facebook!")
                return
            if facebook_page_name not in self.facebook_config['registered_account']:
                self.noti(f"Trang {facebook_page_name} chưa được đăng ký!")
                return
            self.config['current_page'] = facebook_page_name
            self.save_config()
        self.reset()

        self.facebook = FacebookManager(facebook_page_name, self.download_thread, self.upload_thread)
        self.facebook.get_start_facebook()

#---------------------------------------------edit audio-------------------------------------------
        
    def open_edit_audio_option(self):
        def start_thread_edit_audio():
            def start_edit_audio():
                if save_seting_input():
                    first_cut = self.first_cut_var.get().strip()
                    end_cut = self.end_cut_var.get().strip()
                    edit_audio_ffmpeg(input_audio_folder=self.config['audios_edit_folder'], start_cut=first_cut, end_cut=end_cut, pitch_factor=self.config['pitch_factor'], cut_silence=self.config['cut_silence'], aecho=self.config['aecho'])

            if not self.edit_audio_thread or not self.edit_audio_thread.is_alive():
                self.edit_audio_thread = threading.Thread(target=start_edit_audio)
                self.edit_audio_thread.start()
        def save_seting_input():
            self.config['audio_speed'] = self.audio_speed_var.get().strip()
            self.config['pitch_factor'] = self.pitch_factor_var.get().strip()
            self.config['cut_silence'] = self.cut_silence_var.get().strip() == 'Yes'
            self.config['aecho'] = self.aecho_var.get().strip()
            self.config['audios_edit_folder'] = self.folder_get_audio_var.get().strip()
            if not check_folder(self.config['audios_edit_folder']):
                return False
            self.save_config()
            return True

        self.reset()
        self.is_edit_audio_option = True
        self.setting_window_size()
        self.show_window()
        self.end_cut_var, self.first_cut_var = create_frame_label_input_input(self.root, text="Cắt ở đầu/cuối video (s)", width=self.width, left=0.4, mid=0.28, right=0.32)
        # self.end_cut_var.delete(0, ctk.END)
        self.end_cut_var.insert(0, 0)
        self.first_cut_var.insert(0, 0)
        self.audio_speed_var = self.create_settings_input(text="Tốc độ phát", config_key="audio_speed", values=['0.8', '1', '1.2'], left=0.4, right=0.6)
        self.pitch_factor_var = self.create_settings_input(text="Điều chỉnh cao độ (vd: 1.2)", config_key="pitch_factor", values=['-0.8','1','1.2'], left=0.4, right=0.6)
        self.cut_silence_var = self.create_settings_input(text="Cắt bỏ những đoạn im lặng", config_key="cut_silence", values=['Yes', 'No'], left=0.4, right=0.6)
        self.aecho_var = self.create_settings_input(text="Tạo tiếng vang (ms)", config_key="aecho", values=['100', '500', '1000'], left=0.4, right=0.6)
        self.folder_get_audio_var = create_frame_button_and_input(self.root,text="Chọn thư mục chứa audio", command= self.choose_folder_get_audio, left=0.4, right=0.6, width=self.width)
        self.folder_get_audio_var.insert(0, self.config['audios_edit_folder'])
        create_button(self.root, text="Bắt đầu chỉnh sửa audio", command=start_thread_edit_audio, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.open_edit_audio_window, width=self.width)
        
    def open_extract_audio_option(self):
        self.reset()
        self.is_extract_audio_option = True
        self.setting_window_size()
        self.show_window()
        self.segment_audio_var = create_frame_label_and_input(self.root, text="Thời gian bắt đầu-kết thúc", width=self.width, left=0.4, right=0.6)
        self.video_get_audio_url = create_frame_label_and_input(self.root, text="Lấy audio từ Link", left=0.4, right=0.6)
        self.audio_edit_path = create_frame_button_and_input(self.root,text="Lấy audio từ file MP3", command= self.choose_audio_edit_file, left=0.4, right=0.6)
        self.video_get_audio_path = create_frame_button_and_input(self.root,text="Lấy audio từ file video", command= self.choose_video_get_audio_path, left=0.4, right=0.6)
        self.folder_get_audio_var = create_frame_button_and_input(self.root,text="Lấy audio từ video trong thư mục", command= self.choose_folder_get_audio, left=0.4, right=0.6)
        self.folder_get_audio_var.insert(0, self.config['download_folder'])
        self.download_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục lưu file", command= self.choose_folder_download, left=0.4, right=0.6, width=self.width)
        create_button(frame=self.root, text="Bắt đầu trích xuất audio", command=self.create_thread_edit_audio, padx=8)
        create_button(self.root, text="Lùi lại", command=self.open_edit_audio_window, width=self.width)

    def choose_folder_download(self):
        folder = choose_folder()
        self.download_folder_var.delete(0, ctk.END)
        self.download_folder_var.insert(0, folder)

    def choose_folder_get_audio(self):
        folder = choose_folder()
        self.folder_get_audio_var.delete(0, ctk.END)
        self.folder_get_audio_var.insert(0, folder)

    def choose_audio_edit_file(self):
        audio_edit_path = choose_file()
        if audio_edit_path:
            self.audio_edit_path.delete(0, ctk.END)
            self.audio_edit_path.insert(0, audio_edit_path)
        else:
            self.noti("Hãy chọn file audio muốn xử lý")

    def chose_account_txt_file(self):
        account_txt_path = choose_file()
        if account_txt_path:
            self.chose_account_txt_file_var.delete(0, ctk.END)
            self.chose_account_txt_file_var.insert(0, account_txt_path)
        else:
            print("Hãy chọn file txt chứa tài khoản cần đăng ký")

    def choose_video_get_audio_path(self):
        video_get_audio_path = choose_file()
        if video_get_audio_path:
            self.video_get_audio_path.delete(0, ctk.END)
            self.video_get_audio_path.insert(0, video_get_audio_path)
        else:
            self.noti("Hãy chọn file video chứa audio muốn xử lý")

    def create_thread_edit_audio(self):
        thread_edit_audio = threading.Thread(target=self.start_edit_audio)
        thread_edit_audio.daemon = True
        thread_edit_audio.start()

    def start_edit_audio(self):
        try:
            download_folder = self.download_folder_var.get()
            if not os.path.exists(download_folder):
                self.noti("hãy chọn thư mục lưu file.")
                return
            video_get_audio_url = self.video_get_audio_url.get()
            audio_edit_path = self.audio_edit_path.get()
            video_get_audio_path = self.video_get_audio_path.get()
            video_folder = self.folder_get_audio_var.get()
            if not video_get_audio_url and not os.path.exists(audio_edit_path) and not os.path.exists(video_get_audio_path) and not os.path.exists(video_folder):
                self.noti("Hãy chọn 1 nguồn lấy audio !!!")
                return
            segment_audio = self.segment_audio_var.get().strip()
            extract_audio_ffmpeg(audio_path=audio_edit_path, video_path=video_get_audio_path, video_url=video_get_audio_url, video_folder=video_folder, segments=segment_audio, download_folder=download_folder)
        except:
            print("Có lỗi trong quá trình trích xuất audio !!!")

#-------------------------------------------edit video-----------------------------------------------------
    def open_edit_video_menu(self):
        self.reset()
        self.is_open_edit_video_menu = True
        self.show_window()
        self.setting_window_size()
        create_button(frame=self.root, text="Thay đổi thông tin video", command=self.open_edit_video_window)
        create_button(self.root, text="Chuyển đổi tỷ lệ video", command=self.convert_videos_window)
        create_button(self.root, text="Cắt video", command=self.open_cut_video_window)
        create_button(self.root, text="Gộp video", command=self.open_combine_video_window)
        create_button(self.root, text="Tăng chất lượng video", command=self.open_increse_video_quality_window)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)
    
    def open_cut_video_window(self):
        self.reset()
        self.is_cut_video_window =True
        self.show_window()
        self.setting_window_size()
        self.segments_var = self.create_settings_input(text="Khoảng thời gian muốn lấy(start-end)", left=0.4, right=0.6)
        self.fast_cut_var = self.create_settings_input(text="Cắt nhanh", values=["Yes", "No"], left=0.4, right=0.6)
        self.fast_cut_var.set(value="No")
        self.get_audio_var = self.create_settings_input(text="Trích xuất MP3", values=["Yes", "No"], left=0.4, right=0.6)
        self.get_audio_var.set(value="No")
        self.choose_is_connect_var = self.create_settings_input(text="Nối các video lại", values=["No", "Connect", "Fast Connect"], left=0.4, right=0.6)
        self.choose_is_connect_var.set(value="No")
        self.videos_edit_path_var = create_frame_button_and_input(self.root, "Chọn video muốn cắt", width=self.width, command=self.choose_videos_edit_file, left=0.4, right=0.6)
        self.videos_edit_folder_var = create_frame_button_and_input(self.root, "Chọn thư mục chứa các video", width=self.width, command=self.choose_videos_edit_folder, left=0.4, right=0.6)
        create_button(self.root, text="Bắt đầu cắt video", command=self.start_thread_cut_video)
        create_button(self.root, text="Lùi lại", command=self.open_edit_video_menu, width=self.width)

    def open_combine_video_window(self):
        self.reset()
        self.is_combine_video_window =True
        self.show_window()
        self.setting_window_size()
        self.file_name_var = create_frame_label_and_input(self.root, "Đặt tên file sau khi gộp", width=self.width, left=0.4, right=0.6)
        self.fast_combine_var = self.create_settings_input(text="Gộp nhanh", values=["Yes", "No"], left=0.4, right=0.6)
        self.fast_combine_var.set('Yes')
        self.videos_edit_folder_var = create_frame_button_and_input(self.root, "Chọn thư mục chứa video", command=self.choose_videos_edit_folder, width=self.width, left=0.4, right=0.6)
        self.videos_edit_folder_var.insert(0, self.config['videos_edit_folder'])
        create_button(self.root, text="Bắt đầu gộp", command=self.create_thread_combine_video)
        create_button(self.root, text="Lùi lại", command=self.open_edit_video_menu, width=self.width)
    
    def open_combine_audio_window(self):
        self.reset()
        self.is_combine_video_window =True
        self.show_window()
        self.setting_window_size()
        self.file_name_var = create_frame_label_and_input(self.root, "Đặt tên file sau khi gộp", width=self.width, left=0.4, right=0.6)
        self.fast_combine_var = self.create_settings_input(text="Gộp nhanh", values=["Yes", "No"], left=0.4, right=0.6)
        self.fast_combine_var.set('Yes')
        self.videos_edit_folder_var = create_frame_button_and_input(self.root, "Chọn thư mục chứa audio", command=self.choose_videos_edit_folder, width=self.width, left=0.4, right=0.6)
        self.videos_edit_folder_var.insert(0, self.config['videos_edit_folder'])
        create_button(self.root, text="Bắt đầu gộp", command=self.create_thread_combine_audio)
        create_button(self.root, text="Lùi lại", command=self.open_edit_audio_window, width=self.width)

    def open_increse_video_quality_window(self):
        self.reset()
        self.is_increse_video_quality_window =True
        self.show_window()
        self.setting_window_size()
        self.videos_edit_folder_var = create_frame_button_and_input(self.root, "Chọn thư mục chứa video", command=self.choose_videos_edit_folder, width=self.width, left=0.4, right=0.6)
        self.videos_edit_folder_var.insert(0, self.config['videos_edit_folder'])
        create_button(self.root, text="Bắt đầu tăng chất lượng video", command=self.create_thread_increse_video_quality)
        create_button(self.root, text="Lùi lại", command=self.open_edit_video_menu, width=self.width)

    def convert_videos_window(self):
        self.reset()
        self.is_convert_video_window = True
        self.show_window()
        self.setting_window_size()
        self.choose_convert_type = self.create_settings_input(text="Chọn tỷ lệ muốn chuyển đổi", config_key="convert_type", values=["16:9 to 9:16", "9:16 to 16:9"])
        self.choose_convert_type.set("16:9 to 9:16")
        self.choose_zoom_size = self.create_settings_input(text="Zoom video(16:9 to 9:16)")
        self.videos_edit_folder_var = create_frame_button_and_input(self.root, "Chọn thư mục chứa video", width=self.width, command=self.choose_videos_edit_folder, left=0.4, right=0.6)
        self.videos_edit_folder_var.insert(0, self.config['videos_edit_folder'])
        create_button(self.root, text="Bắt đầu chuyển đổi", width=self.width, command=self.start_convert_video)
        create_button(self.root, text="Lùi lại", command=self.open_edit_video_menu, width=self.width)
    

    def start_convert_video(self):
        convert_type = self.choose_convert_type.get()
        if convert_type == "16:9 to 9:16":
            self.is_169_to_916 = True
        elif convert_type == "9:16 to 16:9":
            self.is_169_to_916 = False
        else:
            self.noti("Hãy chọn tỷ lệ chuyển đổi cho phù hợp!")
            return
        self.start_thread_edit_video()

    def start_thread_edit_video(self):
        if not self.edit_thread or not self.edit_thread.is_alive():
            self.is_stop_edit = False
            self.edit_thread = threading.Thread(target=self.convert_videos)
            self.edit_thread.start()

    def start_thread_cut_video(self):
        if not self.edit_thread or not self.edit_thread.is_alive():
            self.is_stop_edit = False
            self.edit_thread = threading.Thread(target=self.cut_videos_by_timeline)
            self.edit_thread.start()

    def cut_videos_by_timeline(self):
        segments = self.segments_var.get()
        is_connect = self.choose_is_connect_var.get().lower()
        fast_cut = self.fast_cut_var.get() == 'Yes'
        get_audio = self.get_audio_var.get() == 'Yes'
        if not segments:
            self.noti("Hãy nhập các khoảng thời gian muốn cắt, ví dụ: 05:50,60:90,...")
            return
    
        video_path = self.videos_edit_path_var.get()
        if os.path.exists(video_path):
            is_edit_ok, message = cut_video_by_timeline_use_ffmpeg(video_path, segments=segments, is_connect=is_connect, fast_cut=fast_cut, get_audio=get_audio)
            if is_edit_ok:
                self.noti(f"--> Xử lý thành công video: {video_path}")
            else:
                self.noti(message)
        else:
            videos_folder = self.videos_edit_folder_var.get()
            edit_videos = get_file_in_folder_by_type(videos_folder, ".mp4")
            if not edit_videos:
                return
            cnt = 0
            for i, video_file in enumerate(edit_videos):
                if self.is_stop_edit:
                    return
                video_path = f'{videos_folder}\\{video_file}'
                is_edit_ok, message = cut_video_by_timeline_use_ffmpeg(video_path, segments=segments, is_connect=is_connect, fast_cut=fast_cut, get_audio=get_audio)
                if is_edit_ok:
                    print(f"--> Xử lý thành công video: {video_path}")
                    cnt += 1
                else:
                    print(message)
            self.noti(f"Xử lý thành công {cnt} video")

    def combine_video_by_ffmpeg(self):
        videos_folder = self.videos_edit_folder_var.get()
        file_name = self.file_name_var.get()
        fast_combine = self.fast_combine_var.get() == 'Yes'
        if not check_folder(videos_folder):
            return
        try:
            is_ok, message = merge_videos_use_ffmpeg(videos_folder, file_name, is_delete=self.config['is_delete_video'], fast_combine=fast_combine)
            self.noti(message)
        except:
            getlog()
            print(f"Có lỗi trong quá trình gộp video. Đang dùng cách khác để gộp video.")
            self.combine_video_by_moviepy()

    def combine_audio_by_ffmpeg(self):
        videos_folder = self.videos_edit_folder_var.get()
        file_name = self.file_name_var.get()
        fast_combine = self.fast_combine_var.get() == 'Yes'
        if not check_folder(videos_folder):
            return
        try:
            is_ok, message = merge_audio_use_ffmpeg(videos_folder, file_name, fast_combine=fast_combine)
            self.noti(message)
        except:
            print(f"Có lỗi trong quá trình gộp audio !!!")

    def combine_video_by_moviepy(self):
        videos_folder = self.videos_edit_folder_var.get()
        if not check_folder(videos_folder):
            return
        try:
            output_folder = f'{videos_folder}\\merge_videos'
            os.makedirs(output_folder, exist_ok=True)
            edit_videos = get_file_in_folder_by_type(videos_folder)
            if not edit_videos:
                return
            if len(edit_videos) <= 1:
                warning_message("Phải có ít nhất 2 video trong videos folder")
                return
            clips = []
            remove_videos = []
            for i, video_file in enumerate(edit_videos):
                if self.is_stop_edit:
                    return
                video_path = f'{videos_folder}\\{video_file}'
                remove_videos.append(video_path)
                clip = VideoFileClip(video_path)
                clips.append(clip)

            if len(clips) > 0:
                final_clip = concatenate_videoclips(clips, method="compose")
                file_path = f"{output_folder}\\combine_video.mp4"
                final_clip.write_videofile(file_path, codec='libx264')
                final_clip.close()
                for clip in clips:
                    clip.close()
            try:
                for video_path in remove_videos:
                    remove_or_move_file(video_path, is_delete=self.config['is_delete_video'])
            except:
                getlog()
            self.noti(f"Gộp thành công {len(edit_videos)} vào file: {file_path}")
        except Exception as e:
            getlog()
            print(f"Có lỗi trong quá trình gộp video")

    def increse_video_quality_by_ffmpeg(self):
        try:
            videos_folder = self.videos_edit_folder_var.get()
            edit_videos = get_file_in_folder_by_type(videos_folder, ".mp4")
            if not edit_videos:
                return
            output_folder = f'{videos_folder}\\increse_videos_quality'
            os.makedirs(output_folder, exist_ok=True)
            for i, video_file in enumerate(edit_videos):
                if self.is_stop_edit:
                    return
                video_path = f'{videos_folder}\\{video_file}'
                outpath_video = os.path.join(output_folder, video_file)
                if increase_video_quality(video_path, outpath_video):
                    remove_or_move_file(video_path, is_delete=self.config['is_delete_video'])
        except:
            getlog()

    def convert_videos(self):
        try:
            zoom_size = self.choose_zoom_size.get()
            videos_folder = self.videos_edit_folder_var.get()
            if not check_folder(videos_folder):
                return
            self.config['videos_edit_folder'] = videos_folder
            self.save_config()
            edit_videos = os.listdir(videos_folder)
            edit_videos = [k for k in edit_videos if k.endswith('.mp4')]
            if len(edit_videos) == 0:
                self.noti(f"Không tìm thấy video trong thư mục {videos_folder}")
                return
            list_edit_finished = []
            for i, video_file in enumerate(edit_videos):
                if self.is_stop_edit:
                    return
                video_path = f'{videos_folder}\\{video_file}'
                if self.is_169_to_916:
                    is_edit_ok = convert_video_169_to_916(video_path, zoom_size=zoom_size, is_delete=self.config['is_delete_video'])
                else:
                    is_edit_ok = convert_video_916_to_169(video_path, is_delete=self.config['is_delete_video'])
                if is_edit_ok:
                    list_edit_finished.append(video_file)
            cnt = len(list_edit_finished)
            if cnt > 0:
                self.noti(f"Xử lý thành công {cnt} video: {list_edit_finished}")
        except:
            getlog()

    def open_edit_video_window(self):
        self.reset()
        self.is_edit_video_window = True
        self.setting_window_size()
        self.show_window()
        self.end_cut_var, self.first_cut_var = create_frame_label_input_input(self.root, text="Cắt ở đầu/cuối video (s)", width=self.width, left=0.4, mid=0.28, right=0.32)
        self.first_cut_var.insert(0, self.config['first_cut'])
        self.end_cut_var.insert(0, self.config['end_cut'])
        self.flip_video_var = self.create_settings_input("Lật ngang video", "flip_video", values=["Yes", "No"])
        self.speed_up_var = self.create_settings_input("Tăng tốc", "speed_up", values=["0.8", "0.9", "1", "1.1", "1.2"])
        self.max_zoom_size_var = self.create_settings_input("Tỷ lệ Zoom", "max_zoom_size", values=["1", "1.1", "1.2", "1.3", "1.4"])
        self.horizontal_position_var = self.create_settings_input("Vị trí zoom theo chiều ngang", "horizontal_position", values=["left", "center", "right"])
        self.vertical_position_var = self.create_settings_input("Vị trí zoom theo chiều dọc", "vertical_position", values=["top", "center", "bottom"])
        self.top_bot_overlay_var = self.create_settings_input("Lớp phủ trên, dưới(vd: 10,10,black,100)", "top_bot_overlay", values=["10,10,black,100", "10,10,white,100", "10,10,red,100", "10,10,green,100", "10,10,blue,100", "10,10,yellow,100", "10,10,gray,100", "10,10,orange,100", "10,10,purple,100", "10,10,pink,100"])
        self.left_right_overlay_var = self.create_settings_input("Lớp phủ trái, phải(vd: 10,10,black,100)", "left_right_overlay", values=["10,10,black,100", "10,10,white,100", "10,10,red,100", "10,10,green,100", "10,10,blue,100", "10,10,yellow,100", "10,10,gray,100", "10,10,orange,100", "10,10,purple,100", "10,10,pink,100"])
        self.is_delete_original_audio_var = self.create_settings_input("Xóa audio gốc", "is_delete_original_audio", values=["Yes", "No"])
        self.background_music_path, self.background_music_volume_var = create_frame_button_input_input(self.root,text="Chọn thư mục chứa nhạc nền", width=self.width, command= self.choose_background_music_folder, place_holder1="Đường dẫn thư mục chứa file mp3", place_holder2="âm lượng")
        self.background_music_path.insert(0, self.config['background_music_path'])
        self.background_music_volume_var.insert(0, self.config['background_music_volume'])
        self.pitch_factor_var = self.create_settings_input("Điều chỉnh cao độ audio", "pitch_factor", values=['-0.8','1','1.2'], left=0.4, right=0.6)
        self.water_path_var = create_frame_button_and_input(self.root,text="Chọn ảnh Watermark", width=self.width, command= self.choose_water_mask_image, left=0.4, right=0.6)
        self.vertical_watermark_position_var, self.horizontal_watermark_position_var = create_frame_label_input_input(self.root, "Vị trí Watermark (ngang - dọc)", place_holder1="nhập vị trí chiều ngang", place_holder2="Nhập vị trí chiều dọc", width=self.width, left=0.4, mid=0.28, right=0.32)
        self.horizontal_watermark_position_var.insert(0, self.config['horizontal_watermark_position'])
        self.vertical_watermark_position_var.insert(0, self.config['vertical_watermark_position'])
        self.watermark_scale_var = self.create_settings_input("Chỉnh kích thước Watermark (ngang - dọc)", config_key='watermark_scale')
        self.edit_level_2_var = self.create_settings_input("Thêm nhiễu - Gợn sóng", 'edit_level_2', values=["Yes", "No"], left=0.4, right=0.6)
        if not self.edit_level_2_var.get().strip():
            self.edit_level_2_var.set('Yes')
        self.top_text_var, self.bot_text_var = create_frame_label_input_input(self.root, text="Chữ ở đầu/cuối video", place_holder1='bot text,0.9,1', place_holder2='top text,0.1,1.2', width=self.width, left=0.4, mid=0.28, right=0.32)
        self.top_text_var.insert(0, self.config['top_text'])
        self.bot_text_var.insert(0, self.config['bot_text'])
        self.videos_edit_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục chứa video", command= self.choose_videos_edit_folder, left=0.4, right=0.6, width=self.width)
        self.water_path_var.insert(0, self.config['water_path'])
        self.videos_edit_folder_var.insert(0, self.config['videos_edit_folder'])
        create_button(self.root, text="Xử lý video", command=self.create_thread_edit_video, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.open_edit_video_menu, width=self.width)


    def create_thread_edit_video(self):
        if not self.edit_thread or not self.edit_thread.is_alive():
            self.is_stop_edit = False
            self.edit_thread = threading.Thread(target=self.start_edit_video)
            self.edit_thread.start()

    def create_thread_combine_video(self):
        if not self.edit_thread or not self.edit_thread.is_alive():
            self.edit_thread = threading.Thread(target=self.combine_video_by_ffmpeg)
            self.edit_thread.start()
    def create_thread_combine_audio(self):
        if not self.edit_audio_thread or not self.edit_audio_thread.is_alive():
            self.edit_audio_thread = threading.Thread(target=self.combine_audio_by_ffmpeg)
            self.edit_audio_thread.start()
    def create_thread_increse_video_quality(self):
        if not self.edit_thread or not self.edit_thread.is_alive():
            self.edit_thread = threading.Thread(target=self.increse_video_quality_by_ffmpeg)
            self.edit_thread.start()

    def start_edit_video(self):
        def save_edit_setting():
            self.config['videos_edit_folder'] = self.videos_edit_folder_var.get()
            self.config['is_delete_original_audio'] = self.is_delete_original_audio_var.get() == "Yes"
            self.config['background_music_path'] = self.background_music_path.get()
            self.config['background_music_volume'] = self.background_music_volume_var.get()
            self.config['first_cut'] = self.first_cut_var.get()
            self.config['pitch_factor'] = self.pitch_factor_var.get() or "1"
            self.config['end_cut'] = self.end_cut_var.get()
            self.config['flip_video'] = self.flip_video_var.get() == "Yes"
            self.config['speed_up'] = self.speed_up_var.get()
            self.config['max_zoom_size'] = self.max_zoom_size_var.get()
            self.config['vertical_position'] = self.vertical_position_var.get()
            self.config['horizontal_position'] = self.horizontal_position_var.get()
            self.config['water_path'] = self.water_path_var.get()
            self.config['vertical_watermark_position'] = self.vertical_watermark_position_var.get()
            self.config['edit_level_2'] = self.edit_level_2_var.get() == 'Yes'
            self.config['top_text'] = self.top_text_var.get().strip().upper()
            self.config['bot_text'] = self.bot_text_var.get().strip().upper()
            self.config['horizontal_watermark_position'] = self.horizontal_watermark_position_var.get()
            self.config['watermark_scale'] = self.watermark_scale_var.get()
            if not self.config['watermark_scale']:
                self.config['watermark_scale'] = "1,1"
            self.config['top_bot_overlay'] = self.top_bot_overlay_var.get()
            self.config['left_right_overlay'] = self.left_right_overlay_var.get()
            if not self.config['videos_edit_folder']:
                self.noti("Hãy chọn thư mục lưu video.")
                return
            try:
                if not self.config['max_zoom_size'] or float(self.config['max_zoom_size']) <= 1:
                    self.config['max_zoom_size'] = "1.01"
            except:
                self.config['max_zoom_size'] = "1.01"
            self.save_config()
        save_edit_setting()
        videos_folder = self.config['videos_edit_folder']
        list_edit_finished = []
        edit_videos = get_file_in_folder_by_type(videos_folder, ".mp4")
        if not edit_videos:
            return
        
        for i, video_file in enumerate(edit_videos):
            if self.is_stop_edit:
                return
            if '.mp4' not in video_file:
                continue
            print(f'Bắt đầu xử lý video: {video_file}')
            video_path = f'{videos_folder}\\{video_file}'
            output_video_path = self.fast_edit_video(video_path)
            if not output_video_path:
                print(f'{thatbai} Chỉnh sửa video {video_file} thất bại!!!')
                continue
            if self.config['edit_level_2']:
                print(f'\nXử lý thêm hiệu ứng, viền, chữ vào video...')
                temp_video = process_video(
                            output_video_path,
                            wave_amplitude=1.2,    # Biên độ gợn sóng (càng cao, sóng càng mạnh)
                            wave_frequency=0.1, # Tần suất gợn sóng
                            line_spacing=10,     # Khoảng cách giữa các đường gạch ngang
                            line_thickness=1,    # Độ dày của đường gạch ngang
                            line_opacity=0.1,     # Độ mờ của đường gạch ngang (0.0 - 1.0)
                            text_top_input=self.config['top_text'],
                            text_bottom_input=self.config['bot_text']
                        )
                if temp_video:
                    merge_audio(temp_video, output_video_path)
                    remove_file(temp_video)

        cnt = len(list_edit_finished)
        if cnt > 0:
            self.noti(f"Chỉnh sửa thành công {cnt} video")

    def get_overlay_demention(self, demention_str="0,0,black,100"):
        try:
            top_bot = demention_str.split(',')
            if len(top_bot) == 4:
                top_overlay, bot_overlay, color, transparent = top_bot
            elif len(top_bot) == 2:
                top_overlay, bot_overlay = top_bot
            else:
                print(f'Thiết lập lớp phủ chưa đúng định dạng(phủ trên,phủ dưới, màu sắc, độ trong suốt)\nVí dụ: 10,10 hoặc 10,10,black,50')
                return False
            try:
                top_overlay = int(top_overlay.strip())
            except:
                top_overlay = 5
            try:
                bot_overlay = int(bot_overlay.strip())
            except:
                bot_overlay = 5
                
            transparent = float(transparent.strip()) / 100 if transparent.strip().isdigit else 1
        except:
            pass
        return top_overlay, bot_overlay, color, transparent

    def fast_edit_video(self, input_video_path, upload_folder=None):
        speed_up = self.config.get('speed_up', '1')
        if not speed_up:
            speed_up = '1'
        first_cut = self.config.get('first_cut', '0')
        end_cut = self.config.get('end_cut', '0')
        zoom_size = self.config.get('max_zoom_size', '1')
        horizontal_position = self.config.get('horizontal_position', 'center')
        vertical_position = self.config.get('vertical_position', 'center')
        watermark = self.config.get('water_path', None)
        horizontal_watermark_position = self.config.get('horizontal_watermark_position', 'center')
        vertical_watermark_position = self.config.get('vertical_watermark_position', 'center')
        watermark_scale = self.config.get('watermark_scale', '1,1')
        flip_horizontal = self.config.get('flip_video', False)
        top_bot_overlay = self.config.get('top_bot_overlay', '2,2,black,100')
        left_right_overlay = self.config.get('left_right_overlay', '2,2,black,100')
        pitch_factor = self.config.get('pitch_factor', "1")
        try:
            pitch = float(pitch_factor)
        except:
            pitch = 1
        new_audio_folder = self.config.get('background_music_path', None)
        new_audio_path = None
        if new_audio_folder and os.path.exists(new_audio_folder):
            new_audio_path = get_random_audio_path(new_audio_folder)
            if not new_audio_path or not os.path.exists(new_audio_path):
                print(f"Không có file .mp3 nào trong thư mục {new_audio_folder}")
                return None
        background_music_volume = self.config.get('background_music_volume', '100')
        remove_original_audio = self.config.get('is_delete_original_audio', False)
        try:
            audio_volume = int(background_music_volume)/100
        except:
            audio_volume = 1.0

        top_overlay, bot_overlay, color_top_bot, transparent_t_b = self.get_overlay_demention(top_bot_overlay)
        left_overlay, right_overlay, color_left_right, transparent_l_r = self.get_overlay_demention(left_right_overlay)

        try:
            output_folder, file_name = get_output_folder(input_video_path, output_folder_name='edited_videos')
            if self.new_name:
                if '<index>' not in self.new_name:
                    self.new_name = f"{self.new_name} <index>"
                file_name = self.new_name.replace("<index>", str(self.index))
                self.index += 1
            else:
                file_name = file_name.split('.mp4')[0]

            output_file = os.path.join(output_folder, f"{file_name}.mp4")
            video_info = get_video_info(input_video_path)
            if not video_info:
                print(f"Không lấy được thông tin từ video {input_video_path}, hãy đảm bảo rằng video không bị hỏng.")
                return None
            video_width = video_info['width']
            video_height = video_info['height']
            video_duration = float(video_info.get('duration', None))
            if not video_duration:
                print(f'Không lấy được thời lượng video!')
                return None
            video_fps = 30 if video_info['fps'] == 25 or video_info['fps'] == 24 else 25
            
            if speed_up:
                try:
                    speed_up = float(speed_up)
                except:
                    speed_up = 1.01
            duration = video_duration/speed_up

            first_cut = convert_time_to_seconds(first_cut)/speed_up
            end_cut = convert_time_to_seconds(end_cut)/speed_up
            if not end_cut or end_cut >= duration:
                end_cut = 0
            if not first_cut or first_cut >= duration - end_cut:
                first_cut = 0
            end_cut = duration - end_cut

            if watermark:
                if os.path.isfile(watermark):
                    watermark_x, watermark_y = add_watermark_by_ffmpeg(video_width, video_height, horizontal_watermark_position, vertical_watermark_position)
                    if watermark_x is None or watermark_y is None:
                        print("Có lỗi trong khi lấy vị trí watermark. Hãy đảm bảo thông số đầu vào chính xác!")
                        return None
                else:
                    print("Đường dẫn watermark không hợp lệ")
                    return None

            if zoom_size:
                try:
                    zoom_size = float(zoom_size)
                except:
                    zoom_size = 1

            if horizontal_position == 'center':
                zoom_x = int(video_width * (1 - 1 / zoom_size) / 2)
            elif horizontal_position == 'left':
                zoom_x = 0
            elif horizontal_position == 'right':
                zoom_x = int(video_width * (1 - 1 / zoom_size))
            else:
                try:
                    zoom_x = int(video_width * horizontal_position / 100)
                except:
                    print("Vị trí zoom theo chiều ngang không hợp lệ. Lấy mặc định zoom từ trung tâm")
                    zoom_x = int(video_width * (1 - 1 / zoom_size) / 2)

            if vertical_position == 'center':
                zoom_y = int(video_height * (1 - 1 / zoom_size) / 2)
            elif vertical_position == 'top':
                zoom_y = 0
            elif vertical_position == 'bottom':
                zoom_y = int(video_height * (1 - 1 / zoom_size))
            else:
                try:
                    zoom_y = int(video_height * vertical_position / 100)
                except:
                    print("Vị trí zoom theo chiều dọc không hợp lệ. Lấy mặc định zoom từ trung tâm")
                    zoom_y = int(video_height * (1 - 1 / zoom_size) / 2)

            flip_filter = ''
            if flip_horizontal:
                flip_filter += ',hflip'

            top_black_bar = f"drawbox=x=0:y=0:w=iw:h={top_overlay}:color={color_top_bot}@{transparent_t_b}:t=fill"
            bottom_black_bar = f"drawbox=x=0:y=ih-{bot_overlay}:w=iw:h={bot_overlay}:color={color_top_bot}@{transparent_t_b}:t=fill"
            left_black_bar = f"drawbox=x=0:y=0:w={left_overlay}:h=ih:color={color_left_right}@{transparent_l_r}:t=fill"
            right_black_bar = f"drawbox=x=iw-{right_overlay}:y=0:w={right_overlay}:h=ih:color={color_left_right}@{transparent_l_r}:t=fill"

            zoom_filter = f"scale=iw*{zoom_size*1.04}:ih*{zoom_size*0.96},crop={int(video_width*0.998)}:{int(video_height*0.999)}:{zoom_x}:{zoom_y}{flip_filter}"

            if watermark:
                try:
                    watermark_scale = watermark_scale.split(',')
                    scale_w = float(watermark_scale[0])
                    scale_h = float(watermark_scale[1])
                except:
                    scale_w = 1
                    scale_h = 1
                watermark_filter = f"[0:v]{zoom_filter},{left_black_bar},{right_black_bar},{top_black_bar},{bottom_black_bar},setpts=PTS/{speed_up}[v];[1:v]scale=iw*{scale_w}:ih*{scale_h},format=yuva420p[wm];[v][wm]overlay={watermark_x}:{watermark_y}[video]"
            else:
                watermark_filter = f"[0:v]{zoom_filter},{left_black_bar},{right_black_bar},{top_black_bar},{bottom_black_bar},setpts=PTS/{speed_up}[video]"
            combined_audio_path = os.path.join(output_folder, "combined_audio.wav")
            temp_audio_path = os.path.join(output_folder, "new_combined_audio.wav")
            if new_audio_path:
                audio_duration_info = get_audio_info(new_audio_path)
                audio_duration = float(audio_duration_info.get('duration', 0))
                if audio_duration < video_duration:
                    repeat_count = int(video_duration / audio_duration) + 1
                    loop_audio_command = [ 'ffmpeg', '-loglevel', 'quiet', '-stream_loop', str(repeat_count - 1), '-i', new_audio_path, '-t', str(video_duration), '-y', temp_audio_path ]
                    if not run_command_ffmpeg(loop_audio_command):
                        return None
                    new_audio_path = temp_audio_path
                combine_audio_command = [
                    'ffmpeg', '-loglevel', 'quiet', '-i', input_video_path, '-i', new_audio_path,
                    '-filter_complex', f'[0:a]volume=1[a1];[1:a]volume={audio_volume}[a2];[a1][a2]amerge=inputs=2[a]',
                    '-map', '[a]', '-ac', '2', '-y', combined_audio_path
                ]
                run_command_ffmpeg(combine_audio_command)

            command = [ 'ffmpeg', '-loglevel', 'quiet', '-progress', 'pipe:1', ]
            if first_cut > 0:
                command.extend(['-ss', str(first_cut)])
            command.extend(['-i', input_video_path])
            if watermark:
                command.extend(['-i', watermark])
            audio_index = 1
            if new_audio_path:
                if remove_original_audio:
                    command.extend(['-i', new_audio_path])
                else:
                    command.extend(['-i', combined_audio_path]) 
            if watermark and new_audio_path:
                audio_index = 2

            command.extend(['-filter_complex', watermark_filter])
            if new_audio_path:
                if remove_original_audio:
                    command.extend([ '-map', '[video]', f'-map', f'{audio_index}:a', '-filter:a:0', f'volume={audio_volume}', ])
                else:
                    command.extend([ '-map', '[video]', f'-map', f'{audio_index}:a', '-filter:a:0', f'volume=1,atempo={speed_up},rubberband=pitch={pitch}', ])
            elif not remove_original_audio:
                command.extend([ '-map', '[video]', '-map', '0:a', '-filter:a', f'volume=1,atempo={speed_up},rubberband=pitch={pitch}', ])
            else:
                command.extend([ '-map', '[video]', '-an' ])
            command.extend([ '-vcodec', 'libx264', '-acodec', 'aac', '-r', str(video_fps), '-y', ])
            if end_cut is not None:
                duration = end_cut - first_cut
                command.extend(['-to', str(duration)])
            command.append(output_file)
            if not run_command_with_progress(command, duration):
                if not run_command_ffmpeg(command):
                    print(f"Video lỗi !!!")
                    return None

            if upload_folder:
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder, exist_ok=True)
                new_file_path = os.path.join(upload_folder, f"{file_name}.mp4")
                shutil.move(output_file, new_file_path)
            remove_file(combined_audio_path)
            remove_file(temp_audio_path)
            remove_or_move_file(input_video_path, is_delete=self.config['is_delete_video'], finish_folder_name='Finished Edit')
            return output_file
        except:
            print(f"Có lỗi trong quá trình xử lý video {input_video_path}")
            getlog()
            return None


    def edit_video_by_moviepy(self, input_video_path):
        def adjust_audio_pitch(input_audio_path):
            output_audio_path = os.path.join(current_dir, 'adjust_audio.mp3')
            try:
                pitch_factor = float(self.config.get('pitch_factor', "1.0"))
            except:
                pitch_factor = 1.0
            if pitch_factor == 1.0:
                return input_audio_path
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")  # Tạo file tạm
            output_audio_path = temp_file.name

            try:
                cmd = [ 'ffmpeg', '-i', input_audio_path, '-filter:a', f'volume=1,atempo=1,rubberband=pitch={pitch_factor}', '-y', output_audio_path ]
                run_command_ffmpeg(cmd, hide=False)
                return output_audio_path
            except:
                getlog()
                temp_file.close()
                raise
        
        try:
            new_audio_folder = self.config.get('background_music_path', None)
            new_audio_path = None
            if new_audio_folder and os.path.exists(new_audio_folder):
                new_audio_path = get_random_audio_path(new_audio_folder)
                if not os.path.exists(new_audio_path):
                    print(f"Không có file .mp3 nào trong thư mục {new_audio_folder}")
                    return
            output_folder, file_name = get_output_folder(input_video_path, output_folder_name='edited_videos')
            file_name = file_name.split('.mp4')[0]
            output_file = os.path.join(output_folder, f"{file_name}.mp4")
            
            input_clip = VideoFileClip(input_video_path)
            resized_clip = resize_clip(input_clip)
            if not resized_clip:
                resized_clip = input_clip
            if self.config['flip_video']:
                f_clip = flip_clip(resized_clip)
            else:
                f_clip = resized_clip
            video_clip = strip_first_and_end_video(f_clip, first_cut=self.config['first_cut'], end_cut=self.config['end_cut'])
            if not video_clip:
                return

            temp_audio_path = os.path.join(current_dir, "temp_audio.mp3")
            if new_audio_path:
                final_audio_path = adjust_audio_pitch(new_audio_path)
                volumn = self.config['background_music_volume']
            else:
                volumn = '100'
                original_audio = video_clip.audio
                if original_audio:
                    original_audio.write_audiofile(temp_audio_path)
                    final_audio_path = adjust_audio_pitch(temp_audio_path)
                else:
                    final_audio_path = None

            video_clip = remove_audio_from_clip(video_clip)

            if final_audio_path and os.path.exists(final_audio_path):
                add_audio_clip = set_audio_for_clip(video_clip, final_audio_path, volumn)
            else:
                add_audio_clip = video_clip


            speed_clip = speed_up_clip(add_audio_clip, speed=self.config['speed_up'])
            if self.config['is_random_zoom']:
                zoom_clip = zoom_video_random_intervals(clip=speed_clip, max_zoom_size=self.config['max_zoom_size'], vertical_position=self.config['vertical_position'], horizontal_position=self.config['horizontal_position'], is_random_zoom=self.config['is_random_zoom'])
            else:
                zoom_clip = apply_zoom(clip=speed_clip, zoom_factor=self.config['max_zoom_size'], vertical_position=self.config['vertical_position'], horizontal_position=self.config['horizontal_position'])
            if not zoom_clip:
                return
            water_clip = add_image_watermark_into_video(zoom_clip, top_bot_overlay_height=self.config['top_bot_overlay'], left_right_overlay_width=self.config['left_right_overlay'], watermark=self.config['water_path'], vertical_watermark_position=self.config['vertical_watermark_position'], horizontal_watermark_position=self.config['horizontal_watermark_position'], watermark_scale=self.config['watermark_scale'])
            if self.is_stop_edit:
                water_clip.close()
                input_clip.close()
                return

            water_clip.write_videofile(output_file, codec='libx264', threads=4, fps=input_clip.fps + 1)
            water_clip.close()
            input_clip.close()
            sleep(1)
            if os.path.exists(temp_audio_path):
                remove_file(temp_audio_path)
            remove_or_move_file(input_video_path, is_delete=self.config['is_delete_video'])
            return True
        except:
            getlog()
            return False
    
#---------------------------Các Hàm gọi chung co class----------------------------------
    def load_download_info(self):
        self.download_info = get_json_data(download_info_path)
        if not self.download_info:
            self.download_info = {}
        if 'downloaded_urls' not in self.download_info:
            self.download_info['downloaded_urls'] = []
        save_to_json_file(self.download_info, download_info_path)


    def open_common_settings(self):
        def save_common_config():
            self.config["auto_start"] = self.auto_start_var.get() == "Yes"
            self.config["time_check_status_video"] = self.time_check_status_video_var.get()
            self.config["is_delete_video"] = self.is_delete_video_var.get() == "Yes"
            self.save_config()
            self.get_start_window()
        self.reset()
        self.is_open_common_setting = True
        self.show_window()
        self.setting_window_size()
        self.auto_start_var = self.create_settings_input("Khởi động ứng dụng cùng window", "auto_start", values=["Yes", "No"], left=0.4, right=0.6)
        self.time_check_status_video_var = self.create_settings_input("Khoảng cách mỗi lần kiểm tra trạng thái video (phút)", "time_check_status_video", values=["0", "60"], left=0.4, right=0.6)
        self.is_delete_video_var = self.create_settings_input("Xóa video gốc sau chỉnh sửa", "is_delete_video", values=["Yes", "No"], left=0.4, right=0.6)
        create_button(self.root, text="Lưu cài đặt", command=save_common_config, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.get_start_window, width=self.width)
        

    def choose_background_music_folder(self):
        background_music_folder = choose_folder()
        self.background_music_path.delete(0, ctk.END)
        self.background_music_path.insert(0, background_music_folder)

    def choose_videos_edit_folder(self):
        videos_edit_folder = filedialog.askdirectory()
        if self.videos_edit_folder_var:
            self.videos_edit_folder_var.delete(0, ctk.END)
            self.videos_edit_folder_var.insert(0, videos_edit_folder)

    def choose_videos_edit_file(self):
        videos_edit_path = choose_file()
        self.videos_edit_path_var.delete(0, ctk.END)
        self.videos_edit_path_var.insert(0, videos_edit_path)

    def choose_water_mask_image(self):
        water_mask_image = filedialog.askopenfilename()
        self.water_path_var.delete(0, ctk.END)
        self.water_path_var.insert(0, water_mask_image)

#------------------------------------------------------Common-----------------------------------------------------
    def create_settings_input(self, text, config_key=None, values=None, is_textbox = False, left=0.4, right=0.6, add_button=False, command=None, text_btn=None):
        frame = create_frame(self.root)
        if add_button:
            create_button(frame= frame, text=text_btn, command=command, width=0.2, side=RIGHT)
        create_label(frame, text=text, side=LEFT, width=self.width*left, anchor='w')

        if values:
            if not config_key:
                val = ""
            elif config_key not in self.config:
                val = ""
            else:
                val = self.config[config_key]
                if self.config[config_key] == True:
                    val = "Yes"
                elif self.config[config_key] == False:
                    val = "No"
            var = ctk.StringVar(value=str(val))

            combobox = ctk.CTkComboBox(frame, values=values, variable=var, width=self.width*right)
            combobox.pack(side="right", padx=padx)
            if config_key == "category_id":
                combobox.set(val[0])
            setattr(self, f"{config_key}_var", var)
            result = combobox
        elif is_textbox:
            textbox = ctk.CTkTextbox(frame, height=120, width=self.width*right)
            textbox.insert("1.0", self.config[config_key])
            textbox.pack(side=RIGHT, padx=padx)
            result = textbox
        else:
            if config_key:
                var = self.config[config_key]
            else:
                var = ""
            entry = ctk.CTkEntry(frame, width=self.width*right)
            entry.pack(side="right", padx=padx)
            entry.insert(0, var)
            setattr(self, f"{config_key}_var", var)
            result = entry
        return result
    
    def reset(self):
        self.is_start_window = False
        self.is_youtube_window = False
        self.is_tiktok_window = False
        self.is_interact_setting_window = False
        self.is_auto_upload_tiktok_window = False
        self.is_facebook_window= False
        self.is_edit_video_window= False
        self.is_edit_video_window= False
        self.is_add_new_channel= False
        self.is_remove_channel= False
        self.is_sign_up_facebook = False
        self.is_sign_up_tiktok = False
        self.is_convert_video_window = False
        self.is_open_common_setting = False
        self.is_open_edit_video_menu = False
        self.is_cut_video_window = False
        self.is_text_to_mp3_window = False
        self.is_combine_video_window = False
        self.is_increse_video_quality_window = False
        self.is_rename_file_by_index_window = False
        self.is_remove_char_in_file_name_window = False
        self.is_open_change_mac_addres_window = False
        self.is_extract_image_from_video_window = False
        self.is_other_window = False
        self.is_other_download_window = False
        self.is_download_douyin_video_window = False
        self.is_edit_audio_window = False
        self.is_edit_audio_option = False
        self.is_extract_audio_option = False
        self.is_open_auto_process_window = False
        self.clear_after_action()
        clear_widgets(self.root)
        self.videos_edit_folder_var = None
        self.file_name_var = None
        self.index_file_name_var = None

    def clear_after_action(self):
        self.root.withdraw()
    
    def noti(self, message):
        notification(parent=self.root, message=message)
        
    def save_config(self):
        save_to_json_file(self.config, config_path)
        
    def create_icon(self):
        try:
            icon_path = os.path.join(current_dir, 'import' , 'icon.png')
            if not os.path.exists(icon_path):
                icon_path = None
            image = self.create_image(icon_path)
            menu = (
                item("Hiển thị menu", self.get_start_window),
                item("Dừng tiến trình tải video/audio", self.stop_download),
                item("Dừng tiến trình đăng video", self.stop_upload),
                item("Dừng tiến trình chỉnh sửa video", self.stop_edit_videos),
                item("Dừng tất cả tiến trình đang chạy", self.stop_all_process),
                item("Thoát ứng dụng", self.exit_app),
            )
            self.icon = pystray.Icon("Super Social Media", image, "Super Social Media", menu)
            tray_thread = threading.Thread(target=self.icon.run_detached)
            tray_thread.daemon = True
            tray_thread.start()
        except:
            getlog()

    def stop_download(self):
        self.is_stop_download = True
        if self.youtube:
            self.youtube.is_stop_download = True
        if self.facebook:
            self.facebook.is_stop_download = True
        if self.tiktok:
            self.tiktok.is_stop_download = True
        print("Đang dừng quá trình tải video, vui lòng chờ trong giây lát ...")
    def stop_upload(self):
        self.is_stop_upload = True
        if self.youtube:
            self.youtube.is_stop_upload = True
        if self.facebook:
            self.facebook.is_stop_upload = True
        if self.tiktok:
            self.tiktok.is_stop_upload = True
        print("Đang dừng quá trình đăng video, vui lòng chờ trong giây lát ...")
    def stop_edit_videos(self):
        self.is_stop_edit = True
        print("Đang dừng quá trình chỉnh sửa video, vui lòng chờ trong giây lát ...")

    def stop_all_process(self):
        self.stop_download()
        self.stop_upload()
        self.stop_edit_videos()
        if self.config['time_check_auto_upload']:
            self.config['time_check_auto_upload'] = "0"
            self.save_config()

    def create_image(self, icon_path=None):
        if icon_path:
            image = Image.open(icon_path)
        else:
            width = 64
            height = 64
            image = Image.new("RGB", (width, height), (255, 255, 255))
            dc = ImageDraw.Draw(image)
            dc.rectangle( (width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10), fill=(0, 0, 0), )
        return image

    def exit_app(self):
        self.reset()
        self.icon.stop()
        self.root.destroy()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", 1)
        self.root.attributes("-topmost", 0)

    def hide_window(self):
        self.root.iconify()
        self.root.withdraw()

    def on_close(self):
        self.save_config()
        self.hide_window()
    
    def close_driver(self):
        if self.driver:
            self.driver.close()
#----------------------------------Setting Window--------------------------------------------------------
    def setting_screen_position(self):
        try:
            self.root.update_idletasks()
            x = screen_width - self.width - 10
            y = screen_height - self.height_window
            self.root.geometry(f"{self.width}x{self.height_window - 80}+{x}+{y}")
        except:
            getlog()

    def setting_window_size(self):
        if self.is_start_app:
            self.width = 500
            self.height_window = 523
            if height_element == 30:
                self.height_window = 516
        else:
            if self.is_start_window:
                self.root.title("SSM App")
                self.width = 500
                self.height_window = 527
                if height_element == 30:
                    self.height_window = 520
                self.is_start_window = False
            elif self.is_add_new_channel:
                self.root.title("Add New Channel")
                self.width = 500
                self.height_window = 266
            elif self.is_remove_channel:
                self.root.title("Remove Channel")
                self.width = 500
                self.height_window = 217
                self.is_remove_channel = False
            elif self.is_open_common_setting:
                self.root.title("Common Setting")
                self.width = 310
                self.height_window = 300
                if height_element == 30:
                    self.height_window = 450
                self.is_open_common_setting = False
            elif self.is_edit_video_window:
                self.root.title("Edit Videos")
                self.width = 700
                self.height_window = 990
                if height_element == 30:
                    self.height_window = 940
                self.is_edit_video_window = False
            elif self.is_open_edit_video_menu:
                self.root.title("Edit Video Window")
                self.width = 500
                self.height_window = 342
                if height_element == 30:
                    self.height_window = 346
                self.is_open_edit_video_menu = False
            elif self.is_convert_video_window:
                self.root.title("Convert Videos Window")
                self.width = 500
                self.height_window = 315
                self.is_convert_video_window = False
            elif self.is_cut_video_window:
                self.root.title("Cut Video Window")
                self.width = 500
                self.height_window = 457
                self.is_cut_video_window = False
            elif self.is_combine_video_window:
                self.root.title("Combine Video Window")
                self.width = 500
                self.height_window = 315
                self.is_combine_video_window = False
            elif self.is_increse_video_quality_window:
                self.root.title("Increse Video Quality Window")
                self.width = 500
                self.height_window = 218
                if height_element == 30:
                    self.height_window = 224
                self.is_increse_video_quality_window = False
            elif self.is_edit_audio_window:
                self.root.title("Edit Audio Window")
                self.width = 500
                self.height_window = 302
                self.is_edit_audio_window = False
            elif self.is_edit_audio_option:
                self.root.title("Edit Audio Option")
                self.width = 500
                self.height_window = 458
                if height_element == 30:
                    self.height_window = 450
                self.is_edit_audio_option = False
            elif self.is_extract_audio_option:
                self.root.title("Extract Audio Option")
                self.width = 500
                self.height_window = 458
                if height_element == 30:
                    self.height_window = 450
                self.is_extract_audio_option = False
            elif self.is_text_to_mp3_window:
                self.root.title("Text to MP3 window")
                self.width = 500
                self.height_window = 314
                self.is_text_to_mp3_window = False
            elif self.is_youtube_window:
                self.root.title("Youtube Window")
                self.width = 500
                self.height_window = 355
                self.is_youtube_window = False
            elif self.is_sign_up_youtube:
                self.root.title("Sign Up Youtube")
                self.width = 500
                self.height_window = 265
                self.is_sign_up_youtube = False
            elif self.is_facebook_window:
                self.root.title("Facebook Window")
                self.width = 500
                self.height_window = 355
                self.is_facebook_window = False
            elif self.is_sign_up_facebook:
                self.root.title("Sign Up Facebook")
                self.width = 500
                self.height_window = 313
                self.is_sign_up_facebook = False
            elif self.is_tiktok_window:
                self.root.title("Tiktok Window")
                self.width = 500
                self.height_window = 397
                self.is_tiktok_window = False
            elif self.is_interact_setting_window:
                self.root.title("Tiktok Insteract Window")
                self.width = 600
                self.height_window = 600
                self.is_interact_setting_window = False
            elif self.is_auto_upload_tiktok_window:
                self.root.title("Tiktok Auto Upload Window")
                self.width = 600
                self.height_window = 307
                self.is_auto_upload_tiktok_window = False
            elif self.is_sign_up_tiktok:
                self.root.title("Sign Up Tiktok")
                self.width = 500
                self.height_window = 407
                self.is_sign_up_tiktok = False
            elif self.is_rename_file_by_index_window:
                self.root.title("Rename Files")
                self.width = 500
                self.height_window = 361
                self.is_rename_file_by_index_window = False
            elif self.is_remove_char_in_file_name_window:
                self.root.title("Remove Char in Files")
                self.width = 500
                self.height_window = 315
                self.is_remove_char_in_file_name_window = False
            elif self.is_extract_image_from_video_window:
                self.root.title("Extract Image From Video")
                self.width = 500
                self.height_window = 265
                self.is_extract_image_from_video_window = False
            elif self.is_open_change_mac_addres_window:
                self.root.title("Change Mac Address")
                self.width = 500
                self.height_window = 315
                self.is_open_change_mac_addres_window = False
            elif self.is_other_window:
                self.root.title("Other")
                self.width = 500
                self.height_window = 303
                self.is_other_window = False
            elif self.is_other_download_window:
                self.root.title("Other Download Window")
                self.width = 500
                self.height_window = 263
                if height_element == 30:
                    self.height_window = 270
                self.is_other_download_window = False
            elif self.is_download_douyin_video_window:
                self.root.title("Download Douyin Video")
                self.width = 500
                self.height_window = 215
                if height_element == 30:
                    self.height_window = 230
                self.is_download_douyin_video_window = False
            elif self.is_open_auto_process_window:
                self.root.title("Automatic Setup")
                self.width = 600
                self.height_window = 747
                if height_element == 30:
                    self.height_window = 712
                self.is_open_auto_process_window = False

        self.height_window = int(self.height_window * default_percent )
        self.setting_screen_position()

    def open_rename_file_by_index_window(self):
        self.reset()
        self.is_rename_file_by_index_window = True
        self.setting_window_size()
        self.file_name_var = create_frame_label_and_input(self.root, text="Tên file muốn đổi", place_holder="Tên file có chứa \"<index>\" làm vị trí đặt số", width=self.width, left=0.4, right=0.6)
        self.index_file_name_var = create_frame_label_and_input(self.root, text="Số thứ tự bắt đầu", width=self.width, left=0.4, right=0.6)
        self.index_file_name_var.insert(0, '1')
        self.file_name_extension_var = create_frame_label_and_input(self.root, text="Loại file muốn đổi tên", width=self.width, left=0.4, right=0.6)
        self.file_name_extension_var.insert(0, '.mp4')
        self.videos_edit_folder_var = create_frame_button_and_input(self.root,text="Chọn Thư Mục Chứa File", command= self.choose_videos_edit_folder, left=0.4, right=0.6, width=self.width)
        create_button(frame=self.root, text="Bắt Đầu Đổi Tên", command= self.rename_file_by_index)
        create_button(self.root, text="Lùi lại", command=self.other_function, width=self.width)
        self.show_window()

    def extract_image_from_video_window(self):
        self.reset()
        self.is_extract_image_from_video_window = True
        self.setting_window_size()
        self.image_position_var = create_frame_label_and_input(self.root, text="Chọn vị trí trích xuất ảnh", width=self.width, left=0.4, right=0.6, place_holder='Ví dụ: 00:40 hoặc 00:10:15')
        self.videos_edit_folder_var = create_frame_button_and_input(self.root,text="Chọn Thư Mục Chứa Video", command= self.choose_videos_edit_folder, left=0.4, right=0.6, width=self.width)
        create_button(frame=self.root, text="Bắt Đầu Trích Xuất Ảnh", command= self.extract_image_from_video)
        create_button(self.root, text="Lùi lại", command=self.other_function, width=self.width)
        self.show_window()

    def open_remove_char_in_file_name_window(self):
        self.reset()
        self.is_remove_char_in_file_name_window = True
        self.setting_window_size()
        self.char_want_to_remove_var = create_frame_label_and_input(self.root, text="Nhập các ký tự muốn loại bỏ", width=self.width, left=0.4, right=0.6, place_holder='Ví dụ: .,-,#')
        self.file_name_extension_var = create_frame_label_and_input(self.root, text="Loại file muốn đổi tên", width=self.width, left=0.4, right=0.6)
        self.file_name_extension_var.insert(0, '.mp4')
        self.videos_edit_folder_var = create_frame_button_and_input(self.root,text="Chọn Thư Mục Chứa File", command= self.choose_videos_edit_folder, left=0.4, right=0.6, width=self.width)
        create_button(frame=self.root, text="Bắt Đầu Đổi Tên", command= self.remove_char_in_file_name)
        create_button(self.root, text="Lùi lại", command=self.other_function, width=self.width)
        self.show_window()

    def rename_file_by_index(self):
        base_name = self.file_name_var.get()
        index = self.index_file_name_var.get()
        extension = self.file_name_extension_var.get()
        videos_folder = self.videos_edit_folder_var.get()
        if check_folder(videos_folder):
            rename_files_by_index(videos_folder, base_name, extension, index)

    def remove_char_in_file_name(self):
        chars_want_to_remove = self.char_want_to_remove_var.get()
        extension = self.file_name_extension_var.get()
        videos_folder = self.videos_edit_folder_var.get()
        if not chars_want_to_remove:
            self.noti("Hãy nhập các ký tự muốn loại bỏ và cách nhau bởi dấu \",\". Ví dụ:  \".,#\"")
            return
        if check_folder(videos_folder):
            remove_char_in_file_name(folder_path=videos_folder, chars_want_to_remove=chars_want_to_remove, extension=extension)

    def extract_image_from_video(self, videos_folder=None):
        position = self.image_position_var.get().strip()
        if not videos_folder:
            videos_folder = self.videos_edit_folder_var.get()
        if not position:
            self.noti("Hãy nhập vị trí thời gian muốn trích xuất ảnh")
            return
        if check_folder(videos_folder):
            get_image_from_video(videos_folder=videos_folder, position=position)

#-------------------------------Convert MP3------------------------------------------------
    def open_text_to_mp3_window(self):
        self.reset()
        self.is_text_to_mp3_window = True
        self.setting_window_size()
        self.file_path_get_var = create_frame_button_and_input(self.root, text="File \'.txt\' muốn chuyển đổi", command= self.choose_directory_get_txt_file, width=self.width, left=0.4, right=0.6)
        self.speed_talk_var = self.create_settings_input(text="Tốc độ đọc", config_key='speed_talk', values=["0.8", "0.9", "1", "1.1", "1.2"])
        self.convert_multiple_record_var = self.create_settings_input(text="Chế độ chuyển theo từng dòng", values=["Yes", "No"])
        self.convert_multiple_record_var.set("No")
        create_button(frame=self.root, text="Bắt đầu chuyển đổi", command= self.text_to_mp3)
        create_button(self.root, text="Lùi lại", command=self.open_edit_audio_window, width=self.width)
        self.show_window()

    def choose_directory_get_txt_file(self):
        file_path_get = filedialog.askopenfilename( title="Select a txt file", filetypes=(("Text files", "*.txt"),))
        self.file_path_get_var.delete(0, ctk.END)
        self.file_path_get_var.insert(0, file_path_get)

    def text_to_mp3(self, voice=None, speed=1):
        print("Đã bỏ tính năng này!")

app = MainApp()
try:
    app.root.mainloop()
except:
    pass
