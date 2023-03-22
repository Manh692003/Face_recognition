import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("TaiKhoanDichVu.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://databasenhandienkhuanmat-default-rtdb.firebaseio.com/"
})

ref = db.reference('Thanh_Vien')

data = {
    "060903":
        {
            "ho_ten": "Phan Manh",
            "nganh": "AI programmer",
            "nam_bat_dau": 2023,
            "so_du_an": 1,
            "thanh_tich": "G",
            "nam": 1,
            "lan_cuoi_tham_du": "2023-02-07 10:13:24"
        },
    "852741":
        {
            "ho_ten": "Bill Gates",
            "nganh": "Microsoft founder",
            "nam_bat_dau": 2021,
            "so_du_an": 12,
            "thanh_tich": "G",
            "nam": 1,
            "lan_cuoi_tham_du": "2023-02-07 10:13:24"
        },
    "963852":
        {
            "ho_ten": "Elon Musk",
            "nganh": "Bachelor of Economics",
            "nam_bat_dau": 2020,
            "so_du_an": 7,
            "thanh_tich": "G",
            "nam": 2,
            "lan_cuoi_tham_du": "2023-02-07 10:13:24"
        }
}

for key, value in data.items():
    ref.child(key).set(value)