import requests
import pandas as pd
from tqdm import tqdm
from tkinter import Tk, filedialog

# Tiêu đề và mô tả chương trình
def print_header():
    print("\033[1;36mTitle: Code Python đổi tên và đổi Proxy Profile GPM nhanh chóng by Đan Giáo Sư\033[0m")
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
        "page": 1,
        "per_page": 1000,  # Tăng số lượng để lấy nhiều profile hơn
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

# Hàm lấy thông tin profile
def get_profile_info(profile_id):
    info_url = f"http://127.0.0.1:19995/api/v3/profiles/{profile_id}"
    response = requests.get(info_url)
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Không thể lấy thông tin Profile {profile_id}. Status: {response.status_code}, Message: {response.text}")
        return None

# Hàm cập nhật profile
def update_profile(profile_id, update_data):
    update_url = f"http://127.0.0.1:19995/api/v3/profiles/update/{profile_id}"
    
    response = requests.post(update_url, json=update_data)
    if response.status_code == 200:
        print(f"Cập nhật thành công: {update_data.get('profile_name', 'No Name')}")
        return get_profile_info(profile_id)
    else:
        print(f"Không thể cập nhật Profile {profile_id}. Status: {response.status_code}, Message: {response.text}")
        return None

# Chức năng đổi tên Profile
def process_profiles_rename(file_path, profiles):
    try:
        df = pd.read_excel(file_path)
        if 'ProfileName' not in df.columns or 'NewName' not in df.columns:
            raise ValueError("File Excel không có cột 'ProfileName' và 'NewName'")
    except Exception as e:
        print("\033[1;31mĐịnh dạng file Excel không chuẩn - Xin vui lòng chọn lại\033[0m")
        return process_profiles_rename(select_excel_file(), profiles)

    full_info = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Đang đổi tên profile..."):
        profile_name = row['ProfileName']
        new_name = row['NewName']
        
        # Tìm ProfileID dựa vào ProfileName
        profile_id = find_profile_id_by_name(profiles, profile_name)
        if profile_id:
            # Lấy thông tin hiện tại của profile để giữ lại các thông tin khác
            profile_info = get_profile_info(profile_id)
            if profile_info:
                # Chuẩn bị dữ liệu cập nhật
                update_data = {
                    "profile_name": new_name,
                    "group_id": profile_info.get('group_id', 1),
                    "raw_proxy": profile_info.get('raw_proxy', ""),
                    "startup_urls": "",
                    "note": profile_info.get('note', ""),
                    "color": profile_info.get('color', "#FFFFFF"),
                    "user_agent": "auto"
                }
                # Cập nhật profile
                updated_info = update_profile(profile_id, update_data)
                if updated_info:
                    full_info.append(updated_info)
        else:
            print(f"Không tìm thấy ProfileName: {profile_name}")

    # Xuất ra file Excel nếu có dữ liệu
    if full_info:
        output_df = pd.DataFrame(full_info)
        output_df.to_excel("FullInfo_DataGPM.xlsx", index=False)
        print("\033[1;32mThông tin đã được lưu vào FullInfo_DataGPM.xlsx\033[0m")

# Hàm kiểm tra định dạng proxy
def validate_proxy(proxy):
    if proxy.startswith(('socks5://', 'tm://', 'tin://', 'tinsoft://')) or len(proxy.split(':')) == 4:
        return True
    else:
        print(f"Proxy không hợp lệ: {proxy}")
        return False

# Chức năng đổi Proxy theo ProfileName
def process_profiles_change_proxy(file_path, profiles):
    try:
        df = pd.read_excel(file_path)
        if 'ProfileName' not in df.columns or 'ProxyMoi' not in df.columns:
            raise ValueError("File Excel không có cột 'ProfileName' và 'ProxyMoi'")
    except Exception as e:
        print("\033[1;31mĐịnh dạng file Excel không chuẩn - Xin vui lòng chọn lại\033[0m")
        return process_profiles_change_proxy(select_excel_file(), profiles)

    full_info = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Đang cập nhật proxy..."):
        profile_name = row['ProfileName']
        new_proxy = row['ProxyMoi']
        
        if validate_proxy(new_proxy):
            # Tìm ProfileID dựa vào ProfileName
            profile_id = find_profile_id_by_name(profiles, profile_name)
            if profile_id:
                # Lấy thông tin hiện tại của profile để giữ lại các thông tin khác
                profile_info = get_profile_info(profile_id)
                if profile_info:
                    # Chuẩn bị dữ liệu cập nhật
                    update_data = {
                        "profile_name": profile_info.get('name', ''),
                        "group_id": profile_info.get('group_id', 1),
                        "raw_proxy": new_proxy,  # Cập nhật proxy mới
                        "startup_urls": "",
                        "note": profile_info.get('note', ""),
                        "color": profile_info.get('color', "#FFFFFF"),
                        "user_agent": "auto"
                    }
                    # Cập nhật profile
                    updated_info = update_profile(profile_id, update_data)
                    if updated_info:
                        full_info.append(updated_info)
            else:
                print(f"Không tìm thấy ProfileName: {profile_name}")

    # Xuất ra file Excel nếu có dữ liệu
    if full_info:
        output_df = pd.DataFrame(full_info)
        output_df.to_excel("UpdatedProxies_DataGPM.xlsx", index=False)
        print("\033[1;32mThông tin đã được lưu vào UpdatedProxies_DataGPM.xlsx\033[0m")

# Menu chính quay lại sau mỗi tác vụ
def main_menu(profiles):
    while True:
        print("\nVui lòng chọn lựa:")
        print("1. Đổi tên ProfileName.")
        print("2. Đổi Proxy theo ProfileName.")
        print("3. Thoát.")
        choice = input("Lựa chọn của bạn (1/2/3): ")

        if choice == '1':
            print("Chọn file Excel có chứa cột 'ProfileName' và 'NewName' để đổi tên Profile.")
            file_path = select_excel_file()
            process_profiles_rename(file_path, profiles)
        elif choice == '2':
            print("Chọn file Excel có chứa cột 'ProfileName' và 'ProxyMoi' để cập nhật Proxy.")
            file_path = select_excel_file()
            process_profiles_change_proxy(file_path, profiles)
        elif choice == '3':
            print("Chương trình đã thoát. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

# Chức năng chính để tải và xử lý danh sách profile
def main():
    print_header()
    
    # Lấy danh sách tất cả các profiles hiện có trên máy
    profiles = get_profiles_list()
    
    if profiles:
        # Lưu thông tin profile ra file Excel
        save_profiles_to_excel(profiles)
        # Hiển thị menu chính
        main_menu(profiles)
    else:
        print("Không có profile nào để xử lý.")

if __name__ == "__main__":
    main()
