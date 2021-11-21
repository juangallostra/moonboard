// Sets up the options object needed to send with GetProblems request
const options = (
  pageNum,
  problemsPerPage,
  setupId = 15,
  holdSets = [],
  configAngle = ''
) => {
  const setupFilter = `setupId~eq~'${setupId}'`;
  const holdsetsFilter =
    holdSets.length > 0 ? `~and~Holdsets~eq~'${holdSets.join()}'` : '';
  const configAngleFilter =
    configAngle.length > 0 ? `~and~Configuration~eq~'${configAngle}'` : '';

  return {
    method: 'POST',
    mode: 'cors',
    referrer: 'https://www.moonboard.com/Problems/Index',
    referrerPolicy: 'no-referrer-when-downgrade',
    crossDomain: true,
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        '_itbmdw': 'wdY0Bfh+z8UqMHlDVgtBlSw4SuY9jAxU4pj6AMva3ys=__dGBu/HB93Z1l70xMDye4TTC5t5eefq/JKsGiZFcQzmQ=',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.moonboard.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.moonboard.com/Problems/Index',
        'Cookie': '__atuvc=4%7C41; _ga=GA1.2.539219515.1601981962; __RequestVerificationToken=XopHSWe4bQ3NJeDm6kVbv0mbkvM7Z-WLbifR11HdUvdb98oWlf1ISXu_tXsueQfhW_S1IZWx6qMf5Wz4qFC7S_fNtiUAxwKP8uYpTPegvqw1; _gid=GA1.2.191049862.1602741398; .AspNet.TwoFactorRememberBrowser=i38ZizwRTbiiIZ-Dr2_GxhylI3Mv8l11zoG-JV_EVn5PVL8vrnL7o8xOw0bYs2Udk3I6fZrR14dFA1wfga3tKZQ1oTiWn2VTOS7Ab35nDc1SH6UFaPpF5hqvQ2IFBuo3L0xrQ1rkDENptpcSSfciio9-9RSApN38-52zJ6e3IYYXoXpdC2zcgei0k7sa29U0rzhH9w0va7yu5USkrK3qd9ItGc7DcOCESjaM9dRE-LINqEXyOrsqnrBgWEtcxvni_uJheeF2ZxzO1y-oy8tscgdg_hOAcSs_fPKuZfAgSOm4fWygY37eSaFfgfnKyDF-JKC-BacR15hZgMX2dRaxrh200I1lKHNv4xOrmirjzx8; _MoonBoard=PkqgSrLLH7acRlvcfwsULba9S_SKtbyd70fd-027gIFCLN_ioifmznW48khhM6ACEkefKpKDUZ43KicEDudGAjksqd6LjEbmLNeGmiM7FPTqpBW3ZqoBHPWzn9NCV1LgzIelYt4NQelE3xOKCf_Pe1_sqKhvd3wlhOc4eXIlKa60Uv_q2x2YixsjXL-uczj8PY9i3Ps5sYEAbruFALRq_K9J16HKSDXuS0UTIOHtZyBK3wAMZqZFFX7gaEhHvS-dcxXoPeG0OmFQmRAesL6SdekfpR6CwL-NQ9hgdA1Y8aH00_u3WPz2uovuqTssqgSstqqjXoV5r5Hco7qgy4EBV8v3wajbNGmexL0iRgh-zz28Kpj_pQdwaRSPmospKzt-Ydyt6eXIc6JV30vweDc90E40IK4rjpn0Iae8eE4A8JiwHhYxzJQEgBQhw6g3Tlxuvo4ZFbR4VRGReTjcn815f7aomMx-Bb-JaGtaxOkJr835C-bo928pMiaVM4TOh7Xj; _gat_gtag_UA_73435918_1=1'
    },
    body: `sort=&page=${pageNum}&pageSize=${problemsPerPage}&group=&filter=${setupFilter}${holdsetsFilter}${configAngleFilter}&__RequestVerificationToken=gXW_J944WKxehEnKUfmWesxOysnqvkztmSrDZK5BZ5fJZfaBLl0k-xYGGG-6etRNqPxTUp89FJMK_KKHaZjfee6q6pPI94gxEm7R-amNsii4g6P0PLVPd3aHli8Wp8s4pmL37Fl_EX1i4kwSiumtlw2`,

  };
};

// Sends data GET request with specified options and chunk size
const getProblemDataChunk = async (pageNum, problemChunkSize) => {
  let response = await fetch(
    'https://www.moonboard.com/Problems/GetProblems',
    options(pageNum, problemChunkSize)
  );

  if (response && response.ok) {
    return (await response.json()).Data;
  } else {
    console.log(`Something went wrong with request ${pageNum}`);
    return [];
  }
};

// Set the filters on the page and look at how many problems there are and enter that here.
const getAllProblems = async (
  totalNumberOfProblems,
  problemChunkSize = 500
) => {
  const numberOfRequestsNecessary = Math.ceil(
    totalNumberOfProblems / problemChunkSize
  );
  const leftOvers = totalNumberOfProblems % problemChunkSize;

  let allProblems = [];

  for (let i = 0; i < numberOfRequestsNecessary; i++) {
    const chunkNum = i + 1;
    let problemChunk;

    console.log(`Request ${chunkNum}/${numberOfRequestsNecessary}`);

    if (i + 1 !== numberOfRequestsNecessary) {
      problemChunk = await getProblemDataChunk(chunkNum, problemChunkSize);
    } else {
      problemChunk = await getProblemDataChunk(
        chunkNum,
        leftOvers !== 0 ? leftOvers : problemChunkSize
      );
    }

    allProblems = [...allProblems, ...problemChunk];
  }

  return allProblems;
};

const saveData = function(data, console) {
  if (!data) {
    console.error('No data to save!');
    return;
  }

  var d = new Date(),
    month = '' + (d.getMonth() + 1),
    day = '' + d.getDate(),
    year = d.getFullYear();

  if (month.length < 2) month = '0' + month;
  if (day.length < 2) day = '0' + day;

  const filename = `moonboard_problems_${[year, month, day].join('')}`;

  if (typeof data === 'object') {
    data = JSON.stringify(data, undefined, 4);
  }

  var blob = new Blob([data], { type: 'text/json' }),
    e = document.createEvent('MouseEvents'),
    a = document.createElement('a');

  a.download = filename;
  a.href = window.URL.createObjectURL(blob);
  a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
  e.initMouseEvent('click');
  a.dispatchEvent(e);
};

const problems = await getAllProblems(35548, 500);
saveData(problems, console);
