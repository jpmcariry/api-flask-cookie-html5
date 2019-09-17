from sql_alchemy import banco as db

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    classe = db.Column(db.String(20))
    def __init__(self, id, public_id, classe, name, password):
        self.id=id
        self.public_id = public_id
        self.classe = classe
        self.name = name
        self.password = password


    def json(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'name': self.name,
            'password': self.password,
            'classe': self.classe
        }

    @classmethod
    def seach(cls, public_id):
        user = cls.query.filter_by(public_id=public_id).first()  # SELECT * FROM Users Where public_id=hotel_id
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, classe):
        self.classe = classe

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
