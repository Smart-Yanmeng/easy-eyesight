const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const startButton = document.getElementById("startButton");
const recognizeButton = document.getElementById("recognizeButton");
const usernameInput = document.getElementById("usernameInput");
const face_admin = document.getElementById("face_admin");

// 获取视频流
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error(error);
  });

// 绑定“开始录入”按钮的事件
startButton.addEventListener("click", () => {
  // 将画面截图并转化为base64编码
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0, 640, 480);
  const base64Data = canvas.toDataURL("image/jpeg");

  // 发送录入请求
  fetch("http://127.0.0.1:5000/api/face/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      image: base64Data,
      username: usernameInput.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
    });
});

face_admin.addEventListener("click",() => {
  window.location.href="admin.html";
});

// 绑定“开始识别”按钮的事件
recognizeButton.addEventListener("click", () => {
  // 将画面截图并转化为base64编码
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0, 640, 480);
  const base64Data = canvas.toDataURL("image/jpeg");

  // 发送识别请求
  fetch("http://127.0.0.1:5000/api/face/recognize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      image: base64Data,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.code === 0) {
        alert(`识别成功！该用户是${data.username}`);
      } else {
        alert("未识别到用户");
      }
    })
    .catch((error) => {
      console.error(error);
    });
});