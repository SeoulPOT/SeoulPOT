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

        // 배경 업데이트
        updateBackground(currentTime);
    }


    // 배경을 변경하는 함수
    function updateBackground(date) {
        const hour = date.getHours();
        const body = document.body;

        // 이전 클래스 제거
        body.classList.remove('morning-bg', 'afternoon-bg', 'evening-bg');

        // 시간대에 따른 클래스 추가
        if (hour >= 6 && hour < 14) {
            body.classList.add('morning-bg'); // 아침 배경
        } else if (hour >= 14 && hour < 22) {
            body.classList.add('afternoon-bg'); // 오후 배경
        } else if (hour >= 22 && hour < 6) {
            body.classList.add('evening-bg'); // 저녁 배경
        } 
    }
    // 1초마다 시간을 갱신
    setInterval(updateTime, 1000);

    // 초기 시간 표시
    updateTime();
});
