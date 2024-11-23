import {
  Grid,
  html
} from "https://unpkg.com/gridjs?module";

const newGroupArea = document.getElementsByClassName('newGroupArea')[0];
const dateNewArea = document.getElementsByClassName('dateNewArea')[0];
const dateStartArea = document.getElementsByClassName('dateStartArea')[0];
const dateFinishArea = document.getElementsByClassName('dateFinishArea')[0];
const tableWrapper = document.getElementById("table");
const imgMock = document.getElementsByClassName('imgMock')[0];

const dataColumnInputs = document.getElementsByClassName('dataColumnInputs')[0];

const submitBtn = document.getElementsByClassName('submitMainForm')[0];

const groupElem = document.getElementById('group');
const groupInput = document.getElementById('newGroup');

let goalElem;

const dateNew = document.getElementById('dateNew');
const dateStart = document.getElementById('dateStart');
const dateFinish = document.getElementById('dateFinish');

const temperature = document.getElementById('temperature');
const NH4 = document.getElementById('NH4');
const NO2 = document.getElementById('NO2');
const pH = document.getElementById('pH');
const Kh = document.getElementById('Kh');
const CO2 = document.getElementById('CO2');
const amount = document.getElementById('amount');
const biomass = document.getElementById('biomass');
const averMass = document.getElementById('averMass');

let breed;
let gender;

const feedStandartPercent = document.getElementById('feedStandartPercent');
const feedStrategy = document.getElementById('feedStrategy');
const realStandart = document.getElementById('realStandart');
const feedStandartMass = document.getElementById('feedStandartMass');
const feedSize = document.getElementById('feedSize');

const deathAmount = document.getElementById('deathAmount');
const deathPercent = document.getElementById('deathPercent');


let groupDataObj = {};

function identifyGoal() {
  goalElem = document.querySelector('input[name="goal"]:checked');
  if (goalElem.value === "newData") {
    dateNewArea.style.visibility = 'visible';
    dataColumnInputs.style.visibility = 'visible';
    dateStartArea.style.visibility = 'hidden';
    dateFinishArea.style.visibility = 'hidden';

    dateStart.removeAttribute('required');
    dateFinish.removeAttribute('required');
    dateNew.setAttribute('required', '');
    
    groupInput.readOnly = false;

    temperature.setAttribute('required', '');
    NH4.setAttribute('required', '');
    NO2.setAttribute('required', '');
    pH.setAttribute('required', '');
    Kh.setAttribute('required', '');
    CO2.setAttribute('required', '');

    amount.setAttribute('required', '');
    biomass.setAttribute('required', '');
    averMass.setAttribute('required', '');

    feedStandartPercent.setAttribute('required', '');
    feedStrategy.setAttribute('required', '');
    realStandart.setAttribute('required', '');
    feedStandartMass.setAttribute('required', '');
    feedSize.setAttribute('required', '');

    deathAmount.setAttribute('required', '');
    deathPercent.setAttribute('required', '');

    submitBtn.innerHTML = "Внести запись";
  } else {
    dateNewArea.style.visibility = 'hidden';
    dataColumnInputs.style.visibility = 'hidden';
    dateStartArea.style.visibility = 'visible';
    dateFinishArea.style.visibility = 'visible';

    dateNew.removeAttribute('required');
    dateStart.setAttribute('required', '');
    dateFinish.setAttribute('required', '');

    groupInput.value = "";
    groupInput.readOnly = true;

    temperature.removeAttribute('required');
    NH4.removeAttribute('required');
    NO2.removeAttribute('required');
    pH.removeAttribute('required');
    Kh.removeAttribute('required');
    CO2.removeAttribute('required');

    amount.removeAttribute('required');
    biomass.removeAttribute('required');
    averMass.removeAttribute('required');

    feedStandartPercent.removeAttribute('required');
    feedStrategy.removeAttribute('required');
    realStandart.removeAttribute('required');
    feedStandartMass.removeAttribute('required');
    feedSize.removeAttribute('required');

    deathAmount.removeAttribute('required');
    deathPercent.removeAttribute('required');

    submitBtn.innerHTML = "Посмотреть статистику";
  }
};


