import hashlib

def compute_hash(data):
    # Преобразуем данные в строку
    data_str = str(data)

    # Создаем объект хэша с алгоритмом Blake2s
    hash_object = hashlib.blake2s()

    # Обновляем хэш с данными
    hash_object.update(data_str.encode('utf-8'))

    # Вычисляем и возвращаем хэш в шестнадцатеричном формате
    return hash_object.hexdigest()

def my_plan():
    bin = [527576, 543763, 547964, 515460, 527404, 531310, 533669, 536961, 538150, 545152, 546901, 547902, 547905, 547906, 547907, 547910,547911,547912,547913,547920,547901,547935,547948]
    number_last = 2301
    flag = False
    hash = "140495200b351b7f18a46e3796f2875ebdf0023568933ef3b99efb285af3f06b"
    i = 0
    while(flag==False):
        number = str(i).zfill(6)
        for j in range(len(bin)):
            card = int(str(bin[j])+ str(number) + str(number_last))
            hash_value = compute_hash(card)
            print(card)
            if(hash_value == hash):
                good_card= card
                flag= True 
        i+=1
    print("good card = ",good_card)#5479054156572301

if __name__ == '__main__':
    my_plan()
    


