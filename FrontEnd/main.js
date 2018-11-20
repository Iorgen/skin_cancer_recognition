

var JSONINPUT = '{ "name":"John", "surname":"Vagner", "diag":"Melanoma"}';



let dropArea = document.getElementById('drop__area');

// dropArea.addEventListener('dragenter', handlerFunction, false)
// dropArea.addEventListener('dragleave', handlerFunction, false)
// dropArea.addEventListener('dragover', handlerFunction, false)
// dropArea.addEventListener('drop', handlerFunction, false)

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
};

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files

    handleFiles(files)
}


function previewFile(file) {
    let reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = function () {
        let img = document.createElement('img')
        img.src = reader.result
        var gallery = document.getElementById('gallery')
        while (gallery.firstChild) {
            gallery.removeChild(gallery.firstChild);
        }
        document.getElementById('gallery').appendChild(img)
    }
}
function handleFiles(files) {
    files = [...files]
    files.forEach(uploadFile)
    files.forEach(previewFile)
}
function pMaker(_text){
    var pBlock = document.createElement("p");
    pBlock.textContent = _text;
    return pBlock;
}
function showResult(data){
    var result = document.getElementById('result__area');
    while (result.firstChild) {
        result.removeChild(result.firstChild);
    }
    result.appendChild(pMaker('Name: ' + data.name));
    result.appendChild(pMaker('surname: ' + data.surname));
    result.appendChild(pMaker('Diagnoses: ' + data.diag));
}


function uploadFile(file) {
    var url = 'upload.php';
    var xhr = new XMLHttpRequest()
    var formData = new FormData()
    xhr.open('POST', url, true)

    xhr.addEventListener('readystatechange', function (e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.response);
            var response = JSON.parse(JSONINPUT);
            showResult(response);
        }
        else if (xhr.readyState == 4 && xhr.status != 200) {
            console.log(xhr.response);
        }
    })

    formData.append('file', file)
    xhr.send(formData)
}









// document.forms.upload.onsubmit = function () {
//     var file = this.elements.myfile.files[0];
//     if (file) {
//         upload(file);
//     }
//     return false;
// }
// function upload(file) {

//     var xhr = new XMLHttpRequest();

//     // обработчики можно объединить в один,
//     // если status == 200, то это успех, иначе ошибка
//     xhr.onload = xhr.onerror = function () {
//         if (this.status == 200) {
//             console.log("success");
//         } else {
//             console.log("error " + this.status);
//         }
//     };

//     // обработчик для закачки
//     xhr.upload.onprogress = function (event) {
//         console.log(event.loaded + ' / ' + event.total);
//     }
//     // xhr.setRequestHeader("Content-type","multipart/form-data; charset=utf-8; boundary=" + Math.random().toString().substr(2));
//     xhr.open("POST", "upload.php");
//     var formData = new FormData();
//     formData.append("myfile", file);
//     xhr.send(formData);
//     // xhr.send(file);
// }