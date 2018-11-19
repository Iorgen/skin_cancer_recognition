function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}




function sendImg() {
    // var formdata = new FormData();
    // formdata.append('file', file);
    var selectedFile = document.getElementById('files').files[0];

    var formData = new FormData();
    formData.append("image", selectedFile);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'image.php', true);
    xhr.setRequestHeader("Content-type","multipart/form-data; charset=utf-8; boundary=" + Math.random().toString().substr(2));

    xhr.onreadystatechange = function () {
        if (xhr.readyState != 4) return;
        if (xhr.status != 200) {
            alert("Status: " + xhr.status);
        } else {
            alert(xhr.responseText);
        }
    };
    xhr.onload = function () {
        if (this.status == 200) {
            var resp = JSON.parse(this.response);
            console.log(this.response)
            console.log('Server got:', resp);
            var image = document.createElement('img');
            image.src = resp.dataUrl;
            document.body.appendChild(image);
        };
    };
    xhr.send(formData);

}

