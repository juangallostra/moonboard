import requests
import json


class Moonboard():
    def __init__(self):
        self.moon_session = requests.Session() 
        self.base_url = 'https://www.moonboard.com'
        self.endpoints = {
            'get_problems': '/Problems/GetProblems',
            'login': '/Account/Login'
        }
    
    def login(username, password):
        payload = {
	        "Login.Username": username, 
	        "Login.Password": password, 
	        "__RequestVerificationToken": None
        }
        result = session_requests.get(base_url + login_endpoint)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='__RequestVerificationToken']/@value")))[0]

        # Complete payload
        payload[[key for key in payload if payload[key] is None][0]] = authenticity_token
        r = session_requests.post(base_url + login_endpoint, data=payload)
        print(r.text)

def fetch_problems():
    base_url = 'https://www.moonboard.com'
    problems_endpoint = '/Problems/GetProblems'
    cookies = {
        '__atuvc': '2%7C41',
        '_ga': 'GA1.2.539219515.1601981962',
        '__RequestVerificationToken': 'XopHSWe4bQ3NJeDm6kVbv0mbkvM7Z-WLbifR11HdUvdb98oWlf1ISXu_tXsueQfhW_S1IZWx6qMf5Wz4qFC7S_fNtiUAxwKP8uYpTPegvqw1',
        '_gid': 'GA1.2.1993484748.1602081563',
        '_MoonBoard': '7d7hOAxR3rEcjWVGu_ldK4NQVHho62fcirT-3yTZaV7hkm6kYGpcbHog5HsCC-T0cNseTHcXAcfyVfFrbVsnvQIZQr12hZyjUf_UbuUSgYy2R7f0NuwrK8vXkFQpppUEgKWiynPrp_OuCXfuks4aYdSlUea9PizJjdtf745C4SDe-tm4rO3h0yO4S4xziW3cdwaMFEEouOjhUUsZ3po1nJxYgHdD1h6hOKRHRI3S_PsDtSCzfDdl9BE65CFSrBZzY1BU49yvleSzPpcoB8lAoCUz3DckxWiRm_FZRozGbVc33F7MONRltClaLSZavDfzrdyEs2mMQx73x66JmpD_ij2AM09PpKwsm96Xu55uEGdM0SY-5ZuAlGwDSrxadj6FN9bBUU1Q7PnO5ZQPIZSBG7TYq7vCqqNg7tnPWOc79n7icMfMJqxm9MYZZiG-VURkKRn2kA9k7O_quKt6wNxZQuQ4iAdqX1JQMKuRPU2iOS60CEeSfk21zCJ1LSQtqMRK5RD05meBfaLk76-zrkKgzQ',
        '_gat_gtag_UA_73435918_1': '1',
    }
    data = {
        'sort': '',
        'page': '1',
        'pageSize': '15',
        'group': '',
        'filter': f'setupId~eq~{15}',
        '__RequestVerificationToken': 'sTyFBS8rBviyNk_09IqlelMah9ha27vUKf8mUS7IXv1YVUbA0NkGsHfT2PusbtmCuThsb4BCdaEKE8iILtnPSqtl5k2KfZVBR8_GmQkCp7xjAPwmLbSx9yogw2Dw59GcwkD_HHsaYP9G_0ZQ3GfN4g2'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.moonboard.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.moonboard.com/Problems/Index',
    }
    s = requests.post(base_url + problems_endpoint, headers=headers, cookies=cookies, data=data)
    # p = session_requests.post(
    #     base_url + problems_endpoint,
    #     data=data,
    #     headers=headers,
    #     cookies=cookies
    # )
    print(s.json())
    print(s.status_code)

    with open('problems.json', 'w') as f:
        f.write(json.dumps(s.json()))
    # print(p.status_code)
    # print(p.json())

if __name__ == "__main__":
    fetch_problems()