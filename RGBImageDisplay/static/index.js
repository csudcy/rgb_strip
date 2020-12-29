function main() {
  setInterval(get_frame_info, 1000);
  document.querySelector("#move_next").onclick = move_next_click;
}

function get_frame_info() {
  fetch('/frame_info')
    .then((response) => {
      response.json().then((data) => {
        document.querySelector("#frame_name").textContent = data.name;
        document.querySelector("#frame_index").textContent = data.frame_index;
        document.querySelector("#frame_count").textContent = data.frames;
      });
    })
    .catch((err) => {
      console.error(err);
    })
}

function move_next_click() {
  fetch("/api/move_next");
}

window.onload = main;
