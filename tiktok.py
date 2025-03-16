from common_function import *

class TikTokManager:
    def __init__(self, other_name, upload_thread=None, download_thread=None, is_auto_upload=False, is_auto_and_schedule=True):
        self.upload_thread = upload_thread
        self.download_thread = download_thread
        self.is_auto_upload = is_auto_upload
        self.is_auto_and_schedule = is_auto_and_schedule
        self.account = other_name
        self.get_tiktok_config()
        self.password = self.acc_config['password']
        self.email = self.acc_config['email']
  
        if not is_auto_upload:
            self.root = ctk.CTk()
            self.title = self.root.title(other_name)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.is_schedule = False
        else:
            self.is_schedule = True
        self.width = 500
        self.driver = None
        self.is_start_tiktok = True
        self.is_first_start = True
        self.is_upload_video_window = False
        self.is_stop_upload = False
        self.is_stop_download = False
        self.check_copyright = True
        self.is_stop_interact = False

#-----------------------------Thao tác trên tiktok--------------------------------------------------------------

    def interact_with_tiktok(self, video_number_interact_str=None):
        is_interact_only = False
        def leave_video():
            if self.check_leave_video:
                leave = get_element_by_text(self.driver, 'Leave')
                if leave and leave.text.lower() == 'leave':
                    try:
                        leave.click()
                        self.check_leave_video = False
                    except:
                        self.check_leave_video = True
                        pass
                else:
                    self.check_leave_video = False
            sleep_random(1,2)

        def close_video():
            browse_close_x = get_xpath_by_multi_attribute('button', ['aria-label="Close"'])
            browse_close = get_element_by_xpath(self.driver, browse_close_x)
            if browse_close:
                browse_close.click()
                sleep_random(1.5,3)
        try:
            if video_number_interact_str:
                is_interact_only = True
                self.login(True, driver_type='web')
            else:
                video_number_interact_str = self.acc_config['video_number_interact_befor_upload']
            if video_number_interact_str == 'không tương tác':
                video_number_interact = 0
            else:
                try:
                    video_number_interact_list = [int(fff.strip()) for fff in video_number_interact_str.split('-')]
                    video_number_interact = get_random_number_int(video_number_interact_list[0],video_number_interact_list[1])
                except:
                    print(f'{thatbai} {self.account} Định dạng số video tương tác phải là min-max. Ví dụ muốn tương tác 3 đến 5 video thì phải đặt là 3-5')
                    video_number_interact = get_random_number_int(0,3)
            total_config = load_config()
            watch_percent = int(total_config.get('watch_percent', 60)) / 100
            print(f' {self.account} Tỷ lệ tương tác: {watch_percent*100}%')
            like_percent = int(total_config.get('like_percent', 40)) / 100
            comment_percent = int(total_config.get('comment_percent', 20)) / 100
            follow_percent = int(total_config.get('follow_percent', 30)) / 100
            print(f' {self.account} Tỷ lệ bấm like: {like_percent*100}%')
            print(f' {self.account} Tỷ lệ comment: {comment_percent*100}%')
            print(f' {self.account} Tỷ lệ bấm follow so với tỷ lệ comment: {follow_percent*100}%')
            
            if random.random() > watch_percent:
                print(f"🚀 {self.account} Bỏ qua tương tác TikTok lần này.")
                return
            self.driver.get(trang_chu_tiktok)
            sleep_random(3,5)
            print(f"🎯 {self.account} Bắt đầu tương tác trên TikTok...")

            if 'comments_texts' not in total_config:
                total_config['comments_texts'] = ""
            if total_config['comments_texts']:
                comments_list = total_config['comments_texts'].split(',')
            else:
                comments_list = [
                    "Amazing!", "Love this!", "Pure talent!", "You killed it!", "Insane skills!",
                    "So creative!", "Obsessed!", "You nailed it!", "Mind-blowing!", "Iconic!",
                    "Masterpiece!", "This is next level!", "Legendary!", "Unbelievable!", "So cool!",
                    "Brilliant!", "Absolutely stunning!", "On another level!", "Epic!", "You're a genius!",
                    "Too good!", "Incredible work!", "Simply the best!", "Masterclass!", "Sensational!",
                    "Phenomenal!", "I'm in awe!", "Talent overload!", "Flawless!", "So much talent!",
                    "This deserves an award!", "Picture perfect!", "This is gold!", "Insanely good!",
                    "You inspire me!", "You're a pro!", "Mind = Blown!", "Top-tier content!", "This is it!",
                    "Can't stop watching!", "You were born for this!", "Perfection!", "Extraordinary!",
                    "Chills!", "Wow, just wow!", "Absolute fire!", "Totally mesmerizing!", "Too smooth!",
                    "Flawless execution!", "You're unstoppable!", "Viral-worthy!", "Took my breath away!",
                    "A masterpiece in motion!", "Unmatched energy!", "Stunning visuals!", "Perfectly done!",
                    "Game-changer!", "100% impressive!", "Dream-level content!", "Sooo satisfying!",
                    "Too good to be true!", "Movie star vibes!", "The definition of talent!", "Straight-up magic!",
                    "Out of this world!", "Such a gift!", "The GOAT!", "Everything about this is amazing!",
                    "Pure perfection!", "Legend in the making!", "Brilliantly done!", "Chef's kiss!",
                    "Picture-perfect moment!", "A true masterpiece!", "On point!", "The internet won today!",
                    "Screaming, crying, stunning!", "This is ART!", "Sooo talented!", "How do you do this?!",
                    "Golden content!", "The best of the best!", "Speechless!", "Total legend!",
                    "A must-watch!", "Unreal talent!", "Absolutely breathtaking!", "No words!",
                    "You did THAT!", "Beyond impressive!", "Icon status!", "Keep shining!",
                    "Talent level = 1000%!", "You're built different!", "Effortlessly amazing!",
                    "Straight-up iconic!", "Certified masterpiece!", "Too legendary!",
                    "This is why I love the internet!", "Mind-blowingly good!", "A standing ovation!",
                    "Your energy is unmatched!", "So inspiring!", "Dream-level creativity!",
                    "This deserves to be framed!", "Simply magical!", "You just won TikTok!"
                ]
            cnt = 0
            body = None
            watch_time_str = total_config.get('watch_time', '5-30')
            watch_time_list = watch_time_str.split('-')
            try:
                watch_time_min = int(watch_time_list[0])
                watch_time_max = int(watch_time_list[1])
            except:
                watch_time_min = 5
                watch_time_max = 30
            print(f' {self.account} số video sẽ tương tác : {video_number_interact}')
            self.check_leave_video = False
            for _ in range(video_number_interact+1):
                check = 0
                if self.is_stop_interact:
                    break
                cnt += 1
                leave_video()
                if cnt > 1:
                    print(f"▶️ {self.account} Đang xem video thứ {cnt-1}...")
                    watch_time = float(get_time_random(watch_time_min,watch_time_max))
                    print(f' {self.account} Thời gian xem video: {int(watch_time)}s')
                    start_time = time()
                    sleep(watch_time*2/3)
                    # Xác suất like video
                    if random.random() < like_percent:
                        check += 1
                        try:
                            like_button_xpath = get_xpath('button', attribute='aria-label', attribute_value='Like video', contain=True)
                            like_buttons = get_element_by_xpath(self.driver, like_button_xpath, multiple_ele=True)
                            for like_button in like_buttons:
                                try:
                                    like_button.click()
                                    print(f"{like_icon} {self.account} Đã like video")
                                    break
                                except:
                                    pass
                            sleep_random(0.5,1)
                        except Exception:
                            print(f"{thatbai} {self.account} Không tìm thấy nút like")
                    # Xác suất comment video (10%)
                    if random.random() < comment_percent:
                        check += 1
                        try:
                            comment_xpath = get_xpath('button', attribute='aria-label', attribute_value='Read or add comment', contain=True)
                            comment_eles = get_element_by_xpath(self.driver, comment_xpath, multiple_ele=True)
                            for comment_ele in comment_eles:
                                try:
                                    comment_ele.click()
                                    sleep_random(1,3)
                                    comment_text = random.choice(comments_list)
                                    comment_box_xpath = get_xpath_by_multi_attribute('div', ['role="textbox"', 'contenteditable="true"'])
                                    comment_box = get_element_by_xpath(self.driver, comment_box_xpath)
                                    if comment_box:
                                        input_char_by_char(comment_box, comment_text)
                                        sleep_random(1,2)
                                        post_xpath = get_xpath_by_multi_attribute('div', ['aria-label="Post"', 'role="button"'])
                                        post_ele = get_element_by_xpath(self.driver, post_xpath)
                                        if post_ele:
                                            post_ele.click()
                                        else:
                                            comment_box.send_keys(Keys.RETURN)
                                        sleep_random(3,5)
                                        print(f"{comment_icon}  {self.account} Đã comment: {comment_text}")
                                    if random.random() < follow_percent:
                                        follow = self.driver.find_element(By.XPATH, '//button[div//div[text()="Follow"]]')
                                        if follow:
                                            follow.click()
                                            print(f'{thanhcong} {self.account} Đã bấm follow')
                                            sleep_random(0.7,2)
                                    close_video()
                                    leave_video()
                                    break
                                except:
                                    pass
                            
                        except:
                            getlog()
                            self.check_leave_video = True
                            print(f"{thatbai} {self.account} Không tìm thấy ô nhập comment")
                    # if check == 0:
                    #     sleep(watch_time/3)
                    sleep_random(0.5,1.5)
                else:
                    sleep_random(1,3)
                # Lướt sang video tiếp theo
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ARROW_DOWN)
            if cnt > 1:
                print(f"✅ {self.account} Hoàn thành tương tác trên TikTok!")
        except:
            getlog()
        finally:
            if is_interact_only:
                self.close()


    def login(self, show=False, driver_type=None):
        try:
            self.driver_type = self.acc_config.get('driver_type', 'web')
            if driver_type:
                self.driver_type = driver_type
            self.is_stop_upload = False
            proxy = self.acc_config["proxy"]
            if self.acc_config['use_profile_type'] == 'Firefox':
                self.driver = get_firefox_driver_with_profile(target_email=self.account, show=show, proxy=proxy)
                if not self.driver:
                    return False
                self.load_session(trang_chu_tiktok)

                return True
            elif self.acc_config['use_profile_type'] == 'Chrome':
                self.driver = get_chrome_driver_with_profile(target_email=self.account, show=show, proxy=proxy)
                if not self.driver:
                    return False
                self.load_session("https://www.tiktok.com")
                return True
            else:
                self.driver = get_driver(show=show, proxy=proxy, mode=self.driver_type, target_email=self.account)
                if not self.driver:
                    return False
                self.load_session()
                self.upload_link = None
                if self.driver_type == 'web':
                    if not self.acc_config['first_login']:
                        sleep_random(6,9)
                        self.upload_link = self.get_upload_button()
                        

                if not self.upload_link:
                    if not self.input_username_and_pass():
                        return False
                    if self.driver_type != 'web':
                        self.check_get_app_button_for_mobi()
                        return True
                    press_esc_key(2, self.driver)
                    self.upload_link = self.get_upload_button()

                if not self.upload_link:
                    print(f"{thatbai} {self.account}: Đăng nhập thất bại!!!")
                    return False
                return True
        except:
            getlog()
            print(f"{thatbai} {self.account} : Lỗi trong quá trình đăng nhập tiktok.")
            return False

    def check_get_app_button_for_mobi(self):
        try:
            ele = get_element_by_text(self.driver, 'Not now', 'button')
            if ele:
                ele.click()
                sleep_random(0.5,1.5)
        except:
            pass
    def input_username_and_pass(self):
        try:
            email_xpath = '//input[@name="username"]'
            email_input = get_element_by_xpath(self.driver, email_xpath)
            if email_input:
                email_input.send_keys(self.email)
                sleep(0.5)
            else:
                self.waiting_for_capcha_verify()
                return True
            pass_xpath = get_xpath_by_multi_attribute("input", ["type='password'", "placeholder='Password'"])
            password_input = get_element_by_xpath(self.driver, pass_xpath)
            if password_input:
                password_input.send_keys(self.password)
                sleep_random(1,2)
                password_input.send_keys(Keys.RETURN)
                sleep_random(3,5)
                self.waiting_for_capcha_verify()
                return True
        except:
            getlog
            return False

    def get_upload_button(self):
        upload_link = get_element_by_text(self.driver, 'Upload', tag_name='div')
        if not upload_link:
            sleep(4)
            xpath = get_xpath_by_multi_attribute('a', ['aria-label="Upload a video"'])
            upload_link = get_element_by_xpath(self.driver, xpath)
        return upload_link

    def load_session(self, url="https://www.tiktok.com/login/phone-or-email/email"):
        self.driver.get(url)
        sleep(1.5)
        try:
            if self.driver_type != 'web':
                cookies_info = self.acc_config['mobi_cookies']
            elif self.acc_config['use_profile_type'] == 'Firefox':
                cookies_info = self.acc_config['firefox_cookies']
            else:
                cookies_info = self.acc_config['chrome_cookies']
            if not cookies_info:
                return
            for cookie in cookies_info:
                self.driver.add_cookie(cookie)
            sleep(1.5)
            if self.acc_config['use_profile_type'] != 'Firefox' and self.acc_config['use_profile_type'] != 'Chrome':
                self.driver.refresh()
                sleep(2)
        except:
            getlog()
        
    def save_session(self):
        try:
            if self.driver_type != 'web':
                self.acc_config['mobi_cookies']= self.driver.get_cookies()
            elif self.acc_config['use_profile_type'] == 'Firefox':
                self.acc_config['firefox_cookies']= self.driver.get_cookies()
            else:
                self.acc_config['chrome_cookies']= self.driver.get_cookies()
            self.save_tiktok_config()
        except:
            getlog()

    def select_time(self, public_time):
            hh, mm = public_time.split(':')
            xpath = get_xpath('input', "TUXTextInputCore-input", "type", "text")
            date_time_ele = self.driver.find_elements(By.XPATH, xpath)
            if date_time_ele:
                time_ele = date_time_ele[0]
                time_ele.click()
                sleep(1)
                xpath_hh = get_xpath('span', "tiktok-timepicker-option-text tiktok-timepicker-left")
                hh_elements = self.driver.find_elements(By.XPATH, xpath_hh)
                for element in hh_elements:
                    self.scroll_into_view(element)
                    if int(element.text) == int(hh):
                        element.click()
                        break
                sleep(0.5)
                xpath_mm = get_xpath('span', "tiktok-timepicker-option-text tiktok-timepicker-right")
                mm_elements = self.driver.find_elements(By.XPATH, xpath_mm)
                for element in mm_elements:
                    self.scroll_into_view(element)
                    if int(element.text) == int(mm):
                        element.click()
                        break
                sleep(0.3)
            try:
                time_ele.click()
            except:
                print(f"{thatbai} {self.account} Ngày giờ đăng không hợp lệ --> Không thể lên lịch quá 10 ngày so với ngày hiện tại !!!")
                self.is_stop_upload = True

    def select_date(self, date_string):
        if is_date_greater_than_current_day(date_str=date_string, day_delta=9):
            print(f"{thatbai} {self.account} Ngày giờ đăng không hợp lệ --> Không thể lên lịch quá 10 ngày so với ngày hiện tại !!!")
            self.is_stop_upload = True
            return True
        year, month, day = date_string.strip().split("-")
        xpath1 = get_xpath('input', "TUXTextInputCore-input", "type", "text")
        xpath2 = get_xpath('span', "day valid", contain=True)
        kq=[]
        date_time_ele = get_element_by_xpath(self.driver, xpath1, multiple_ele=True)
        if date_time_ele and len(date_time_ele) > 1:
            date_ele = date_time_ele[1]
        else:
            press_esc_key(1, self.driver)
            date_time_ele = get_element_by_xpath(self.driver, xpath1, multiple_ele=True)
            try:
                date_ele = date_time_ele[1]
            except:
                print(f"{thatbai} {self.account} Gặp lỗi khi nhập ngày đăng video --> Dừng đăng video.")
                self.is_stop_upload = True
                return False
        if date_ele:
            date_ele.click()
            sleep(1)
            date_elements = get_element_by_xpath(self.driver, xpath2, multiple_ele=True) or []
            if len(date_elements) == 0:
                self.is_stop_upload = True
                return False
            
            for ele in date_elements:
                date = ele.text
                if int(date) == int(day):
                    ele.click()
                    sleep(1)
                    return False
            if len(date_elements) < 11:
                date_elements[-1].click()
                sleep(0.5)
                date_ele.click()
                sleep(1)
                date_elements = get_element_by_xpath(self.driver, xpath2, multiple_ele=True)
                if len(date_elements) == 0:
                    self.is_stop_upload = True
                    return False
                for ele in date_elements:
                    date = ele.text
                    if int(date) == int(day):
                        kq.append(ele)
                        ele.click()
                        sleep(1)
                        return False
                self.is_stop_upload = True


            
    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(0.2)

    def input_video_on_tiktok(self, video_path):
            try:
                if not os.path.exists(video_path):
                    return False
                video_path = Path(video_path)
                xpath = "//input[@accept='video/*']"
                ele = get_element_by_xpath(self.driver, xpath)
                if ele:
                    ele.send_keys(str(video_path))
                    sleep(3)
                    return True
                else:
                    return False
            except:
                return False
   
    def input_description(self, description, hashtags=[]):
        try:
            xpath = get_xpath('div', 'notranslate public-DraftEditor-content')
            ele = get_element_by_xpath(self.driver, xpath)
            if not ele:
                xpath = get_xpath_by_multi_attribute("div", ["contenteditable='true'", "role='combobox'"])
                ele = get_element_by_xpath(self.driver, xpath)
            if ele:
                if description.strip():
                    ele.send_keys(description.strip())
                    sleep(0.5)
                    press_esc_key(1, self.driver)
                ele.send_keys(Keys.RETURN)
                sleep(1)
                print(f"Nhập hashtags ... {hashtags}")
                for hash in hashtags:
                    for char in hash:
                        ele.send_keys(char)
                        sleep(0.15)
                    sleep(4)
                    ele.send_keys(Keys.RETURN)
                    sleep(1)
        except:
            print(f"{thatbai} {self.account} Lỗi khi nhập nội dung")
            pass

    def input_thumbnail(self, thumbnail_path):
        try:
            def click_upload_image_tab():
                xpath = get_xpath('div', 'cover-edit-tab', contain=True)
                ele = get_element_by_xpath(self.driver, xpath, key='Upload cover')
                if ele:
                    ele.click()
                    sleep(1)
            ele = get_element_by_text(self.driver, 'Edit cover')
            if not ele:
                xpath = get_xpath('div', 'cover-container', contain=True)
                ele = get_element_by_xpath(self.driver, xpath)
            ele.click()
            sleep(1)
            click_upload_image_tab()
            input_xpath = get_xpath_by_multi_attribute('input', ['accept="image/png, image/jpeg, image/jpg"'])
            input_ele = get_element_by_xpath(self.driver, input_xpath)
            if input_ele:
                input_ele.send_keys(thumbnail_path)
                sleep(1)
                confirm_xpath = get_xpath('div', 'TUXButton-label')
                confirm_ele = get_element_by_xpath(self.driver, confirm_xpath, key="Confirm")
                if confirm_ele:
                    confirm_ele.click()
                    sleep(1)
        except:
            pass


    def input_location(self, location):
        try:
            xpath = get_xpath_by_multi_attribute('input', ['placeholder="Search locations"'])
            ele = get_element_by_xpath(self.driver, xpath)
            if ele:
                ele.click()
                ele.clear()
                ele.send_keys(location)
                sleep(2)
                choose_xpath = get_xpath('div', 'Select__itemInner', contain=True)
                choose_ele = get_element_by_xpath(self.driver, choose_xpath, index=0)
                if choose_ele:
                    sleep(1)
                    choose_ele.click()
                    try:
                        choose_ele.click()
                    except:
                        pass
                    sleep(1)
                else:
                    choose_xpath = get_xpath('div', 'SearchableSelect-OptionBox', contain=True)
                    choose_ele = get_element_by_xpath(self.driver, choose_xpath, index=0, timeout=4)
                    if choose_ele:
                        choose_ele.click()
                        sleep(1)
        except:
            try:
                choose_xpath = get_xpath('div', 'SearchableSelect-OptionBox', contain=True)
                choose_ele = get_element_by_xpath(self.driver, choose_xpath, index=0, timeout=4)
                if choose_ele:
                    choose_ele.click()
                    sleep(1)
            except:
                pass
            

    def click_schedule_button(self):
        # xpath = get_xpath_by_multi_attribute('input', ['name="postSchedule"', 'value="schedule"'])
        # ele = get_element_by_xpath(self.driver, xpath)
        ele = get_element_by_text(self.driver, text='Schedule', tag_name='span')
        if ele:
            ele.click()
            sleep(1)
            allow_btn = get_element_by_text(self.driver, 'Allow', 'div')
            if allow_btn:
                allow_btn.click()
                sleep(1)
        else:
            print(f"{thatbai} {self.account} không tìm thấy nút lên lịch đăng video")

    def click_copyright_check(self):
        try:
            xpath = get_xpath_by_multi_attribute('input', ['type="checkbox"'])
            ele = get_element_by_xpath(self.driver, xpath, index=-1)
            if ele:
                self.scroll_into_view(ele)
                ele.click()
            else:
                self.check_copyright = False
        except:
            xpath = get_xpath("div", "Switch__root", contain=True)
            ele = get_element_by_xpath(self.driver, xpath, index=-1)
            if ele:
                try:
                    self.scroll_into_view(ele)
                    ele.click()
                except:
                    self.check_copyright = False
            else:
                self.check_copyright = False
    def check_status_copyright_check(self):
        if not self.check_copyright:
            return True
        print("Bắt đầu kiểm tra bản quyền video ...")
        cnt = 0
        while True:
            try:
                xpath = "//span[contains(text(), 'Run a copyright check')]"
                ele = get_element_by_xpath(self.driver, xpath)
                if not ele:
                    print("Không phát hiện nút check bản quyền --> Tiếp tục đăng video ...")
                    return True
                if self.is_stop_upload:
                    return False
                issues_xpath = "//div[contains(@class, 'copyright')]//span[contains(text(), 'ssues')]"
                issues_ele = get_element_by_xpath(self.driver, issues_xpath)
                if issues_ele:
                    if 'no issues detected'in  issues_ele.text.lower():
                        return True
                    else:
                        return False
                cnt += 1
                if cnt > 30:
                    return False
                sleep(2)
            except:
                return True

    def click_post_button(self):
        try:
            xpath = get_xpath_by_multi_attribute('button', ['data-e2e="post_video_button"'])
            ele = get_element_by_xpath(self.driver, xpath)
            ele.click()
            sleep(4)
            return True
        except:
            try:
                xpath = get_xpath("button", "TUXButton TUXButton--default TUXButton--large TUXButton--primary")
                ele = get_element_by_xpath(self.driver, xpath)
                ele.click()
                sleep(4)
                return True
            except:
                return False

    def check_progress_upload(self):
        cnt = 0
        while True:
            if self.is_stop_upload:
                return False
            ele = get_element_by_text(self.driver, text='Uploaded', tag_name='span')
            if ele:
                return True
            else:
                sleep(5)
                cnt += 1
            if cnt > 10:
                return False

    def click_schedule_post(self):
        ele = get_element_by_text(self.driver, 'Schedule', tag_name='div')
        if ele:
            ele.click()
            sleep(6)
        else:
            print(f'{thatbai} {self.account} không tìm thấy Schedule button')

    def click_upload_more_video_button(self):
        xpath = get_xpath('div', "TUXButton-label")
        ele = get_element_by_xpath(self.driver, xpath, "Upload")
        if ele:
            ele.click()
            sleep(1)
        else:
            print("không thấy upload more video button")
    
    def waiting_for_capcha_verify(self, time_wait=25):
        if self.acc_config['waiting_verify']:
            sleep_random(time_wait, time_wait + 3)
