document.addEventListener('DOMContentLoaded', function() {
    const serverTime = window.serverTime;
    const startTime = new Date(serverTime);
    
    // 클라이언트의 시간 오프셋을 계산
    const timeOffset = startTime.getTime() - new Date().getTime();
 
    // 시간을 포맷하는 함수
    function formatTime(date) {
        let hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // 0을 12로 바꿈
        const minutesStr = minutes < 10 ? '0' + minutes : minutes;
        const secondsStr = seconds < 10 ? '0' + seconds : seconds;
        return `${ampm} ${hours}:${minutesStr}`;
    }

    // 실시간으로 시간을 갱신하는 함수
    function updateTime() {
        const currentTime = new Date(new Date().getTime() + timeOffset);
        const formattedTime = formatTime(currentTime);
        document.querySelector('.time').textContent = formattedTime;
    }

    // 1초마다 시간을 갱신
    setInterval(updateTime, 1000);

    // 초기 시간 표시
    updateTime();
});
