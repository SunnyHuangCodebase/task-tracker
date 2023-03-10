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
async function add_task(form){
    csrftoken = get_cookie("csrftoken")
    url = "/add"

    fetch(form.action, {method: form.method, body: new FormData(form)})
    .then(() => location.reload())
}
async function update_task(button){
    csrftoken = get_cookie("csrftoken")
    url = `/update/${button.value}`
    fetch(
        url, {
            method: "PATCH",
            headers: {"X-CSRFTOKEN": csrftoken}
        }
    )
    .then(() => location.reload())
}

async function delete_task(button){
    csrftoken = get_cookie("csrftoken")
    url = `/delete/${button.value}`
    fetch(
        url, {
            method: "DELETE",
            headers: {"X-CSRFTOKEN": csrftoken}
        }
    )
    .then(() => location.reload())
}
async function delete_all_tasks(){
    csrftoken = get_cookie("csrftoken")
    url = "/delete_all"
    fetch(
        url, {
            method: "DELETE",
            headers: {"X-CSRFTOKEN": csrftoken}
        }
    )
    .then(() => location.reload())
}
