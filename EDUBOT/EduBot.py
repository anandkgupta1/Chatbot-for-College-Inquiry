from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

user_names = {}
user_states = {}


@app.route("/sms", methods=['POST'])
def sms_reply():
    user_message = request.form.get('Body', '').strip()
    user_phone = request.form.get('From')
    response = MessagingResponse()

    print(f"[{user_phone}] State: {user_states.get(user_phone, 'NEW')} | Message: {user_message}")

    # ── NEW USER ──────────────────────────────────────────────
    if user_phone not in user_states:
        user_states[user_phone] = "name_prompt"
        response.message("Hi there! My name is EduBot. I'm your Virtual Assistant for today!\nWhat's your name?")
        return str(response)

    state = user_states[user_phone]

    # ── NAME PROMPT ───────────────────────────────────────────
    if state == "name_prompt":
        user_names[user_phone] = user_message
        user_states[user_phone] = "menu"
        # FIX 1: Greeting + menu in ONE message so order is always correct
        response.message(
            f"Hello {user_message}, how can I assist you today?\n\n"
            "1 -> STUDENT SECTION\n"
            "2 -> FACULTY SECTION\n"
            "3 -> VISITOR SECTION\n"
            "4 -> MISCELLANEOUS SECTION\n"
            "5 -> EXIT"
        )

    # ── MAIN MENU ─────────────────────────────────────────────
    elif state == "menu":
        name = user_names.get(user_phone, "there")
        if user_message == '1':
            user_states[user_phone] = "student_level"
            response.message("SELECT YOUR GRADUATION LEVEL:\n1 -> UnderGraduation\n2 -> PostGraduation")
        elif user_message == '2':
            user_states[user_phone] = "faculty_dept"
            response.message(
                "CHOOSE YOUR DEPARTMENT:\n"
                "1. Computer Applications\n"
                "2. Management\n"
                "3. Visiting Faculty Industrial\n"
                "4. Visiting Faculty International\n"
                "5. Visiting Faculty Academic"
            )
        elif user_message == '3':
            user_states[user_phone] = "visitor_option"
            response.message(
                "SELECT YOUR OPTION:\n"
                "1. Admission\n"
                "2. Examination\n"
                "3. Placement\n"
                "4. Contact Us\n"
                "5. About EduBot"
            )
        elif user_message == '4':
            user_states[user_phone] = "misc_option"
            response.message(
                "SELECT YOUR OPTION:\n"
                "1 -> Examination Fees\n"
                "2 -> Scholarship\n"
                "3 -> Hostel Fees\n"
                "4 -> SMS Law College"
            )
        elif user_message == '5':
            response.message(f"THANK YOU, {name}, for connecting with us. Have a great day!\nFor any query, connect with me anytime. Bye! 👋")
            user_states.pop(user_phone, None)
            user_names.pop(user_phone, None)
        else:
            response.message(
                "Invalid option. Please choose 1-5:\n\n"
                "1 -> STUDENT SECTION\n"
                "2 -> FACULTY SECTION\n"
                "3 -> VISITOR SECTION\n"
                "4 -> MISCELLANEOUS SECTION\n"
                "5 -> EXIT"
            )

    # ── STUDENT: LEVEL ────────────────────────────────────────
    # FIX 2: Sub-menu states now handled directly here — no more routing bug
    elif state == "student_level":
        if user_message == '1':
            user_states[user_phone] = "student_ug"
            response.message(
                "UNDERGRADUATION COURSES:\n"
                "1. BBA\n2. BCA\n3. BA-HONS\n"
                "4. B.COM\n5. B.COM-HONS\n6. BA-LLB\n\n"
                "Please select your course:"
            )
        elif user_message == '2':
            user_states[user_phone] = "student_pg"
            response.message(
                "POSTGRADUATION COURSES:\n"
                "1. MBA\n2. MCA\n3. M.COM\n\n"
                "Please select your course:"
            )
        else:
            response.message("Invalid option. Please enter 1 for UG or 2 for PG.")

    # ── STUDENT: UG COURSE ────────────────────────────────────
    elif state == "student_ug":
        courses = {
            '1': ("BBA",        "https://www.smsvaranasi.com/bba.html"),
            '2': ("BCA",        "https://www.smsvaranasi.com/bca.html"),
            '3': ("BA-HONS",    "https://www.smsvaranasi.com/bahonsmasscomm.html"),
            '4': ("B.COM",      "https://www.smsvaranasi.com/bcom.html"),
            '5': ("B.COM-HONS", "https://www.smsvaranasi.com/bcomhons.html"),
            '6': ("BA-LLB",     "http://smslawcollege.com/ba-llb.html"),
        }
        if user_message in courses:
            cname, url = courses[user_message]
            response.message(f"Visit {cname}:\n{url}\n\nThank you for connecting with us!")
            _show_main_menu(user_phone, response)
        else:
            response.message("Invalid option. Please select 1-6.")

    # ── STUDENT: PG COURSE ────────────────────────────────────
    elif state == "student_pg":
        courses = {
            '1': ("MBA",   "https://www.smsvaranasi.com/mba.html"),
            '2': ("MCA",   "https://www.smsvaranasi.com/mca.html"),
            '3': ("M.COM", "https://www.smsvaranasi.com/mcom.html"),
        }
        if user_message in courses:
            cname, url = courses[user_message]
            response.message(f"Visit {cname}:\n{url}\n\nThank you for connecting with us!")
            _show_main_menu(user_phone, response)
        else:
            response.message("Invalid option. Please select 1-3.")

    # ── FACULTY: DEPARTMENT ───────────────────────────────────
    elif state == "faculty_dept":
        if user_message == '1':
            response.message(
                "COMPUTER APPLICATIONS FACULTIES:\n"
                "1. Dr. Kamal Sheel Mishra (HoD)\nhttps://www.smsvaranasi.com/view-faculty-details/40.html\n"
                "2. Mr. Shambhu Sharan Srivastava\nhttps://www.smsvaranasi.com/view-faculty-details/41.html\n"
                "3. Mr. Anand Prakash Dubey\nhttps://www.smsvaranasi.com/view-faculty-details/42.html\n"
                "4. Mr. Ram Gopal Gupta\nhttps://www.smsvaranasi.com/view-faculty-details/43.html\n"
                "5. Dr. Aditya Kumar Gupta\nhttps://www.smsvaranasi.com/view-faculty-details/44.html\n"
                "6. Mr. Vikash Chandra Sharma\nhttps://www.smsvaranasi.com/view-faculty-details/46.html\n"
                "7. Dr. Radha Raman Chandan\nhttps://www.smsvaranasi.com/view-faculty-details/55.html"
            )
        elif user_message == '2':
            response.message(
                "MANAGEMENT FACULTIES:\n"
                "1. Prof. Pinak Nath Jha (Director)\nhttps://www.smsvaranasi.com/view-faculty-details/1.html\n"
                "2. Mr. Sandeep Singh\nhttps://www.smsvaranasi.com/view-faculty-details/2.html\n"
                "3. Dr. Raj Kumar Singh\nhttps://www.smsvaranasi.com/view-faculty-details/3.html\n"
                "4. Dr. Sanjay Saxena\nhttps://www.smsvaranasi.com/view-faculty-details/4.html\n"
                "5. Dr. Avinash Chandra Supkar\nhttps://www.smsvaranasi.com/view-faculty-details/5.html\n"
                "6. Dr. Pallavi Pathak\nhttps://www.smsvaranasi.com/view-faculty-details/6.html\n"
                "7. Dr. Amitabh Pandey\nhttps://www.smsvaranasi.com/view-faculty-details/7.html\n"
                "8. Dr. Amit Kishore Sinha\nhttps://www.smsvaranasi.com/view-faculty-details/8.html\n"
                "9. Mr. Atish Khadse\nhttps://www.smsvaranasi.com/view-faculty-details/9.html\n"
                "10. Dr. Bhavana Singh\nhttps://www.smsvaranasi.com/view-faculty-details/10.html"
            )
        elif user_message == '3':
            response.message(
                "VISITING FACULTIES INDUSTRIAL:\n"
                "- Mr. Yogesh Kumar (Ex. VP-HR, Bhartiya International)\n"
                "- Mr. K. Gopal (VP Finance, Price Water House Coopers)\n"
                "- Mr. Alok Agrawal (Ex. Executive Director, Polar Industries)\n"
                "- Mr. D.V. Singh (Director, NOV SARRA India Pvt. Ltd.)\n"
                "- Mr. Ramesh Singh (Technical Director, NIC, New Delhi)\n"
                "- Mr. Rajeev Chandola (Head-HR & Admin, ColdEx)\n"
                "- Mr. B. Sudhakar (Head-HR, Tata Chemicals)\n"
                "- Mr. Rajeev Gupta (Head-HR, Kajaria Group)"
            )
        elif user_message == '4':
            response.message(
                "VISITING FACULTIES INTERNATIONAL:\n"
                "- Prof. Benjamin Yumol, Claffin University, USA\n"
                "- Prof. Roberto Biloslavo, University of Primoska, Slovenia\n"
                "- Mr. Arun Kumar, Sr. Manager, Hanson, Australia\n"
                "- Dr. Harriet Nettles, Educational Psychologist, USA\n"
                "- Prof. Michael De Wilde, Grand Valley State University, USA\n"
                "- Dr. Sant Kumar, University of Gondar, Ethiopia\n"
                "- Rev. Patrick McCollum, Patrick Foundation, USA\n"
                "- Prof. Graham Ward, Director, INSEAD, France"
            )
        elif user_message == '5':
            response.message(
                "VISITING FACULTIES ACADEMIC:\n"
                "- Prof. S.K. Kak, Former VC, Mahamaya Technical University\n"
                "- Prof. M.S. Lakshmi, ICFAI, Gurgaon\n"
                "- Dr. Reena Shrivastava, Lucknow University\n"
                "- Prof. H. Karnik, IIT Kanpur\n"
                "- Prof. S.K. Singh, FMS BHU Varanasi\n"
                "- Prof. A.K. Tripathi, IIT BHU Varanasi\n"
                "- Prof. Atul Tandon, Former Director-MICA, Ahmedabad"
            )
        else:
            response.message("Invalid option. Please enter 1-5.")
            return str(response)
        response.message("Thank you for connecting with us!")
        _show_main_menu(user_phone, response)

    # ── VISITOR: OPTION ───────────────────────────────────────
    elif state == "visitor_option":
        name = user_names.get(user_phone, "there")
        if user_message == '1':
            user_states[user_phone] = "visitor_admission"
            response.message(
                "ADMISSION OPTIONS:\n"
                "1. UnderGraduate Level\n"
                "2. PostGraduate Level\n"
                "3. Admission Process/Details"
            )
            return str(response)
        elif user_message == '2':
            response.message("EXAMINATION PORTAL:\nhttps://examination.smsvaranasi.com/")
        elif user_message == '3':
            user_states[user_phone] = "visitor_placement"
            response.message(
                "PLACEMENT PORTAL:\n"
                "1. Placement Cell\n"
                "2. Placement Process\n"
                "3. Placement Track Record\n"
                "4. Placement Recruiters\n"
                "5. Current Year Placement"
            )
            return str(response)
        elif user_message == '4':
            response.message("CONTACT US:\nhttps://www.smsvaranasi.com/contact-us.html")
        elif user_message == '5':
            response.message(
                "ABOUT EDUBOT\n"
                "I am EduBot, developed by 4 members from SMS College Varanasi:\n"
                "- Sumit Kumar\n- Anand Gupta\n- Atul Mishra\n- Vivek Raghuvanshi\n\n"
                f"THANK YOU, {name}! See you soon. Have a nice day!"
            )
        else:
            response.message("Invalid option. Please enter 1-5.")
            return str(response)
        response.message("Thank you for connecting with us!")
        _show_main_menu(user_phone, response)

    # ── VISITOR: ADMISSION ────────────────────────────────────
    elif state == "visitor_admission":
        options = {
            '1': ("UG Admission",      "https://online.smsvaranasi.com/apply/index.php"),
            '2': ("PG Admission",      "https://online.smsvaranasi.com/apply/index.php"),
            '3': ("Admission Process", "https://online.smsvaranasi.com/"),
        }
        if user_message in options:
            label, url = options[user_message]
            response.message(f"{label}:\n{url}\n\nThank you for connecting with us!")
            _show_main_menu(user_phone, response)
        else:
            response.message("Invalid option. Please select 1, 2, or 3.")

    # ── VISITOR: PLACEMENT ────────────────────────────────────
    elif state == "visitor_placement":
        options = {
            '1': ("Placement Cell",         "https://www.smsvaranasi.com/training-placement-cell.html"),
            '2': ("Placement Process",      "https://www.smsvaranasi.com/placement-process.html"),
            '3': ("Placement Track Record", "https://www.smsvaranasi.com/placement-track-record.html"),
            '4': ("Placement Recruiters",   "https://www.smsvaranasi.com/list-of-recruiters.html"),
            '5': ("Current Year Placement", "https://www.smsvaranasi.com/current-year-placement.html"),
        }
        if user_message in options:
            label, url = options[user_message]
            response.message(f"{label}:\n{url}\n\nThank you for connecting with us!")
            _show_main_menu(user_phone, response)
        else:
            response.message("Invalid option. Please select 1-5.")

    # ── MISCELLANEOUS ─────────────────────────────────────────
    elif state == "misc_option":
        name = user_names.get(user_phone, "there")
        options = {
            '1': ("Examination Fee Portal", "https://epay.smsvaranasi.com/"),
            '2': ("Scholarship Portal",     "https://www.smsvaranasi.com/sms-scholarship-form.html"),
            '3': ("Hostel Portal",          "https://www.smsvaranasi.com/hostel-requistion-form.html"),
            '4': ("SMS Law College",        "http://smslawcollege.com/"),
        }
        if user_message in options:
            label, url = options[user_message]
            response.message(f"{label}:\n{url}\n\nTHANK YOU, {name}, for connecting with us!")
            _show_main_menu(user_phone, response)
        else:
            response.message("Invalid option. Please select 1-4.")

    # ── UNKNOWN STATE FALLBACK ────────────────────────────────
    else:
        user_states[user_phone] = "name_prompt"
        response.message("Hi there! My name is EduBot. What's your name?")

    return str(response)


def _show_main_menu(user_phone, response):
    """Reset state to menu and show main menu options."""
    user_states[user_phone] = "menu"
    response.message(
        "Back to Main Menu:\n"
        "1 -> STUDENT SECTION\n"
        "2 -> FACULTY SECTION\n"
        "3 -> VISITOR SECTION\n"
        "4 -> MISCELLANEOUS SECTION\n"
        "5 -> EXIT"
    )


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
