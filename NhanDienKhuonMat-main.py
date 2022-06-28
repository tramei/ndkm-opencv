import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import os
import sqlite3
from PIL import Image

def laydulieu():
    def insertOrUpdate(id, name):  # them moi/update ban ghi
        # ket noi db
        conn = sqlite3.connect('DataFace.db')
        # viet 1 cau lenh ktra ID ton tai hay chua.Ton tai->update, chua->insert
        query = "SELECT * FROM People WHERE ID=" + str(id)
        cusror = conn.execute(query)  # lay ra cac ban ghi tu cau lenh tren

        isRecordExist = 0  # neu co ID trong db=1, chua=0
        for row in cusror:  # duyet tung hang tren ban ghi
            isRecordExist = 1  # co ton tai thi chuyen ve=1
        if (isRecordExist == 0):  # them moi vao db
            query = "INSERT INTO People(ID, Name) VALUES(" +str(id)+ "," +str(name)+ ")"
        else:  # co roi thi update
            query = "UPDATE People SET Name=" +str(name) + " WHERE ID=" +str(id)
        conn.execute(query)
        conn.commit()
        conn.close()

    # thu vien mac dinh cho opencv nhan dien km trên cam
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # truy cap webcam
    cap = cv2.VideoCapture(0)

    # đưa dl vao db
    #id = input('Nhap ID: ')
    #name = input('Nhap ten: ')
    id = int1.get()
    name = "'"+str1.get()+"'"
    insertOrUpdate(id, name)

    sample_number = 0  # tạo chỉ số index của ảnh chụp
    while True:
        # lay dl tu webcam
        ret, frame = cap.read()  # ret=true neu truy cap thanh cong #frame: dl lay dc tu cam
        #cv2.resize(frame, (0, 0), None, fx=2.0, fy=2.0)
        # chuyển anh thanh anh xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # chuyen mau bgr torng opencv sang gray
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # ket hop voi thu vien km mac dinh de ndkm trên cam

        for (x, y, w, h) in faces:  # ve hinh vuong quanh km
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # frame:hinh anh tu cam #x,y: toa do dau tien de lay hv
                                                                        # x+w,y+h:tọa độ tịnh tiến  #màu xanh   #độ dày hv

            # tao folder de luu anh dc chup lai tu hinh vuong tren
            # ktra đường dẫn đã có folder chưa, nếu chưa thì tạo
            if not os.path.exists('data_face'):
                os.makedirs('data_face')  # makedirs: tạo folder mới

            sample_number += 1  # tăng dần chỉ số lưu ảnh, ID1.1, 1.2
            cv2.imwrite('data_face/User.' + str(id) + '.' + str(sample_number) + '.jpg', gray[y: y + h, x: x + w])  #lưu ảnh với tên #ts2: phần cắt ảnh
        # show cam
        cv2.imshow('Lay du lieu khuon mat', frame)
        if(cv2.waitKey(10) == ord("q")):  # độ trễ 1/1000s #nếu bấm q sẽ thoát
            break

        if sample_number > 100: #lấy 50 tấm ảnh
            cap.release()  # giai phong bo nho
            cv2.destroyAllWindows()  # huy ctrinh
            break
    #txtID.delete(0,"end")
    #txtName.delete(0,"end")

def training():
    recognizer = cv2.face_LBPHFaceRecognizer.create()  #thư viện mặc định của opencv để training hình ảnh nhận diện
    path = 'data_face'  #biến lấy đường dẫn đến thư mục ảnh data_face

    # hàm lấy ID và Danh sách ảnh để training
    def getImageWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # lấy ra tất cả các đg dẫn ảnh từ folder

        # tạo 2 mảng để lưu
        faces = []  # lưu dl ảnh
        IDs = []  # lưu ds ID
        for imagePath in imagePaths:  # duyệt từng đg dẫn ảnh trong tất cả đg dãn ảnh
            faceImg = Image.open(imagePath).convert('L');  # chuyển đổi các ảnh về đúng kiểu định dạng training=PIL
            faceNp = np.array(faceImg, 'uint8')  # chuyển ảnh về ma trận

            # cắt ID từ đg dẫn ảnh, lấy ra để nó biết ảnh thuộc ID nào
            ID = int(imagePath.split('\\')[1].split('.')[1])       #'data_face\\User.1.1.jpg'
            #ID=int(os.path.split(imagePath)[1].split('.')[1])
            faces.append(faceNp)  # nối đuôi các ảnh lại
            IDs.append(ID)  # nối đuôi các ID lại

            cv2.imshow('training', faceNp)
            cv2.waitKey(10)  # thực hiện trong 20 giây
        return faces, IDs   #ts2: np.array(IDs)

    faces, IDs = getImageWithID(path)
    recognizer.train(faces, np.array(IDs) )  # training  #ts2: IDs

    # train xong sẽ trả file yml. Tạo folder trong BT-NDKM để lưu lại
    if not os.path.exists('trainer'):
        os.makedirs('trainer')  # nếu chưa có thì sẽ tạo folder này ra
    # lưu file yml vào folder trainer
    recognizer.save('trainer/FaceData-training.yml')
    cv2.destroyAllWindows() # hủy chương trình

