import json
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

onemsiz_kelimeler = set(stopwords.words('english'))

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        yeni_dugum = Node(data)
        if not self.head:
            self.head = yeni_dugum
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = yeni_dugum
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

class Dictionary:
    def __init__(self):
        self.items = []

    def ekle(self, anahtar, deger):
        for item in self.items:
            if item[0] == anahtar:
                item[1] = deger
                return
        self.items.append([anahtar, deger])
    
    def guncelle(self, anahtar, deger):
        for item in self.items:
            if item[0] == anahtar:
                item[1] = deger
                return
    
    def al(self, anahtar, deger):
        for item in self.items:
            if item[0] == anahtar:
                return item[1]
        
    def hepsini_al(self):
        return self.items
    
class Kume:
    def __init__(self, elements=None):
        self.elements = elements or []

    def boyut(self):
        return len(self.elements)

    def ekle(self, item):
        if item not in self.elements:
            self.elements.append(item)

    def guncelle(self, items):
        for item in items:
            self.ekle(item)

    def kesisim(self, other_set):
        sonuc = Kume()
        for item in self.elements:
            if item in other_set.elements:
                sonuc.ekle(item)
        return sonuc

    def __iter__(self):
        return iter(self.elements)
    
class UserHashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def hash_fonksiyonu(self, key):
        return sum(ord(char) for char in key) % self.size

    def ekle(self, user):
        anahtar = user.username
        index = self.hash_fonksiyonu(anahtar)
        if self.table[index] is None:
            self.table[index] = [(anahtar, user)]
        else:
            for i, (bulunan_anahtar, _) in enumerate(self.table[index]):
                if bulunan_anahtar == anahtar:
                    self.table[index][i] = (anahtar, user)
                    break
            else:
                self.table[index].append((anahtar, user))

    def get(self, key):
        index = self.hash_fonksiyonu(key)
        if self.table[index] is not None:
            for bulunan_anahtar, user in self.table[index]:
                if bulunan_anahtar == key:
                    return user
                
class IlgiAlanlariHashTablosu:
    def __init__(self):
        self.ilgi_alanlari_kullanicilar = {}

    def ekle(self, ilgi_alani, kullanici):
        if ilgi_alani not in self.ilgi_alanlari_kullanicilar:
            self.ilgi_alanlari_kullanicilar[ilgi_alani] = set()
        self.ilgi_alanlari_kullanicilar[ilgi_alani].add(kullanici)

    def getir(self, ilgi_alani):
        return list(self.ilgi_alanlari_kullanicilar.get(ilgi_alani, set()))
    

class IlgiAlanlariHashTablosuTakipci(IlgiAlanlariHashTablosu):
    pass

class IlgiAlanlariHashTablosuTakipEdilen(IlgiAlanlariHashTablosu):
    pass

class SimpleGraph:
    def __init__(self):
        self.nodes = Kume()
        self.edges = Dictionary()

    def dugum_ekle(self, node):
        self.nodes.ekle(node)

    def kenar_ekle(self, node1, node2, label=None):
        if any((node1, node2) == item[0] for item in self.edges.items):
            self.edges.ekle((node1, node2), label)
        else:
            self.edges.ekle((node1, node2), label)

class Queue:
    def __init__(self):
        self.items = LinkedList()

    def bos_mu(self):
        return len(self.items) == 0

    def siraya_al(self, item):
        self.items.append(item)

    def kuyruktan_al(self):
        if not self.bos_mu():
            return self.items.pop(0)
        else:
            raise IndexError("Queue is empty!")
        
def bfs_search(graph, start):
    ziyaret_edilen = Kume()
    sira = Queue()
    sonuc = LinkedList()

    sira.siraya_al(start)

    while not sira.bos_mu():
        bulundugun_dugum = sira.kuyruktan_al()

        if bulundugun_dugum not in ziyaret_edilen:
            sonuc.append(bulundugun_dugum)
            ziyaret_edilen.ekle(bulundugun_dugum)

            komsular = graph.edges.get(bulundugun_dugum, LinkedList())
            for komsu in komsular:
                if komsu not in ziyaret_edilen and komsu not in sira.items:
                    sira.siraya_al(komsu)

    return sonuc

