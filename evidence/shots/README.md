# Hướng dẫn chụp ảnh mô phỏng thật

Chưa có ảnh trong thư mục này. Môi trường tự động hóa hiện không mở được `file://`: thao tác vào `viewer/index.html` bị trả về `URL protocol not allowed`, và danh sách automation không có tab trình duyệt để điều khiển. Đây là chặn truy cập viewer cục bộ; chưa xác nhận được trạng thái WebGL thực tế trong Safari hay Chrome. Không dùng ảnh dựng thay thế.

## Mở viewer

Từ thư mục gốc dự án:

```sh
open -a Safari "$PWD/viewer/index.html"
```

Nếu Safari không dựng được hình, thử Chrome:

```sh
open -a "Google Chrome" "$PWD/viewer/index.html"
```

Trong Chrome, nhập `chrome://gpu` vào thanh địa chỉ và kiểm tra trạng thái WebGL. Nếu WebGL bị tắt, vào `chrome://settings/system`, bật **Use graphics acceleration when available**, khởi động lại Chrome rồi thử lại.

## Ảnh cần lưu

Trong chương 9, mở `evidence/viewer.json` bằng vùng tải file của phòng lab. Chọn lượt trong danh sách, tạm dừng thanh thời gian tại mốc va chạm, rồi chạy lệnh chụp tương ứng ở terminal khác. Lệnh sẽ chờ bạn kéo vùng cần chụp trên màn hình; chọn cả khung 3D và phần đọc kết quả.

```sh
screencapture -i evidence/shots/bus_bypass.png
```

Chụp lượt `B-01` (va chạm lách xe buýt, khoảng 12.5 s).

```sh
screencapture -i evidence/shots/crosswalk_block.png
```

Chụp lượt `C-01` (xe ego chặn lối người đi bộ, khoảng 19.2 s).

```sh
screencapture -i evidence/shots/baseline_vs_optimized.png
```

Chọn `B-01` và giữ bóng mờ của planner được chọn hiện cùng xe planner gốc tại khoảng 12.5 s.

```sh
screencapture -i evidence/shots/hazard_bicycle.png
```

Trong chương 10, bấm **Mở file…**, tải `hazard.json`, phát cảnh và dừng quanh 10–12 s khi xe đạp bắt đầu lạng. Đây là cảnh nguyên dạng được khai báo trong file; cảnh cụ thể này không va chạm.
