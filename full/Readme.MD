# Đổi Tên, Group ID, Proxy và cả Note Profile GPM By Đan Giáo Sư - ft ChatGpt, Claude 🚀  
## Tốc độ nhanh gấp 10 lần so với phương pháp sử dụng script thông thường 🚀
### "If you are good at something never do it for free" -Joker

Công cụ Python tự động xử lý đổi Tên, Group ID, Proxy và cả Note Profile trên GPM. Chỉ cần vài bước đơn giản, bạn đã có thể tự động hóa quy trình một cách nhanh chóng và chính xác.  

---

## Yêu cầu hệ thống  
- Python. 
- Thư viện Python: `requests`, `pandas`, `tqdm`, `openpyxl`, `tk`.  

---

## Cách sử dụng  

### Bước 1: Cài đặt Python  
1. Tải Python tại [python.org](https://www.python.org/downloads/).  
2. Trong quá trình cài đặt, nhớ tick vào ô **"Add Python to PATH"**.  

### Bước 2: Cài đặt thư viện cần thiết  
1. Chạy tệp `install.bat` để tự động cài đặt các thư viện.  
2. Đợi quá trình cài đặt hoàn tất.  

### Bước 3: Chuẩn bị file Excel  
1. Điền thông tin vào file Excel mẫu:  
   - Các cột cần thiết: `ProfileName`, `NewName`, `NewGroupID`, `NewProxy`.  
   - Các giá trị không thay đổi, bạn có thể để trống.  
2. Lưu file sau khi chỉnh sửa.  

### Bước 4: Chạy script  
1. Mở tệp `start.bat` để khởi động chương trình.  
2. Chọn file Excel khi được yêu cầu.  
3. Theo dõi kết quả và kiểm tra file `Updated_Profiles_Info.xlsx` để xem thông tin đã được cập nhật.  

---

## Hàm chính: Lấy danh sách Profiles  

Nếu bạn là coder giỏi, có thời gian hãy hỗ trợ mình sửa đoạn code dưới này nhé, hiện tại mình test đang chạy ngon lành với số lượng profiles  <5000

```
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
```


# Liên hệ

## Đan Giaó Sư
### NEVER DM YOU FIRST
### Chuyên lùa gà, nhưng vẫn ghét fake news.**

### Kết nối với tôi:
- **Facebook:** [Click here](https://www.facebook.com/Prof.Danta)
- **Telegram:** [Click here](https://t.me/dangiaosu)
- **Zalo:** 0828092390

### Thông tin ngân hàng:
- **Số tài khoản:** 6309230990
- **Ngân hàng:** MBBank
- **Chủ tài khoản:** Tạ Đình Mạnh