def ortak_dugumleri_bul(graph1, graph2):
    ortak_dugumler = (graph1.nodes) & (graph2.nodes)
    return ortak_dugumler

class User:
    def __init__(self, username, name, followers_count, following_count, language, region, followers, following, tweets, hashtags):
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.language = language
        self.region = region
        self.followers = LinkedList()
        self.following = LinkedList()
        self.tweets = LinkedList()
        self.hashtags = hashtags

        # followers
        for follower in followers:
            self.followers.append(follower)

        # following
        for follow in following:
            self.following.append(follow)
       
       # tweets
        for tweet in tweets:
            self.tweets.append(tweet)

    def bolgeye_ozel_hashtagler(self):
        return self.hashtags.get(self.region, LinkedList())
    
  
with open('sahte_veriler.json', 'r') as file:
    data = json.load(file)

# kullanıcı hash tablosu olustur.
kullanici_hash_tablosu = UserHashTable(size=100)

for kullanici_verisi in data:
    user = User(
        kullanici_verisi.get('kullanici_adi', ''),
        kullanici_verisi.get('ad_soyad', ''),
        kullanici_verisi.get('takipci_sayisi', 0),
        kullanici_verisi.get('takip_edilen_sayisi', 0),
        kullanici_verisi.get('dil', ''),
        kullanici_verisi.get('bolge', ''),
        kullanici_verisi.get('takipciler', LinkedList()),
        kullanici_verisi.get('takip_edilen', LinkedList()),
        kullanici_verisi.get('tweetler', LinkedList()),
        kullanici_verisi.get('hashtags', LinkedList())  
    )

    kullanici_hash_tablosu.ekle(user)

# random kullanıcı sec
random_kullanici_verisi1 = random.choice(data)
random_kullanici_verisi2 = random.choice(data)

random_kullanici_adi1 = random_kullanici_verisi1.get('kullanici_adi', '')
random_kullanici_adi2 = random_kullanici_verisi2.get('kullanici_adi', '')

# hash tablosundan random kullanıcıları al
random_kullanici1 = kullanici_hash_tablosu.get(random_kullanici_adi1)
random_kullanici2 = kullanici_hash_tablosu.get(random_kullanici_adi2)

print(f"\nKullanici Adi: {random_kullanici1.username}")
print(f"Isim: {random_kullanici1.name}")
print(f"Takipci Sayisi: {random_kullanici1.followers_count}")
print(f"Takip Edilen Sayisi: {random_kullanici1.following_count}")
print(f"Dil: {random_kullanici1.language}")
print(f"Bolge: {random_kullanici1.region}")
print(f"Hashtagler: {random_kullanici1.hashtags}")

print("\nTakipciler:")
for takipci_dugumu in random_kullanici1.followers:
    print(takipci_dugumu.data)

print("\nTakip Edilenler:")
for takip_edilen_dugumu in random_kullanici1.following:
    print(takip_edilen_dugumu.data)

print("\nTweetler:")
for tweet_verisi in random_kullanici_verisi1['kullanici_tweetler']:
    print(tweet_verisi['icerik'])

simple_graph = SimpleGraph()
simple_graph.dugum_ekle(random_kullanici1.username)

for takipci_dugumu in random_kullanici1.followers:
    simple_graph.dugum_ekle(takipci_dugumu.data)
    simple_graph.kenar_ekle(takipci_dugumu.data, random_kullanici1.username, label='T')

for takip_edilen_dugumu in random_kullanici1.following:
    simple_graph.dugum_ekle(takip_edilen_dugumu.data)
    simple_graph.kenar_ekle(random_kullanici1.username, takip_edilen_dugumu.data, label='TE')

G = nx.DiGraph()

for dugum in simple_graph.nodes:
    G.add_node(dugum)

for (kenar_baslangic, kenar_bitis), label in simple_graph.edges.items:
    G.add_edge(kenar_baslangic, kenar_bitis, label=label)

pos = nx.spring_layout(G, k=1, iterations=50)

dugum_renkleri = ['blue' if node == random_kullanici1.username else 'red' for node in G.nodes]
kenar_renkleri = ['black' if G[kenar_baslangic][kenar_bitis]['label'] == 'TE' else 'gray' for kenar_baslangic, kenar_bitis in G.edges]

