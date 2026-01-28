# **GIÁO ÁN CHÍNH THỨC**

## **WORKSHOP: THU THẬP DỮ LIỆU TỪ WEB**

---

### **I. THÔNG TIN CHUNG**

| Mục | Nội dung |
|-----|----------|
| **Tên bài giảng** | Web Data Crawling: Từ Cơ Bản Đến Tự Động Hóa |
| **Thời lượng** | 4 tiếng (240 phút) |
| **Số lượng sinh viên** | 70 người |
| **Đối tượng** | SV ngành Toán Kinh tế & Thương mại điện tử |
| **Nền tảng** | Python cơ bản (biết vòng lặp, hàm, list) |
| **Nền tảng học tập** | Google Colab (không cài đặt local) |

---

### **II. MỤC TIÊU HỌC TẬP (Learning Outcomes)**

Sau buổi học, sinh viên có khả năng:

| # | Mục tiêu | Bloom's Level | Cách đánh giá |
|---|----------|---------------|---------------|
| **LO1** | Phân biệt 3 loại website: Static (SSR), Dynamic (CSR), API-based | Hiểu (Understand) | Quiz nhanh giữa buổi |
| **LO2** | Trích xuất dữ liệu từ trang HTML tĩnh bằng BeautifulSoup | Áp dụng (Apply) | Bài tập thực hành |
| **LO3** | Sử dụng Selenium để thu thập dữ liệu từ trang JavaScript | Áp dụng (Apply) | Demo hoàn chỉnh |
| **LO4** | Khám phá và sử dụng API ẩn của website | Phân tích (Analyze) | Bài tập tìm API |

---

### **III. CHUẨN BỊ TRƯỚC BUỔI HỌC**

#### **A. Phía Giảng Viên**
- [ ] Notebook Colab đã test trên 3 trình duyệt (Chrome, Firefox, Edge)
- [ ] Link Colab rút gọn (bit.ly hoặc QR code)
- [ ] Backup code trên GitHub/Google Drive
- [ ] Slide PDF backup (phòng mất mạng)

#### **B. Phía Sinh Viên (Gửi trước 1 ngày)**
- [ ] Tài khoản Google (để dùng Colab)
- [ ] Cài extension Chrome "JSON Viewer"
- [ ] Đọc trước: "HTML là gì?" (5 phút)

---

### **IV. PHÂN CHIA THỜI GIAN TỔNG QUAN**

```
┌──────────────────────────────────────────────────────────────────┐
│ SESSION 1: Khởi động + Static Scraping        │ 60 phút │ 🟢   │
├──────────────────────────────────────────────────────────────────┤
│ ☕ NGHỈ GIẢI LAO                              │ 10 phút │      │
├──────────────────────────────────────────────────────────────────┤
│ SESSION 2: Dynamic Content với Selenium       │ 55 phút │ 🟡   │
├──────────────────────────────────────────────────────────────────┤
│ ☕ NGHỈ GIẢI LAO                              │ 10 phút │      │
├──────────────────────────────────────────────────────────────────┤
│ SESSION 3: Khám phá API ẩn                    │ 55 phút │ 🟠   │
├──────────────────────────────────────────────────────────────────┤
│ SESSION 4: Tổng kết + Q&A + Bài tập về nhà    │ 50 phút │ 🔴   │
└──────────────────────────────────────────────────────────────────┘
                              Tổng: 240 phút
```

---

## **V. NỘI DUNG CHI TIẾT (TỪNG PHÚT)**

---

## **🟢 SESSION 1: KHỞI ĐỘNG + STATIC SCRAPING (60 phút)**

### **Mục tiêu session**: Sinh viên thành công crawl được dữ liệu từ 1 trang web tĩnh

---

