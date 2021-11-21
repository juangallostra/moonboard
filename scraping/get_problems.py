import requests
import json

BASE_URL = 'https://www.moonboard.com'
PROBLEMS_ENDPOINT = '/Problems/GetProblems'

def fetch_problems_by_page(page=1, page_size=20):
    
    cookies = {
        '__atuvc': '2%7C41',
        '_ga': 'GA1.2.539219515.1601981962',
        '__RequestVerificationToken': 'XopHSWe4bQ3NJeDm6kVbv0mbkvM7Z-WLbifR11HdUvdb98oWlf1ISXu_tXsueQfhW_S1IZWx6qMf5Wz4qFC7S_fNtiUAxwKP8uYpTPegvqw1',
        '_gid': 'GA1.2.1993484748.1602081563',
        '_MoonBoard': 'YsSnTjfXkoXSZKZjPYsLB6vMm5LrHzdgg0afyaUibcjD1uac4YSSVkeh2_EtiTjU3E7w0wsxpWgkEw3vzEhcQjg0eKeGVQdtDipnVUXcZaZn4pzv-KzZN0wzQDY9GZXk4PSBANGcCYV_RsGcIQrb6hqV_EulRkMP5nsjq7Lj4V9Bte9qQ6OAzh_ffKcBU8zdA4DB-ut_mctFLwamq9EyukZ7_jCGIFgptsVvq71A2Ef9vfDi7yYAVlBBa9D2QUh3e4FTsV4dTIGuhLZZkMT9cChTQS859EGZMfwjZwADCGH3pqsDhb-hIhswnd-Du-Z-EErxdDG5uueof_O-yhlJ9t6nYPMcmIDIa0AtQR2QUUelAjt8N0m6YnANOTh14NF0zIgqdA0rT3jBaVOwaqR5eFEcmWGImQ2WMDX4OfSQPcKrE6mZgPmoqd5nYAEZSCbTSw3M2Xs2eu8ZXzs4-taTQuqlTvhad2Nrem0XbWHxTLGWDJ3be2AKO0cQXZSr_iRQdgxFNA3t6Q-72tb02dWvhQ',
        '_gat_gtag_UA_73435918_1': '1',
    }

    data = {
        'sort': '',
        'page': str(page),
        'pageSize': str(page_size),
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

    response = requests.post(BASE_URL + PROBLEMS_ENDPOINT, headers=headers, cookies=cookies, data=data)
    print(response.status_code)
    # p = session_requests.post(
    #     base_url + problems_endpoint,
    #     data=data,
    #     headers=headers,
    #     cookies=cookies
    # )

    with open('problems.json', 'w') as f:
        f.write(json.dumps(response.json()))

if __name__ == "__main__":
    fetch_problems_by_page(page=1)