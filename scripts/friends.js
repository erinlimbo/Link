
let allInput = document.getElementsByClassName('input');

const createList = (json) => {
  let friendList = document.querySelector('#friendList');
  datesList.innerHTML = '';
  for (let friend of json.friends){
    let friendItem = document.createElement('li');
    friendItem.innerHTML = friend;
    let removeButton = document.createElement('button');
    removeButton.innerHTML = 'remove';
    removeButton.classList.add('remove')
    removeButton.id = friend;
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
    friendItem.appendChild(removeButton);
    friendList.appendChild(friendItem);
  }
};

//
// const createList = (json) => {
//   let datesList = document.querySelector('#datesList');
//   datesList.innerHTML = '';
//   for (let date of json.added_dates){
//     let dateItem = document.createElement('li');
//     dateItem.innerHTML = date;
//
//     let removeButton = document.createElement('button');
//     removeButton.innerHTML = 'remove';
//     removeButton.classList.add('remove')
//     removeButton.id = date;
//     removeButton.class = 'removeButton';
//     removeButton.addEventListener('click', function(){
//       createList(json)
//       let data = {'date_removed': date}
//       fetch('/profile', {
//         method:'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//       })
//       .then((response)=>response.json())
//       .then((json) => {
//           createList(json)
//       });
//     });
//     dateItem.appendChild(removeButton);
//     datesList.appendChild(dateItem);
//   }
// };

let addFriendButton = document.querySelector('#addFriend');
addFriendButton.addEventListener('click', () => {
  let tempDate = document.querySelector('#user_free_date').value);
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
      alert('You have already added that friend.');
    }
    else {
      createList(json)
    }
  });
});