| Thời gian | Phút | Nội dung | Hoạt động | Phương pháp | Lý do sư phạm |
|-----------|------|----------|-----------|-------------|---------------|
| **0:00-0:05** | 5' | **HOOK: "1 triệu dòng trong 1 giờ"** | Chiếu video/gif một script đang chạy, data đổ về ào ào. Hỏi: "Các bạn có muốn làm được như này không?" | Demo trực quan | **Tạo động lực.** Sinh viên cần biết ĐIỂM ĐÍCH trước khi học ĐƯỜNG ĐI. |
| **0:05-0:10** | 5' | **Giới thiệu 3 Cấp Độ** | Trình chiếu sơ đồ: Level 1 (Nhà hàng phục vụ sẵn) → Level 2 (Lẩu tự nấu) → Level 3 (Gọi điện đặt hàng trực tiếp). Không giải thích sâu, chỉ overview. | Ẩn dụ trực quan | **Advance Organizer**: Cho não bộ một "bản đồ" trước khi đi vào chi tiết. |
| **0:10-0:15** | 5' | **Setup Colab** | Sinh viên mở link Colab. GV hướng dẫn "Runtime > Run All" để test. | Làm theo | **Buffer cài đặt.** Giải quyết sớm, tránh gián đoạn sau. |
| **0:15-0:20** | 5' | **BUFFER** | Đi vòng quanh lớp kiểm tra. Hỏi: "Ai chưa thấy output đầu tiên giơ tay?" | Troubleshoot | **Không ai bị bỏ lại.** 10% sinh viên LUÔN gặp vấn đề. |
| **0:20-0:25** | 5' | **Demo "View Source" vs "Inspect"** | Mở bonbanh.com. Bấm Ctrl+U → "Đây là HTML mà server gửi về." Bấm F12 → "Đây là HTML sau khi JavaScript chạy xong." | Demo trực quan | **Cụ thể trước trừu tượng.** Sinh viên THẤY trước khi được giải thích. |
| **0:25-0:35** | 10' | **Live Coding: Step 1-2** | `step1_basic_request.py`: Gửi request, in HTML. `step2_parse_html.py`: BeautifulSoup tìm thẻ. **DỪNG** sau mỗi `print()` để sinh viên thấy output. | Live coding + narration | **Cognitive chunking.** Không code ào ào. Mỗi chunk nhỏ = 1 khái niệm. |
| **0:35-0:40** | 5' | **Checkpoint #1** | Hỏi: "Kết quả các bạn có giống màn hình thầy/cô không?" Giơ tay nếu KHÁC. | Kiểm tra hiểu | **Formative assessment.** Điều chỉnh tốc độ dựa trên phản hồi. |
| **0:40-0:50** | 10' | **Live Coding: Step 3-4** | `step3_extract_data.py`: Lấy tên, giá, năm. `step4_pydantic_model.py`: Đưa vào class. | Live coding | **Tăng dần độ khó.** Sau khi hiểu cơ bản, thêm cấu trúc. |
| **0:50-0:55** | 5' | **Bài tập nhanh** | "Hãy sửa code để lấy thêm LINK ảnh xe." (Chỉ 1 dòng code thay đổi) | Thực hành cá nhân | **Active learning.** Tự làm = nhớ lâu hơn. |
| **0:55-1:00** | 5' | **Giải đáp + Kết luận Session 1** | Chạy `step5_pagination.py` để cho thấy có thể lặp qua nhiều trang. "Session 1 là Level 1 - trang web đơn giản. Nhưng không phải trang nào cũng vậy..." | Cliffhanger | **Tạo tò mò cho session sau.** |

---

## **☕ NGHỈ GIẢI LAO (10 phút)**

> **Quan trọng:** Bật nhạc nhẹ. Cho sinh viên đứng dậy đi lại. Não cần oxy.

---

## **🟡 SESSION 2: DYNAMIC CONTENT VỚI SELENIUM (55 phút)**

### **Mục tiêu session**: Sinh viên hiểu TẠI SAO cần Selenium và có thể chạy thành công trên Colab

---

| Thời gian | Phút | Nội dung | Hoạt động | Phương pháp | Lý do sư phạm |
|-----------|------|----------|-----------|-------------|---------------|
| **1:10-1:15** | 5' | **HOOK: "Thử copy kỹ thuật cũ"** | Sinh viên tự chạy `requests.get()` trên URL cafef.vn. Kết quả: Bảng rỗng! | Problem-based learning | **Gây cognitive conflict.** "Tại sao cách cũ không hoạt động?" = Động lực học cách mới. |
| **1:15-1:20** | 5' | **Giải thích SSR vs CSR** | Quay lại ẩn dụ nhà hàng. "Trang CafeF này là NỒI LẨU. Khi `requests` đến, món ăn chưa được nấu." | Liên kết kiến thức | **Spiral curriculum.** Dùng lại ẩn dụ cũ, bổ sung ý mới. |
| **1:20-1:22** | 2' | **Giới thiệu Selenium** | "Selenium = Thuê một đầu bếp (browser thật) ngồi đợi nấu xong rồi mới lấy đồ ăn về." | Ẩn dụ | **Mental model.** Sinh viên cần hiểu Selenium "đợi" được. |
| **1:22-1:30** | 8' | **Setup Selenium trên Colab** | Chạy cell cài đặt. **GV PHẢI test trước buổi học.** Nếu Colab fail → có backup notebook khác. | Làm theo | **Giảm friction.** Colab = không cần cài Chrome local. |
| **1:30-1:35** | 5' | **BUFFER** | "Ai có lỗi màu đỏ giơ tay?" Giải quyết nhanh. Nếu quá 20% fail → chuyển sang demo mode (GV code, sinh viên xem). | Troubleshoot | **Plan B.** Không để lỗi kỹ thuật phá hỏng momentum. |
| **1:35-1:50** | 15' | **Live Coding: Selenium Step 1-3** | `step1`: Mở browser. `step2`: Đợi element. `step3`: Lấy data từ bảng. **QUAN TRỌNG:** Giải thích TỪNG dòng XPath. | Live coding chậm | **XPath là khó.** Dành thời gian cho phần này. |
| **1:50-1:55** | 5' | **Demo Click Button** | Bonus: Click nút "Xem thêm" hoặc chuyển trang. "Đây là sức mạnh của Selenium - nó TƯƠNG TÁC được." | Demo wow | **Gamification.** Cho họ thấy điều cool để giữ hứng thú. |
| **1:55-2:00** | 5' | **Kết luận + So sánh** | Bảng so sánh: BeautifulSoup (nhanh, đơn giản, chỉ SSR) vs Selenium (chậm, mạnh, cả CSR). "Nhưng có cách NÀO NHANH HƠN cả hai không?" | Cliffhanger | **Tạo bridge cho session sau.** |

