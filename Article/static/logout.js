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

// 为注销按钮绑定点击事件
document.getElementById('logoutButton').addEventListener('click', function (event) {
    console.log('Document Cookie:', document.cookie);
    console.log('CSRF Token:', getCookie('csrftoken'));
    event.preventDefault();

    // 获取CSRF Token
    const csrftoken = getCookie('csrftoken');


    fetch('/Article/api/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('authToken')}` // 添加 Token 认证头
        // 注意：移除了 'X-CSRFToken' 头，因为不再需要
        },
        credentials: 'include' // 如果您不再需要维持 session，此处甚至可以省略
    })
    .then(response => {
        // 首先检查HTTP状态码是否成功
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // 注销成功后的处理
        // 1. 清除前端保存的认证令牌（如果存在）
        localStorage.removeItem('authToken');
        // 2. 给用户成功反馈
        document.getElementById('message').textContent = '注销成功！';
        // 3. 跳转到登录页或首页
        setTimeout(() => {
            window.location.href = 'Article/login/'; // 跳转到登录页
        }, 1000);
    })
    .catch(error => {
        if (error.response && error.response.status === 403) {
            document.getElementById('message').textContent = '认证失败，请重新登录';
            localStorage.removeItem('authToken');
            setTimeout(() => window.location.href = '/login/', 1500);
        } else {
            console.error('注销请求发生错误:', error);
        }
    });
});