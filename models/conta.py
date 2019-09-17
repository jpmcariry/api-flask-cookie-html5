from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(30))
    password = banco.Column(banco.String(30))
    admin = banco.Column(banco.Boolean)

    def __init__(self, login, password, admin):
        self.login = login
        self.password = password
        self.admin = admin

    def json(self):
        return {
        'login': self.login,
        'password': self.password,
        'admin': self.admin
        }
    @classmethod
    def seach(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()# SELECT * FROM HOTEIS Where hotel_id=hotel_id
        if user:
            return user
        return None
    @classmethod
    def seach_by_login(cls, login):
        login = cls.query.filter_by(login=login).first()
        if login:
            return login
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def update_user(self, login, password):
        self.login = login
        self.password = password

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