#--------------------------------Giao diện upload--------------------------------------

    def get_start_tiktok(self):
        if not self.is_first_start:
            self.reset()
        else:
            self.is_first_start = False
        self.is_start_tiktok = True
        self.show_window()
        self.setting_window_size()
        create_button(frame = self.root,text="Đăng video", command= self.open_upload_video_window)
        create_button(frame = self.root,text="Tải video từ kênh", command=self.open_download_video_window)
        try:
            self.root.mainloop()
        except:
            getlog()

    def open_upload_video_window(self):
        self.reset()
        self.is_upload_video_window = True
        self.show_window()
        self.setting_window_size()

        def set_thumbnail_folder():
            folder_path = filedialog.askdirectory()
            if folder_path:
                self.thumbnail_folder_var.delete(0, ctk.END)
                self.thumbnail_folder_var.insert(0, folder_path)

        def load_template():
            load_other_name = self.load_template_var.get().strip()
            acc_config = load_tiktok_config(load_other_name)
            self.description_var.delete("1.0", ctk.END)
            self.description_var.insert(ctk.END, acc_config['description'])
            self.upload_date_var.delete(0, ctk.END)
            self.upload_date_var.insert(0, acc_config['upload_date'])
            self.publish_times_var.delete(0, ctk.END)
            self.publish_times_var.insert(0, acc_config['publish_times'])
            self.upload_folder_var.delete(0, ctk.END)
            self.upload_folder_var.insert(0, acc_config['upload_folder'])
            self.thumbnail_folder_var.delete(0, ctk.END)
            self.thumbnail_folder_var.insert(0, acc_config['thumbnail_folder'])
            self.number_of_days_var.delete(0, ctk.END)
            self.number_of_days_var.insert(0, acc_config['number_of_days'])
            self.location_var.delete(0, ctk.END)
            self.location_var.insert(0, acc_config['location'])
            self.proxy_var.delete(0, ctk.END)
            self.proxy_var.insert(0, acc_config['proxy'])
            self.day_gap_var.delete(0, ctk.END)
            self.day_gap_var.insert(0, acc_config['day_gap'])
            self.show_browser_var.set(convert_boolean_to_Yes_No(self.commond_config['show_browser']))
            self.is_delete_after_upload_var.set(convert_boolean_to_Yes_No(acc_config['is_delete_after_upload']))

        def choose_folder_upload():
            folder = choose_folder()
            if folder:
                self.upload_folder_var.delete(0, ctk.END)
                self.upload_folder_var.insert(0, folder)
        self.description_var = self.create_settings_input("Mô tả", "description", config=self.acc_config, is_textbox=True, left=left, right=right)
        self.hashtags_var = self.create_settings_input("Hashtags", "hashtags", config=self.acc_config, left=left, right=right)
        self.upload_date_var = self.create_settings_input("Ngày đăng(yyyy-mm-dd)", "upload_date", config=self.acc_config, left=left, right=right)
        self.publish_times_var = self.create_settings_input("Giờ đăng(hh:mm)", "publish_times", config=self.acc_config, left=left, right=right)
        self.waiting_verify_var = self.create_settings_input(text="Thêm giời gian chờ xác minh capcha", config_key="waiting_verify", config=self.acc_config, values=['Yes', 'No'], left=left, right=right)
        # self.number_of_days_var = self.create_settings_input("Số ngày muốn đăng", config_key="number_of_days", config=self.acc_config, left=left, right=right)
        # self.day_gap_var = self.create_settings_input("Khoảng cách giữa các ngày đăng", "day_gap", config=self.acc_config, left=left, right=right)
        self.day_gap_var, self.number_of_days_var = create_frame_label_input_input(self.root,text="Số ngày đăng/Khoảng cách ngày đăng", width=self.width, left=left, mid=0.33, right=0.37)
        self.number_of_days_var.insert(0, self.acc_config['number_of_days'])
        self.day_gap_var.insert(0, self.acc_config['day_gap'])
        self.location_var = self.create_settings_input("Vị trí muốn đăng(vd: New York)", "location", config=self.acc_config, left=left, right=right)
        self.is_delete_after_upload_var = self.create_settings_input("Xóa video sau khi đăng", "is_delete_after_upload", config=self.acc_config, values=["Yes", "No"], left=left, right=right)
        self.use_profile_type_var = self.create_settings_input(text="Sử dụng profile", config_key="use_profile_type", config=self.acc_config, values=['Không dùng', 'Firefox', 'Chrome'], left=left, right=right)
        self.show_browser_var = self.create_settings_input(text="Hiển thị trình duyệt", config_key="show_browser", config=self.commond_config, values=['Yes', 'No'], left=left, right=right)
        self.show_browser_var.set('Yes')
        self.driver_type_var = self.create_settings_input(text="Hiển thị dạng", config_key="driver_type", config=self.acc_config, values=['web', 'mobi'], left=left, right=right)
        self.proxy_var = create_frame_label_and_input(self.root,text="Proxy", width=self.width, left=left, right=right)
        if 'proxy' not in self.acc_config:
            self.acc_config['proxy'] = ""
        self.video_number_interact_var = self.create_settings_input(text="Số video tương tác khi đăng (min-max)", config_key="video_number_interact_befor_upload", config=self.acc_config, values=['không tương tác', '3-5', '5-10', '10-20'], left=left, right=right)
        if not self.video_number_interact_var.get().strip():
            self.video_number_interact_var.set('không tương tác')
        self.auto_interact_var = self.create_settings_input(text="Tương tác tự động", config_key="auto_interact", config=self.commond_config, values=['Yes', 'No'], left=left, right=right)
        self.auto_interact_var.set('Yes')
        self.proxy_var.insert(0, self.acc_config['proxy'])
        self.thumbnail_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục chứa thumbnail", command=set_thumbnail_folder, width=self.width)
        self.thumbnail_folder_var.insert(0, self.acc_config['thumbnail_folder'])
        self.upload_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục chứa video", command=choose_folder_upload, width=self.width, left=left, right=right)
        self.upload_folder_var.insert(0, self.acc_config['upload_folder'])
        self.load_template_var = create_frame_button_and_combobox(self.root, "Tải mẫu có sẵn", command=load_template, values=self.commond_config['registered_account'], width=self.width, left=left, right=right)
        self.load_template_var.set(self.account)
        create_frame_button_and_button(self.root, text1="Đăng video ngay", text2="Lên lịch đăng video", command1=self.upload_video_now, command2=self.schedule_upload, width=self.width, left=0.5, right=0.5)
        create_button(self.root, text="Lùi lại", command=self.get_start_tiktok, width=self.width)
    

    def schedule_upload(self):
        if not self.save_upload_setting():
            return
        self.is_schedule = True
        self.start_thread_upload_video()
    def upload_video_now(self):
        if not self.save_upload_setting():
            return
        self.is_schedule = False
        self.start_thread_upload_video()

    def save_upload_setting(self):
        videos_folder = self.upload_folder_var.get()
        if not videos_folder:
            notification(self.root, "Hãy chọn thư mục chứa video!")
            return False
        try:
            upload_date = self.upload_date_var.get()
            is_valid_date, message = is_format_date_yyyymmdd(upload_date, daydelta=10)
            if not is_valid_date:
                notification(self.root, message)
                return False
            self.acc_config["description"] = self.description_var.get("1.0", ctk.END).strip()
            self.acc_config["location"] = self.location_var.get().strip().strip()
            self.acc_config["hashtags"] = self.hashtags_var.get().strip().strip()
            self.acc_config["upload_date"] = upload_date
            self.acc_config["publish_times"] = self.publish_times_var.get().strip()
            self.acc_config['cnt_upload_in_day'] = 0
            self.acc_config["upload_folder"] = self.upload_folder_var.get().strip()
            self.acc_config["thumbnail_folder"] = self.thumbnail_folder_var.get().strip()
            self.acc_config["waiting_verify"] = self.waiting_verify_var.get() == 'Yes'
            self.acc_config["use_profile_type"] = self.use_profile_type_var.get().strip()
            self.acc_config["proxy"] = self.proxy_var.get().strip()
            self.commond_config["show_browser"] = self.show_browser_var.get() == 'Yes'
            self.commond_config["is_delete_after_upload"] = self.is_delete_after_upload_var.get() == 'Yes'
            self.acc_config["driver_type"] = self.driver_type_var.get().strip()
            self.acc_config["number_of_days"] = self.number_of_days_var.get().strip()
            self.acc_config["day_gap"] = self.day_gap_var.get().strip()
            self.acc_config["video_number_interact_befor_upload"] = self.video_number_interact_var.get().strip()
            self.acc_config["auto_interact"] = self.auto_interact_var.get().strip()
            self.save_tiktok_config()
            return True
        except:
            getlog()
            return False
        
    def start_thread_upload_video(self):
        self.is_stop_upload = False
        upload_video_thread = threading.Thread(target=self.upload_video)
        upload_video_thread.start()

    def upload_video(self, videos_folder=None):
        try:
            thumbnail_folder = self.acc_config['thumbnail_folder']
            if not videos_folder:
                videos_folder = self.acc_config['upload_folder']
            if not check_folder(videos_folder):
                return False, False
            self.acc_config['upload_folder'] = videos_folder
            videos = get_file_in_folder_by_type(videos_folder, ".mp4")   
            if not videos:
                return False, False
            upload_count = 0
            date_cnt = 0
            if 'cnt_upload_in_day' not in self.acc_config:
                self.acc_config['cnt_upload_in_day'] = 0
            if self.is_auto_upload and not self.is_auto_and_schedule:
                self.is_schedule = False
                number_of_days = 1
            else:
                number_of_days = get_number_of_days(self.acc_config['number_of_days'])
                
            hashtag_str = self.acc_config['hashtags']
            hashtags = []
            if hashtag_str:
                hashtags = hashtag_str.split(',')
            current_day = convert_datetime_to_string(datetime.now().date())
            if self.is_schedule:
                publish_times_str = self.acc_config['publish_times']
                publish_times = publish_times_str.split(',')   
                if not publish_times:
                    return False, False
                day_gap = get_day_gap(self.acc_config['day_gap'])
                old_upload_date_str = self.acc_config['upload_date']
                if not old_upload_date_str:
                    return False, False
                upload_date = get_upload_date(old_upload_date_str)
                upload_date_str = convert_datetime_to_string(upload_date)
                if upload_date_str != old_upload_date_str:
                    self.acc_config['cnt_upload_in_day'] = 0
                if self.is_auto_upload:
                    number_of_days = 100
                    self.commond_config['show_browser'] = False
                    if videos_folder:
                        self.commond_config['show_browser'] = True
                    if self.acc_config['cnt_upload_in_day'] == 0 or self.acc_config['cnt_upload_in_day'] >= len(publish_times):
                        upload_date_str = add_date_into_string(upload_date_str, day_gap)
                        self.acc_config['cnt_upload_in_day'] = 0
            else:
                upload_date_str = current_day
            for i, video_file in enumerate(videos):
                if self.is_stop_upload:
                    break
                video_path = os.path.join(videos_folder, video_file)
                temp_video_folder = os.path.join(videos_folder, 'temp_folder')
                os.makedirs(temp_video_folder, exist_ok=True)
                temp_video_path = os.path.join(temp_video_folder, video_file)
                try:
                    shutil.move(video_path, temp_video_path)
                except:
                    continue
                video_path = temp_video_path

                if is_date_greater_than_current_day(upload_date_str, 9):
                    print(f"{thatbai} {self.account} Dừng đăng video vì ngày lên lịch đã vượt  quá giới hạn mà tiktok cho phép(tối đa 10 ngày)")
                    break
                if self.is_schedule:
                    cnt_upload_in_day = self.acc_config['cnt_upload_in_day']
                    while True:
                        publish_time = publish_times[cnt_upload_in_day % len(publish_times)].strip()
                        publish_time = get_pushlish_time_hh_mm(publish_time)
                        if not check_datetime_input(upload_date_str, publish_time):
                            cnt_upload_in_day += 1
                            if cnt_upload_in_day % len(publish_times) == 0:
                                upload_date_str = add_date_into_string(upload_date_str, day_gap)
                                self.acc_config['cnt_upload_in_day'] = 0
                        else:
                            break
                if upload_count == 0:
                    if not self.login(self.commond_config['show_browser']):
                        print(f'{self.account}: Có lỗi trong quá trình đăng nhập.')
                        return False, False
                    self.acc_config['first_login'] = False
                    self.acc_config['waiting_verify'] = False
                    if self.driver_type == 'web':
                        self.interact_with_tiktok()
                self.driver.get("https://www.tiktok.com/tiktokstudio/upload")
                sleep_random(3,4)
                if upload_count == 0:
                    self.waiting_for_capcha_verify(20)
                    self.save_session()
                video_name = os.path.splitext(video_file)[0] #lấy tên
                thumbnail_path = os.path.join(thumbnail_folder, f'{video_name}.png')
    
                location = self.acc_config['location']
                description = self.acc_config['description']
                description = f"\n{description}" if description else ''

                print(f'--> {self.account}  Bắt đầu đăng video {video_file}')
                if self.is_stop_upload:
                    break
                if not self.input_video_on_tiktok(video_path):
                    print(f'{thatbai} {self.account} Có lỗi trong quá trình tải video lên.')
                    break
                self.input_description(description, hashtags)

                if location:
                    self.input_location(location)
                if os.path.exists(thumbnail_path):
                    self.input_thumbnail(thumbnail_path)
                if self.is_stop_upload:
                    break
                self.click_copyright_check()

                if self.is_schedule:   
                    self.click_schedule_button()
                    if self.select_date(upload_date_str):
                        return False, True
                    if self.is_stop_upload:
                        break
                    self.select_time(publish_time)
                    if self.is_stop_upload:
                        break
                    if self.check_progress_upload():
                        if self.check_status_copyright_check():
                            if self.is_stop_upload:
                                break
                            self.click_schedule_post()
                        else:
                            print(f'{thatbai} {self.account} :  video {video_path} có thể đã vi phạm chính sách tiltok, hãy kiểm tra lại...')
                            continue
                    else:
                        continue
                    upload_count += 1
                    cnt_upload_in_day += 1
                    self.acc_config['cnt_upload_in_day'] = cnt_upload_in_day
                    if self.acc_config['upload_date'] != upload_date_str:
                        self.acc_config['upload_date'] = upload_date_str
                    print(f'{thanhcong} {self.account} Đăng thành công video {video_file}')
                    sleep_random(1,3)
                    remove_or_move_file(video_path, is_delete=self.acc_config['is_delete_after_upload'], finish_folder_name='tiktok_upload_finished')
                    if cnt_upload_in_day % len(publish_times) == 0:
                        upload_date_str = add_date_into_string(upload_date_str, day_gap)
                        date_cnt += 1
                        self.acc_config['cnt_upload_in_day'] = 0
                    self.save_tiktok_config()
                    if date_cnt == number_of_days:
                        break
                else:
                    if self.is_stop_upload:
                        break
                    if self.is_stop_upload:
                        break
                    if self.check_progress_upload():
                        if self.check_status_copyright_check():
                            if self.is_stop_upload:
                                break
                            if not self.click_post_button():
                                print(f'{thatbai} {self.account} Đăng video không thành công.')
                                sleep_random(1,3)
                                return False, False
                        else:
                            print(f'{thatbai} {self.account}: video {video_path} có thể đã vi phạm chính sách tiltok, hãy kiểm tra lại...')
                            continue
                    else:
                        print(f"{thatbai} {self.account} Không thể kiểm tra tiến trình đăng video --> Dừng đăng video !!!")
                        break
                    
                    upload_count += 1
                    if self.acc_config['upload_date'] != upload_date_str:
                        self.acc_config['upload_date'] = upload_date_str
                    self.save_tiktok_config()
                    print(f'{thanhcong} {self.account}  Đăng thành công video {video_file}')
                    remove_or_move_file(video_path, is_delete=self.acc_config['is_delete_after_upload'], finish_folder_name='tiktok_upload_finished')
                    if upload_count == number_of_days:
                        break
            if upload_count > 0:
                print(f"Đăng thành công {upload_count} video.")
                sleep_random(1,3)
                return True, False
            return False, False
        except:
            getlog()
            return False, False
        finally:
            self.close()

    def save_tiktok_config(self):
        save_tiktok_config(data=self.commond_config)
        save_tiktok_config(self.account, self.acc_config)

    def get_tiktok_config(self):
        self.commond_config = load_tiktok_config()
        self.acc_config = load_tiktok_config(self.account)

