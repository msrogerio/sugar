from . import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)  
    username = db.Column(db.String(255), default='')
    name = db.Column(db.String(532), default='')
    login = db.Column(db.String(255), default='')
    scr = db.Column(db.String(1000), default='')
    _folowers = db.relationship('Folowers', backref='folowers')
    _folowing = db.relationship('Following', backref='folowing')
    _unfollow = db.relationship('Unfollow', backref='folowing')
    
    def __repr__(self):
        return '[ Users ] id: %d | username: %s ' % (self.id, self.username)


class Folowers(db.Model):
    __tablename__ = 'folowers'
    id = db.Column(db.Integer(), primary_key=True)  
    username = db.Column(db.String(255), default='')
    name = db.Column(db.String(532), default='')
    email = db.Column(db.String(255), default='')
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '[ Folowers ] id: %d | username: %s ' % (self.id, self.username)


class Following(db.Model):
    __tablename__ = 'following'
    id = db.Column(db.Integer(), primary_key=True)  
    username = db.Column(db.String(255), default='')
    name = db.Column(db.String(532), default='')
    email = db.Column(db.String(255), default='')
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '[ Following ] id: %d | username: %s ' % (self.id, self.username)


class Unfollow(db.Model):
    __tablename__ = 'unfollow'
    id = db.Column(db.Integer(), primary_key=True)  
    username = db.Column(db.String(255), default='')
    name = db.Column(db.String(532), default='')
    email = db.Column(db.String(255), default='')
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '[ Unfollow ] id: %d | username: %s ' % (self.id, self.username)


class CheckProgress(db.Model):
    __tablename__ = 'check_progress'
    id = db.Column(db.Integer(), primary_key=True)  
    mensage = db.Column(db.String(1000), default='')
    status = db.Column(db.Boolean(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '[ CheckProgress ] id: %d | total de registros: %s ' % (self.id, self.total_recordsusername)


class StoppedFollowing(db.Model):
    __tablename__ = 'stopped_following'
    id = db.Column(db.Integer(), primary_key=True)  
    username = db.Column(db.String(255), default='')
    name = db.Column(db.String(532), default='')
    email = db.Column(db.String(255), default='')
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '[ StoppedFollowing ] id: %d | username: %s ' % (self.id, self.username)