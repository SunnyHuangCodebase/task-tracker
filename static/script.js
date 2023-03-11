function get_cookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i ++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

function set_cookie(name, value, time = 5) {
    let expiry = new Date()
    expiry.setTime(Date.now() + time * 60 * 1000)
    document.cookie = name + "=" + value + "; expires=" + expiry.toUTCString();
}

function delete_cookie(name) {
    set_cookie(name, value, 0)
}

function get_csrftoken() {
    return get_cookie("csrftoken")
}

async function add_task(form){
    fetch(form.action, {
        method: form.method,
        body: new FormData(form),
        headers: {"X-CSRFTOKEN": get_csrftoken()}
    })
    .then(response => response.text())
    .then(html => document.body.innerHTML = html)
}

async function update_task(button) {
    let token = get_csrftoken()
    console.log(token)
    let url = `/update/${button.value}`
    fetch(url, {
        method: "PATCH",
        headers: {"X-CSRFTOKEN": get_csrftoken()}
    })
    .then(response => response.text())
    .then(html => document.body.innerHTML = html)
}

async function delete_task(button) {
    let url = `/delete/${button.value}`
    fetch(url, {
        method: "DELETE",
        headers: {"X-CSRFTOKEN": get_csrftoken()}
    })
    .then(response => response.text())
    .then(html => document.body.innerHTML = html)
}
async function delete_all_tasks() {
    let url = "/delete_all"
    fetch(url, {
        method: "DELETE",
        headers: {"X-CSRFTOKEN": get_csrftoken()}
    })
    .then(response => response.text())
    .then(html => document.body.innerHTML = html)

}
