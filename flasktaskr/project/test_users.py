def test_default_user_role(self):
    db.session.add(
        User(
            "Johnny",
            "jon@gamm.com",
            "joo"
        )
    )

    db.session.commit()

    users = db.session.query(User).all()
    print(users)
    for user in users :
        self.assertEquals(user.role, 'user')