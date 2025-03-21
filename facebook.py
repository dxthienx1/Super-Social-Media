from common_function import *

class FacebookManager:
    def __init__(self, page_name=None, download_thread=None, upload_thread=None, is_auto_upload=False):
        self.download_thread = download_thread
        self.upload_thread = upload_thread
        self.page_name = page_name
        self.get_facebook_config()
        self.account = self.acc_config['email']
        self.password = self.acc_config['password']
            
        self.is_auto_upload = is_auto_upload
        if not is_auto_upload:
            self.root = ctk.CTk()
            self.title = self.root.title(page_name)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.is_schedule = False
        else:
            self.is_schedule = True
        self.width = 500

        self.driver = None
        self.cookies_info = {}
        self.local_storage_info = {}

        self.is_start_tiktok = True
        self.download_thread = None
        self.download_thread_url = None
        self.is_upload_video_window = False
        self.is_stop_upload = False
        self.is_stop_download = False
        self.is_first_start = True
    
    def get_start_facebook(self):
        if not self.is_first_start:
            self.reset()
        else:
            self.is_first_start = False
        
        self.is_start_facebook = True
        self.show_window()
        self.setting_window_size()
        create_button(frame = self.root, text="Đăng video", command= self.open_upload_video_window)
        create_button(frame = self.root, text="Tải video từ trang", command=self.open_download_page_video_window)
        try:
            self.root.mainloop()
        except:
            getlog()

    def get_facebook_config(self):
        self.facebook_config = load_facebook_config()
        self.acc_config = load_facebook_config(self.page_name)

    def open_upload_video_window(self):
        self.reset()
        self.is_upload_video_window = True
        self.show_window()
        self.setting_window_size()

        def load_template():
            template_name = self.load_template_var.get()
            temppale = load_facebook_config(template_name)
            self.title_var.delete(0, ctk.END)
            self.title_var.insert(0, temppale['title'])
            self.description_var.delete("1.0", ctk.END)
            self.description_var.insert(ctk.END, temppale['description'])
            self.upload_date_var.delete(0, ctk.END)
            self.upload_date_var.insert(0, temppale['upload_date'])
            self.publish_times_var.delete(0, ctk.END)
            self.publish_times_var.insert(0, temppale['publish_times'])
            self.is_title_plus_video_name_var.set(convert_boolean_to_Yes_No(temppale['is_title_plus_video_name']))
            self.show_browser_var.set(convert_boolean_to_Yes_No(self.facebook_config['show_browser']))
            self.is_delete_after_upload_var.set(convert_boolean_to_Yes_No(temppale['is_delete_after_upload']))
            self.is_reel_video_var.set(convert_boolean_to_Yes_No(temppale['is_reel_video']))
            self.waiting_verify_var.set(temppale['waiting_verify'])
            self.upload_folder_var.delete(0, ctk.END)
            self.upload_folder_var.insert(0, temppale['upload_folder'])
            self.number_of_days_var.delete(0, ctk.END)
            self.number_of_days_var.insert(0, temppale['number_of_days'])
            self.day_gap_var.delete(0, ctk.END)
            self.day_gap_var.insert(0, temppale['day_gap'])

        def choose_folder_upload():
            folder = choose_folder()
            if folder:
                self.upload_folder_var.delete(0, ctk.END)
                self.upload_folder_var.insert(0, folder)
        self.title_var = self.create_settings_input("Tiêu đề", "title", left=left, right=right)
        self.is_title_plus_video_name_var = self.create_settings_input("Thêm tên video vào tiêu đề", "is_title_plus_video_name", values=["Yes", "No"], left=left, right=right)
        self.description_var = self.create_settings_input("Mô tả", "description", is_textbox=True, left=left, right=right)
        self.upload_date_var = self.create_settings_input("Ngày đăng(yyyy-mm-dd)", "upload_date", left=left, right=right)
        self.publish_times_var = self.create_settings_input("Giờ đăng(vd: 08:00)", "publish_times", left=left, right=right)
        self.number_of_days_var = self.create_settings_input("Số ngày muốn đăng", "number_of_days", left=left, right=right)
        self.day_gap_var = self.create_settings_input("Khoảng cách giữa các ngày đăng", "day_gap", left=left, right=right)
        self.is_delete_after_upload_var = self.create_settings_input("Xóa video sau khi đăng", "is_delete_after_upload", values=["Yes", "No"], left=left, right=right)
        self.is_reel_video_var = self.create_settings_input("Đây là thước phim?", "is_reel_video", values=["Yes", "No"], left=left, right=right)
        self.waiting_verify_var = self.create_settings_input("Thêm thời gian chờ xác minh (s)", "waiting_verify", values=["0", "30", "60"], left=left, right=right)
        self.show_browser_var = self.create_settings_input(text="Hiển thị trình duyệt", config_key="show_browser", values=['Yes', 'No'], left=left, right=right, is_data_in_template=False)
        self.upload_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục chứa video", command=choose_folder_upload, width=self.width, left=left, right=right)
        self.upload_folder_var.insert(0, self.acc_config['upload_folder'])
        self.load_template_var = create_frame_button_and_combobox(self.root, "Tải mẫu có sẵn", command=load_template, values=self.facebook_config['registered_account'], width=self.width, left=left, right=right)
        self.load_template_var.set(self.page_name)
        create_frame_button_and_button(self.root, text1="Đăng video ngay", text2="Lên lịch đăng video", command1=self.start_upload_video_now, command2=self.start_schedule_upload, width=self.width, left=0.5, right=0.5)
        create_button(self.root, text="Lùi lại", command=self.get_start_facebook, width=self.width)

    def start_schedule_upload(self):
        self.is_schedule = True
        if not self.save_upload_setting():
            return
        self.start_thread_upload_video()
    def start_upload_video_now(self):
        self.is_schedule = False
        if not self.save_upload_setting():
            return
        self.start_thread_upload_video()

    def start_thread_upload_video(self):
        if not self.upload_thread or not self.upload_thread.is_alive():
            self.is_stop_upload = False
            self.upload_video_thread = threading.Thread(target=self.upload_video)
            self.upload_video_thread.start()

    def save_facebook_config(self):
        save_facebook_config(self.page_name, self.acc_config)
        save_facebook_config(data= self.facebook_config)

    def save_upload_setting(self):
        def check_publish_times_facebook(publish_times):
            try:
                publish_times = publish_times.split(',')
                for time in publish_times:
                    get_time = get_pushlish_time_hh_mm(time, facebook_time=True)
                    if not get_time:
                        return False
                return True
            except:
                return False
        try:
            upload_date = self.upload_date_var.get()
            is_valid_date, message = is_format_date_yyyymmdd(upload_date, daydelta=29)
            if not is_valid_date:
                notification(self.root, message)
                return False
            publish_times = self.publish_times_var.get()
            if self.is_schedule:
                if not check_publish_times_facebook(publish_times):
                    return
            self.acc_config["title"] = self.title_var.get()
            self.acc_config["description"] = self.description_var.get("1.0", ctk.END).strip()
            self.acc_config["upload_date"] = upload_date
            self.acc_config["publish_times"] = publish_times
            self.acc_config['cnt_upload_in_day'] = 0
            self.acc_config["is_title_plus_video_name"] = self.is_title_plus_video_name_var.get() == "Yes"
            self.acc_config["upload_folder"] = self.upload_folder_var.get()
            self.acc_config["is_delete_after_upload"] = self.is_delete_after_upload_var.get() == 'Yes'
            self.acc_config["is_reel_video"] = self.is_reel_video_var.get() == 'Yes'
            self.acc_config["waiting_verify"] = self.waiting_verify_var.get().strip()
            self.acc_config["number_of_days"] = self.number_of_days_var.get()
            self.acc_config["day_gap"] = self.day_gap_var.get()
            self.facebook_config['show_browser'] = self.show_browser_var.get() == "Yes"
            self.save_facebook_config()
            return True
        except:
            getlog()
            return False
        

    def open_download_page_video_window(self):
        self.reset()
        self.is_download_video_window = True
        self.show_window()
        self.setting_window_size()

        def choose_folder_to_save():
            download_folder = choose_folder()
            if download_folder:
                self.download_folder_var.delete(0, ctk.END)
                self.download_folder_var.insert(0, download_folder)

        def start_thread_download_page_video():
            if not self.download_thread or not self.download_thread.is_alive():
                self.is_stop_download = False
                if save_download():
                    self.download_thread = threading.Thread(target=self.download_page_videos_now)
                    self.download_thread.start()
                else:
                    print("Đang tải ở nơi khác !!!")

        def save_download():
            try:
                self.facebook_config['download_url'] = self.page_link_var.get().strip()
                self.facebook_config['download_folder'] = self.download_folder_var.get().strip()
                self.facebook_config['filter_by_views'] = self.filter_by_views_var.get().strip() or "0"
                if not self.facebook_config['download_url']:
                    print("Nhập link tải video !!!")
                    return False
                if not check_folder(self.facebook_config['download_folder']):
                    return False
                self.save_facebook_config()
                return True
            except:
                return False
        
        self.download_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục lưu video", command=choose_folder_to_save, width=self.width, left=0.35, right=0.65)
        self.download_folder_var.insert(0, self.facebook_config['download_folder'])
        self.page_link_var = create_frame_label_and_input(self.root,text="Tải từ link trang facebook", width=self.width, left=0.35, right=0.65)
        self.filter_by_views_var = create_frame_label_and_input(self.root, text="Lọc theo số lượt xem", width=self.width, left=0.35, right=0.65)
        self.filter_by_views_var.insert(0,'0')
        create_button(self.root, text="Bắt đầu tải video", command=start_thread_download_page_video, width=self.width)
        create_button(self.root, text="Lùi lại", command=self.get_start_facebook, width=self.width)

    def download_page_videos_now(self):
        try:
            t = time()
            video_urls = []
            filter_by_views = self.facebook_config['filter_by_views']
            try:
                view_cnt = int(float(filter_by_views))
            except:
                view_cnt = 0
            page_link = self.facebook_config['download_url']
            if 'quantity_download' not in self.facebook_config:
                self.facebook_config['quantity_download'] = "2000"
            quantity_download = int(self.facebook_config['quantity_download'])
            if self.login(show=True):
                self.driver.get(page_link)
                press_esc_key(2, self.driver)
                sleep(2)
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                cnt_search = 0
                k = 0
                print(f"Bắt đầu quét video trong trang facebook theo link {page_link}...")
                while True:
                    if self.is_stop_download:
                        break
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        if k < 2:
                            k += 1
                            self.driver.execute_script("window.scrollBy(0, -400);")
                            sleep(1)
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            sleep(2)
                        else:
                            break
                    else:
                        k = 0
                    last_height = new_height
                    cnt_search += 1
                    sys.stdout.write(f'\rCuộn trang lần thứ {cnt_search} ...')
                    sys.stdout.flush()
                    if cnt_search > 250:
                        break
                reel_xpath = './/a[contains(@href, "/reel/") and not(contains(@href, "?comment"))]'
                video_xpath = './/a[contains(@href, "/videos/") and not(contains(@href, "?comment"))]'
                link_reel_eles = self.driver.find_elements(By.XPATH, reel_xpath)
                link_video_eles = self.driver.find_elements(By.XPATH, video_xpath)
                video_eles = link_reel_eles + link_video_eles

                if len(video_eles) > 0:
                    for video_ele in video_eles:
                        if self.is_stop_download:
                                break
                        url = video_ele.get_attribute('href') or None
                        if not url:
                            continue
                        view_count = 0
                        if view_cnt > 0:
                            try:
                                parent_div = video_ele.find_element(By.XPATH, './/ancestor::span[1]')
                            except:
                                parent_div = None
                            if parent_div:
                                try:
                                    text = parent_div.text.split('·\n')[-1].strip()
                                    view_text = text.split('\n')[0]
                                    view_count_str = get_views_text(view_text)
                                    view_count = get_view_count(view_count_str)
                                except:
                                    view_count = 0
                        if view_count >= view_cnt:
                            if url not in video_urls:
                                video_urls.append(url)
                    t1 = int(time() - t)
                    print(f'\nThời gian quét video là {int(t1/60)} phút {t1%60} giây --> Tổng tìm thấy {len(video_urls)} video có số lượt xem lớn hơn {view_cnt} ...')
                else:
                    print(f"Không tìm thấy video nào từ link {page_link}")
                cnt = 0
                self.close_driver()
                if len(video_urls) > 0:
                    print('Quá trình tải video bắt đầu ...')
                    download_info = get_json_data(download_info_path)
                    download_folder = self.facebook_config['download_folder']
                    for url in video_urls.copy():
                        if self.is_stop_download:
                                break
                        if download_video_by_url(url, download_folder):
                            if url not in download_info['downloaded_urls']:
                                download_info['downloaded_urls'].append(url)
                                video_urls.remove(url)
                                save_to_json_file(download_info, download_info_path)
                                cnt += 1
                                if cnt > quantity_download:
                                    break
                    if cnt > 0:
                        print(f'Đã tải thành công {cnt} video')
                    else:
                        download_video_by_bravedown(video_urls, download_folder)
                else:
                    print(f'Không tìm thấy video có số lượt xem lớn hơn {view_cnt}')
        except:
            getlog()

