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
      let datesList = document.querySelector('#datesList');
      datesList.innerHTML = '';
      for (let date of json.added_dates){
        let dateItem = document.createElement('li');
        dateItem.innerHTML = date;
        let removeButton = document.createElement('button');
        removeButton.innerHTML = 'remove';
        dateItem.appendChild(removeButton);
        datesList.appendChild(dateItem);
      }
    }
  });
});