nx.draw(G, pos, with_labels=True, font_weight='light', node_color=dugum_renkleri, edge_color=kenar_renkleri, node_size=400, font_size=6)

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

kelimeler_kullanici = Kume()

for tweet_verisi in random_kullanici_verisi1['kullanici_tweetler']:
    kelimeler = word_tokenize(tweet_verisi['icerik'].lower())
    kelimeler_kullanici.guncelle([kelime for kelime in kelimeler if kelime.isalnum() and kelime not in onemsiz_kelimeler])

# kullanıcının ilgi alanlarını tutacak ilgi alanları hash tablosu olustur.
ilgi_alanlari_takipciler1 = IlgiAlanlariHashTablosuTakipci()
ilgi_alanlari_takipedilenler1 = IlgiAlanlariHashTablosuTakipEdilen()

# kullanıcının ilgi alanlarını ilgili hash tablosuna ekle
for ilgi_alani in kelimeler_kullanici:
    ilgi_alanlari_takipciler1.ekle(ilgi_alani, random_kullanici1.username)
    ilgi_alanlari_takipedilenler1.ekle(ilgi_alani, random_kullanici1.username)

# kullanıcının takipçilerinin bütün tweetlerinde geçen kelimeleri topla
for takipci_verisi in random_kullanici_verisi1['tweetler_takipci']:
    takipci_kullanici_adi = takipci_verisi['takipci_kullanici']
    kelimeler_kullanici_takipci = Kume()

    for tweet_verisi in takipci_verisi['takipci_tweetleri']:
        kelimeler = word_tokenize(tweet_verisi['takipci_tweet'].lower())
        kelimeler_kullanici_takipci.guncelle([kelime for kelime in kelimeler if kelime.isalnum() and kelime not in onemsiz_kelimeler])

# ortak kelimeleri bul ve hash tablosuna ekle
    ortak_kelimeler = kelimeler_kullanici.kesisim(kelimeler_kullanici_takipci)
    for ilgi_alani in ortak_kelimeler:
        ilgi_alanlari_takipciler1.ekle(ilgi_alani, takipci_kullanici_adi)


for takip_edilen_verisi in random_kullanici_verisi1['tweetler_takip_edilen']:
    takip_edilen_kullanici_adi = takip_edilen_verisi['takip_edilen_kullanici']
    kelimeler_kullanici_takip_edilen = Kume()

    for tweet_verisi in takip_edilen_verisi['takip_edilen_tweetleri']:
        kelimeler = word_tokenize(tweet_verisi['takip_edilen_tweet'].lower())
        kelimeler_kullanici_takip_edilen.guncelle([kelime for kelime in kelimeler if kelime.isalnum() and kelime not in onemsiz_kelimeler])

    ortak_kelimeler = kelimeler_kullanici.kesisim(kelimeler_kullanici_takip_edilen)

    for ilgi_alani in ortak_kelimeler:
        ilgi_alanlari_takipedilenler1.ekle(ilgi_alani, takip_edilen_kullanici_adi)

# çıktıyı dosyaya kaydet
with open('ortak_ilgi_alanlari_takipciler1.txt', 'w', encoding='utf-8') as file_takipciler, \
     open('ortak_ilgi_alanlari_takipedilenler1.txt', 'w', encoding='utf-8') as file_takipedilenler:
    
    for ilgi_alani, kullanicilar in ilgi_alanlari_takipciler1.ilgi_alanlari_kullanicilar.items():
        if len(kullanicilar) > 1:
            file_takipciler.write(f"\nIlgi Alani: {ilgi_alani}\n")
            file_takipciler.write(f"Kullanici ve takipcileri: {', '.join(kullanicilar)}\n")
    
    for ilgi_alani, kullanicilar in ilgi_alanlari_takipedilenler1.ilgi_alanlari_kullanicilar.items():
        if len(kullanicilar) > 1:
            file_takipedilenler.write(f"\nIlgi Alani: {ilgi_alani}\n")
            file_takipedilenler.write(f"Kullanici ve takip edilenleri: {', '.join(kullanicilar)}\n")

plt.show()

# 2.kullanıcı icin
print(f"\nKullanici Adi: {random_kullanici2.username}")
print(f"Isim: {random_kullanici2.name}")
print(f"Takipci Sayisi: {random_kullanici2.followers_count}")
print(f"Takip Edilen Sayisi: {random_kullanici2.following_count}")
print(f"Dil: {random_kullanici2.language}")
print(f"Bolge: {random_kullanici2.region}")
print(f"Hashtagler: {random_kullanici2.hashtags}")

