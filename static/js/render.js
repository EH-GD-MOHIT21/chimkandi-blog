id = setInterval(satija, 100);
pendingres = false

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

for (var i = 1; i <= 5; i++) {
    document.getElementById("rating-" + i).addEventListener('change', async function() {
        if (pendingres) {
            alert('hold on please.')
            return
        }
        pendingres = true
        axios.post('/makerate', {
                'blog_url': document.URL,
                "rating": this.id
            })
            .then(res => {
                pendingres = false
                if (res['data']['message'] == 'success') {
                    window.location.reload()
                } else
                    alert(res['data']['message']);
            });
    })
}