def nhandien():
    # Gọi thư viện nhận diện km,thư viện training hình ảnh nhận diện trên cam của opencv
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face_LBPHFaceRecognizer.create()

    recognizer.read('trainer/FaceData-training.yml')  # đọc file yml sau khi đc training

    # nhận xét xem km trên cam có trong tập dl đã train kh? Là ai?
    # hàm lấy thông tin người trong database bằng ID
    def getProfile(ID):
        conn = sqlite3.connect('DataFace.db')  # kết nối db
        query = "SELECT * FROM People WHERE ID=" + str(ID)
        cursor = conn.execute(query)  # thực thi câu lệnh

        # tạo 1 biến lưu giá trị lấy đc từ db
        profile = None
        for row in cursor:
            profile = row
        conn.close()  # đóng kết nối
        return profile  # trả kq để xíu dùng

    # nhận diện km ở đâu trên cam. ng này là ai trong tập dl đã train?
    cap = cv2.VideoCapture(0)  # truy cập cma

    while True:
        ret, frame = cap.read()  # đọc dl từ cam
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # chuyển ảnh xám
        # kết hợp cam và face_cascade để nhận diện km trên cam
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # vẽ hình vuông trên km
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            # cắt ảnh khung vuông km đó trên cam=>so sánh tập dl. Train ảnh xám nên ảnh cắt ra cũng xám
            roi_gray = gray[y: y+h, x: x+w]  # cắt ảnh bằng cỡ hình vuông trên
            # hàm nhận diện khuôn mặt trên cam là ai, trả về id
            ID, confidence = recognizer.predict(roi_gray)  # confidence: độ chính xác
            if confidence < 50:
                profile = getProfile(ID)
                # ktra nếu profile có dữ liệu->trả về dl đấy, null -> 'unknow'
                if (profile != None):
                    cv2.putText(frame, "" + str(profile[1]), (x + 10, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknow", (x + 10, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # show cam
        cv2.imshow('Nhan dien khuon mat', frame)
        if (cv2.waitKey(1) == ord('q')):
            break
    cap.release()  # giai phong bo nho
    cv2.destroyAllWindows()  # hủy chương trình

#------------THIẾT KẾ GIAO DIỆN------------
wd = tk.Tk()    #tạo cửa sổ
wd.title("Hệ thống nhận diện khuôn mặt")
wd.iconbitmap('face-recognition.ico')
wd.geometry('500x270')  #kích thước cửa sổ
wd.configure(bg='salmon')
#label tiêu đề
lbl = ttk.Label(wd,text="HỆ THỐNG NHẬN DIỆN KHUÔN MẶT",
                background="salmon",foreground="darkred",font=25)
lbl.place(x=80,y=15)
#label ID
lblID = ttk.Label(wd,text="ID:",background="salmon",foreground="black")
lblID.place(x=10,y=80)
#label Name
lblName = ttk.Label(wd,text="Name:",background="salmon",foreground="black")
lblName.place(x=10,y=120)

#textbox ID
int1 = tk.IntVar()
txtID = ttk.Entry(wd, textvariable=int1, width=50)
txtID.place(x=90,y=80)
txtID.focus()

#textbox Name
str1 = tk.StringVar()
txtName = ttk.Entry(wd,textvariable=str1, width=50)
txtName.place(x=90,y=120)

#button Lấy dữ liệu
btnlaydulieu = ttk.Button(wd, text="Lấy dữ liệu", command=laydulieu)
btnlaydulieu.place(x=50,y=200)
#button Train
btntrain = ttk.Button(wd, text="Traning", command=training)
btntrain.place(x=200,y=200)
#button Nhận diện
btnnhandien = ttk.Button(wd, text="Nhận diện", command=nhandien)
btnnhandien.place(x=350,y=200)

wd.mainloop()   #duy trì cửa sổ không bị tắt
