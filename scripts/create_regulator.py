from django.contrib.auth import get_user_model
from tickets.models import Profile

DEFAULT_PASSWORD = "123qwe!@#"

def run():
    User = get_user_model()
    
    username = input("Username: ")
    qs = User.objects.filter(username=username)
    if qs.exists():
        print("Username already exists")
        return
    
    new_user = User(
        username=username,
        email="regulador@gmail.com",
        first_name="Teste",
        last_name="Regulador",
    )
    new_user.set_password(DEFAULT_PASSWORD)

    user_profile = Profile(user=new_user, user_type="R", phone="51 99259-2848")

    new_user.save()
    user_profile.save()

    print("User created")
