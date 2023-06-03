import hashlib
import logging

logging.basicConfig(level="DEBUG")


def compute_hash(card: int, CONFIG) -> int:
    """Функция делает проверку хэша по номеру карты

    Args:
        card_center (int): середина номера карты
        card_begin (int): начало номера карты

    Returns:
        int: номер, если проверка пройдена, и False в противном случае
    """
    card_str = str(card)
    hash_object = hashlib.blake2s()
    hash_object.update(card_str.encode('utf-8'))
    hash_object.hexdigest()
    if (CONFIG["hash"] == hash_object.hexdigest()):
        return True
    else:
        return False


def luna(card: int) -> bool:
    """Функция проверки номера карты алгоритмом Луна

    Args:
        card_number (int): номер карты

    Returns:
        bool: результат проверки
    """
    logging.info(f"Запущен алгоритм луна с картой {card}")
    card = str(card)
    card = card[::-1]
    card = list(card)
    for i in range(1, len(card), 2):
        card[i] = str(int(card[i])*2)
        if (int(card[i]) >= 10):
            num = int(card[i])
            card[i] = str(num % 10)
            num //= 10
            card[i] = str(int(card[i])+num % 10)
    summ = 0
    for i in range(len(card)):
        summ += int(card[i])
    if (summ % 10 == 0):
        logging.info("Номер карты является корректным")
        return True
    else:
        logging.error("Номер карты не является корректным")
        return False
