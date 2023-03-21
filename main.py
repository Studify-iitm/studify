import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, make_response, request, render_template

import json
import os

# Use the application default credentials.
# cred = credentials.ApplicationDefault()

# firebase_admin.initialize_app(cred)
# db = firestore.client()

app = Flask(__name__)

# route to intake course


@app.route("/course", methods=["POST"])
def ingest_course():
    # extract data from the request
    data = request.get_json()

    # sanity check to confirm Notebook version
    try:
        assert data['ALE_VERSION'] == os.environ.get("ALE_VERSION")
        del data['ALE_VERSION']
    except AssertionError:
        return make_response({"message": "Please update your script"}, 412)

    # figure out the course from the data
    course_id = data['course_id'].split("_")
    course_level = ["foundation", "diploma", "degree"][int(course_id[2][2])-1] 

    # store  the contents corresponding to the course
    course_ref = db.collection("ds_courses").document(
        course_id[1]).collection(course_id[2]).document("course")
    flag = False
    if not course_ref.get().exists:
        # new course, set flag to write metadata
        flag = True
    course_ref.set(data)

    if flag:
        print("writing metadata")
        metadata_ref = db.document(f"ds_courses/{course_id[1]}")
        if metadata_ref.get().exists:
            print("term reference exists")
            metadata_ref.update({
                f"course_metadata.{course_level}.{course_id[2]}": data['title']
            })
        else:
            metadata_ref.set({
                "prefix": course_id[0],
                "term": course_id[1],
                "course_metadata": {
                    course_level: {
                        course_id[2]: data['title']
                    }
                }
            })

    return make_response("file written successfully", 200)