#-----------------------------------Đăng Nhập FB--------------------------------------------
    def load_session(self, url="https://www.facebook.com"):
        self.driver.get(url)
        sleep(2)
        try:
            current_cookies = self.acc_config.get('chrome_cookies', [])
            for cookie in current_cookies:
                if 'domain' in cookie and cookie['domain'] in self.driver.current_url:
                    self.driver.add_cookie(cookie)
                elif 'domain' not in cookie:
                    self.driver.add_cookie(cookie)
        except FileNotFoundError:
            sleep(0.1)
        try:
            local_storage = self.acc_config.get('local_storage', {})
            if local_storage:
                for key, value in local_storage.items():
                    self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
            sleep(0.5)
            self.driver.refresh()
            sleep(3)
        except FileNotFoundError:
            sleep(0.1)

    def save_session(self):
        self.acc_config['chrome_cookies'] = self.driver.get_cookies()
        self.acc_config['local_storage'] = self.driver.execute_script("return {...window.localStorage};")
        self.acc_config['waiting_verify'] = "0"
        save_facebook_config(self.page_name, self.acc_config)

    def waiting_for_capcha_verify(self, time_wait=None):
        try:
            if not time_wait:
                time_wait = self.acc_config['waiting_verify']
            time_wait = int(time_wait)
        except:
            print(f"{self.page_name} Thời gian chờ không hợp lệ: {self.acc_config['waiting_verify']} --> Bỏ qua chờ xác minh")
            time_wait = 1
        sleep_random(time_wait, time_wait + 2)


    def login(self, show=False):
        try:
            if self.facebook_config['use_profile_facebook']:
                self.driver = get_chrome_driver_with_profile(target_gmail=self.account, show=show)
                sleep(5)
            else:
                self.driver = get_driver(show=show)
            if not self.driver:
                return False
            self.load_session()
            self.profile_element, language = self.get_profile_element()
            if not self.profile_element:
                email_input = self.driver.find_element(By.ID, 'email')
                email_input.send_keys(self.account)
                sleep(0.8)
                password_input = self.driver.find_element(By.ID, 'pass')
                password_input.send_keys(self.password)
                sleep(0.8)
                password_input.send_keys(Keys.RETURN)
                sleep(2)
                self.waiting_for_capcha_verify()
                self.profile_element, language = self.get_profile_element()
            if self.profile_element:
                if language == 'en':
                    self.en_language = True
                else:
                    self.en_language = False
                print("Đăng nhập thành công!")
                return True
            else:
                print("Đăng nhập không thành công, có thể cần xác minh tài khoản!")
                return False
        except:
            getlog()
            if self.is_auto_upload:
                print("Lỗi khi đăng nhập, có thể do đường truyền mạng không ổn định!")
            else:
                notification(self.root, "Lỗi khi đăng nhập, có thể do đường truyền mạng không ổn định!")
            return False
        

