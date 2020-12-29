function main() {
  setInterval(get_frame_info, 1000);
}

function get_frame_info() {
  fetch('/frame_info')
    .then((response) => {
      response.json().then((data) => {
        console.log(data);
        let ele = document.querySelector(".frame_info");
        ele.textContent = `${data.name}, ${data.frame_index}/${data.frames}`;
      });
    })
    .catch((err) => {
      console.error(err);
    })
}

window.onload = main;
