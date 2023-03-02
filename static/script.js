async function update_task(button){
    url = `/update/${button.value}`
    fetch(url, {method: "PATCH"})
    .then(() => location.reload())
}

async function delete_task(button){
    url = `/delete/${button.value}`
    fetch(url, {method: "DELETE"})
    .then(() => location.reload())
}
async function delete_all_tasks(){
    url = "/delete_all"
    fetch(url, {method: "DELETE"})
    .then(() => location.reload())
}
