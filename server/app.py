from flask import Flask, render_template, request
from forms import SignupForm
from database.database import db_session, init_db
import os
import json
from models.faculty import faculty
from models.project import project

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app.secret_key = "dev-key"


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():    
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            return "Dummy Signup"
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/faculty')
def faculty_page():
    return render_template('faculty.html')


@app.route('/listofprojects', methods=['GET', 'POST'])
def listofprojects():

    if request.method == 'POST':
        f_first_name = request.form.get('facultyFirstName', None)
        f_last_name = request.form.get('facultyLastName',None)

        name = f_first_name +' ' + f_last_name

        f_ph = request.form.get('facultyPhone', None)
        f_email = request.form.get('facultyEmail', None)
        f_dept = str(request.form.get('facultyDepartment', None))
        sf = None
        g = None

        sf_first_name = request.form.get('secondFacultyFirstName',None)
        sf_last_name = request.form.get('secondFacultyLastName',None)

        sf_name= sf_first_name + ' ' + sf_last_name

        sf_ph = request.form.get('secondFacultyPhone',None)
        sf_email = request.form.get('secondFacultyEmail',None)
        sf_dept = str(request.form.get('secondDepartment',None))

        g_first_name = request.form.get('gradStudentFirstName',None)
        g_last_name = request.form.get('gradStudentLastName',None)

        g_name = g_first_name+ ' ' + g_last_name
        g_ph = request.form.get('gradStudentPhone',None)
        g_email = request.form.get('gradStudentEmail',None)
        g_dept = str(request.form.get('gradStudentDepartment',None))
        is_focus = request.form.get('isDevelopingCommunities', False)
        #print is_focus

        is_focus_value = False
        if is_focus == "yes":
            is_focus_value= True

        p_title = request.form.get('apprenticeshipTitle',None)
        p_website = request.form.get('apprenticeshipWeblink',None)
        p_req = request.form.get('specialRequirements1',None) + '::' + request.form.get('specialRequirements2', None) + '::' + request.form.get(
            'specialRequirements3', None) + '::' + request.form.get('specialRequirements4', None) + '::' + request.form.get(
            'specialRequirements5', None)

        p_desc = request.form.get('apprenticeshipDescription',None)
        p_dept_n = request.form.getlist('fieldOfStudy[]')
        p_dept_n_value = ",".join(p_dept_n)

        p_amt_sup = request.form.get('amountOfSupervision', None)
        #print p_amt_sup
        p_amt_sup_value = None
        if p_amt_sup == "little":
            p_amt_sup_value = "Very little supervision; student will need to work largely independently"
        elif p_amt_sup == "moderate":
            p_amt_sup_value = "Moderate amount of supervision and interaction with others"
        else:
            p_amt_sup_value = "Good deal of supervision; student will work as an integral part of a research team"

        p_sup_prov = request.form.get('supervisor', None)
        p_sup_prov_value = None

        if p_sup_prov == "faculty":
            p_sup_prov_value = "Faculty"
        elif p_sup_prov == "graduateStudent":
            p_sup_prov_value = "Graduate Student"
        else:
            p_sup_prov_value = "Combination of Faculty and Graduate Students"

        p_nat_w = request.form.get('primaryNature', None)

        p_nat_w_value = None

        if p_nat_w == "theoretical":
            p_nat_w_value = "Theoretical, most work on paper/electronic medium"
        elif p_nat_w == "experimental":
            p_nat_w_value="Experimental, requiring hands-on work in a lab"
        elif p_nat_w == "fieldBased":
            p_nat_w_value="Field based, requiring hands-on work in the field"
        elif p_nat_w == "computerRelated":
            p_nat_w_value="Computer-related, involving coding/analysis"
        elif p_nat_w == "combination":
            p_nat_w_value ="Combination of several types of work"
        else:
            p_nat_w_value = request.form.get('otherNatureOfWork',None)

        p_amt_pr = request.form.get('priorWork', None)
        p_amt_pr_value = None

        if p_amt_pr== "none":
            p_amt_pr_value = "No prior work; student will be starting from basic idea"
        elif p_amt_pr == "some":
            p_amt_pr_value ="Some prior work; student will build on work of others"
        elif p_amt_pr =="wellEstablished":
            p_amt_pr_value = "Well-established body of work; student will refine/improved upon efforts of others"
        else:
            p_amt_pr_value =  request.form.get('otherAmountOfWork',None)

        p_n_spec_stud = request.form.get('desiredStudent', None)

        p_sp_typ = request.form.get('speedType', None)
        if p_sp_typ == '':
            p_sp_typ = request.form.get('isNotSure', None)

        p_acc_cnt = request.form.get('accountingContactName', None)

        f_has_sup_dla = request.form.get('isSupervisedBefore', "no")

        f_has_sup_dla_value = False
        if f_has_sup_dla == "yes":
            f_has_sup_dla_value = True
        else:
            f_has_sup_dla_value = False

        f = faculty(name, f_ph, f_email, f_dept, False, f_has_sup_dla_value)

        if sf_name:
            sf = faculty(sf_name, sf_ph, sf_email, sf_dept, False, False)
        if g_name:
            g = faculty(g_name, g_ph, g_email, g_dept, True, False)

        p = project(p_title,f.get_id(),is_focus_value, p_website, p_req, p_desc, p_dept_n_value, p_amt_sup_value,  p_sup_prov_value, p_nat_w_value, p_amt_pr_value,
                    p_n_spec_stud, p_sp_typ, p_acc_cnt)

        db_session.add(f)
        if g:
            db_session.add(g)
        if sf:
            db_session.add(sf)
        db_session.commit()
        db_session.add(p)
        db_session.commit()

    facs = faculty.query.all()
    rows = []

    for f in facs:
        for p in f.projects:
            row = {"Faculty Name": f.faculty_name, "id": p.id, "Project Name": p.title, "Project Description": p.description}
            rows.append(row)

    return render_template('listofprojects.html', pRows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)