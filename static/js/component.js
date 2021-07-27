id = 0
BlogOBJ = []
document.getElementById('adp').addEventListener('click', function() {
    if (id >= 9) {
        this.style.display = "none"
        alert('limit reached')
        return
    }
    var newelm = document.createElement('textarea');
    newelm.setAttribute('class', 'textarea w-100');
    newelm.setAttribute('id', id + 1)
    newelm.setAttribute('required', true)
    newelm.setAttribute('name', id + 1)
    id += 1
    document.getElementById('xtra').appendChild(newelm)
    BlogOBJ.push("t")
    document.getElementById('changeablespan').textContent -= 1
})

document.getElementById('ai').addEventListener('click', function() {
    if (id >= 9) {
        this.style.display = "none"
        alert('limit reached')
        return
    }
    var newelm = document.createElement('input');
    newelm.setAttribute('type', 'file');
    newelm.setAttribute('class', 'image');
    newelm.setAttribute('name', id + 1)
    newelm.setAttribute('id', id + 1)
    newelm.setAttribute('required', true)
    id += 1
    newelm.setAttribute('accept', 'image/*');
    document.getElementById('xtra').appendChild(newelm)
    BlogOBJ.push("i")
    document.getElementById('changeablespan').textContent -= 1
})