async function makeRequest(url, method = "POST", body) {
    let headers = {
        'X-CSRFToken': getCookie('csrftoken'), 
        'Content-Type': 'application/json'
    };

    const response = await fetch(url, {
        method: method,
        headers: headers,
        body: JSON.stringify(body)
    });

    if (response.ok) {
        return await response.json();
    } else {
        let error = await response.text();
        console.error('Request failed:', error);
        throw new Error(error);
    }
}

async function onClickFavorite(event) {
    event.preventDefault();
    let button = event.currentTarget;
    let photoId = button.dataset.photoId;
    let albumId = button.dataset.albumId;
    let action = button.dataset.action;
    let url = `/favorites/${action}/`;
    let body = {
        photo_id: photoId,
        album_id: albumId
    };

    try {
        let data = await makeRequest(url, action === 'add' ? 'POST' : 'DELETE', body);

        if (action === 'add') {
            button.textContent = 'Удалить из избранного';
            button.dataset.action = 'remove';
        } else if (action === 'remove') {
            button.textContent = 'Добавить в избранное';
            button.dataset.action = 'add';
        }
    } catch (error) {
        console.error('Error handling favorite button click:', error);
    }
}

function onLoad() {
    let favoriteButtons = document.querySelectorAll('[data-js="favorite-button"]');
    for (let button of favoriteButtons) {
        button.addEventListener('click', onClickFavorite);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener('load', onLoad);