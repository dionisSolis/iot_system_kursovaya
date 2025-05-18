function toggleDevice(deviceId, action) {
    fetch(`/api/devices/${deviceId}/${action}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Обновляем страницу после успешного изменения
                window.location.reload();
            } else {
                alert('Ошибка при изменении состояния устройства');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка');
        });
}