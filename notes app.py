import streamlit as st
import html
import json , requests
sess = requests.Session()



main_host ='http://localhost:3001'
api_host = "http://api.localhost:3001"
token = '50191c35f96895eefbf7'


if "notes" not in st.session_state:
    st.session_state.notes = []

#colours with their codes
COLOURS = {
    "Yellow": "#fff3b0",
    "Pink": "#ffd6e8",
    "Blue": "#bde0fe",
    "Green": "#caffbf",
    "Purple": "#e0bbff",
    "Orange": "#ffd8a8",
    "Peach": "#ffcfd2",
    "Mint": "#b8f2e6",
    "Lavender": "#d0bfff",
    "Coral": "#ffb3ba",
    "Sky": "#a2d2ff",
    "Lemon": "#fdffb6",
    "Rose": "#ffc9de",
    "Teal": "#99e2b4",
    "Grey": "#e2e2e2",
}

# refresh page karne ke liya function tke koi aur bi same token per note add kare wo muje show ho jaye 
# me abi kise ke sath connected ni hon to refresh button ki zarrirt ni hai per koi mare token le to ye button kam kare ga 
def load_again ():
    r = sess.get (f"{api_host}/{token}")
    st.session_state.notes = r.json()["notes"]

# ui page
# name . message . color. button in form
with st.form('post notes',clear_on_submit=True):
    
    c4 = st.columns(1)[0]
    about = c4.text_input(label= 'ABOUT',placeholder='Add short title of your note')

    c1,c2,c3 = st.columns((2,4,1))
    name=c1.text_input(label='name')
    message=c2.text_input(label='message')
    colour= c3.selectbox('colour',list(COLOURS.keys()))
    submit_button=st.form_submit_button("Post")


    if name and message and submit_button:
        st.session_state.notes.append({
                "about":about,
                "name": name,
                "message": message,
                "colour": colour
            })
        
        r = sess.post(f"{api_host}/{token}",json={"notes":st.session_state.notes})
        st.write(r.status_code) 
if st.button("REFRESH"):
    load_again()
    st.rerun()


#loop sab notes dekhane le liya
for i , note in enumerate(st.session_state.notes):
    #html.escape  use kar rahi ho tke special charater koi masla na karen
    final_about = html.escape(note["about"])
    final_name = html.escape(note["name"])
    final_message = html.escape(note["message"])
    background_colour = COLOURS.get(note.get("colour"),"Grey")
    st.markdown(
        f"""
        <div style="background:{background_colour}; border-radius:8px; padding:12px; margin-bottom:8px;">
        
        <h3>
            {final_about}
        </h3>
        <br>
        <h5>
            {final_name} 
        </h5>
        <br>
        <b>
            {final_message}
        </b>
       
        
        </div>""",

        unsafe_allow_html=True
    )
