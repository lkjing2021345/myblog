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
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        // 获取CSRF Token
        const csrftoken = getCookie('csrftoken');

        fetch('/Article/api/login/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // 关键：将Token添加到请求头
            },
            body: JSON.stringify({username: username, password: password})
    })
        .then(response => response.json())
        .then(data => {
            // 1. 首先根据后端返回的数据结构，判断请求是否在业务上成功了
            if (data.token) {
            // 登录成功！
            // a. 将令牌保存起来，用于后续请求
            localStorage.setItem('authToken', data.token);
            // b. 给用户一个成功反馈
            document.getElementById('message').textContent = '登录成功！';
            // c. 跳转到其他页面（如首页）
            setTimeout(() => {
            window.location.href = '/Article'; // 跳转延迟1秒，让用户看到成功提示
            }, 1000);
        } else {
            // 登录失败（例如密码错误）
            // 显示后端返回的错误原因
            document.getElementById('message').textContent = '登录失败：' + data.error;
        }
        })
        .catch(error => {
        // 1. 在控制台打印详细错误，方便开发者调试
        console.error('网络请求发生错误:', error);
        // 2. 给用户一个友好的提示
        document.getElementById('message').textContent = '网络异常，请检查您的连接后重试。';
        });
    })