---

## **☕ NGHỈ GIẢI LAO (10 phút)**

---

## **🟠 SESSION 3: KHÁM PHÁ API ẨN (55 phút)**

### **Mục tiêu session**: Sinh viên biết cách tìm API endpoint và gọi trực tiếp

---

| Thời gian | Phút | Nội dung | Hoạt động | Phương pháp | Lý do sư phạm |
|-----------|------|----------|-----------|-------------|---------------|
| **2:10-2:15** | 5' | **HOOK: Tốc độ chênh lệch 100 lần** | Chạy song song: Selenium (30 giây) vs API call (0.3 giây). "CẢI TIẾN này không phải 10%, mà là 10000%." | Trực quan | **Motivation through comparison.** |
| **2:15-2:25** | 10' | **Giới thiệu DevTools Network Tab** | Live demo mở F12 → Network → XHR/Fetch. Reload trang cafef. "Đây là TẤT CẢ các request mà JavaScript gửi đi." | Demo chậm, giải thích kỹ | **Core skill.** Đây là kỹ năng quan trọng nhất của session. |
| **2:25-2:30** | 5' | **Tìm API Endpoint** | GV hướng dẫn tìm request có data (thường là JSON). Copy URL. "Đây chính là 'số điện thoại kho hàng'." | Hướng dẫn từng bước | **Scaffolding.** Không để sinh viên tự mò. |
| **2:30-2:35** | 5' | **Bài tập: Tự tìm API** | Sinh viên tự mở F12 trên một URL khác (GV cung cấp). Tìm 1 API endpoint. Giơ tay khi tìm được. | Thực hành có hướng dẫn | **Guided practice trước independent practice.** |
| **2:35-2:40** | 5' | **BUFFER + Kiểm tra** | "Ai chưa tìm được?" Hỗ trợ nhanh. | Troubleshoot | **Không ai bị bỏ lại.** |
| **2:40-2:55** | 15' | **Live Coding: Gọi API bằng requests** | `step1_find_api.py` → `step2_call_api.py` → `step3_parse_json.py`. Nhấn mạnh: Không cần BeautifulSoup, không cần Selenium! | Live coding | **Aha moment.** "Hóa ra dễ vậy sao!" |
| **2:55-3:00** | 5' | **Giới thiệu Headers/Authentication** | "Một số API yêu cầu 'thẻ VIP' (headers/cookies). Copy từ browser." Demo copy headers. | Quick intro | **Không đi sâu.** Chỉ cho biết tồn tại. |
| **3:00-3:05** | 5' | **Kết luận Session 3** | Quy tắc vàng: "API first, Selenium second, BeautifulSoup last." | Takeaway | **Tổng kết thành 1 câu dễ nhớ.** |

---

## **🔴 SESSION 4: TỔNG KẾT + BÀI TẬP NÂNG CAO (50 phút)**

### **Mục tiêu session**: Củng cố kiến thức, giới thiệu async (preview), giao bài tập về nhà

---

