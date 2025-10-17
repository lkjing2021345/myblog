// 函数用于从Cookie中获取CSRF Token
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
    document.getElementById('RegisterForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/Article/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({username: username, password: password})
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                // 注册成功！将Token保存起来
                localStorage.setItem('authToken', data.token);
                document.getElementById('message').innerHTML = '注册成功！';
                // 跳转到主页面，比如文章列表
                setTimeout(() => { window.location.href = '/Article/'; }, 1000);
            } else {
                document.getElementById('message').innerHTML = '注册失败：' + data.error;
            }
        });
    });