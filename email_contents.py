# email_contents.py

def get_registration_email_content(verification_link):
    return f"""<p>Welcome to BowieGame! To confirm your email, please click here: 
               <a href='{verification_link}'>Confirm Email</a></p>"""

def get_password_reset_email_content(reset_link):
    return f"""<p>You requested a password reset for your BowieGame account. Please click the link below to reset your password:
               <a href='{reset_link}'>Reset Password</a></p>"""

def get_user_recovery_email_content(recovery_link):
    return f"""<p>A request has been received to recover your account. Please click the link below to proceed with the recovery:
               <a href='{recovery_link}'>Recover Account</a></p>"""
