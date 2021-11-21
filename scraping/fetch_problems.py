# use the nice tool https://curl.trillworks.com/ 
# to generate the request from chrome "copy to cURL"
import pathlib
import json 

import requests

cookies = {
    '__atuvc': '4%7C41',
    '_ga': 'GA1.2.539219515.1601981962',
    '__RequestVerificationToken': 'XopHSWe4bQ3NJeDm6kVbv0mbkvM7Z-WLbifR11HdUvdb98oWlf1ISXu_tXsueQfhW_S1IZWx6qMf5Wz4qFC7S_fNtiUAxwKP8uYpTPegvqw1',
    '_gid': 'GA1.2.191049862.1602741398',
    '.AspNet.TwoFactorRememberBrowser': '69mqbs9auD92dHN70LbXhGTOb7DV6Ky_M1eAHFYCon34XL6YY-pmLhHEgVDcZ5ralEblqJSXrRGVcL-G8nS6S4uX9EmlZOfrZTM3qiMGHVplLHXJj88GggG-CLjdqOqi0Unvoj5c7RMbmlqpEDG1mZeUtu-GZqnItYUW03yZjL1YYjkKA9Jxsj7uB12fZKM9E-sO3fRZHP6DaZyvf3zNKJftiQ6mRA35Ny0DK8dbiKNvFJmdgnN_nAc4tT-FcoYEsGDtzJd01FHfFNPw50zrZhmMibXhSbZR4nmixtDQk1VwyOhwhxrUS79AE-lz2283yakbPr3rJEQO0vb5jjDYDnqqVYUYkfeMxjka_pIa1m0',
    '_MoonBoard': '451DUJ5efykMWaOkhvHcnGED-OXhfbwJUv_KLQrOhJhrmm3ke2lHlhaMHsLmJ3S6JKK1SRK-jGQw1752I-u6WY_bF88wOY4KFsk8gJlU4KSTyI-yct6ForgiPLxYuDQYhsXvEho_JiFROSXvWYVx_L4wzOnGYKVf-HDQFjEuA1kTgzp_8oj8SWkE7nC25LFpvqGFgAShFPlVaycLJDFrR-C70NY0Vfh8To40_5MRxm9uWkUDoeeNn5zERa2a7UMstrfCG80ryMESTaSlLfWhDIm0Isdmdi7ywQMTMEmnpKCv3s_XhyuEzOxWEeaq9DIWX9Gfsjo1rQM4ZzxsIjVKch8cTkCdXdstwWJLflVfNYWdVTEw49g7ozUzSfBJtgufb2LquxdNSSkYHBPxAHK9oh6JU1BpJBBt7WS-e1ekf33oeD5BMtCXPkuome08oWh385WdFJkcLs6wRFbvLJ57bBV5Yef0EyGLJvVo46mXcgwGpewnixoW9s_S5JqVtux4',
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

# with pathlib.Path("remove_keys.json").open("r+") as f:
#     remove_key=json.load(f)

def filter_problem(problem):
    return None
    # for k,v in remove_key.items():
    #     if isinstance(v,dict):
    #         for kk in v.keys():
    #             problem[k].pop(kk)
    #     else:
    #         problem.pop(k)

def fetch_problems_page(page, pagesize=500, setup="master2017"):
    hold_setup = {"2016":1, "master2017":15}
    data = {
    'sort': '',
    'page': str(page),
    'pageSize': str(pagesize),
    'group': '',
    'filter': '',#f'setupId~eq~{hold_setup[setup]}',
    '__RequestVerificationToken': '3YMUXLuXa_UJI3YT-wUVYEc8Q_jTatcvqt_mIJvMnLmdlZ6MFklzVnGUQwRuht632i_dztxuZn51o0Lbxbh6PRFdjDalBvf9fc001x2DHXbMi2dUTq9ihVba1O4NbCOPrmoW6TM6CABMVNLxz6QeIQ2'
    }   

    response = requests.post('https://www.moonboard.com/Problems/GetProblems', headers=headers, cookies=cookies, data=data)
    print(vars(response))
    rj= response.json()
    if rj.get('Errors') is not None:
        print(f"Error {rj.get('Errors')}")
    d={}
    for problem in rj['Data']:
        filter_problem(problem)
        k = problem.pop('Id')
        d[k]=problem
    return d, rj['Total']


setup =  "master2017"
#setup =  "2016"
filename = f"moonboard_problems_setup_{setup}"
pagelen = 500
max_fetch=40000


fetches = []
found = 0
page = 1

while True:
    print(f"fetch page {page}")
    d, tot = fetch_problems_page(page, pagelen, setup)
    fetches.append(d)
    found += len(d)
    print(f"Total problem after update: {found}/{tot}.")
    if found==tot or page>(tot/pagelen+1) or found>=max_fetch:
        break    
    page+=1
# 
print(f"concat problems.")
MoonProb ={}
for d in fetches:
    MoonProb.update(d)

print(f"Total problem after concat: {len(MoonProb)}.")
file_p = pathlib.Path(f'{filename}.json')
print(f"Export problems")

with file_p.open('w+') as f:
    json.dump(MoonProb, f, indent=3)