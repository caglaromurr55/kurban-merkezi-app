import sqlite3
from flask import session,flash

class Database:
    def __init__(self, db_name='Database.db'):
        """Veritabanı bağlantısını başlatır."""
        self.db_name = db_name

    def connect(self):
        """Veritabanına bağlanır. Timeout özelliği eklendi."""
        conn = sqlite3.connect(self.db_name, timeout=10)  # 10 saniye bekleme süresi eklendi
        conn.row_factory = sqlite3.Row  # Sözlük formatında veri döndürmek için
        return conn

class UserModel(Database):
    def __init__(self, db_name='Database.db'):
        super().__init__(db_name)

    def get_user_by_phone(self, phone):
        """Telefon numarasına göre kullanıcıyı getirir."""
        conn = self.connect()
        user = conn.execute('SELECT * FROM user WHERE phone = ?', (phone,)).fetchone()
        conn.close()
        return user
    
    def register_user(self, phone, password):
        """Yeni kullanıcıyı kaydeder ve müşteri tablolarını oluşturur."""
        yurtici_tablo = f"yimusteri_{phone}"
        yurtdisi_tablo = f"ydmusteri_{phone}"

        # Tablo oluşturma sorguları
        yurtici_query = f'''
        CREATE TABLE IF NOT EXISTS {yurtici_tablo} (
            id INTEGER NOT NULL UNIQUE,
            isim TEXT NOT NULL,
            soyisim TEXT NOT NULL,
            referans TEXT,
            tarih TEXT NOT NULL,
            numara TEXT NOT NULL,
            hissetutar INTEGER NOT NULL,
            adres TEXT NOT NULL,
            aciklama TEXT,
            hisseturu TEXT NOT NULL,
            odenen INTEGER,
            durum TEXT,
            PRIMARY KEY("id")
        )
        '''
        
        yurtdisi_query = f'''
        CREATE TABLE IF NOT EXISTS {yurtdisi_tablo} (
            id INTEGER NOT NULL UNIQUE,
            isim TEXT NOT NULL,
            soyisim TEXT NOT NULL,
            referans TEXT,
            tarih TEXT NOT NULL,
            numara TEXT NOT NULL,
            hissetutar INTEGER NOT NULL,
            adres TEXT NOT NULL,
            aciklama TEXT,
            hisseturu TEXT NOT NULL,
            odenen INTEGER,
            durum TEXT,
            PRIMARY KEY("id")
        )
        '''

        conn = self.connect()
        try:
            # Kullanıcı kaydı
            conn.execute('INSERT INTO user (phone, password) VALUES (?, ?)', (phone, password))
            conn.commit()  # Kullanıcıyı kaydetme işlemini tamamla

            # Müşteri tablolarını oluşturma
            conn.execute(yurtici_query)
            conn.execute(yurtdisi_query)
            conn.commit()  # Tablo oluşturma işlemlerini tamamla

            print(f"Kayıt başarılı: {phone}")  # Kayıt başarılı mesajı
        except sqlite3.OperationalError as e:
            print(f"Veritabanı hatası: {e}")  # Hata mesajını yazdır
        finally:
            conn.close()  # Bağlantıyı kapat

