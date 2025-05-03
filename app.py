from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import UserModel, CustomerModel

app = Flask(__name__)
app.secret_key = 'gizli_sifre'  # Flash mesajları için bir anahtar belirleyin

user_model = UserModel()
customer_model = CustomerModel()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        
        user = user_model.get_user_by_phone(phone)
        
        if user and user['password'] == password:
            session['user_id'] = user['phone']  # Kullanıcının oturumunu başlatıyoruz
            session['phone'] = phone
            print("Session phone kaydedildi:", session['phone'])
            flash("Başarıyla giriş yaptınız!")
            return redirect(url_for('dashboard'))  # Başarılı giriş sonrası dashboard yönlendirme
        else:
            flash("Hatalı telefon numarası veya şifre!")
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form['register_phone']
        password = request.form['register_password']
        confirm_password = request.form['confirm_password']
        
        # Şifrelerin eşleşip eşleşmediğini kontrol et
        if password != confirm_password:
            flash("Şifreler uyuşmuyor!")  # Flash mesajı ile popup tetikleyeceğiz
            return redirect(url_for('index'))  # Şifreler uyuşmazsa ana ekrana dön
        
        # Kullanıcı zaten var mı kontrol et
        existing_user = user_model.get_user_by_phone(phone)
        if existing_user:
            flash("Bu telefon numarası zaten kayıtlı!")
            return redirect(url_for('index'))  # Kullanıcı zaten varsa, ana ekrana dön
        
        # Yeni kullanıcıyı kaydet
        user_model.register_user(phone, password)
        flash("Kayıt başarılı! Lütfen giriş yapın.")
        return redirect(url_for('index'))  # Kayıt işlemi başarılıysa, giriş sayfasına yönlendir

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Bu sayfaya erişebilmek için giriş yapmalısınız.")
        return redirect(url_for('index'))
    
    phone = session.get('phone')
    tummusteriler = customer_model.tum_musteri_getir(phone)
    toplam_hisse = customer_model.toplam_hisse(phone)
    yi_hissesayi = customer_model.musteri_sayi(phone)
    yd_hissesayi = customer_model.ydmusteri_sayi(phone)
    toplam_odenen = customer_model.toplam_odenen(phone)
    return render_template('anasayfa.html', tummusteriler=tummusteriler, toplam_hisse=toplam_hisse, yi_hissesayi=yi_hissesayi, yd_hissesayi=yd_hissesayi, toplam_odenen=toplam_odenen)


@app.route('/logout')
def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız.")
    return redirect(url_for('index'))



@app.route('/yurtici')
def yurtici():
    phone = session.get('phone')
    musteriler = customer_model.musteri_getir(phone)
    toplam_yikayit = customer_model.musteri_sayi(phone)
    new_toplamtutar = customer_model.yi_odemeler(phone)
    bekleyenhisseyi = customer_model.durum_sorguyi(phone)
    durum = customer_model.kesilenyi(phone)

    return render_template('yurtici.html', musteriler=musteriler, toplam_yikayit=toplam_yikayit, new_toplamtutar=new_toplamtutar, bekleyenhisseyi=bekleyenhisseyi, durum=durum)

@app.route('/yurtdisi')
def yurtdisi():
    phone = session.get('phone')
    ydmusteriler = customer_model.ydmusteri_getir(phone)    
    toplam_ydkayit = customer_model.ydmusteri_sayi(phone)    
    new_toplamtutaryd = customer_model.yd_odemeler(phone)    
    bekleyenhisseyd = customer_model.durum_sorguyd(phone)    
    durumyd = customer_model.kesilenyd(phone)

    return render_template('yurtdisi.html', ydmusteriler=ydmusteriler, toplam_ydkayit=toplam_ydkayit, new_toplamtutaryd=new_toplamtutaryd, bekleyenhisseyd=bekleyenhisseyd, durumyd=durumyd)

@app.route('/yurticisatis', methods=['GET', 'POST'])
def satisekle1():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        referans = request.form['referans']
        tarih = request.form['tarih']
        telephone = request.form['telephone']
        tutar = request.form['tutar']
        adres = request.form['adres']
        aciklama = request.form['aciklama']
        hisse_turu = request.form['hisse_turu']
        odenen = request.form['odenen']
        durum = "Ücret Bekleniyor"

        phone = session.get('phone')

        customer_model.register_musteri(name, surname, referans, tarih, telephone, tutar, adres, aciklama, hisse_turu, odenen, phone, durum)
        return redirect(url_for('satisekle1'))

    return render_template('satisekle1.html')

@app.route('/yurtdisisatis', methods=['GET', 'POST'])
def satisekle2():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        referans = request.form['referans']
        tarih = request.form['tarih']
        telephone = request.form['telephone']
        tutar = request.form['tutar']
        adres = request.form['adres']
        aciklama = request.form['aciklama']
        hisse_turu = request.form['hisse_turu']
        odenen = request.form['odenen']
        durum = "Ücret Bekleniyor"

        phone = session.get('phone')

        customer_model.registeryd_musteri(name, surname, referans, tarih, telephone, tutar, adres, aciklama, hisse_turu, odenen, phone, durum)
        return redirect(url_for('satisekle2'))

    return render_template('satisekle2.html')


if __name__ == '__main__':
    app.run(debug=True)
