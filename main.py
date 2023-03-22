import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("TaiKhoanDichVu.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://databasenhandienkhuanmat-default-rtdb.firebaseio.com/",
    'storageBucket': "databasenhandienkhuanmat.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('TaiNguyenAnh/HinhNen.png')

folderModePath = 'TaiNguyenAnh/CheDo'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Sử dụng module pickle.load() để đọc dữ liệu từ tệp "EncodeFile.p". Sau khi đọc xong, tệp sẽ được đóng lại
print("Loading file")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Downloaded file")

face = face_recognition

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Thay đổi kích thức ảnh bằng 1/4 kích thức ban đầu
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # face_locations(img) dùng để tìm vị trí của tất cả các mặt trong khung hiện tại và trả về chúng dưới dạng danh sách các bộ
    faceCurFrame = face.face_locations(img)
    # face_encodings(img, faceCurFrame) tạo mã hóa khuôn mặt
    encodeCurFrame = face.face_encodings(img, faceCurFrame)
    
    # Thêm hình nền
    imgBackground[162:162 + 480, 55:55 + 640] = img
    # Thêm các chế độ vào nền
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face.compare_faces(encodeListKnown, encodeFace)
            faceDis = face.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Dang tai", (275, 400))
                    cv2.imshow("Nhan dien khuon mat", imgBackground)
                    cv2.waitKey(0)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:

                studentInfo = db.reference(f'Thanh_Vien/{id}').get()
                print(studentInfo)

                blob = bucket.get_blob(f'AnhThanhVien/{id}.png')
                array = np.frombuffer(blob.download_as_string() , np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                datetimeObject = datetime.strptime(studentInfo['lan_cuoi_tham_du'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Thanh_Vien/{id}')
                    studentInfo['so_du_an'] += 1
                    ref.child('so_du_an').set(studentInfo['so_du_an'])
                    ref.child('lan_cuoi_tham_du').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['so_du_an']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['nganh']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['thanh_tich']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['nam']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['nam_bat_dau']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['ho_ten'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['ho_ten']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    if cv2.waitKey(1) == 27:
        break

    cv2.imshow("Nhan dien khuon mat", imgBackground)

cap.release()
cv2.destroyAllWindows()