@app.route("/course/<course_id>", methods=["GET"])
def fetch_post(course_id):
    # course_id = course_id.split("_")
    result = {"course_id": "ns_23t1_cs1002", "forum_url": "https://discourse.onlinedegree.iitm.ac.in/c/courses/python-kb", "title": "Jan 2023 - Python", "week_wise": [{"title": "Course Introduction", "videos": [{"title": " How to submit a programming assignment", "transcript_vtt_url": "", "yt_vid": "5XFoXlIwNe0"}]}, {"title": "Week 1", "videos": [{"title": "L1.1: Introduction", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec1W1.vtt", "yt_vid": "8ndsDXohLMQ"}, {"title": "L1.2: Introduction to Replit", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec2W1.vtt", "yt_vid": "NgZZ0HIUqbs"}, {"title": "L1.3: More on Replit, print and Common Mistakes", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3W1.vtt", "yt_vid": "As7_aq6XGfI"}, {"title": "L1.4: A Quick Introduction to Variables", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4W1.vtt", "yt_vid": "Yg6xzi2ie5s"}, {"title": "L1.5: Variables and Input Statement", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.vtt", "yt_vid": "ruQb8jzkGyQ"}, {"title": "L1.6: Variables and Literals", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6W1.vtt", "yt_vid": "tDaXdoKfX0k"}, {"title": "L1.7: Data Types 1", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec7W1.vtt", "yt_vid": "8n4MBjuDBu4"}, {"title": "L1.8: Data Types 2", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec8W1.vtt", "yt_vid": "xQXxufhEJHw"}, {"title": "L1.9: Operators and Expressions 1", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec9W1.vtt", "yt_vid": "8pu73HKzNOE"}, {"title": "L1.10: Operators and Expressions 2", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec10W1.vtt", "yt_vid": "Y53K9FFu97Q"}, {"title": "L1.11: Introduction to Strings", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec11W1.vtt", "yt_vid": "sS89tiDuqoM"}, {"title": "L1.12: More on Strings", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec12W1.vtt", "yt_vid": "e45MVXwya7A"}, {"title": "L1.13: Conclusion: FAQs", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec13W1.vtt", "yt_vid": "_Ccezy5hlc8"}]}, {"title": "Week 2", "videos": [{"title": "L2.1: Introduction", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec1.vtt", "yt_vid": "aEPFZSzZ6VQ"}, {"title": "L2.2: Variables : A Programmer's Perspective", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec2.vtt", "yt_vid": "XZSnqseRbZY"}, {"title": "L2.3: Variables Revisited: Dynamic Typing", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.vtt", "yt_vid": "2OFZY77eOjw"}, {"title": "L2.4: More on Variables, Operators and Expressions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.vtt", "yt_vid": "-f833WH_cVo"}, {"title": "L2.5: Escape characters and types of quotes", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.vtt", "yt_vid": "4vWM2oTGEio"}, {"title": "L2.6: String Methods", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.vtt", "yt_vid": "bRAo6TJJjCU"}, {"title": "L2.7: An Interesting Cipher: More on Strings", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec7.vtt", "yt_vid": "oxFYdHVNpg8"}, {"title": "L2.8: Introduction to the if statement", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec8.vtt", "yt_vid": "FTX5wF_3J9Q"}, {"title": "L2.9: Tutorial on if, else and else-if (elif) conditions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec9.vtt", "yt_vid": "-dBqiRCHbNw"}, {"title": "L2.10: Introduction to \"import library\"", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec10.vtt", "yt_vid": "OdjXL5U95eI"}, {"title": "L2.11: Different ways to import a library", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec11.vtt", "yt_vid": "eW58_ky7oc8"}, {"title": "L2.12: Conclusion", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec12.vtt", "yt_vid": "DK16M8EvOLE"}]}, {"title": "Week 3", "videos": [{"title": "L3.1: Introduction", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.1.vtt", "yt_vid": "xiEzc_m2izc"}, {"title": "L3.2: Introduction to while loop", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.2.vtt", "yt_vid": "KTvVNN7ia8o"}, {"title": "L3.3: While to Compute Factorial", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.3.vtt", "yt_vid": "-ZMw8D-Xapk"}, {"title": "L3.4: Tutorial on while loop", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.4.vtt", "yt_vid": "SqMeT9caxpE"}, {"title": "L3.5: Introduction to for loop", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.5.vtt", "yt_vid": "lvXuQ_x7EsI"}, {"title": "L3.6: for loop to add the first n numbers", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.6.vtt", "yt_vid": "lrbqrxIZcaQ"}, {"title": "L3.7: for loop for multiplication tables", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.7.vtt", "yt_vid": "SMASd0rbt0g"}, {"title": "L3.8: More on range and for loop without range", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.8.vtt", "yt_vid": "ihL3Eac9tFc"}, {"title": "L3.9: Formatted Printing", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.9.vtt", "yt_vid": "DR0BhSzGnPo"}, {
        "title": "L3.10: Tutorial on for loop and difference between while loop and for loop", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.10.vtt", "yt_vid": "7D2SFKSiiLg"}, {"title": "L3.11: Nested for loop", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.11.vtt", "yt_vid": "-4MRaWABCuo"}, {"title": "L3.12: Tutorial on nested loops", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.12.vtt", "yt_vid": "590mjTALkj0"}, {"title": "L3.13: break, continue and pass", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.13.vtt", "yt_vid": "SVAVQHfJbE0"}, {"title": "L3.14: Conclusion", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec3.14.vtt", "yt_vid": "DhjvmkGgw8U"}]}, {"title": "Week 4", "videos": [{"title": "L4.1: Introduction", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.1.vtt", "yt_vid": "02BCThws054"}, {"title": "L4.2: Warmup with Lists", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.2.vtt", "yt_vid": "toMhJJHSIYk"}, {"title": "L4.3: Birthday Paradox", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.3.vtt", "yt_vid": "wpM41ZYLt0k"}, {"title": "L4.4: Naive Search in a List", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.4.vtt", "yt_vid": "3huwiAPi-_I"}, {"title": "L4.5: The Obvious Sort", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.5.vtt", "yt_vid": "hkDAafi09yo"}, {"title": "L4.6: Dot Product", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.6.vtt", "yt_vid": "qSOoiWNplGo"}, {"title": "L4.7: Matrix Addition", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.7.vtt", "yt_vid": "CRhUooqcvcU"}, {"title": "L4.8: Matrix Multiplication - 1", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.8.vtt", "yt_vid": "seYP1F6Ct2g"}, {"title": "L4.9: Matrix Multiplication - 2", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.9.vtt", "yt_vid": "mtRRS_ssl3s"}, {"title": "L4.10: Conclusion", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec4.10.vtt", "yt_vid": "Z-1CxNrmRR4"}]}, {"title": "Week 5", "videos": [{"title": "Introduction to Functions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.1.vtt", "yt_vid": "zDZRfWWetg0"}, {"title": "More Examples of Functions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.2.vtt", "yt_vid": "TBFTFusLIco"}, {"title": "Sorting using Functions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.3.vtt", "yt_vid": "8MQBieBCRFA"}, {"title": "Matrix Multiplication using Functions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.4.vtt", "yt_vid": "HJetH-CCOGY"}, {"title": "Theoretical Introduction to Recursion", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.5.vtt", "yt_vid": "htu4ZCW7hzA"}, {"title": "Recursion - An Illustration", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.6.vtt", "yt_vid": "PAUlGa9wAxA"}, {"title": "Types of Function Arguments", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.7.vtt", "yt_vid": "NqjnCY2qQWU"}, {"title": "Scope of Variables", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.8.vtt", "yt_vid": "4q5rGHfR-ic"}, {"title": "Types of Functions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.9.vtt", "yt_vid": "F9xeVMToUJ8"}, {"title": "Tutorial on functions", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec5.10.vtt", "yt_vid": "mkAbfQM2OJY"}]}, {"title": "Week 6", "videos": [{"title": "L6.1: Lists and Sets", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.1.vtt", "yt_vid": "WQNxG2B85rc"}, {"title": "L6.2: Dictionaries", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.2.vtt", "yt_vid": "X8Nj5cxaP9E"}, {"title": "L6.3: Tuples", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.3.vtt", "yt_vid": "z-n9yQaWr7o"}, {"title": "L6.4: More on Lists", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.4.vtt", "yt_vid": "aaaENpVGS5U"}, {"title": "L6.5: More on Tuples", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.5.vtt", "yt_vid": "V7r6DB3a6_o"}, {"title": "L6.6: More on Dictionaries", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.6.vtt", "yt_vid": "gTpPI3SMnAA"}, {"title": "L6.7: More on Sets", "transcript_vtt_url": "https://backend.seek.onlinedegree.iitm.ac.in/21t2_cs1002/assets/img/Lec6.7.vtt", "yt_vid": "qoV4tdDD8zE"}]}, {"title": "Week 8", "videos": [{"title": "L8.1: Introduction to the week and introduction to recursion", "transcript_vtt_url": "", "yt_vid": "SGCy1yBLbsg"}, {"title": "L8.2: Recursion: a simple question", "transcript_vtt_url": "", "yt_vid": "wkglgM6uUmI"}, {"title": "L8.3: Recursion: find 0 in a list", "transcript_vtt_url": "", "yt_vid": "eNARY_uyLqo"}, {"title": "L8.4: Sorting Recursively", "transcript_vtt_url": "", "yt_vid": "vRajQuHdlBE"}, {"title": "L8.5: Introduction to Binary Search", "transcript_vtt_url": "", "yt_vid": "WEJt1L7YTpM"}, {"title": "L8.6: Warm up for Binary Search", "transcript_vtt_url": "", "yt_vid": "Bb7oymEgX_I"}, {"title": "L8.7: Binary Search Implementation", "transcript_vtt_url": "", "yt_vid": "1l83L1ZKF5k"}, {"title": "L8.8: Binary Search Recursion Way", "transcript_vtt_url": "", "yt_vid": "v_WYTBhHONo"}]}]}
    return render_template("course.html", data=result)


    # read the contents of {course_id}.json
'''   course_ref = db.collection(f"ds_courses/{course_id[1]}/{course_id[2]}").document("course")
    data = course_ref.get()
    
    if data.exists:
        return data.to_dict()
    else:
        return make_response("course not found", 404)'''


@app.route("/terms", methods=["GET"])
def list_terms():
    terms = []
    terms_ref = db.collection("ds_courses")
    for document in terms_ref.list_documents():
        terms.append(document.id)
    return make_response(sorted(terms, reverse=True), 200)


@app.route("/term/<term_id>", methods=["GET"])
def get_term_metadata(term_id):
    term_metadata_ref = db.document(f"ds_courses/{term_id}")
    data = term_metadata_ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return make_response({"metadata for course not found"}, 404)


@app.route("/test")
def test():
    data = {
        "course_metadata": {
            "degree": {
                "cs3003": "Degree Test"
            },
            "diploma": {
                "cs2002": "Diploma Test"
            },
            "foundation": {
                "cs1002": "Jan 2023 - Python",
                "hs1002": "Jan 2023 - English II",
                "ma1003": "Jan 2023 - Mathematics II"
            }
        },
        "prefix": "ns",
        "term": "23t1"
    }
    return render_template("ind.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, port=51000)
