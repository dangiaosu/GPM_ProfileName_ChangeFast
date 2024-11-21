import requests
import pandas as pd
from tqdm import tqdm
from tkinter import Tk, filedialog
import math
import logging

# Cấu hình log
logging.basicConfig(
    filename="update_profiles.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Tiêu đề và mô tả chương trình
def print_header():
    print("\033[1;36mCode Python đổi tên, đổi Proxy, đổi group Profile GPM nhanh chóng by Đan Giáo Sư\033[0m")
    print("\n\033[1;33mChuyên lùa gà, nhưng vẫn ghét fake news\033[0m")
    print("\n\x1b[1;33mThông tin liên hệ:\x1b[0m")
    print("\x1b[1;34mTelegram: https://t.me/dangiaosu/\x1b[0m")
    print("\x1b[1;35mFacebook: https://fb.com/prof.danta/\x1b[0m")
    print("\x1b[1;32mZalo: https://zalo.me/0828092390/\x1b[0m\n")

def select_excel_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chọn file Excel",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    return file_path

def get_profiles_list():
    url = "http://127.0.0.1:19995/api/v3/profiles"
    params = {"page": 1, "per_page": 5000, "sort": 2}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        logging.error(f"Không thể lấy danh sách profiles: {response.text}")
        print(f"Không thể lấy danh sách profiles. Status: {response.status_code}")
        return []

def find_profile_id_by_name(profiles, profile_name):
    for profile in profiles:
        if profile['name'] == profile_name:
            return profile['id']
    return None

def get_profile_info(profile_id):
    info_url = f"http://127.0.0.1:19995/api/v3/profiles/{profile_id}"
    response = requests.get(info_url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        logging.error(f"Không thể lấy thông tin Profile {profile_id}: {response.text}")
        return None

def sanitize_data(data):
    for key, value in data.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            data[key] = None
    return data

def update_profile(profile_id, update_data):
    update_url = f"http://127.0.0.1:19995/api/v3/profiles/update/{profile_id}"
    update_data = sanitize_data(update_data)
    response = requests.post(update_url, json=update_data)
    if response.status_code == 200:
        logging.info(f"Profile {profile_id} cập nhật thành công: {update_data}")
        return get_profile_info(profile_id)
    else:
        logging.error(f"Không thể cập nhật Profile {profile_id}: {response.text}")
        return None

def process_update_profiles(file_path, profiles):
    try:
        df = pd.read_excel(file_path)
        required_columns = ['ProfileName', 'NewName', 'NewGroupID', 'NewProxy']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("File Excel cần có các cột: 'ProfileName', 'NewName', 'NewGroupID', 'NewProxy'")
    except Exception as e:
        logging.error(f"Định dạng file Excel không hợp lệ: {e}")
        return process_update_profiles(select_excel_file(), profiles)

    full_info = []
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Đang cập nhật profiles..."):
        profile_name = row['ProfileName']
        new_name = row['NewName'] if pd.notna(row['NewName']) else None
        new_group_id = row['NewGroupID'] if pd.notna(row['NewGroupID']) else None
        new_proxy = row['NewProxy'] if pd.notna(row['NewProxy']) else None

        profile_id = find_profile_id_by_name(profiles, profile_name)
        if profile_id:
            profile_info = get_profile_info(profile_id)
            if profile_info:
                update_data = {
                    "profile_name": new_name or profile_info.get('name', ''),
                    "group_id": new_group_id or profile_info.get('group_id', 1),
                    "raw_proxy": new_proxy or profile_info.get('raw_proxy', ''),
                    "note": profile_info.get('note', ''),
                    "color": profile_info.get('color', "#FFFFFF"),
                    "user_agent": "auto"
                }
                updated_info = update_profile(profile_id, update_data)
                if updated_info:
                    full_info.append(updated_info)
        else:
            logging.warning(f"Không tìm thấy ProfileName: {profile_name}")

    if full_info:
        output_df = pd.DataFrame(full_info)
        output_df.to_excel("Updated_Profiles_Info.xlsx", index=False)
        logging.info("Đã lưu kết quả vào Updated_Profiles_Info.xlsx")
        print("\033[1;32mThông tin đã được lưu vào Updated_Profiles_Info.xlsx\033[0m")

if __name__ == "__main__":
    print_header()
    profiles = get_profiles_list()
    if profiles:
        print("\033[1;34mDanh sách profiles đã được lấy thành công.\033[0m")
        file_path = select_excel_file()
        if file_path:
            process_update_profiles(file_path, profiles)
    else:
        print("\033[1;31mKhông thể lấy danh sách profiles, vui lòng kiểm tra API.\033[0m")
