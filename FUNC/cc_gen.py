import random

def check_luhn(card_no):
    digits = list(map(int, card_no))
    checksum = 0
    parity = len(digits) % 2

    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0

def cc_generator(cc, mes, ano, cvv):
    cc, mes, ano, cvv = str(cc), str(mes), str(ano), str(cvv)

    if mes.lower() in ["none", "x", "xx", "rnd"]:
        mes = str(random.randint(1, 12)).zfill(2)

    if ano.lower() in ["none", "x", "xx", "rnd"]:
        ano = str(random.randint(2024, 2035))

    if cvv.lower() in ["none", "x", "xx", "rnd"]:
        cvv = str(random.randint(1000, 9999) if cc.startswith(("34", "37")) else random.randint(100, 999))

    while True:
        gen = "".join(str(random.randint(0, 9)) if x.lower() == 'x' else x for x in cc)
        length = 15 if gen.startswith(("34", "37")) else 16
        card = gen[:length]

        if check_luhn(card):
            break

    return f"{card}|{mes}|{ano}|{cvv}"

def luhn_card_generator(cc, mes, ano, cvv, amount):
    cards = []
    for _ in range(amount):
        card = cc_generator(cc, mes, ano, cvv)
        cards.append(card)
    return "\n".join(cards)