print("\nTakipciler:")
for takipci_dugumu in random_kullanici2.followers:
    print(takipci_dugumu.data)

print("\nTakip Edilenler:")
for takip_edilen_dugumu in random_kullanici2.following:
    print(takip_edilen_dugumu.data)

print("\nTweetler:")
for tweet_verisi in random_kullanici_verisi2['kullanici_tweetler']:
    print(tweet_verisi['icerik'])

simple_graph = SimpleGraph()
simple_graph.dugum_ekle(random_kullanici2.username)

for takipci_dugumu in random_kullanici2.followers:
    simple_graph.dugum_ekle(takipci_dugumu.data)
    simple_graph.kenar_ekle(takipci_dugumu.data, random_kullanici2.username, label='T')

for takip_edilen_dugumu in random_kullanici2.following:
    simple_graph.dugum_ekle(takip_edilen_dugumu.data)
    simple_graph.kenar_ekle(random_kullanici2.username, takip_edilen_dugumu.data, label='TE')

G = nx.DiGraph()

for dugum in simple_graph.nodes:
    G.add_node(dugum)

for (kenar_baslangic, kenar_bitis), label in simple_graph.edges.items:
    G.add_edge(kenar_baslangic, kenar_bitis, label=label)

pos = nx.spring_layout(G, k=1, iterations=50)

dugum_renkleri = ['yellow' if node == random_kullanici2.username else 'green' for node in G.nodes]
kenar_renkleri = ['black' if G[kenar_baslangic][kenar_bitis]['label'] == 'TE' else 'gray' for kenar_baslangic, kenar_bitis in G.edges]

nx.draw(G, pos, with_labels=True, font_weight='light', node_color=dugum_renkleri, edge_color=kenar_renkleri, node_size=400, font_size=6)

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

kelimeler_kullanici = Kume()

for tweet_verisi in random_kullanici_verisi2['kullanici_tweetler']:
    kelimeler = word_tokenize(tweet_verisi['icerik'].lower())
    kelimeler_kullanici.guncelle([kelime for kelime in kelimeler if kelime.isalnum() and kelime not in onemsiz_kelimeler])

ilgi_alanlari_takipciler2 = IlgiAlanlariHashTablosuTakipci()
ilgi_alanlari_takipedilenler2 = IlgiAlanlariHashTablosuTakipEdilen()

for ilgi_alani in kelimeler_kullanici:
    ilgi_alanlari_takipciler2.ekle(ilgi_alani, random_kullanici2.username)
    ilgi_alanlari_takipedilenler2.ekle(ilgi_alani, random_kullanici2.username)

for takipci_verisi in random_kullanici_verisi2['tweetler_takipci']:
    takipci_kullanici_adi = takipci_verisi['takipci_kullanici']
    kelimeler_kullanici_takipci = Kume()

    for tweet_verisi in takipci_verisi['takipci_tweetleri']:
        kelimeler = word_tokenize(tweet_verisi['takipci_tweet'].lower())
        kelimeler_kullanici_takipci.guncelle([word for word in kelimeler if word.isalnum() and word not in onemsiz_kelimeler])

    ortak_kelimeler = kelimeler_kullanici.kesisim(kelimeler_kullanici_takipci)

    for ilgi_alani in ortak_kelimeler:
        ilgi_alanlari_takipciler2.ekle(ilgi_alani, takipci_kullanici_adi)

for takip_edilen_verisi in random_kullanici_verisi2['tweetler_takip_edilen']:
    takip_edilen_kullanici_adi = takip_edilen_verisi['takip_edilen_kullanici']
    kelimeler_kullanici_takip_edilen = Kume()

    for tweet_verisi in takip_edilen_verisi['takip_edilen_tweetleri']:
        kelimeler = word_tokenize(tweet_verisi['takip_edilen_tweet'].lower())
        kelimeler_kullanici_takip_edilen.guncelle([word for word in kelimeler if word.isalnum() and word not in onemsiz_kelimeler])

    ortak_kelimeler = kelimeler_kullanici.kesisim(kelimeler_kullanici_takip_edilen)

    for ilgi_alani in ortak_kelimeler:
        ilgi_alanlari_takipedilenler2.ekle(ilgi_alani, takip_edilen_kullanici_adi)


