import traceback
from FUNC.defs import *
from FUNC.usersdb_func import *


async def get_charge_resp(result, user_id, fullcc):
    try:

        if type(result) == str:
            status   = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = result
            hits     = "NO"


            if (
                '"success":true,"data":"status":"succeeded"' in result
                or 'succeeded' in result
            ):
                    status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                    response = "Stripe Auth 🔥"
                    hits = "YES"

            elif (
                '{"success":true,"data":{"status":"requires_action"' in result
                or 'succeeded' in result
            ):
                    status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                    response = "3D 🔥"
                    hits = "YES"
                    









            elif ("Your card was declined" in result):
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    response = "Card was declined"
                    hits = "NO"

            elif ("Declined - Call Issuer" in result):
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    response = "Declined - Call Issuer"
                    hits = "NO"

            elif ("Cannot Authorize at this time" in result):
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    response = "Cannot Authorize at this time"
                    hits = "NO"

            elif ("Processor Declined - Fraud Suspected" in result):
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    response = "Fraud Suspected"
                    hits = "NO"

            elif "Status code risk_threshold: Gateway Rejected: risk_threshold" in result:
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    response = "Gateway Rejected: risk_threshold"
                    hits = "NO"

            elif ("We're sorry, but the payment validation failed. Declined - Call Issuer" in result or
                    "Payment failed: Declined - Call Issuer" in result
                    ):
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    response = "Declined - Call Issuer"
                    hits = "NO"

            elif "Payment Intent Creation Failed ❌" in result:
                status   = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "Payment Intent Creation Failed ❌"
                hits     = "NO"
                await refundcredit(user_id)

            elif "ProxyError" in result:
                status   = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "Proxy Connection Refused ❌"
                hits     = "NO"
                await refundcredit(user_id)

            else:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = await find_between(result , "System was not able to complete the payment. ", ".")
                if response is None:
                    response = "Card Declined"
                    await result_logs(fullcc, "Stripe Charge", result)
                response = response + " ❌"
                hits = "NO"

            json = {
                "status": status,
                "response": response,
                "hits": hits,
                "fullz": fullcc,
            }
            return json 

    except Exception as e:
        status   = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        response = str(e) + " ❌"
        hits     = "NO"

        json = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json
