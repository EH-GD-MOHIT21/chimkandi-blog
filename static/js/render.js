console.log('rendering...')
id = setInterval(satija, 100);

function replaceAll(string, search, replace) {
    return string.split(search).join(replace);
}

function satija() {
    clearInterval(id);
    tcobjs = document.getElementsByClassName('textcontent')
    for (obj of tcobjs) {
        ans = replaceAll(obj.innerHTML, '&lt;', '<');
        ans = replaceAll(ans, '&gt;', '>');
        obj.innerHTML = ans;
    }
}