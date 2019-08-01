// const parseDate = (inputString) => {
//   split_string = inputString.split('-')
//   index = [1,2,0]
//   temp = [split_string[x] for x in index]
//   perm = temp.join('-')
//   return perm
// }


const createList = (json) => {
  let datesList = document.querySelector('#datesList');
  datesList.innerHTML = '';
  for (let date of json.added_dates){
    let dateItem = document.createElement('li');
    dateItem.innerHTML = date;

    let removeButton = document.createElement('button');
    removeButton.innerHTML = 'remove';
    removeButton.classList.add('remove')
    removeButton.id = date;
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
