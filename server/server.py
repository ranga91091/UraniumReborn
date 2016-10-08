from flask import Flask
from flask import render_template
from flask import request
from database.database import db_session
from database.database import init_db
from models.faculty import faculty
from models.project import project
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask("UraniumReborn", template_folder=tmpl_dir)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['POST', 'GET'])
def mainpage():
    if request.method == 'POST':
        f_name = request.form['facultyName']
        f_ph = request.form['facultyPhone']
        f_email = request.form['facultyEmail']
        f_dept = request.form['departmentOrProgram']
        sf = None
        g = None

        sf_name = request.form['secondFacultyName']
        sf_ph = request.form['secondFacultyPhone']
        sf_email = request.form['secondFacultyEmail']
        sf_dept = request.form['secondDepartmentOrProgram']

        g_name = request.form['gradStudentName']
        g_ph = request.form['gradStudentPhone']
        g_email = request.form['gradStudentEmail']

        is_focus = request.form['isDevelopingCommunities'] == 'yes' if True else False
        p_title = request.form['apprenticeshipTitle']
        p_website = "abc"
        #request.form['apprenticeshipWebLink']
        p_req = request.form['specialRequirement1'] + '::' + request.form['specialRequirement2'] + '::' + request.form[
            'specialRequirement3'] + '::' + request.form['specialRequirement4'] + '::' + request.form[
                    'specialRequirement5']
        p_desc = request.form['apprenticeshipDescription']
        p_dept_n = str(request.form.getlist('fieldOfStudy[]'))
        p_amt_sup = request.form['amountOfSupervision']
        p_sup_prov = request.form['primarySupervisor']
        p_nat_w = request.form['primaryNature']
        p_amt_pr = request.form['priorWork']
        p_n_spec_stud = request.form['desiredStudentName']
        p_sp_typ = request.form['speedType']
        p_acc_cnt = request.form['accountingContactName']
        p_has_sup_dla = request.form['other'] == 'yes' if True else False

        p = project(p_title, is_focus, p_website, p_req, p_desc, p_dept_n, p_amt_sup, p_sup_prov, p_nat_w, p_amt_pr,
                    p_n_spec_stud, p_sp_typ, p_acc_cnt, p_has_sup_dla)

        f = faculty(f_name, f_ph, f_email, f_dept, False, p.get_id())
        if sf_name:
            sf = faculty(sf_name, sf_ph, sf_email, sf_dept, False, p.get_id())
        if g_name:
            g = faculty(g_name, g_ph, g_email, None, True, p.get_id())

        db_session.add(p)
        db_session.commit()
        db_session.add(f)
        if g:
            db_session.add(g)
        if sf:
            db_session.add(sf)
        db_session.commit()

        result = project.query.all()
        return str(result).replace("<", "").replace(">", "")
    else:
        return render_template("Faculty.html")


init_db()
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
