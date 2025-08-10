from common_function import *

def text_to_speeed_by_evenlab_with_multi_email(input_txt_path, emails, start_idx):
    for email in emails:
        start_idx, is_change_email = text_to_speeed_by_evenlab(input_txt_path, email, start_idx)
        if not start_idx or not is_change_email:
            return

def move_file(input_folder, output_folder, idx):
    wav_files = get_file_in_folder_by_type(input_folder, file_type='.mp3')
    if not wav_files:
        return False
    if len(wav_files) > 1:
        for ggg in wav_files:
            ggg_path = os.path.join(input_folder, ggg)
            remove_file(ggg_path)
        return False
    for wav_file in wav_files:
        wav_file_path = os.path.join(input_folder, wav_file)
        wav_file_outpath = os.path.join(output_folder, f"{idx}.wav")
        try:
            shutil.move(wav_file_path, wav_file_outpath)
            return True
        except:
            getlog()
            return False

def text_to_speeed_by_evenlab(input_txt_path, email=None, start_idx=0, url="https://elevenlabs.io/app/speech-synthesis/text-to-speech"):
    if not email:
        print(f"{thatbai} Nhập email của profile trước.")
        return None, False
    driver = get_firefox_driver_with_profile(target_email=email)
    if not driver:
        return None, None
    driver.get(url)
    sleep(3)
    textarea_xpath = get_xpath_by_multi_attribute('textarea', ['aria-label="Main textarea"'])
    textarea = get_element_by_xpath(driver, textarea_xpath)
    if not textarea:
        email_x = get_xpath_by_multi_attribute('input', ['type="email"'])
        email_ele = get_element_by_xpath(driver, email_x)
        if email_ele:
            email_ele.clear()
            sleep(0.5)
            email_ele.send_keys(email)
            sleep(0.5)
            pass_x = get_xpath_by_multi_attribute('input', ['type="password"'])
            pass_ele = get_element_by_xpath(driver, pass_x)
            if pass_ele:
                pass_ele.clear()
                sleep(0.5)
                pass_ele.send_keys('thien191!')
                sleep(0.5)
                pass_ele.send_keys(Keys.RETURN)
                sleep(4)
                textarea_xpath = get_xpath_by_multi_attribute('textarea', ['aria-label="Main textarea"'])
                textarea = get_element_by_xpath(driver, textarea_xpath)
                if not textarea:
                    print(f"Không tìm thấy chỗ nhập nội dung.")
                    return None, None
        else:
            print(f"Không tìm thấy chỗ nhập nội dung.")
            return None, None
    sleep(3)
   
        
emails = [
    'JasonPotts19741119@hotmail.com',
]


input_txt_path = r"E:\Python\developping\review comic\test\du lieu train\vbee\2.txt"
start_idx = 0

text_to_speeed_by_evenlab_with_multi_email(input_txt_path=input_txt_path, emails=emails, start_idx=start_idx)