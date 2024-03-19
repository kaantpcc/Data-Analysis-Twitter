import json
from faker import Faker
import random

fake = Faker('en_US')

# Desteklenen bölgeler listesi
desteklenen_bolgeler = {
    'US': ['#uspolitics', '#usnews', '#usculture', '#ustech', '#uslifestyle'],
    'EU': ['#eupolitics', '#eunews', '#euculture', '#eutech', '#eulifestyle'],
    'ASIA': ['#asiapolitics', '#asianews', '#asiaculture', '#asiatech', '#asialifestyle'],
    'AFRICA': ['#africapolitics', '#africanews', '#africaculture', '#africatech', '#africalifestyle'],
    'AUSTRALIA': ['#australiapolitics', '#australianews', '#australiaculture', '#australiatech', '#australialifestyle']
}

sahte_veri_listesi = []

for _ in range(30000):
    ad_soyad = fake.name().split()
    ad = ad_soyad[0]
    soyad = ad_soyad[1]

    takipci_sayisi = random.randint(5, 30)
    takip_edilen_sayisi = random.randint(5, 30)
    bolge = random.choice(list(desteklenen_bolgeler.keys()))  # Rastgele bir bölge seç

    kullanici_verisi = {
        'ad_soyad': ' '.join(ad_soyad),
        'kullanici_adi': f"{ad.lower()}_{soyad.lower()}",
        'takipci_sayisi': takipci_sayisi,
        'takipciler': [f"{fake.first_name().lower()}_{fake.last_name().lower()}" for _ in range(takipci_sayisi)],
        'takip_edilen_sayisi': takip_edilen_sayisi,
        'takip_edilen': [f"{fake.first_name().lower()}_{fake.last_name().lower()}" for _ in range(takip_edilen_sayisi)],
        'dil': 'en',
        'bolge': bolge,
        'kullanici_tweetler': [],
        'tweetler_takipci': [],
        'tweetler_takip_edilen': [],
        'hashtags': desteklenen_bolgeler[bolge]  # Her kullanıcı için bölgeye özel hashtagleri kullan
    }

    # Her takipçiye maksimum 20 tweet atama
    for takipci in kullanici_verisi['takipciler']:
        tweet_sayisi = random.randint(1, 10)
        tweetler = [{'takipci_tweet': fake.text(max_nb_chars=140)} for _ in range(tweet_sayisi)]
        kullanici_verisi['tweetler_takipci'].append({'takipci_kullanici': takipci, 'takipci_tweetleri': tweetler})

    # Her takip edilene maksimum 20 tweet atama
    for takip_edilen in kullanici_verisi['takip_edilen']:
        tweet_sayisi = random.randint(1, 10)
        tweetler = [{'takip_edilen_tweet': fake.text(max_nb_chars=140)} for _ in range(tweet_sayisi)]
        kullanici_verisi['tweetler_takip_edilen'].append({'takip_edilen_kullanici': takip_edilen, 'takip_edilen_tweetleri': tweetler})

    for _ in range(random.randint(20, 40)):
        tweet_verisi = {
            'icerik': fake.text(max_nb_chars=140)
        }
        kullanici_verisi['kullanici_tweetler'].append(tweet_verisi)

    sahte_veri_listesi.append(kullanici_verisi)

for veri in sahte_veri_listesi:
    veri['takipciler'] = [takipci.lower() for takipci in veri['takipciler']]
    veri['takip_edilen'] = [takip_edilen.lower() for takip_edilen in veri['takip_edilen']]

with open('sahte_veriler.json', 'w', encoding='utf-8') as json_file:
    json.dump(sahte_veri_listesi, json_file, ensure_ascii=False, indent=2)

print("Sahte veriler başarıyla oluşturuldu ve 'sahte_veriler.json' dosyasına kaydedildi.")