groupElem.addEventListener("change", () => {
  const groupValue = groupElem.value;
  console.log(groupValue);

  if (groupValue === "new") {
    newGroupArea.style.visibility = 'visible';

    groupElem.removeAttribute('required');
    groupInput.setAttribute('required', '');
  } else {
    newGroupArea.style.visibility = 'hidden';

    groupInput.removeAttribute('required');
    groupElem.setAttribute('required', '');
  }
});

document.querySelectorAll('input[type="radio"][name="goal"]').forEach(radio => {
  radio.addEventListener('change', () => {
    identifyGoal();
    tableWrapper.style.visibility = 'hidden';
    imgMock.style.visibility = 'hidden';
  });
});


document.forms.postFish.addEventListener('submit', function (event) {
  event.preventDefault();

  breed = document.querySelector('input[name="breed"]:checked').value;
  gender = document.querySelector('input[name="gender"]:checked').value;

  const dateStartValue = new Date(dateStart.value);
  const dateStartUnix = Math.floor(dateStartValue.getTime() / 1000);
  const dateFinishValue = new Date(dateFinish.value);
  const dateFinishUnix = Math.floor(dateFinishValue.getTime() / 1000);
  const dateNewValue = new Date(dateNew.value);
  const dateNewUnix = Math.floor(dateNewValue.getTime() / 1000);

  /* Проверка на то, какое имя группы брать: из существующих или новое */
  const groupName = groupElem.hasAttribute("required") ? groupElem.value : groupInput.value;

  groupDataObj = {
    groupElem: groupName,
    dateNew: dateNewUnix,
    // dateStart: dateStartUnix,
    // dateFinish: dateFinishUnix,
    temperature: temperature.value,
    NH4: NH4.value,
    NO2: NO2.value,
    pH: pH.value,
    Kh: Kh.value,
    CO2: CO2.value,

    amount: amount.value,
    biomass: biomass.value,
    averMass: averMass.value,

    breed: breed,
    gender: gender,

    feedStandartPercent: feedStandartPercent.value,
    feedStrategy: feedStrategy.value,
    realStandart: realStandart.value,
    feedStandartMass: feedStandartMass.value,
    feedSize: feedSize.value,

    deathAmount: deathAmount.value,
    deathPercent: deathPercent.value
  };

  const getObj = {
    group_id: groupName,
    from_ts: dateStartUnix,
    to_ts: dateFinishUnix,
  }

  if (submitBtn.innerHTML === "Внести запись") {
    sendPost(groupDataObj);
    console.log(groupDataObj);
    alert("Запись внесена!");
  } else {
    getData(getObj);
    console.log(getObj);
  }

});

function sendPost(obj) {
  // fetch('http://10.8.10.2:8835/test_get')
  // .then((res) => {
  //   return res.json();
  // })
  // .then((data) => {
  //   console.log(data);
  // })
  // .catch((e) => {
  //   console.log(e);
  // })


  fetch('http://10.8.10.2:8835/items/', {
    // mode: 'no-cors',
    method: 'POST',
    body: JSON.stringify({
      body: obj
    }),
    headers: {
      'Content-Type': 'application/json; charset=UTF-8'
    }
  })
  .then(post => post.json())
  .then((data) => {
    console.log(data);
  })
};

function getData(obj) {
  fetch('http://10.8.10.2:8835/test_get?'+ new URLSearchParams(obj).toString())
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
    })

  tableWrapper.style.visibility = 'visible';
  imgMock.style.visibility = 'visible';
}

new Grid({
  columns: ["Вес тела, г", "Вес икринки, мг", "Рабочая плодовитость, тыс.шт"],
  sort: true,
  data: [
    [2600, 110, 3.68],
    [2430, 90.1, 5.06],
    [2080, 92, 4.18],
    [2280, 88.6, 5.49],
    [2280, 89.5, 4.59]
  ],
  style: {
    container: {
      'max-width': '50vw'
    },
    table: {
      border: '3px solid #ccc',
    },
    th: {
      'background-color': 'rgba(0, 0, 0, 0.1)',
      'color': '#000',
      'border-bottom': '3px solid #ccc',
      'text-align': 'center',
      'padding': '4px 8px',
      'max-width': '120px',
      'min-width': '120px',
      'width': '120px',
    },
    td: {
      'text-align': 'center',
      'padding': '4px 8px',
      'max-width': '120px',
      'min-width': '120px',
      'width': '120px',
    }
  }
}).render(document.getElementById("table"));
