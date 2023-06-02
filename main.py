import hashlib
import logging 
import multiprocessing
logging.basicConfig(level="DEBUG")
def luna(card: int):
    #one step
    card = str(card)
    card = card[::-1]
    card = list(card)
    logging.info(card)
    #two step
    for i in range(1,len(card),2):
        card[i] = str(int(card[i])*2)
        if(int(card[i])>= 10):
            num = int(card[i]) 
            card[i]= str(num%10)
            num//=10
            card[i]= str(int(card[i])+num%10)
    logging.info(card)
    #three step 
    summ =0
    for i in range(len(card)):
        summ+=int(card[i])
    logging.info(summ)
    if(summ%10==0):
        logging.info("Номер карты является корректным")
        return True
    else:
        logging.info("Номер карты не является корректным")
        return False


def compute_hash(data:int):
    """Считает хэш 

    Args:
        data (int): номер карты
    Returns:
        str: хэш
    """
    data_str = str(data)
    hash_object = hashlib.blake2s()
    hash_object.update(data_str.encode('utf-8'))
    return hash_object.hexdigest()


def my_plan():
    """Функция которая штрудирует все возможные комбинации и находит карту по известном хэшу, бину и последним 4 цифрам"""
    bin = [527576, 543763, 547964, 515460, 527404, 531310, 533669, 536961, 538150, 545152, 546901,
           547902, 547905, 547906, 547907, 547910, 547911, 547912, 547913, 547920, 547901, 547935, 547948]
    number_last = 2301
    flag = False
    hash = "140495200b351b7f18a46e3796f2875ebdf0023568933ef3b99efb285af3f06b"
    i = 0
    while (flag == False):
        number = str(i).zfill(6)
        for j in range(len(bin)):
            card = int(str(bin[j]) + str(number) + str(number_last))
            hash_value = compute_hash(card)
            print(card)
            if (hash_value == hash):
                good_card = card
                flag = True
        i += 1
    if(flag == False):
        logging.info("Карта не найдена")
    else:
        logging.info(f"Найденая карта: {good_card}")  # 547905 415657 2301
        luna(good_card)



if __name__ == '__main__':
    luna(5479054156572301)
    logging.info(compute_hash(5479054156572301))
