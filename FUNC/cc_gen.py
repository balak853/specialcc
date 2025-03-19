import random

async def checkLuhn(cardNo):
    nSum = 0
    isSecond = False
    for d in reversed(cardNo):
        d = int(d)
        if isSecond:
            d *= 2
            if d > 9:
                d -= 9
        nSum += d
        isSecond = not isSecond
    return nSum % 10 == 0

async def cc_genarator(cc, mes, ano, cvv):
    cc = str(cc)
    
    # Expiry month randomization
    if mes in ["None", "X", "x", "rnd"]:
        mes = f"{random.randint(1, 12):02d}"

    # Expiry year randomization
    if ano in ["None", "X", "x", "rnd"]:
        ano = str(random.randint(2024, 2035))

    # CVV randomization
    if cvv in ["None", "X", "x", "rnd"]:
        cvv = str(random.randint(100, 999)) if cc.startswith(("4", "5")) else str(random.randint(1000, 9999))

    # Generate random CC number with Luhn compliance
    while True:
        cc_body = cc + "".join(random.choices("0123456789", k=15-len(cc)))
        check_digit = (10 - (sum(int(d) * 2 - 9 if i % 2 else int(d) for i, d in enumerate(reversed(cc_body))) % 10)) % 10
        final_cc = cc_body + str(check_digit)
        if await checkLuhn(final_cc):
            return f"{final_cc}|{mes}|{ano}|{cvv}"

async def luhn_card_genarator(cc, mes, ano, cvv, amount):
    tasks = [cc_genarator(cc, mes, ano, cvv) for _ in range(amount)]
    cards = await asyncio.gather(*tasks)
    return "\n".join(cards)
