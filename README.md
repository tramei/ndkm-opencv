# ndkm-opencv

Đây là video demo để mn xem hiểu cách "Hệ thống nhận diện khuôn mặt" hoạt động như nào:
https://www.youtube.com/watch?v=ljsNw76F7Eo&list=PLQ-mLtmt_kpsUJ6XDphHpq04smBoang08&index=1&t=28s

Đây là giải thích code của từng phần:

- Bước 1: Lấy dữ liệu khuôn mặt qua cam
https://www.youtube.com/watch?v=Lusa912ax5g
https://www.youtube.com/watch?v=E5_EHQr-aRQ&t=8s

- Bước 2: Training dữ liệu
https://www.youtube.com/watch?v=kAH9Bih32WE&t=634s

- Bước 3: Nhận diện khuôn mặt
https://www.youtube.com/watch?v=o7YaiI42jZg

- Bước 4: Thiết kế giao diện hệ thống

Trong code có chú thích rõ. Chỉ có 1 chỗ mn phải hiểu là tọa độ để sắp xếp label, textbox, button được canh theo (x,y) = (0,0)

Vị trí tọa độ (0,0) là ở góc trên-bên trái của cửa sổ "Hệ thống nhận diện khuôn mặt"

Rồi từ đó mà tịnh tiến cho x,y = ... bao nhiêu đó để cân bằng

------------------------------------------
Ai muốn chạy thử thì mn down Project ở đây, do tui kh tải lên github đc :<
https://drive.google.com/file/d/196d2fG95uHc529oCbm_YT_53lIvUyvCy/view?usp=sharing

Vào terminal, cài các thư viện này trước:
- pip install cmake
- pip install opencv-contrib-python
- pip install opencv-python
- pip install Pillow
