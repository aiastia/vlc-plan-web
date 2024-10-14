function sendControl(action) {
    fetch('/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // 移除对按钮可见性的控制
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
