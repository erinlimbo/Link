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

const createList = (json) => {
  let datesList = document.querySelector('#datesList');
  datesList.innerHTML = '';
  for (let date of json.added_dates){
    let dateItem = document.createElement('li');
    dateItem.innerHTML = parseDate(date);
    dateItem.classList.add('dates');

    let removeButton = document.createElement('button');
    removeButton.innerHTML = 'remove';
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
