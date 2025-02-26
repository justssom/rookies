document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("edit-profile-form");
    const newPasswordInput = document.getElementById("new_password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const passwordError = document.getElementById("passwordError");
    const confirmPasswordError = document.getElementById("confirmPasswordError");

    function validatePassword(password) {
        return /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$/.test(password);
    }

    newPasswordInput.addEventListener("input", function() {
        passwordError.style.display = this.value && !validatePassword(this.value) ? "block" : "none";
        checkPasswordMatch();
    });

    confirmPasswordInput.addEventListener("input", checkPasswordMatch);

    function checkPasswordMatch() {
        if (newPasswordInput.value && confirmPasswordInput.value) {
            confirmPasswordError.style.display = newPasswordInput.value !== confirmPasswordInput.value ? "block" : "none";
        } else {
            confirmPasswordError.style.display = "none";
        }
    }

    form.addEventListener("submit", function(e) {
        e.preventDefault();

        if (newPasswordInput.value !== confirmPasswordInput.value) {
            alert("새 비밀번호가 일치하지 않습니다.");
            return;
        }

        const formData = {
            new_password: newPasswordInput.value,
            postal_code: document.getElementById('postal_code').value,
            address: document.getElementById('address').value,
            add_detail: document.getElementById('add_detail').value
        };

        fetch('/member/edit_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                window.location.href = '/'; // 메인 페이지로 리다이렉트
            } else {
                alert(data.error || '오류가 발생했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('정보 수정 중 오류가 발생했습니다: ' + error.message);
        });
    });
});
