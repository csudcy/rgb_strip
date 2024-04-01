function main() {
  setInterval(get_frame_info, 1000);
  document.querySelector("#move_next").onclick = move_next_click;
  document.querySelectorAll(".play").forEach((ele) => {
    ele.onclick = play_click;
  });
}

function get_frame_info() {
  fetch('/frame_info')
    .then((response) => {
      response.json().then((data) => {
        document.querySelector("#frame_parent").textContent = data.parent;
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

function play_click(ele) {
  let ds = ele.target.dataset;
  console.log(`Play: ${ds.group}/${ds.image}`)
  fetch(`/api/play?group=${ds.group}&image=${ds.image}`);
}

window.onload = main;
