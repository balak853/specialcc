import random
import asyncio

# ✅ Fast Luhn Algorithm (Direct Valid CC Generate)
def generate_luhn_valid(cc_prefix):
    cc_body = cc_prefix + "".join(random.choices("0123456789", k=15-len(cc_prefix)))
    total = sum(int(d) * 2 - 9 if (i % 2) else int(d) for i, d in enumerate(reversed(cc_body)))
    check_digit = (10 - (total % 10)) % 10
    return cc_body + str(check_digit)

# ✅ Generate a Single Card
def cc_generator(cc, mes, ano, cvv):
    if mes in ["None", "X", "x", "rnd"]:
        mes = f"{random.randint(1, 12):02d}"
    if ano in ["None", "X", "x", "rnd"]:
        ano = str(random.randint(2024, 2035))
    if cvv in ["None", "X", "x", "rnd"]:
        cvv = str(random.randint(100, 999)) if cc.startswith(("4", "5")) else str(random.randint(1000, 9999))
    
    return f"{generate_luhn_valid(cc)}|{mes}|{ano}|{cvv}"

# ✅ Multi-threaded Generator (Super Fast!)
async def luhn_card_generator(cc, mes, ano, cvv, amount):
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, cc_generator, cc, mes, ano, cvv) for _ in range(amount)]
    cards = await asyncio.gather(*tasks)
    return "\n".join(cards)
