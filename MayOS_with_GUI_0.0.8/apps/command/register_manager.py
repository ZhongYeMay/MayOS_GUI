from apps.command.user_manager import UserManager

class RegisterManager:
    @staticmethod
    def register_user(username, password):
        if not username or not password:
            return False, "用户名和密码不能为空！"
        if UserManager.add_user(username, password):
            return True, f"用户 {username} 注册成功！"
        else:
            return False, "用户名已存在！"
