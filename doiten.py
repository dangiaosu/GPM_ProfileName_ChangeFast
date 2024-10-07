import requests
import pandas as pd
from tqdm import tqdm
from tkinter import Tk, filedialog

# Tiêu đề và mô tả chương trình
def print_header():
    print("\033[1;36mTitle: Code python đổi tên Profile GPM nhanh chóng by Đan Giáo Sư\033[0m")
    print("\n\033[1;33mMột Đời Liêm Khiết - Nói Không Lùa Gà, Fake News\033[0m")
    print("\n\x1b[1;33mThông tin liên hệ:\x1b[0m")
    print("\x1b[1;34mTelegram: https://t.me/dangiaosu/\x1b[0m")
    print("\x1b[1;35mFacebook: https://fb.com/prof.danta/\x1b[0m")
    print("\x1b[1;32mZalo: https://zalo.me/0828092390/\x1b[0m\n")

# Hàm chọn file Excel với giao diện GUI
def select_excel_file():
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    file_path = filedialog.askopenfilename(
        title="Chọn file Excel",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    return file_path

# Hàm lấy danh sách profiles từ API
def get_profiles_list():
    url = "http://127.0.0.1:19995/api/v3/profiles"
    params = {
        "page": 1,  # Trang đầu tiên
        "per_page": 100,  # Lấy tối đa 100 profile
        "sort": 2  # Sắp xếp theo tên A-Z
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Không thể lấy danh sách profiles. Status: {response.status_code}, Message: {response.text}")
        return []

# Hàm lưu thông tin profile ra file Excel
def save_profiles_to_excel(profiles):
    df = pd.DataFrame(profiles)
    df.to_excel("AllProfiles_Info.xlsx", index=False)
    print("\033[1;32mThông tin đã được lưu vào AllProfiles_Info.xlsx\033[0m")

# Hàm tìm ProfileID từ ProfileName
def find_profile_id_by_name(profiles, profile_name):
    for profile in profiles:
        if profile['name'] == profile_name:
            return profile['id']
    return None

# Hàm lấy thông tin profile trước khi cập nhật
def get_profile_info(profile_id):
    info_url = f"http://127.0.0.1:19995/api/v3/profiles/{profile_id}"
    response = requests.get(info_url)
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Không thể lấy thông tin Profile {profile_id}. Status: {response.status_code}, Message: {response.text}")
        return None

# Hàm cập nhật tên profile mà không thay đổi các thông tin khác
def update_profile(profile_id, new_name, raw_proxy):
    update_url = f"http://127.0.0.1:19995/api/v3/profiles/update/{profile_id}"
    data = {
        "profile_name": new_name,
        "group_id": 1,
        "raw_proxy": raw_proxy,  # Giữ nguyên raw_proxy ban đầu
        "startup_urls": "",
        "note": "",
        "color": "#FFFFFF",
        "user_agent": "auto"
    }
    
    response = requests.post(update_url, json=data)
    if response.status_code == 200:
        print(f"Đổi tên thành công: {new_name}")
        return get_profile_info(profile_id)
    else:
        print(f"Không thể đổi tên Profile {profile_id}. Status: {response.status_code}, Message: {response.text}")
        return None

# Chức năng đổi tên profile nhanh
def process_profiles_rename(file_path, profiles):
    try:
        df = pd.read_excel(file_path)
        if 'ProfileName' not in df.columns or 'NewName' not in df.columns:
            raise ValueError("File Excel không có cột 'ProfileName' và 'NewName'")
    except Exception as e:
        print("\033[1;31mĐịnh dạng file excel không chuẩn - Xin vui lòng chọn lại\033[0m")
        return process_profiles_rename(select_excel_file(), profiles)

    full_info = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Đang xử lý profile..."):
        profile_name = row['ProfileName']
        new_name = row['NewName']
        
        # Tìm ProfileID dựa vào ProfileName
        profile_id = find_profile_id_by_name(profiles, profile_name)
        if profile_id:
            # Lấy thông tin hiện tại của profile để giữ lại raw_proxy
            profile_info = get_profile_info(profile_id)
            if profile_info:
                raw_proxy = profile_info['raw_proxy']
                # Cập nhật tên mà không thay đổi raw_proxy
                updated_info = update_profile(profile_id, new_name, raw_proxy)
                if updated_info:
                    full_info.append(updated_info)

    # Xuất ra file Excel nếu có dữ liệu
    if full_info:
        output_df = pd.DataFrame(full_info)
        output_df.to_excel("FullInfo_DataGPM.xlsx", index=False)
        print("\033[1;32mThông tin đã được lưu vào FullInfo_DataGPM.xlsx\033[0m")

# Chức năng chính để tải và xử lý danh sách profile
def main():
    print_header()
    
    # Lấy danh sách tất cả các profiles hiện có trên máy
    profiles = get_profiles_list()
    
    if profiles:
        # Lưu thông tin profile ra file Excel
        save_profiles_to_excel(profiles)

        # Hỏi người dùng có muốn đổi tên các profile không
        choice = input("Bạn có muốn đổi tên các profile không? (y/n): ")
        if choice.lower() == 'y':
            file_path = select_excel_file()
            process_profiles_rename(file_path, profiles)

if __name__ == "__main__":
    main()