class CustomerModel(Database):
    def __init__(self, db_name='Database.db'):
        super().__init__(db_name)

        

    def register_musteri(self, name, surname, referans, tarih, telephone, tutar, adres, aciklama, hisse_turu, odenen, phone, durum):
            
            table_name = f"yimusteri_{phone}"
            print(table_name)
            conn = self.connect()
            try:

                # None, boş string ve 0 gibi durumları kontrol et
                newodenen = int(odenen) if odenen not in [None, "", 0] else 0
                newreferans = referans if referans not in [None, "", 0] else "Yok"
                newaciklama = aciklama if aciklama not in [None, "", 0] else "Yok"
                tutar = int(tutar)
                # newodenen ve tutar karşılaştırması
                if newodenen >= tutar:
                    newdurum = "Ücret Alındı"
                else:
                    newdurum = "Ücret Bekleniyor"   

                # Veritabanına veri ekleme
                query = f'INSERT INTO {table_name} (isim, soyisim, referans, tarih, numara, hissetutar, adres, aciklama, hisseturu, odenen, durum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                conn.execute(query, (name, surname, newreferans, tarih, telephone, tutar, adres, newaciklama, hisse_turu, newodenen, newdurum))
                conn.commit()  # Değişiklikleri kaydet
                flash("Kayıt başarılı!")
            except sqlite3.OperationalError as e:
                print(f"Veritabanı hatası: {e}")  # Hata mesajını yazdır
            finally:
                conn.close()  # Bağlantıyı her durumda kapat

    def registeryd_musteri(self, name, surname, referans, tarih, telephone, tutar, adres, aciklama, hisse_turu, odenen, phone, durum):
            
            table_name = f"ydmusteri_{phone}"
            print(table_name)
            conn = self.connect()
            try:

                # None, boş string ve 0 gibi durumları kontrol et
                newodenen = int(odenen) if odenen not in [None, "", 0] else 0
                newreferans = referans if referans not in [None, "", 0] else "Yok"
                newaciklama = aciklama if aciklama not in [None, "", 0] else "Yok"
                tutar = int(tutar)
                    # newodenen ve tutar karşılaştırması
                if newodenen >= tutar:
                    newdurum = "Ücret Alındı"
                else:
                    newdurum = "Ücret Bekleniyor"   

                # Veritabanına veri ekleme
                query = f'INSERT INTO {table_name} (isim, soyisim, referans, tarih, numara, hissetutar, adres, aciklama, hisseturu, odenen, durum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                conn.execute(query, (name, surname, newreferans, tarih, telephone, tutar, adres, newaciklama, hisse_turu, newodenen, newdurum))
                conn.commit()  # Değişiklikleri kaydet
                flash("Kayıt başarılı!")
            except sqlite3.OperationalError as e:
                print(f"Veritabanı hatası: {e}")  # Hata mesajını yazdır
            finally:
                conn.close()  # Bağlantıyı her durumda kapat

    def musteri_getir(self, phone):

        table_name = f"yimusteri_{phone}"

        conn = self.connect()
        query = f"SELECT * FROM {table_name}"
        cursor = conn.execute(query)
        musteriler = cursor.fetchall()  # Veriyi çekiyoruz
        conn.close()
        return musteriler
    
    def tum_musteri_getir(self, phone):

        table_name = f"yimusteri_{phone}"
        table_name2 = f"ydmusteri_{phone}"

        conn = self.connect()
        query = f"SELECT * FROM {table_name} UNION ALL SELECT * FROM {table_name2}"
        cursor = conn.execute(query)
        tummusteriler = cursor.fetchall()  # Veriyi çekiyoruz
        conn.close()
        return tummusteriler
    
    def ydmusteri_getir(self, phone):

        table_name = f"ydmusteri_{phone}"

        conn = self.connect()
        query = f"SELECT * FROM {table_name}"
        cursor = conn.execute(query)
        ydmusteriler = cursor.fetchall()  # Veriyi çekiyoruz
        conn.close()
        return ydmusteriler

    def musteri_sayi(self, phone):

        table_name = f"yimusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor = conn.execute(query)
        toplam_yikayit = cursor.fetchone()[0]
        conn.close()
        
        return toplam_yikayit
    
    def ydmusteri_sayi(self, phone):

        table_name = f"ydmusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor = conn.execute(query)
        toplam_ydkayit = cursor.fetchone()[0]
        conn.close()
        
        return toplam_ydkayit
    
    def yi_odemeler(self, phone):

        table_name = f"yimusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COALESCE(SUM(hissetutar), 0) FROM {table_name}"
        query2 = f"SELECT COALESCE(SUM(odenen), 0) FROM {table_name}"
        cursor = conn.execute(query)
        cursor2 = conn.execute(query2)
        toplam_yitutar = cursor.fetchone()[0]
        toplam_yiodenen = cursor2.fetchone()[0]
        conn.close()

        newtoplamtutar = toplam_yitutar-toplam_yiodenen
        return newtoplamtutar
    
    def yd_odemeler(self, phone):

        table_name = f"ydmusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COALESCE(SUM(hissetutar), 0) FROM {table_name}"
        query2 = f"SELECT COALESCE(SUM(odenen), 0) FROM {table_name}"
        cursor = conn.execute(query)
        cursor2 = conn.execute(query2)
        toplam_ydtutar = cursor.fetchone()[0]
        toplam_ydodenen = cursor2.fetchone()[0]
        conn.close()

        newtoplamtutaryd = toplam_ydtutar-toplam_ydodenen
        return newtoplamtutaryd
    
    def durum_sorguyi(self, phone):

        table_name = f"yimusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COUNT(*) FROM {table_name} WHERE durum = 'Kesildi'"
        cursor = conn.execute(query)
        durum = cursor.fetchone()[0]  # Veriyi çekiyoruz
        conn.close()
        toplam_yikayit = self.musteri_sayi(phone)

        bekleyenhisseyi = toplam_yikayit - durum
        return bekleyenhisseyi

    def durum_sorguyd(self, phone):

        table_name = f"ydmusteri_{phone}" 

        conn = self.connect()
        query = f"SELECT COUNT(*) FROM {table_name} WHERE durum = 'Kesildi'"
        cursor = conn.execute(query)
        durum = cursor.fetchone()[0]  # Veriyi çekiyoruz
        conn.close()
        toplam_ydkayit = self.ydmusteri_sayi(phone)

        bekleyenhisseyd = toplam_ydkayit - durum
        return bekleyenhisseyd
    def kesilenyi(self, phone):
        table_name = f"yimusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COUNT(*) FROM {table_name} WHERE durum = 'Kesildi'"
        cursor = conn.execute(query)
        durum = cursor.fetchone()[0]  # Veriyi çekiyoruz
        conn.close()

        return durum
    
    def kesilenyd(self, phone):
        table_name = f"ydmusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COUNT(*) FROM {table_name} WHERE durum = 'Kesildi'"
        cursor = conn.execute(query)
        durumyd = cursor.fetchone()[0]  # Veriyi çekiyoruz
        conn.close()

        return durumyd
    
    def toplam_hisse(self, phone):
        # Yurt içi ve yurt dışı kesilen kayıtları ayrı ayrı al
        toplam_yd = self.musteri_sayi(phone)
        toplam_yi = self.ydmusteri_sayi(phone)  # Eğer 'kesilenyi' benzeri bir fonksiyon varsa
        
        # Toplam kesilen sayıyı hesapla
        toplam_hisse = toplam_yd + toplam_yi

        return toplam_hisse
        
    def toplam_odenen(self, phone):
        # Yurt içi ve yurt dışı kesilen kayıtları ayrı ayrı al
        table_name = f"yimusteri_{phone}"
        table_name2 = f"ydmusteri_{phone}"

        conn = self.connect()
        query = f"SELECT COALESCE(SUM(odenen), 0) FROM {table_name}"
        query2 = f"SELECT COALESCE(SUM(odenen), 0) FROM {table_name2}"
        cursor = conn.execute(query)
        cursor2 = conn.execute(query2)
        toplam_yiodenen = cursor.fetchone()[0]
        toplam_ydodenen = cursor2.fetchone()[0]
        conn.close()

        newtoplamodenen = toplam_yiodenen+toplam_ydodenen
        return newtoplamodenen