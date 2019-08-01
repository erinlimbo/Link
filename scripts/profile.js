const parseDate = (inputString) => {
  let splitString = inputString.split('-');
  splitString[1]=splitString[1].replace(/0/, "");
  splitString[2]=splitString[2].replace(/0/, "");
  let tempList = [];
  tempList.push(splitString[1]);
  tempList.push(splitString[2]);
  tempList.push(splitString[0]);

  let a = parseInt(tempList[0]);
  let b = "";

      switch(a){
          case 1: b = "January";
              break;
          case 2: b = "February";
              break;
          case 3: b = "March";
              break;
          case 4: b = "April";
              break;
          case 5: b = "May";
              break;
          case 6: b = "June";
              break;
          case 7: b = "July";
              break;
          case 8: b = "August";
              break;
          case 9: b = "September";
              break;
          case 10: b = "October";
              break;
          case 11: b = "November";
              break;
          case 12: b = "December";
              break;
          }
  tempList[0] = b;
  tempList[1] = tempList[1] + ','
  console.log(b);
  return tempList.join(' ');

}



// <span class="mdl-chip mdl-chip--contact mdl-chip--deletable">
//     <span class="mdl-chip__contact mdl-color--teal mdl-color-text--white">A</span>
//     <span class="mdl-chip__text">Deletable Contact Chip</span>
//     <a href="#" class="mdl-chip__action"><i class="material-icons">cancel</i></a>
// </span>


const createList = (json) => {
  let datesList = document.querySelector('#datesList');
  datesList.innerHTML = '';
  for (let date of json.added_dates){
    let dateItem = document.createElement('li');
    dateItem.innerHTML = parseDate(date);
    dateItem.classList.add('dates');
    ////////////
    let spanClass = document.createElement('span');
    spanClass.classList.add('mdl-chip', 'mdl-chip--contact', 'mdl-chip--deletable')
    let spanText = document.createElement('span');
    spanText.classList.add('mdl-chip__contact', 'mdl-color--pink', 'mdl-color-text--white');
    spanText.innerHTML = parseDate(date)[0];
    spanClass.appendChild(spanText);
    let spanSmall = document.createElement('span');
    spanSmall.innerHTML = parseDate(date);
    spanSmall.classList.add('mdl-chip__text');
    spanClass.appendChild(spanSmall)
    let anchor = document.createElement('a');
    anchor.classList.add('mdl-chip__action')
    let ith = document.createElement('i');
    ith.id = date
    ith.innerHTML = "cancel";
    ith.classList.add('material-icons');
    ith.addEventListener('click', function(){
      createList(json)
      let data = {'date_removed': date}
      fetch('/profile', {
        method:'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then((response)=>response.json())
      .then((json) => {
          createList(json)
      });
    });
    anchor.appendChild(ith);
    spanClass.appendChild(anchor)



///////////
    let removeButton = document.createElement('button');
    removeButton.innerHTML = 'Remove';
    removeButton.classList.add('remove');
    removeButton.id = date;
    removeButton.class = 'removeButton';
    removeButton.addEventListener('click', function(){
      createList(json)
      let data = {'date_removed': date}
      fetch('/profile', {
        method:'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then((response)=>response.json())
      .then((json) => {
          createList(json)
      });
    });
    dateItem.appendChild(removeButton);
    datesList.appendChild(dateItem);
    datesList.appendChild(spanClass);
  }
};

let submitButton = document.querySelector('#submitDate');
submitButton.addEventListener('click', () => {

  let tempDate = document.querySelector('#user_free_date').value;
  let data = {'user_free_date' : tempDate};
  fetch('/profile', {
    method:'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then((response)=>response.json())
  .then((json) => {
    if (!json.status){
      alert('You have already added that date.');
    }
    else {
      createList(json)
    }
  });
});



window.onload = () => {
  fetch('/profile', {
    method:'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  })
  .then((response)=>response.json())
  .then((json) => {
      createList(json)
  });
}