#---------------------------------Giao diện download------------------------------------------
    def open_download_video_window(self):
            self.reset()
            self.is_download_window = True
            self.setting_window_size()
            self.show_window()

            def save_download_settings():
                try:
                    self.download_folder = self.download_folder_var.get()
                    if not self.download_folder:
                        notification(self.root, "Vui lòng chọn thư mục chứa video tải về !!!")
                        return False
                    if not os.path.exists(self.download_folder):
                        notification(self.root, f"Thư mục {self.download_folder} không tồn tại, hãy chọn lại !!!")
                        return False
                    self.commond_config['download_folder'] = self.download_folder
                    self.commond_config['show_browser'] = self.show_browser_var.get() == "Yes"
                    self.commond_config['download_url'] = self.download_by_channel_url_var.get()
                    self.commond_config['filter_by_views'] = self.filter_by_views_var.get()
                    self.save_tiktok_config()
                    return True
                except:
                    return False

            def start_download_by_channel_url():
                if not self.download_thread or not self.download_thread.is_alive():
                    if save_download_settings():
                        self.download_thread = threading.Thread(target=self.get_tiktok_videos_by_channel_url)
                        self.download_thread.start()
                else:
                    notification(self.root, "Đang tải ở một luồng khác.")
            self.download_by_channel_url_var = create_frame_label_and_input(self.root, text="Nhập link tải video", left=0.4, right=0.6, width=self.width)
            self.filter_by_views_var = self.create_settings_input("Lọc theo số lượt xem", "filter_by_views", config=self.commond_config, values=["100000", "200000", "300000", "500000", "1000000"], left=0.4, right=0.6)
            self.show_browser_var = self.create_settings_input(text="Hiển thị trình duyệt", config_key="show_browser", config=self.commond_config, values=['Yes', 'No'])
            self.download_folder_var = create_frame_button_and_input(self.root,text="Chọn thư mục lưu video", command=self.choose_folder_to_save, left=0.4, right=0.6, width=self.width)
            self.download_folder_var.insert(0, self.commond_config['download_folder'])
            create_button(self.root, text="Bắt đầu tải video", command=start_download_by_channel_url, width=self.width)
            create_button(self.root, text="Lùi lại", command=self.get_start_tiktok, width=self.width)

    def choose_folder_to_save(self):
        self.download_folder = filedialog.askdirectory()
        self.download_folder_var.delete(0, ctk.END)
        self.download_folder_var.insert(0, self.download_folder)

    def get_tiktok_videos_by_channel_url(self):
        url = self.commond_config['download_url']
        if not url:
            print(f"{thatbai} {self.account} Hãy nhập link tải video !!!")
            return
        view_cnt = self.commond_config['filter_by_views'] or "0"
        if 'quantity_download' not in self.commond_config:
            self.commond_config['quantity_download'] = "2000"
        quantity_download = int(self.commond_config['quantity_download'])
        t = time()
        cnt_download = 0
        cnt_search = 0
        try:
            view_cnt = int(view_cnt)
        except:
            view_cnt=0
        if not url:
            notification(self.root, "Hãy nhập đường link đến kênh muốn tải video")
            return
            
        try:
            self.driver = get_driver(show=self.commond_config['show_browser'])
            if not self.driver:
                return
            sleep(1)
            self.load_session()
            self.driver.get(url)
            sleep(4)
            press_esc_key(1, self.driver)
            if self.commond_config['show_browser']:
                sleep(6)
            press_esc_key(1, self.driver)
            if self.is_stop_download:
                self.close()
                return None
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            k = 0
            print(f"Bắt đầu quét video trong kênh {url} ...")
            while True:
                if self.is_stop_download:
                    self.close()
                    return None
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    if k < 3:
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
                if cnt_search > 200:
                    break
            
            self.download_info = load_download_info()
            video_urls = []
            if 'search' in url:
                xpath = get_xpath('div', "css-1soki6-DivItemContainerForSearch", contain=True)
                video_divs = self.driver.find_elements(By.XPATH, xpath)
                for video_div in video_divs:
                    if self.is_stop_download:
                        self.close()
                        return None
                    try:
                        # if view_cnt > 0:
                        #     view_xpath = get_xpath('strong', class_name="video-count", contain=True)
                        #     views_element = video_div.find_element(By.XPATH, view_xpath)
                        #     if views_element:
                        #         view_count = get_view_count(views_element.text)
                        #         if view_count < view_cnt:
                        #             continue
                        # print(view_count)
                        link_video = video_div.find_element(By.XPATH, './/a[contains(@href, "/video/")]')
                        if link_video:
                            url = link_video.get_attribute('href')
                            if url and url not in self.download_info['downloaded_urls']:
                                video_urls.append(url)
                    except:
                        continue
            else:
                video_elements = self.driver.find_elements(By.TAG_NAME, 'a')
                for item in video_elements:
                    if self.is_stop_download:
                        self.close()
                        return None
                    url = item.get_attribute('href')
                    if url and '/video/' in url:
                        if url in self.download_info['downloaded_urls']:
                            print(f"{thatbai} {self.account} url này đã tải trước đó: {url}")
                            continue
                        view_count_str = get_views_text(item.text)
                        if view_count_str:
                            view_count = get_view_count(view_count_str)
                            if view_count >= view_cnt:
                                video_urls.append(url)
            self.close()
            print(f"--> Tổng thời gian tìm video là {int((time() - t)/60)} phút {int(time() - t)%60} giây")
            if len(video_urls) > 0:
                print(f"--> Tổng số video tìm được là {len(video_urls)}")
            else:
                print(f'Không tìm thấy video nào phù hợp!!!')
                return
            download_folder = self.commond_config['download_folder']
            for url in video_urls.copy():
                try:
                    if self.is_stop_download:
                        break
                    print(f'--> Bắt đầu tải video: {url}')
                    if download_video_by_url(url, download_folder=download_folder):
                        print(f"--> Tải thành công video: {url}")
                        cnt_download += 1
                        video_urls.remove(url)
                        if url not in self.download_info['downloaded_urls']:
                            self.download_info['downloaded_urls'].append(url)
                        save_download_info(self.download_info)
                    else:
                        print(f"!!! Tải không thành công video {url} !!!")
                    if cnt_download > quantity_download:
                        break
                except:
                    getlog()
                    print(f"Tải không thành công {url}")
            if cnt_download > 0:
                notification(self.root, f"Đã tải thành công {cnt_download} video.")
            else:
                download_video_by_bravedown(video_urls, download_folder)
        except:
            getlog()
            notification(self.root, f"{thatbai} {self.account}  Gặp lỗi trong quá trình tìm quét video --> có thể tiktok yêu cầu xác minh capcha !!!")

    def close(self):
        if self.driver:
            self.driver.quit()
            print(f"{self.account} Đã đóng trình duyệt.")

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
        if self.is_start_tiktok:
            self.root.title(f"Tiktok: {self.account}")
            self.width = 400
            self.height_window = 170
            if height_element == 30:
                self.height_window = 185
            self.is_start_tiktok = False
        elif self.is_upload_video_window:
            self.root.title(f"Upload video Tiktok: {self.account}")
            self.width = 800
            self.height_window = 1024
            if height_element == 30:
                self.height_window = 990
            self.is_upload_video_window = False
        elif self.is_download_window:
            self.root.title("Download videos Tiktok")
            self.width = 700
            self.height_window = 365
            self.is_download_window = False
        self.height_window = int(self.height_window * default_percent)
        self.setting_screen_position()

    def exit_app(self):
        self.reset()
        self.root.destroy()

    def on_close(self):
        self.save_tiktok_config()
        self.hide_window()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", 1)
        self.root.attributes("-topmost", 0)

    def hide_window(self):
        self.root.iconify()
        self.root.withdraw()  # ẩn cửa sổ

    def reset(self):
        self.is_youtube_window = False
        self.clear_after_action()
        clear_widgets(self.root)

    def clear_after_action(self):
        self.root.withdraw()

    
    def create_settings_input(self, text, config_key, values=None, is_textbox = False, left=0.4, right=0.6, config=None):
        frame = create_frame(self.root)
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
            return combobox
        
        elif is_textbox:
            textbox = ctk.CTkTextbox(frame, height=80, width=self.width*right)
            textbox.insert("1.0", config[config_key])  # Đặt giá trị ban đầu vào textbox
            textbox.pack(side=RIGHT, padx=padx)
            return textbox
        else:
            var = config[config_key]
            entry = ctk.CTkEntry(frame, width=self.width*right)
            entry.pack(side="right", padx=padx)
            entry.insert(0, var)
            setattr(self, f"{config_key}_var", var)
            return entry