with open('ortak_ilgi_alanlari_takipciler2.txt', 'w', encoding='utf-8') as file_takipciler, \
     open('ortak_ilgi_alanlari_takipedilenler2.txt', 'w', encoding='utf-8') as file_takipedilenler:
    
    for ilgi_alani, kullanicilar in ilgi_alanlari_takipciler2.ilgi_alanlari_kullanicilar.items():
        if len(kullanicilar) > 1:
            file_takipciler.write(f"\nIlgi Alani: {ilgi_alani}\n")
            file_takipciler.write(f"Kullanici ve takipcileri: {', '.join(kullanicilar)}\n")
    
    for ilgi_alani, kullanicilar in ilgi_alanlari_takipedilenler2.ilgi_alanlari_kullanicilar.items():
        if len(kullanicilar) > 1:
            file_takipedilenler.write(f"\nIlgi Alani: {ilgi_alani}\n")
            file_takipedilenler.write(f"Kullanici ve takip edilenleri: {', '.join(kullanicilar)}\n")

with open('hashtags.txt', 'w', encoding='utf-8') as file_hashtags:
    file_hashtags.write(f"1.Kullanıcının bulundugu bolge: {random_kullanici1.region}")
    file_hashtags.write("\n1.Kullanıcının Bulunduğu Bölgedeki Hashtagler:")
    file_hashtags.write(', '.join(random_kullanici1.hashtags))  
    file_hashtags.write(f"\n2.Kullanıcının bulundugu bolge: {random_kullanici2.region}")
    file_hashtags.write("\n2.Kullanıcının Bulunduğu Bölgedeki Hashtagler:")
    file_hashtags.write(', '.join(random_kullanici2.hashtags))

ilgi_alanlari_takipciler_kume1 = Kume()
ilgi_alanlari_takipciler_kume2 = Kume()

for ilgi_alani, kullanicilar in ilgi_alanlari_takipciler1.ilgi_alanlari_kullanicilar.items():
        if len(kullanicilar) > 1:
             ilgi_alanlari_takipciler_kume1.guncelle([ilgi_alani])

for ilgi_alani, kullanicilar in ilgi_alanlari_takipciler2.ilgi_alanlari_kullanicilar.items():
        if len(kullanicilar) > 1:
             ilgi_alanlari_takipciler_kume2.guncelle([ilgi_alani])

ilgi_alanlari_kesisim_kume = ilgi_alanlari_takipciler_kume1.kesisim(ilgi_alanlari_takipciler_kume2)

with open('ilgi_alanlari_kesisim.txt', 'w', encoding='utf-8') as file_output:
    file_output.write(random_kullanici_adi1 + " ile " + random_kullanici_adi2 + " ortak ilgi alanlari : ")
    for item in ilgi_alanlari_kesisim_kume:
        file_output.write(item + '\n')

plt.show()

# 1.kullanıcı için ortak ilgi alanları grafı
kullanici1 = random_kullanici_adi1
G1 = nx.DiGraph()

G1.add_node(kullanici1, color='blue', node_type='user')

for ilgi_alanlari in ilgi_alanlari_takipciler_kume1:
    G1.add_node(ilgi_alanlari, color='red', node_type='interest')

for ilgi_alanlari in ilgi_alanlari_takipciler_kume1:
    G1.add_edge(kullanici1, ilgi_alanlari, label='')

pos = nx.spring_layout(G1, k=1, iterations=50)

dugum_renkleri = [G1.nodes[node]['color'] for node in G1.nodes]
kenar_renkleri = ['black' if G1[kenar_baslangic][kenar_bitis]['label'] == 'TE' else 'gray' for kenar_baslangic, kenar_bitis in G1.edges]

nx.draw(G1, pos, with_labels=True, font_weight='light', node_color=dugum_renkleri, edge_color=kenar_renkleri, node_size=400, font_size=6)

edge_labels = nx.get_edge_attributes(G1, 'label')
nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels, font_color='black', font_size=6)

plt.show()

# 2.kullanıcı için ortak ilgi alanları grafı
kullanici2 = random_kullanici_adi2

