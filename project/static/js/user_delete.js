document.addEventListener('DOMContentLoaded', function() {
    const togglebtn = document.querySelector('.navbar_togglebtn');
    const menu = document.querySelector('.navbar_menu');
    const member = document.querySelector('.navbar_member');

    togglebtn.addEventListener('click', ()=>{
        menu.classList.toggle('active');
        member.classList.toggle('active');
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("passwordForm");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const inputPassword = document.getElementById("password").value;

        if (!inputPassword) {
            errorMessage.textContent = "비밀번호를 입력해주세요.";
            errorMessage.hidden = false;
            return;
        }

        fetch('/member/user_delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: inputPassword })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('서버 응답이 올바르지 않습니다.');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message);  // "회원 탈퇴가 완료되었습니다." 메시지 표시
                window.location.href = "/";  // 홈페이지로 리다이렉트
            } else {
                throw new Error(data.error || "알 수 없는 오류가 발생했습니다.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = error.message || "서버 오류가 발생했습니다.";
            errorMessage.hidden = false;
        });
    });
});
