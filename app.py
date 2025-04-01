from hydralit import HydraApp
import apps
import streamlit as st

st.set_page_config(page_title='Personal Library',
                   page_icon="📚",
                   layout='wide',
                   initial_sidebar_state='auto')

if __name__ == '__main__':
    hydralit_navbar = True
    sticky_navbar = False
    animate_navbar = True
    hide_st = True

    over_theme = {'txc_inactive': '#FFFFFF'}
    
    app = HydraApp(
        title='Personal Library',
        favicon="📚",
        hide_streamlit_markers=hide_st,
        banner_spacing=[5,30,60,30,5],
        use_navbar=hydralit_navbar, 
        navbar_sticky=sticky_navbar,
        navbar_animation=animate_navbar,
        navbar_theme=over_theme
    )
    
    app.add_app("Home", icon="🏠", app=apps.HomeApp(title='Home'),is_home=True)
    
    app.add_app("User",icon="🧑",app=apps.UserApp(title="User"))
    
    app.add_app("Signup", icon="🛰️", app=apps.SignUpApp(title='Signup'), is_unsecure=True)
    app.add_app("Login", apps.LoginApp(title='Login'),is_login=True)

    
    app.enable_guest_access()
    user_access_level, username = app.check_access()
    
    if user_access_level > 1:
        complex_nav = {
            'Home': ['Home'],
            'User': ['User'],
        }
    elif user_access_level == 1:
        complex_nav = {
            'Home': ['Home'],
        }
    else:
        complex_nav = {
            'Home': ['Home'],
        }
        
    app.run(complex_nav)