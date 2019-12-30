let content = document.getElementById('bio').textContent

const update = () => {
    document.getElementById('bio').outerHTML = `<div id="bio"><form action="/change_bio" method="POST"><textarea name="bio" rows="4" cols="100">${content.trim()}</textarea><br><button class="btn btn-primary" type="submit">Submit</button><button class="btn btn-light" onclick="cancel()">Cancel</button></div> </form>`

} 

const cancel = () => {
    document.getElementById('bio').outerHTML = `<p id="bio">${content}</p>`
}