import time
from selenium import webdriver
import re
import csv

def scrape_data_to_csv():
    url = 'https://www.onlinejcf.com/article/S1071-9164(22)00076-8/fulltext#seccesectitle0026'
    ops = webdriver.ChromeOptions()
    # ops.add_argument('--proxy-server=%s' % ip)
    # Désactiver la barre d'automatisation
    ops.add_experimental_option('excludeSwitches', ['enable-automation'])
    # Bloquer la boîte d'invite de sauvegarde du mot de passe
    prefs = {'credentials_enable_service': False, 'profile.password_manager_enable': False}
    ops.add_experimental_option('prefs', prefs)
    # Fonctionnalités anti-crawler
    ops.add_argument('--disable-blink-features=AutomationControlled')
    browser1 = webdriver.Chrome(options=ops)  # 启动浏览器
    browser1.get(url)
    time.sleep(10)
    content = browser1.page_source

    obj = re.findall(
        'class="sectionTitle"><span class="top__sub">(.*?)</span>(.*?)</span>.*?<strong>Synopsis</strong></div><div class="section-paragraph">(.*?)</div><div class="section-paragraph"><strong>Recommendation-Specific Supportive Text</strong>(.*?)</ul>',
        content, re.S)
    titles = []
    final_recomm = []
    for index, item in enumerate(obj, start=1):
        title = f'{index}. What is ' + item[1].replace('<span class="top__text">', '') + ":"
        titles.append(title)
        sym = item[2]
        final_recomm.append(sym)
        recomm = item[3]
        idx = recomm.index('<span class="label">')
        l = len('<span class="label">')
        idx += l
        recomm = recomm[idx:]
        recomm = 'Recommendations:\n' + recomm.replace('<span class="label">', '').replace('</span>', '').replace(
            '</ a>', '').replace('</div></li>', '').replace('<div class="ce-list--remove-bullets__list-item__text">',
                                                            '')
        title2 = f'{index}. What is Recommendation of ' + item[1].replace('<span class="top__text">', '') + ":"
        titles.append(title2)
        final_recomm.append(recomm)

    header = ['id', 'question', 'answer']
    data = zip(range(1, len(titles) + 1), titles, final_recomm)
    with open('qa_pairs.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    file_path = 'E:\chatbot\Code\qa_pairs.csv'
    # Lire le contenu d'un fichier
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # Utilisez des expressions régulières pour supprimer tous les <... > et leur contenu
    new_contents = re.sub(r'<[^>]*>', '', file_contents)

    # Réécrire le contenu mis à jour dans le fichier
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_contents)