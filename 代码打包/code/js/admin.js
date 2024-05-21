const facesTable = document.querySelector('#facesTable');
const facesTableBody = document.querySelector('#facesTableBody');
const noData = document.querySelector('#noData');
let faces = [];

const deleteFace = async (id) => {
  try {
    const response = await fetch(`http://127.0.0.1:9999/api/faces/${id}`, {
      method: 'DELETE'
    });
    if (response.ok) {
      faces = faces.filter(face => face.id !== Number(id));
      renderTable();
    }
  } catch (error) {
    console.error(error);
  }
};

const renderTable = () => {
  if (faces.length === 0) {
    facesTable.classList.add('is-hidden');
    noData.classList.remove('is-hidden');
    return;
  }

  noData.classList.add('is-hidden');
  facesTable.classList.remove('is-hidden');
  facesTableBody.innerHTML = '';
  faces.forEach(face => {
    const tr = document.createElement('tr');
    const imageTd = document.createElement('td');
    const img = document.createElement('img');
    img.src = `http://127.0.0.1:5000/static/${face.name}.jpg`;
    img.alt = 'face image';
    img.classList.add('image', 'is-64x64');
    imageTd.appendChild(img);
    tr.innerHTML = `
      <td>${face.id}</td>
      <td>${face.name}</td>
    `;
    tr.appendChild(imageTd);
    const buttonTd = document.createElement('td');
    const deleteButton = document.createElement('button');
    deleteButton.classList.add('button', 'is-danger');
    deleteButton.dataset.id = face.id;
    deleteButton.dataset.action = 'delete';
    deleteButton.textContent = '删除';
    deleteButton.addEventListener('click', (event) => {
      if (confirm('确定要删除该人脸信息吗？')) {
        const id = event.target.dataset.id;
        deleteFace(id);
      }
    });
    buttonTd.appendChild(deleteButton);
    tr.appendChild(buttonTd);
    facesTableBody.appendChild(tr);
  });
};

const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:9999/api/faces');
    const data = await response.json();
    faces = data.data;
    console.log(faces);
    renderTable();
  } catch (error) {
    console.error(error);
  }
};

fetchData();