| Thời gian | Phút | Nội dung | Hoạt động | Phương pháp | Lý do sư phạm |
|-----------|------|----------|-----------|-------------|---------------|
| **3:05-3:10** | 5' | **Quiz Tổng Kết** | 5 câu hỏi nhanh trên Kahoot/Mentimeter: "SSR hay CSR?", "Nên dùng tool nào?" | Gamification | **Active recall.** Củng cố trí nhớ. |
| **3:10-3:20** | 10' | **Review Flowchart** | Trình chiếu flowchart quyết định: "Bước 1: Ctrl+U có data không? → Có: BeautifulSoup. Không: → Bước 2..." | Tổng hợp | **Big picture.** Kết nối các mảnh kiến thức. |
| **3:20-3:30** | 10' | **Demo Async (Preview cho tự học)** | Chạy `step4_async_version.py`. Không giải thích code chi tiết. "Đây là level nâng cao, các bạn tự học nếu cần tốc độ cực nhanh." | Demo nhanh | **Zone of proximal development.** Cho thấy "next level" nhưng không bắt buộc. |
| **3:30-3:40** | 10' | **Giao Bài Tập Về Nhà** | 3 bài tập: (1) Crawl 5 trang bonbanh, (2) Tìm API của trang X, (3) So sánh tốc độ Selenium vs API. | Handout | **Transfer learning.** Áp dụng vào context mới. |
| **3:40-3:50** | 10' | **Q&A Mở** | Sinh viên hỏi bất kỳ điều gì. GV trả lời hoặc hướng dẫn resource tự học. | Tương tác | **Closure.** Giải đáp thắc mắc tồn đọng. |
| **3:50-4:00** | 10' | **BUFFER CUỐI** | Dành cho Q&A kéo dài hoặc hỗ trợ cá nhân. | Linh hoạt | **Luôn có backup time.** |

---

## **VI. PHƯƠNG ÁN DỰ PHÒNG (Contingency Plans)**

| Tình huống | Phương án |
|------------|-----------|
| **Colab bị quá tải** | Dùng notebook backup trên Kaggle |
| **Selenium fail hàng loạt** | Chuyển sang demo mode: GV code, sinh viên xem |
| **Website target bị chặn** | Có 2 website backup đã test trước |
| **Hết thời gian** | Cắt Demo Async, thay bằng Q&A |
| **Sinh viên xong sớm** | Giao exercise nâng cao từ `exercises.md` |

---

## **VII. TÀI LIỆU PHÁT CHO SINH VIÊN**

1. **Link Colab Notebook** (tất cả code đã comment sẵn)
2. **Cheat Sheet 1 trang**: SSR vs CSR, BeautifulSoup vs Selenium vs API
3. **exercises.md**: Bài tập tự luyện
4. **resources.md**: Link tutorial, documentation

---

## **VIII. ĐÁNH GIÁ BUỔI HỌC**

| Tiêu chí | Phương pháp | Thời điểm |
|----------|-------------|-----------|
| Hiểu lý thuyết | Quiz Kahoot | Session 4 |
| Thực hành được | Checkpoint giơ tay | Sau mỗi session |
| Hài lòng với buổi học | Google Form survey | Gửi sau buổi học |

---

## **PHỤ LỤC: ĐÁNH GIÁ KẾ HOẠCH CŨ**

### **Những Điểm Thất Bại Cần Tránh**

| # | Vấn đề từ kế hoạch cũ | Đã khắc phục |
|---|----------------------|--------------|
| 1 | Thời gian Session 1 bị vỡ (15 phút mất tích) | ✅ Timeline chi tiết từng phút |
| 2 | Không có buffer cài đặt | ✅ 5-10 phút buffer mỗi session |
| 3 | Selenium trên Colab không ổn định | ✅ Plan B: Demo mode |
| 4 | Session 3 chỉ 2 phút đặt vấn đề | ✅ 10 phút DevTools intro |
| 5 | Session 4 lặp lại Session 3 | ✅ Nội dung riêng biệt |
| 6 | Không có thời gian nghỉ | ✅ 2 lần nghỉ 10 phút |
| 7 | API quá trừu tượng | ✅ Demo trực quan DevTools |
| 8 | Postman ở cuối - sai thứ tự | ✅ Bỏ Postman, dùng Python thẳng |

---

## **NGUYÊN TẮC SƯ PHẠM ÁP DỤNG**

### **1. Cognitive Load Theory**
- Mỗi session chỉ 1-2 concept chính
- Buffer time giữa các concept

### **2. Scaffolding**
- Level 1 → Level 2 → Level 3
- Mỗi level xây trên nền level trước

### **3. Konkret vor Abstrakt (Cụ thể trước Trừu tượng)**
- Demo TRƯỚC, giải thích SAU
- Sinh viên THẤY trước khi HIỂU

### **4. Active Learning**
- Checkpoint mỗi 20 phút
- Bài tập ngắn xen kẽ

---

## **LỜI NHẮC CUỐI**

**Ba điều KHÔNG ĐƯỢC quên:**

1. ⏰ **BUFFER TIME là bắt buộc,** không phải "nếu có thời gian"
2. 👀 **Demo TRƯỚC, giải thích SAU** — không bao giờ làm ngược lại  
3. ❓ **Checkpoint mỗi 20 phút** — nếu 30% sinh viên chưa theo kịp, DỪNG LẠI

---

*Một giờ chuẩn bị của giảng viên = tiết kiệm 10 phút chaos trong lớp.*
