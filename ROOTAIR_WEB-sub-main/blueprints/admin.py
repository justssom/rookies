from flask import Blueprint, render_template, jsonify, request, current_app, session, flash, redirect, url_for
from blueprints.utils import get_db_connection

# 📌 Flask Blueprint 생성 (이름 반드시 'admin_bp'으로 맞출 것)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 📌 관리자 로그인 페이지

@admin_bp.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        userID = request.form.get('userID')
        password = request.form.get('password')
        
        current_app.logger.debug("로그인 시도: userID=%s", userID)
        
        # Users 테이블에서 관리자 계정 조회
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM Users WHERE user_id = '{userID}' AND password = '{password}' AND isadmin = 'Y';"
        current_app.logger.debug("실행할 쿼리: %s", query)
        cursor.execute(query)
        user = cursor.fetchone()
        current_app.logger.debug("쿼리 결과: %s", user)
        
        cursor.close()
        conn.close()
        
        if user:
            session['admin'] = True # 관리자 세션 설정
            session['user_id'] = userID  # 로그인한 사용자의 아이디를 세션에 저장
            current_app.logger.info("로그인 성공: user_id=%s", userID)
            flash('로그인 성공하였습니다.', 'success')
            return redirect(url_for('admin.admin_management')) # 로그인 후 회원정보 페이지로 이동
        else:
            current_app.logger.error("회원 정보를 찾을 수 없습니다. user_id: %s", userID)
            flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'danger')
            return render_template('admin/admin.html')
    return render_template('admin/admin.html')

# admin_man으로 라우트 (세션 검사 추가)
@admin_bp.route('/man')
def admin_management():
    if not session.get('admin'):  # 세션에 'admin' 값이 없으면 로그인 페이지로 리다이렉트
        flash("관리자만 접근할 수 있습니다.", "danger")
        return redirect(url_for('admin.admin_login'))  # 로그인 페이지로 이동

    return render_template("admin/admin_man.html")  # 관리자일 경우만 페이지 렌더링
# get member data API
@admin_bp.route('/get_members', methods=['GET'])
def get_members():

    if not session.get('admin'):  #  관리자가 아니면 접근 불가
        return jsonify({"error": "Unauthorized access"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, user_id, username, phone_number, email FROM users")
    members = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(members)

# API to delete a member
@admin_bp.route('/delete_member', methods=['POST'])
def delete_member():

    if not session.get('admin'):  # 관리자가 아니면 접근 불가
        return jsonify({"error": "Unauthorized access"}), 403
    
    data = request.json
    member_id = data.get("id")

    if not member_id:
        return jsonify({"error": "Invalid member ID"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE id = %s", (member_id,))
    conn.commit()
    
    cursor.close()
    conn.close()

    return jsonify({"message": "Member deleted successfully"})

@admin_bp.route('/logout')
def admin_logout():
    session.clear()  # 모든 세션 데이터 삭제 (로그아웃)
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for('admin.admin_login'))  # 로그인 페이지로 이동