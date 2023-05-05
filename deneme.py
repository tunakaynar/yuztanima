import pypyodbc

db = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-LE5T4BA\SQLEXPRESS;'
    'Database=DbOkul;'
    'UID=;'
    'PWD=;'
)

imlec = db.cursor()


numara = '1'

query = f"INSERT INTO YOKLAMA1 (NUMARA, AD, BOLUM, FAKULTE, TARIH) SELECT  O.NUMARA, O.AD, O.BOLUM, O.FAKULTE, GETDATE() FROM OGRENCI O WHERE O.NUMARA = '{numara}'"

sonuc = imlec.execute(query)
db.commit()