#-----------------------------------Thao tác trên facebook--------------------------------------------  

    def click_page_list(self):
        if self.en_language:
            text = "See all profiles"
            xpath = get_xpath_by_multi_attribute('div', ['aria-label="See all profiles"'])
        else:
            text = "Xem tất cả trang cá nhân"
            xpath = get_xpath_by_multi_attribute('div', ['aria-label="Xem tất cả trang cá nhân"'])
        page_list_ele = get_element_by_text(self.driver, text)
        if page_list_ele:
            page_list_ele.click()
            sleep(2)
        else:
            page_list_ele = get_element_by_xpath(self.driver, xpath)
            if page_list_ele:
                page_list_ele.click()
                sleep(2)
            else:
                print("Dừng đăng video vì không tìm thấy danh sách trang!")
                self.is_stop_upload = True

    def get_profile_element(self):
        profile_xpath = get_xpath("div", "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz xzsf02u x1rg5ohu")
        profile_element = get_element_by_xpath(self.driver, profile_xpath, "Your profile")
        if profile_element:
            return profile_element, 'en'
        else:
            profile_element = get_element_by_xpath(self.driver, profile_xpath, "Trang cá nhân của bạn")
            if profile_element:
                return profile_element, 'vi'
            else:
                return None, None

    def click_element_by_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(1)
            
    def get_element_by_class(self, class_name, key=None):
        elements = self.driver.find_elements(By.CLASS_NAME, class_name)
        kq = []
        if len(elements) > 0:
            if key:
                for ele in elements:
                    if key in ele.accessible_name or key in ele.text or key in ele.tag_name or key in ele.aria_role:
                        kq.append(ele)
                        break
                if len(kq) > 0:
                    ele = kq[0]
                else:
                    ele = None
            else:
                ele = elements[0]
        else:
            ele = None
        return ele
    
    def get_element_by_id(self, id):
        element = self.driver.find_element(By.ID, id)
        return element

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            print("Đã đóng trình duyệt.")

    def click_schedule_link(self):
        xpath  = get_xpath_by_multi_attribute("a", ["role='link'"])
        ele = get_element_by_xpath(self.driver, xpath, "Meta Business Suite")
        if ele:
            link = ele.get_attribute('href')
            self.driver.get(link) 
            sleep(4)

    def get_meta_business_suite(self):
        def click_page_name():
            check_see_all_page = get_element_by_text(self.driver, 'Xem tất cả ', 'span')
            if check_see_all_page:
                check_see_all_page.click()
                sleep(1)
            xpath = get_xpath('div', 'x1xqt7ti xsuwoey x63nzvj xbsr9hj xuxw1ft x6ikm8r x10wlt62 xlyipyv x1mzt3pk x1vvkbs x13faqbe x1fcty0u xeuugli')
            ele = get_element_by_xpath(self.driver, xpath, self.page_name)
            
            if ele:
                print(ele.text)
                if ele.text == self.page_name:
                    ele.click()
                    sleep(4)
                    return True
            else:
                ele = get_element_by_text(self.driver, self.page_name, tag_name='div')
                if ele and ele.text == self.page_name:
                    ele.click()
                    sleep(4)
                    return True
            print(self.page_name)
            print(ele)
            return False

    
        def check_meta_bussiness_name():
            xpath = get_xpath('div', 'xmi5d70 x1fvot60 xxio538 xbsr9hj xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1fcty0u')
            ele = get_element_by_xpath(self.driver, xpath)
            if ele:
                page = ele.text
                if page != self.page_name:
                    press_esc_key(2, self.driver)
                    ele.click()
                    if not click_page_name():
                        print(f'Có lỗi trong quá trình chuyển trang {self.page_name} trên Meta Bussiness Suite')
                        self.is_stop_upload = True
                        
        self.driver.get("https://business.facebook.com/latest/home?")
        sleep(4)
        check_meta_bussiness_name()
        self.driver.get("https://www.facebook.com/latest/content_calendar?")
        sleep(4)

    def click_option_menu(self):
        att1 = "class='x3nfvp2 x120ccyz x1heor9g x2lah0s x1c4vz4f x1gryazu'"
        att2 = "role='presentation'"
        xpath = get_xpath_by_multi_attribute("div", [att1, att2])
        ele = get_element_by_xpath(self.driver, xpath)
        if ele:
            ele.click()
            sleep(2)
    def input_date(self, date):
        if self.en_language:
            att2 = "placeholder='mm/dd/yyyy'"
            upload_date = convert_date_format_yyyymmdd_to_mmddyyyy(date)
        else:
            att2 = "placeholder='dd/mm/yyyy'"
            upload_date = convert_date_format_yyyymmdd_to_mmddyyyy(date, vi_date=True)
        xpath = get_xpath_by_multi_attribute("input", [att2])
        ele = get_element_by_xpath(self.driver, xpath)
        if ele:
            ele.send_keys(Keys.CONTROL + "a")
            ele.send_keys(upload_date)
            sleep(1)
    def input_hours(self, hour):
        if self.en_language:
            xpath = get_xpath_by_multi_attribute('input', ['aria-label="hours"'])
        else:
            xpath = get_xpath_by_multi_attribute('input', ['aria-label="giờ"'])
        ele = get_element_by_xpath(self.driver, xpath)
        if ele:
            ele.send_keys(hour)
            sleep(1)
    def input_minutes(self, minute):
        if self.en_language:
            xpath = get_xpath_by_multi_attribute('input',  ['aria-label="minutes"'])
        else:
            xpath = get_xpath_by_multi_attribute('input',  ['aria-label="phút"'])
        ele = get_element_by_xpath(self.driver, xpath)
        if ele:
            ele.send_keys(minute)
            sleep(1)

    def input_AM_or_PM(self, meridiem):
        att2 = "aria-label='meridiem'"
        xpath = get_xpath_by_multi_attribute("input", [att2])
        ele = get_element_by_xpath(self.driver, xpath)
        if ele:
            ele.send_keys(meridiem)
            sleep(2)
    def click_update_schedule_button(self):
        if self.en_language:
            ele = get_element_by_text(self.driver, "Update")
        else:
            ele = get_element_by_text(self.driver, "Cập nhật")
        if ele:
            ele.click()
            sleep(1)
    def click_public_schedule_button(self):
        if self.en_language:
            ele = get_element_by_text(self.driver, "Publish", tag_name='div')
        else:
            ele = get_element_by_text(self.driver, "Đăng", tag_name='div')
        if ele:
            ele.click()
            sleep(5)
    def click_schedule_option(self):
        if self.en_language:
            ele = get_element_by_text(self.driver, "Schedule", tag_name='div')
        else:
            ele = get_element_by_text(self.driver, "Lên lịch", tag_name='div')
        if ele:
            ele.click()
            sleep(1)

    def click_bulk_upload_video_button(self):
        if self.en_language:
            if self.is_reel_video:
                ele = get_element_by_text(self.driver, "Bulk upload reels")
            else:
                ele = get_element_by_text(self.driver, "Bulk upload videos")
        else:
            if self.is_reel_video:
                ele = get_element_by_text(self.driver, "Tải hàng loạt thước phim lên")
            else:
                ele = get_element_by_text(self.driver, "Tải video lên hàng loạt")
        if ele:
            ele.click()
            sleep(5)

    def input_schedule_video_on_facebook(self, video_path):
        att1 = "accept='video/*'"
        att2 = "class='_44hf'"
        xpath = get_xpath_by_multi_attribute("input", [att1, att2])
        ele = get_element_by_xpath(self.driver, xpath, )
        if ele:
            ele.send_keys(video_path)
            sleep(3)
        else:
            self.is_stop_upload = True

    def click_upload_video_icon(self):
        xpath_photo_video = "//div[@class=\"x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x78zum5 x1r8uery x1iyjqo2 xs83m0k xl56j7k x1pshirs x1y1aw1k x1sxyh0 xwib8y2 xurb0ha\"]"
        if self.en_language:
            if self.is_reel_video:
                photo_video_button = get_element_by_xpath(self.driver, xpath_photo_video, "Reel")
            else:
                photo_video_button = get_element_by_xpath(self.driver, xpath_photo_video, "photo/video")
        else:
            if self.is_reel_video:
                photo_video_button = get_element_by_xpath(self.driver, xpath_photo_video, "Thước phim")
            else:
                photo_video_button = get_element_by_xpath(self.driver, xpath_photo_video, "Ảnh/video")
        if photo_video_button:
            photo_video_button.click()
            sleep(1.5)

    def input_video_on_facebook(self, video_path):
        if self.is_reel_video:
            xpath = get_xpath('input', 'x1s85apg', 'accept', 'video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv')
        else:
            xpath = "//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv' and @class='x1s85apg']"
        upload_input = get_element_by_xpath(self.driver, xpath)
        if upload_input:
            upload_input.send_keys(video_path)
            sleep(2)

    def input_title(self, title):
        if not title.strip():
            return
        title_xpath = get_xpath("div", "xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x9f619 x1lliihq x5yr21d xh8yej3 notranslate")
        if self.en_language:
            title_element = get_element_by_xpath(self.driver, title_xpath, "What's on your mind")
        else:
            title_element = get_element_by_xpath(self.driver, title_xpath, "bạn đang nghĩ gì thế?")
        if title_element:
            title_element.send_keys(title)
            sleep(2)
        else:
            self.is_stop_upload = True

    def check_status_upload_video(self):
        status_xpath = get_xpath("div", "x117nqv4 x1sln4lm xexx8yu x10l6tqk xh8yej3", contain=True)
        # status_xpath = "//div[contains(@class, 'x117nqv4') and contains(@class, 'x1sln4lm') and contains(@class, 'xexx8yu') and contains(@class, 'x10l6tqk') and contains(@class, 'xh8yej3')]"
        cnt = 0
        pre_v = "0%"
        while True:
            if self.is_stop_upload:
                break
            try:
                status_xpath_element = get_element_by_xpath(self.driver, status_xpath)
                v = status_xpath_element.text
                if v != pre_v:
                    print(v)
                    pre_v = v
                if v == "100%":
                    break
            except:
                cnt += 1
                if cnt > 10:
                    self.is_stop_upload = True
            sleep(2)

    def check_status_schedule_upload_video(self):
        status_xpath = get_xpath("span", "xmi5d70 xw23nyj xo1l8bm x63nzvj xbsr9hj xq9mrsl x1h4wwuj xeuugli", contain=True)
        cnt = 0
        pre_v = "0%"
        while True:
            if self.is_stop_upload:
                break
            try:
                status_xpath_element = get_element_by_xpath(self.driver, status_xpath)
                v = status_xpath_element.text
                if v != pre_v:
                    sys.stdout.write(f'\rĐã tải lên được {v} ...')
                    sys.stdout.flush()
                    pre_v = v
                if v == "100%":
                    break
            except:
                cnt += 1
                if cnt > 10:
                    self.is_stop_upload = True
            sleep(2)

    def input_description(self, description):
        try:
            if self.en_language:
                xpath = get_xpath('div', "notranslate _5rpu", attribute="aria-label", attribute_value="Write into the dialogue box to include text with your post.")
            else:
                xpath = get_xpath('div', "notranslate _5rpu", attribute="aria-label", attribute_value="Hãy viết vào ô hộp thoại để thêm văn bản vào bài viết.")
            ele = get_element_by_xpath(self.driver, xpath)
            if ele:
                ele.send_keys(description)
        except:
            getlog()

    def change_page(self):
        try:
            press_esc_key(4, self.driver)
            self.profile_element.click()
            sleep(2)
            self.click_page_list()
            page_xpath = f"//div[span[text()='{self.page_name}']]"
            page_element = get_element_by_xpath(self.driver, page_xpath)
            self.scroll_into_view(page_element)
            page_element.click()
            print(f'Đã chuyển sang trang {self.page_name}')
            sleep(4)
            press_esc_key(2, self.driver)
            return True
        except:
            try:
                if not page_element:
                    print(f'Không tìm thấy trang {self.page_name}')
                    return False
                self.driver.execute_script("arguments[0].click();", page_element)
                print(11111111)
                return True
            except:
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(page_element).click().perform()
                    print(2222222222)
                    return True
                except:
                    getlog()
        return False
    
    def click_next_button_if_short_video(self):
        for i in range(2):
            if self.en_language:
                xpath = get_xpath("div", "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3", "aria-label", "Next")
            else:
                xpath = get_xpath("div", "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3", "aria-label", "Tiếp")
            element = get_element_by_xpath(self.driver, xpath)
            if element:
                element.click()
                sleep(1)
    
    def input_describe_short_video(self, text):
        if self.en_language:
            xpath = get_xpath("div", "xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x9f619 x1lliihq x5yr21d xh8yej3 notranslate", "aria-label", "Describe your reel...")
        else:
            xpath = get_xpath("div", "xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x9f619 x1lliihq x5yr21d xh8yej3 notranslate", "aria-label", "Mô tả thước phim của bạn...")
        element = get_element_by_xpath(self.driver, xpath)
        if element:
            element.send_keys(text)
            sleep(1)

    def click_public_short_video(self):
        xpath = get_xpath("div", "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")
        try:
            if self.en_language:
                element = get_element_by_xpath(self.driver, xpath, "Publish")
            else:
                element = get_element_by_xpath(self.driver, xpath, "Đăng")
            if element:
                element.click()
                sleep(3)
            else:
                print("Không tìm thấy nút đăng video --> Dừng đăng video !!!")
                self.is_stop_upload = True
        except:
            print("Không tìm thấy nút đăng video --> Dừng đăng video !!!")
            self.is_stop_upload = True

            

    def click_post_button(self):
        if self.en_language:
            xpath = get_xpath('div', 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3', 'aria-label', 'Post')
        else:
            xpath = get_xpath('div', 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3', 'aria-label', 'Đăng')
        element = get_element_by_xpath(self.driver, xpath)
        if element:
            element.click()
            print("Đang tiến hành đăng video...")
            sleep(5)
        else:
            print("không tìm thấy post_button")

    def upload_video(self, folder=None):
        try:
            self.is_reel_video = self.acc_config['is_reel_video']
            if folder:
                videos_folder = folder
            else:
                videos_folder = self.acc_config['upload_folder']
            if not check_folder(videos_folder):
                return
            videos = get_file_in_folder_by_type(videos_folder, ".mp4")   
            if not videos:
                return False
            upload_count = 0
            date_cnt = 0
            if 'cnt_upload_in_day' not in self.acc_config:
                self.acc_config['cnt_upload_in_day'] = 0
            number_of_days = get_number_of_days(self.acc_config['number_of_days'])
            current_day = convert_datetime_to_string(datetime.now().date())
            if self.is_schedule:
                day_gap = get_day_gap(self.acc_config['day_gap'])
                old_upload_date_str = self.acc_config['upload_date']
                if not old_upload_date_str:
                    return False
                upload_date = get_upload_date(old_upload_date_str)
                upload_date_str = convert_datetime_to_string(upload_date)
                if upload_date_str != old_upload_date_str:
                    self.acc_config['cnt_upload_in_day'] = 0
                publish_times_str = self.acc_config['publish_times']
                publish_times = publish_times_str.split(',')
                if not publish_times:
                    return False
                if self.is_auto_upload:
                    number_of_days = 100
                    self.facebook_config['show_browser'] = False
                    if folder:
                        self.facebook_config['show_browser'] = True
                    if self.acc_config['cnt_upload_in_day'] == 0 or self.acc_config['cnt_upload_in_day'] >= len(publish_times):
                        upload_date_str = add_date_into_string(upload_date_str, day_gap)
                        self.acc_config['cnt_upload_in_day'] = 0
            else:
                upload_date_str = current_day


            if not self.login(self.facebook_config['show_browser']):
                return
            if not self.is_schedule:
                if not self.change_page():
                    print(f"Gặp lỗi khi chuyển trang {self.page_name}")
                    return
            self.waiting_for_capcha_verify()
            press_esc_key(2, self.driver)
            self.save_session()
            for i, video_file in enumerate(videos, start=0):
                if self.is_stop_upload:
                    break
                if is_date_greater_than_current_day(upload_date_str, 28):
                    print("Dừng đăng video vì ngày lên lịch đã vượt  quá giới hạn mà facebook cho phép(tối đa 29 ngày)")
                    break
                video_name = os.path.splitext(video_file)[0]
                title = self.acc_config['title']
                description = self.acc_config['description']
                if self.acc_config['is_title_plus_video_name']:
                    full_title = f"{title} {video_name}"
                else:
                    full_title = title
                full_title = f"{full_title}"
                description=f"{full_title}\n{description}"

                video_path = os.path.join(videos_folder, video_file)
                print(f'--> Bắt đầu đăng video {video_file}')
                if self.is_schedule:
                    cnt_upload_in_day = self.acc_config['cnt_upload_in_day']
                    while True:
                        publish_time = publish_times[cnt_upload_in_day % len(publish_times)].strip()
                        if not check_datetime_input(upload_date_str, publish_time):
                            cnt_upload_in_day += 1
                            if cnt_upload_in_day % len(publish_times) == 0:
                                upload_date_str = add_date_into_string(upload_date_str, day_gap)
                                self.acc_config['cnt_upload_in_day'] = 0
                        else:
                            break
                    if self.en_language:
                        publish_time = get_pushlish_time_hh_mm(publish_time, facebook_time=True)
                        if not publish_time:
                            return
                        hour, minute, am_pm = publish_time.split(':')
                    else:
                        publish_time = get_pushlish_time_hh_mm(publish_time)
                        if not publish_time:
                            return
                        hour, minute = publish_time.split(':')
                    self.get_meta_business_suite()
                    if self.is_stop_upload:
                        break
                    try:
                        self.click_option_menu()
                    except:
                        press_esc_key(2, self.driver)
                        self.click_option_menu()

                    self.click_bulk_upload_video_button()
                    if self.is_stop_upload:
                        break
                    self.input_schedule_video_on_facebook(video_path)
                    if self.is_stop_upload:
                        break
                    self.input_description(description)
                    self.click_option_menu()
                    self.click_schedule_option()
                    self.input_date(upload_date_str)
                    if self.is_stop_upload:
                        break
                    self.input_hours(hour)
                    self.input_minutes(minute)
                    if self.en_language:
                        self.input_AM_or_PM(am_pm)
                    if self.is_stop_upload:
                        break
                    self.click_update_schedule_button()
                    self.check_status_schedule_upload_video()
                    if self.is_stop_upload:
                        break
                    self.click_public_schedule_button()
                    upload_count += 1
                    cnt_upload_in_day += 1
                    self.acc_config['cnt_upload_in_day'] = cnt_upload_in_day
                    if self.acc_config['upload_date'] != upload_date_str:
                        self.acc_config['upload_date'] = upload_date_str
                    print(f'--> Đăng thành công video {video_file}')
                    remove_or_move_file(video_path, self.acc_config['is_delete_after_upload'], 'facebook_upload_finished')

                    if (cnt_upload_in_day) % len(publish_times) == 0:
                        upload_date_str = add_date_into_string(upload_date_str, day_gap)
                        date_cnt += 1
                        self.acc_config['cnt_upload_in_day'] = 0
                    self.save_facebook_config()
                    if date_cnt == number_of_days:
                        break
                else:
                    if self.is_reel_video:
                        self.driver.get("https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS")
                        sleep(1)
                        self.input_video_on_facebook(video_path)
                        press_esc_key(2, self.driver)
                        self.click_next_button_if_short_video()
                        self.input_describe_short_video(description)
                        press_esc_key(1, self.driver)
                        if self.is_stop_upload:
                            break
                        self.click_public_short_video()
                    else:
                        self.click_upload_video_icon()
                        self.input_video_on_facebook(video_path)
                        self.input_title(description)
                        self.check_status_upload_video()
                        if self.is_stop_upload:
                            break
                        self.click_post_button()
                    print(f'--> Đăng thành công video {video_file}')
                    if self.acc_config['upload_date'] != upload_date_str:
                        self.acc_config['upload_date'] = upload_date_str
                        self.save_facebook_config()
                    remove_or_move_file(video_path, self.acc_config['is_delete_after_upload'], 'facebook_upload_finished')
                    upload_count += 1
                    if upload_count == number_of_days:
                        break
            if not self.is_auto_upload:
                notification(self.root, f"Đăng thành công {upload_count} video")
            else:
                print(f"Đăng thành công {upload_count} video")
            if upload_count > 0:
                return True
            return False
        except:
            getlog()
            return False
        finally:
            self.close_driver()
#common -------------------------------------------------------------------------------------------------------------
    def setting_screen_position(self):
        try:
            self.root.update_idletasks()
            x = screen_width - self.width - 10
            y = screen_height - self.height_window
            self.root.geometry(f"{self.width}x{self.height_window - 80}+{x}+{y}")
        except:
            getlog()

    def setting_window_size(self):
        if self.is_start_facebook:
            self.root.title(f"Facebook: {self.page_name}")
            self.width = 500
            self.height_window = 170
            if height_element == 30:
                self.height_window = 184
            self.is_start_facebook = False
        elif self.is_upload_video_window:
            self.root.title(f"Facebook: {self.page_name}")
            self.width = 700
            self.height_window = 845
            if height_element == 30:
                self.height_window = 832
            self.is_upload_video_window = False
        elif self.is_download_video_window:
            self.root.title(f"Download Fanpage Videos")
            self.width = 500
            self.height_window = 315
            self.is_download_video_window = False
        self.height_window = int(self.height_window * default_percent)
        self.setting_screen_position()

    def exit_app(self):
        self.reset()
        self.root.destroy()

    def on_close(self):
        save_facebook_config(self.page_name, self.acc_config)
        self.reset()
        self.hide_window()
        self.root.destroy()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", 1)
        self.root.attributes("-topmost", 0)

    def hide_window(self):
        self.root.iconify()
        self.root.withdraw()  # ẩn cửa sổ

    def reset(self):
        self.is_start_facebook = False
        self.clear_after_action()
        clear_widgets(self.root)
        self.root.withdraw()

    def clear_after_action(self):
        pass

    def create_settings_input(self, text, config_key=None, values=None, is_textbox = False, left=0.4, right=0.6, add_button=False, command=None, is_data_in_template=True):
        if is_data_in_template:
            config = self.acc_config
        else:
            config = self.facebook_config
        frame = create_frame(self.root)
        if add_button:
            create_button(frame= frame, text=text, command=command, width=0.2, side=RIGHT)
        create_label(frame, text=text, side=LEFT, width=self.width*left, anchor='w')

        if values:
            if not config_key:
                val = ""
            elif config_key not in config:
                val = ""
            else:
                val = config[config_key]
                if config[config_key] == True:
                    val = "Yes"
                elif config[config_key] == False:
                    val = "No"
            var = ctk.StringVar(value=str(val))

            combobox = ctk.CTkComboBox(frame, values=values, variable=var, width=self.width*right)
            combobox.pack(side="right", padx=padx)
            combobox.set(val)
            setattr(self, f"{config_key}_var", var)
            result = combobox
        elif is_textbox:
            textbox = ctk.CTkTextbox(frame, height=90, width=self.width*right)
            textbox.insert("1.0", config[config_key])  # Đặt giá trị ban đầu vào textbox
            textbox.pack(side=RIGHT, padx=padx)
            result = textbox
        else:
            if not config_key:
                var = ""
            else:
                var = config[config_key]
            entry = ctk.CTkEntry(frame, width=self.width*right)
            entry.pack(side="right", padx=padx)
            entry.insert(0, var)
            setattr(self, f"{config_key}_var", var)
            result = entry
        return result
        
