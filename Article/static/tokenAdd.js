const token = localStorage.getItem('authToken');
fetch('/api/articles/', {
    headers: {
        'Authorization': 'Token ' + token
    }
})