G2 = nx.DiGraph()

G2.add_node(kullanici2, color='yellow', node_type='user')

for ilgi_alanlari in ilgi_alanlari_takipciler_kume2:
    G2.add_node(ilgi_alanlari, color='green', node_type='interest')

for ilgi_alanlari in ilgi_alanlari_takipciler_kume2:
    G2.add_edge(kullanici2, ilgi_alanlari, label='')

pos = nx.spring_layout(G2, k=1, iterations=50)

dugum_renkleri = [G2.nodes[node]['color'] for node in G2.nodes]
kenar_renkleri = ['black' if G2[kenar_baslangic][kenar_bitis]['label'] == 'TE' else 'gray' for kenar_baslangic, kenar_bitis in G2.edges]

nx.draw(G2, pos, with_labels=True, font_weight='light', node_color=dugum_renkleri, edge_color=kenar_renkleri, node_size=400, font_size=6)

edge_labels = nx.get_edge_attributes(G2, 'label')
nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_color='black', font_size=6)

ortak_dugumler = ortak_dugumleri_bul(G1, G2)

print("Ortak düğümler:", ortak_dugumler)

plt.show()

# 1. ve 2. kullanıcılar icin ortak ilgi alanlari
kullanici1 = "ortak_kullanicilar"
ortak_ilgi_alanlari = ilgi_alanlari_kesisim_kume

G = nx.DiGraph()

G.add_node(kullanici1, color='blue', node_type='user')

for ilgi_alanlari in ortak_ilgi_alanlari:
    G.add_node(ilgi_alanlari, color='red', node_type='interest')

for ilgi_alanlari in ortak_ilgi_alanlari:
    G.add_edge(kullanici1, ilgi_alanlari, label='')

pos = nx.spring_layout(G, k=1, iterations=25)

dugum_renkleri = [G.nodes[node]['color'] for node in G.nodes]
kenar_renkleri = ['black' if G[kenar_baslangic][kenar_bitis]['label'] == 'TE' else 'gray' for kenar_baslangic, kenar_bitis in G.edges]

nx.draw(G, pos, with_labels=True, font_weight='light', node_color=dugum_renkleri, edge_color=kenar_renkleri, node_size=400, font_size=6)

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=6)

plt.show()

G = nx.Graph()

G.add_node(random_kullanici_verisi1['kullanici_adi'])
G.add_node(random_kullanici_verisi2['kullanici_adi'])

for ilgi_alani in ilgi_alanlari_kesisim_kume:
    ortak_ilgi_alanina_sahip_kullanicilar = ilgi_alanlari_takipciler1.getir(ilgi_alani)
    for i in range(len(ortak_ilgi_alanina_sahip_kullanicilar) ):
        for j in range(i + 1, len(ortak_ilgi_alanina_sahip_kullanicilar)):
            kullanici1, kullanici2 = ortak_ilgi_alanina_sahip_kullanicilar[i], ortak_ilgi_alanina_sahip_kullanicilar[j]
            G.add_edge(kullanici1, kullanici2)

for ilgi_alani in ilgi_alanlari_kesisim_kume:
    ortak_ilgi_alanina_sahip_kullanicilar = ilgi_alanlari_takipciler2.getir(ilgi_alani)
    for i in range(len(ortak_ilgi_alanina_sahip_kullanicilar) ):
        for j in range(i + 1, len(ortak_ilgi_alanina_sahip_kullanicilar)):
            kullanici1, kullanici2 = ortak_ilgi_alanina_sahip_kullanicilar[i], ortak_ilgi_alanina_sahip_kullanicilar[j]
            G.add_edge(kullanici1, kullanici2)

G.add_edge(random_kullanici_verisi1['kullanici_adi'],random_kullanici_verisi2['kullanici_adi'])
mst_kenarlari = list(nx.minimum_spanning_edges(G))
mst_graph = nx.Graph()
mst_graph.add_edges_from(mst_kenarlari)
pos = nx.spring_layout(mst_graph, seed=42)
nx.draw(mst_graph, pos, with_labels=True, font_weight='light', node_size=800, font_size=8, edge_color='b')

edge_labels = nx.get_edge_attributes(mst_graph, 'weight')
nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=edge_labels, font_color='black', font_size=8)

plt.show()