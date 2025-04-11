import random

def check_luhn(card_no):
    n_sum = 0
    is_second = False
    for i in range(len(card_no) - 1, -1, -1):
        d = int(card_no[i])
        if is_second:
            d *= 2
        n_sum += d // 10
        n_sum += d % 10
        is_second = not is_second
    return n_sum % 10 == 0


def cc_generator(cc, mes, ano, cvv):
    if mes and len(mes) == 1:
        mes = "0" + mes
    if ano and len(ano) == 2:
        ano = "20" + ano

    length = 15 if cc[:2] in ["34", "37"] else 16
    cc_base = cc + ''.join(random.choices("0123456789", k=length))
    cc_gen = cc_base[:length]

    cc_gen = ''.join(
        str(random.randint(0, 9)) if x == 'x' else x
        for x in cc_gen
    )

    mes = mes if mes and "x" not in mes.lower() else f"{random.randint(1, 12):02d}"
    ano = ano if ano and "x" not in str(ano).lower() else str(random.randint(2024, 2035))

    if not cvv or 'x' in str(cvv).lower():
        cvv = str(random.randint(1000, 9999)) if cc_gen.startswith(("34", "37")) else str(random.randint(100, 999))

    return f"{cc_gen}|{mes}|{ano}|{cvv}"


def luhn_card_generator(cc, mes, ano, cvv, amount):
    cards = []
    while len(cards) < amount:
        result = cc_generator(cc, mes, ano, cvv)
        ccx, mesx, anox, cvvx = result.split("|")
        if check_luhn(ccx):
            cards.append(f"{ccx}|{mesx}|{anox}|{cvvx}")
    return "\n".join(cards)
