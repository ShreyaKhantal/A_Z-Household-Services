from flask import Flask, render_template, request, redirect, url_for, Blueprint,session,flash, current_app, send_from_directory, abort
from models import db, Provider, Customer, Admin, ServiceCategory, ServiceSubtype, ServiceRequest, Review
from werkzeug.utils import secure_filename
from sqlalchemy import func, extract, desc
from datetime import datetime
import os, io
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend

import matplotlib.pyplot as plt
from flask import jsonify, send_file, make_response
import base64
# from app2 import app2
app1 = Blueprint('main', __name__)

# app1.register_blueprint(app2)

@app1.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        if "admin" in request.form:
            return redirect(url_for("main.admin_login"))
        elif "login" in request.form:
            return redirect(url_for("main.login"))
        elif "provider" in request.form:
            return  redirect(url_for("main.provider"))
        elif "customer" in request.form:
            return redirect(url_for("main.customer"))
    return render_template("home.html")

@app1.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        exist = Admin.query.filter_by(email=email, password=password).first()
        if not exist:
            flash("Invalid Email or Password")
            return redirect(url_for("main.admin_login"))
        session['admin_id'] = exist.id
        return redirect(url_for("main.admin_home"))
    return render_template("admin_login.html")

@app1.route("/admin_home", methods=["GET", "POST"])
def admin_home():
    # Check if admin is logged in
    if 'admin_id' not in session:
        return "Not Signed In"
    
    admin = Admin.query.filter_by(id=session['admin_id']).first()

    if request.method == 'POST':
        # Handle profile form
        if "profileForm" in request.form:
            admin.email = request.form['email']
            password = request.form['password']
            if password:
                admin.password = password
            db.session.commit()

        # Handle service category form
        if 'serviceCategory' in request.form:
            category_name = request.form.get("serv_type")
            category = ServiceCategory.query.filter_by(name=category_name.lower()).first()
            if not category:
                # Create new category if it doesn't exist
                category = ServiceCategory(name=category_name.lower())
                db.session.add(category)
                db.session.commit()

        # Handle service form (service creation)
        if "serviceForm" in request.form:
            category_name = request.form['serv_categ']
            service_name = request.form["service"]
            exists = ServiceSubtype.query.filter_by(name=service_name.lower()).first()
            if not exists:
                description = request.form.get("description")
                price = request.form.get("price")
                category = ServiceCategory.query.filter_by(name=category_name.lower()).first()
                if not category:
                    return "Category not found"
                # Create new service subtype
                service_subtype = ServiceSubtype(
                    category_id=category.id,
                    name=service_name.lower(),
                    base_price=float(price),
                    description=description
                )
                db.session.add(service_subtype)
                db.session.commit()
                return redirect(url_for("main.admin_home"))
    
    cat_count = ServiceCategory.query.count()
    sub_count = ServiceSubtype.query.count()
    act_cust = Customer.query.filter_by(active=True).count()
    inact_cust = Customer.query.filter_by(active=False).count()
    act_prov = Provider.query.filter_by(active=True).count()
    inact_prov = Provider.query.filter_by(active=False).count()
    req_count = ServiceRequest.query.count()

    # Service request status counts
    stat_data = db.session.query(ServiceRequest.status, db.func.count(ServiceRequest.id)).group_by(ServiceRequest.status).all()
    stat_lbls, stat_vals = zip(*stat_data) if stat_data else ([], [])

    # Flagged providers and customers
    flag_prov = inact_prov
    flag_cust = inact_cust

    # Subtype counts per category
    sub_data = (
    db.session.query(ServiceCategory.name, db.func.count(ServiceSubtype.id))
    .join(ServiceSubtype, ServiceSubtype.category_id == ServiceCategory.id)
    .group_by(ServiceCategory.name)
    .all()
    )

    cat_lbls, cat_vals = zip(*sub_data) if sub_data else ([], [])

    # Chart generation functions
    def pie_chart(lbls, vals, title):
        fig, ax = plt.subplots()
        ax.pie(vals, labels=lbls, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title(title)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode()

    def bar_chart(lbls, vals, title, ylabel):
        fig, ax = plt.subplots()
        ax.bar(lbls, vals)
        plt.title(title)
        plt.ylabel(ylabel)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode()
    cust_chart=None
    prov_chart=None
    # Generate charts
    stat_chart = pie_chart(stat_lbls, stat_vals, "Service Request Status")
    if act_prov or inact_prov:
        prov_chart = pie_chart(['Flagged', 'Unflagged'], [flag_prov, act_prov], "Providers Status")
    if act_cust or inact_cust:
        cust_chart = pie_chart(['Flagged', 'Unflagged'], [flag_cust, act_cust], "Customers Status")
    sub_chart = bar_chart(cat_lbls, cat_vals, "Subtypes per Category", "Subtypes")

    customers = []
    providers = []
    service_requests = []
    categories = ServiceCategory.query.all()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # Handle Customer Search Form
        if form_type == 'customer':
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            contact = request.form.get('contact', '')
            address = request.form.get('address', '')
            pincode = request.form.get('pincode', '')
            active_status = request.form.get('active_status', '')

            customers_query = Customer.query
            if name:
                customers_query = customers_query.filter(Customer.name.like(f'%{name}%'))
            if email:
                customers_query = customers_query.filter(Customer.email.like(f'%{email}%'))
            if contact:
                customers_query = customers_query.filter(Customer.contact.like(f'%{contact}%'))
            if address:
                customers_query = customers_query.filter(Customer.address.like(f'%{address}%'))
            if pincode:
                customers_query = customers_query.filter(Customer.pincode == pincode)
            if active_status:
                customers_query = customers_query.filter(Customer.active == (active_status == 'true'))

            customers = customers_query.all()

        # Handle Provider Search Form
        elif form_type == 'provider':
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            contact = request.form.get('contact', '')
            pincode = request.form.get('pincode', '')
            category = request.form.get('category', '')
            subtype = request.form.get('subtype', '')
            rating = request.form.get('rating', '')
            experience = request.form.get('experience', '')
            balance = request.form.get('balance', '')
            active_status = request.form.get('active_status', '')

            providers_query = Provider.query
            if name:
                providers_query = providers_query.filter(Provider.name.like(f'%{name}%'))
            if email:
                providers_query = providers_query.filter(Provider.email.like(f'%{email}%'))
            if contact:
                providers_query = providers_query.filter(Provider.contact.like(f'%{contact}%'))
            if pincode:
                providers_query = providers_query.filter(Provider.pincode == pincode)
            if category:
                providers_query = providers_query.join(ServiceSubtype, Provider.subtype_id == ServiceSubtype.id).join(ServiceCategory, ServiceSubtype.category_id == ServiceCategory.id).filter(ServiceCategory.id == int(category))
            if subtype:
                providers_query = providers_query.join(ServiceSubtype).filter(ServiceSubtype.id == int(subtype))
            if rating:
                providers_query = providers_query.filter(Provider.rating >= float(rating))
            if experience:
                providers_query = providers_query.filter(Provider.experience >= int(experience))
            if balance:
                providers_query = providers_query.filter(Provider.balance >= float(balance))
            if active_status:
                providers_query = providers_query.filter(Provider.active == (active_status == 'true'))

            providers = providers_query.all()

        elif form_type == 'requests':
            provider_name = request.form.get('provider_name', '').strip()
            customer_name = request.form.get('customer_name', '').strip()
            status = request.form.get('status', '')
            pincode = request.form.get('pincode', '').strip()
            address = request.form.get('address', '').strip()
            date_of_request = request.form.get('date_of_request', '')
            date_of_completion = request.form.get('date_of_completion', '')
            active_status = request.form.get('active_status', '')


            # Base query
            query = db.session.query(ServiceRequest).join(Provider).join(Customer)

            # Apply filters based on search criteria
            if provider_name:
                query = query.filter(Provider.name.ilike(f'%{provider_name}%'))
            if customer_name:
                query = query.filter(Customer.name.ilike(f'%{customer_name}%'))
            if status:
                query = query.filter(ServiceRequest.status == status)
            if pincode:
                query = query.filter(Provider.pincode.ilike(f'%{pincode}%'))
            if address:
                query = query.filter(Provider.address.ilike(f'%{address}%'))
            if date_of_request:
                query = query.filter(func.date(ServiceRequest.date_of_request) == date_of_request)
            if date_of_completion:
                query = query.filter(func.date(ServiceRequest.date_of_completion) == date_of_completion)
            if active_status:
                query = query.filter(ServiceRequest.active == (active_status == 'true'))

            # Execute the query
            service_requests = query.all()
    categories = ServiceCategory.query.all()
    subtypes = ServiceSubtype.query.all()

    # Fetch other required data for the template
    prov = Provider.query.all()
    subtype_data = ServiceSubtype.query.all()
    # customers_list = Customer.query.all()

    return render_template(
        "admin_home.html",
        admin=admin,
        categories=categories,
        subtypes=subtypes,
        prov=prov,
        subtype=subtype_data,
        customers=customers,
        providers=providers,
        ServiceCategory=ServiceCategory,
        cats=cat_count, subs=sub_count, 
        act_c=act_cust, inact_c=inact_cust, 
        act_p=act_prov, inact_p=inact_prov, 
        reqs=req_count, 
        stat_chart=stat_chart, 
        prov_chart=prov_chart, 
        cust_chart=cust_chart, 
        sub_chart=sub_chart,
        service_requests = service_requests
    )

@app1.route('/download/<filename>')
def download_file(filename):
    try:
        # Assuming files are stored in a directory called 'uploads'
        return send_from_directory('uploads', filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app1.route("/flag_customer/<int:customer_id>", methods=["POST"])
def flag_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer.active = False
    db.session.commit()
    return redirect(url_for("main.admin_home"))


@app1.route("/unflag_customer/<int:customer_id>", methods=["POST"])
def unflag_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer.active = True
    db.session.commit()
    return redirect(url_for("main.admin_home"))


@app1.route("/flag_provider/<int:provider_id>", methods=["POST"])
def flag_provider(provider_id):
    p = Provider.query.get_or_404(provider_id)
    p.active = False
    db.session.commit()
    return redirect(url_for("main.admin_home"))


@app1.route("/unflag_provider/<int:provider_id>", methods=["POST"])
def unflag_provider(provider_id):
    p = Provider.query.get_or_404(provider_id)
    p.active = True
    db.session.commit()
    return redirect(url_for("main.admin_home"))

@app1.route("/flag_request/<int:request_id>", methods=["POST"])
def flag_request(request_id):
    p = ServiceRequest.query.get_or_404(request_id)
    p.active = False
    db.session.commit()
    return redirect(url_for("main.admin_home"))

@app1.route("/unflag_request/<int:request_id>", methods=["POST"])
def unflag_request(request_id):
    p = ServiceRequest.query.get_or_404(request_id)
    p.active = True
    db.session.commit()
    return redirect(url_for("main.admin_home"))


@app1.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        exist1 = None
        exist1=Customer.query.filter_by(email=email, password=password).first()
        exist2 = None
        exist2 = Provider.query.filter_by(email=email, password=password).first()
        if not exist1 and not exist2:
            flash("Invalid Credentials")
            return redirect(url_for("main.login"))
        
        if exist1:
            session["cust_id"] = exist1.id
            session["cust_name"]=exist1.name
            return redirect(url_for("main.cust_home"))
        if exist2:
            session["prov_id"] = exist2.id
            session["prov_name"]=exist2.name
            return redirect(url_for("main.prov_home"))
    return render_template("user_login.html")

@app1.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.home')) 

@app1.route("/customer", methods=["GET", "POST"])
def customer():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        contact=request.form['contact']
        pincode=request.form['pincode']
        address=request.form['address']
        exist=Customer.query.filter_by(email=email).first()
        exist1 = Provider.query.filter_by(email=email).first()
        if exist or exist1:
            flash("Customer with this email exists!")
            return redirect(url_for("main.customer"))

        new=Customer(name=name, email=email, password=password, contact=contact, pincode=pincode, address=address)
        db.session.add(new)
        db.session.commit()
        flash("You are now registered! Login to continue")
        return redirect(url_for('main.login'))
    return render_template("cust_regis.html")



@app1.route("/professional", methods=["GET","POST"])
def provider():
    categories = ServiceCategory.query.all()
    # services = ServiceSubtype.query.all()
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        contact=request.form['contact']
        category=request.form['category']
        experience=request.form['exp']
        pincode=request.form['pincode']
        address=request.form['address']
        subtype_id = request.form['subtype']
        exist=Provider.query.filter_by(email=email).first()
        exist1=Customer.query.filter_by(email=email).first()
        if exist or exist1:
            flash("User with this email exists!")
            return redirect(url_for("main.provider"))
        
        if 'filename' not in request.files:
            return 'No file Selected',400
        file = request.files['filename']

        if file.filename == '':
            return 'No file Selected', 400
        
        if file:
            filename=secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD'],filename)
            file.save(file_path)

        new = Provider(
            name=name, email=email, password=password, category=category,
            experience=experience, pincode=pincode, address=address,
            filename=filename, file_path=file_path, subtype_id=subtype_id, contact = contact
        )
        db.session.add(new)
        db.session.commit()
        flash("You are now registered! Login to continue")
        redirect(url_for('main.provider'))
        return redirect(url_for('main.login'))
    
    return render_template("prov_regis.html", categories = categories)

@app1.route("/get_subtypes/<category_id>")
def get_subtypes(category_id):
    subtypes = ServiceSubtype.query.filter_by(category_id=category_id).all()
    subtypes_list = [
        {"id": subtype.id, "name": subtype.name.capitalize(), "base_price": subtype.base_price}
        for subtype in subtypes
    ]
    return jsonify(subtypes_list)


@app1.route('/cust_home', methods=['GET', 'POST'])
def cust_home():
    if 'cust_id' not in session:
        return "Not Signed In"
    
    customer = Customer.query.filter_by(id=session['cust_id']).first()

    # Handle profile update form submission
    if request.method == 'POST' and "profileForm" in request.form:
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.contact = request.form['contact']
        customer.pincode = request.form['pincode']
        customer.address = request.form['address']
        
        password = request.form['password']
        if password:
            customer.password = password
        session['cust_name'] = customer.name
        db.session.commit()

    # Retrieve all categories, subtypes, and professionals
    categories = ServiceCategory.query.all()
    sc = ServiceSubtype.query.all()
    professionals = Provider.query.all()

    # Map ServiceRequest with Provider
    service_requests = ServiceRequest.query.filter_by(customer_id=session['cust_id']).order_by(desc(ServiceRequest.date_of_request)).all()


    mapped_requests = [
        (
            req,
            provider := Provider.query.filter_by(id=req.provider_id).first(),
            subtype := ServiceSubtype.query.filter_by(id=provider.subtype_id).first() if provider else None,
            subtype.base_price if subtype else None
        )
        for req in service_requests
    ]

    def status_chart():
        try:
            status_counts = db.session.query(ServiceRequest.status, func.count(ServiceRequest.status)).filter_by(customer_id=customer.id).group_by(ServiceRequest.status).all()
            statuses, counts = zip(*status_counts)

            fig, ax = plt.subplots()
            ax.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close(fig)
            return base64.b64encode(img.getvalue()).decode('utf8')
        except ValueError:
            return None  # No data to plot

    def requests_over_time_chart():
        try:
            requests_over_time = db.session.query(
                extract('month', ServiceRequest.date_of_request).label('month'),
                func.count(ServiceRequest.id)
            ).filter_by(customer_id=customer.id).group_by('month').all()

            months, counts = zip(*requests_over_time)
            month_labels = [datetime(2024, month, 1).strftime('%b') for month in months]

            fig, ax = plt.subplots()
            ax.bar(month_labels, counts, color='skyblue')
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Requests')
            ax.set_title('Service Requests Over Time')

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close(fig)
            return base64.b64encode(img.getvalue()).decode('utf8')
        except ValueError:
            return None

    # Generate charts
    graph1 = status_chart()
    graph2 = requests_over_time_chart()

    # Get statistics
    total_requests = ServiceRequest.query.filter_by(customer_id=customer.id).count()
    unique_services = db.session.query(ServiceRequest.subtype_id).filter_by(customer_id=customer.id).distinct().count()
    pending_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='requested').count()
    active_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='assigned').count()
    finished_requests = ServiceRequest.query.filter(ServiceRequest.customer_id == customer.id, ServiceRequest.status.in_(['closed', 'completed'])).count()


    # Initialize providers for search results
    providers = []

    # Handle search form submission
    if request.method == 'POST' and not "profileForm" in request.form:
        # Fetch search criteria from form inputs
        name = request.form.get('name')
        category = request.form.get('category')
        subtype = request.form.get('subtype')
        contact = request.form.get('contact')
        min_rating = request.form.get('min_rating')
        min_experience = request.form.get('min_experience')

        # Build the query dynamically based on inputs
        query = Provider.query
        if name:
            query = query.filter(Provider.name.ilike(f"%{name}%"))
        if category:
            query = query.join(ServiceSubtype, Provider.subtype_id == ServiceSubtype.id) \
                         .join(ServiceCategory, ServiceSubtype.category_id == ServiceCategory.id) \
                         .filter(ServiceCategory.id == int(category))
        if subtype:
            query = query.join(ServiceSubtype).filter(ServiceSubtype.id == int(subtype))
        if contact:
            query = query.filter(Provider.contact.ilike(f"%{contact}%"))
        if min_rating:
            query = query.filter(Provider.rating >= float(min_rating))
        if min_experience:
            query = query.filter(Provider.experience >= int(min_experience))

        # Execute the query and fetch results
        providers = query.all()
    today = datetime.today()
    # Render the template with all necessary data
    return render_template(
        "cust_home.html", 
        customer=customer, 
        categories=categories, 
        subtype=sc, 
        provider=professionals, 
        service_requests=mapped_requests,
        ServiceRequest=ServiceRequest,
        providers=providers,
        total_requests=total_requests,
        unique_services=unique_services,
        pending_requests=pending_requests,
        active_requests=active_requests,
        finished_requests=finished_requests,
        g1=graph1,
        g2=graph2, today=today
    )




@app1.route('/book_service/<int:provider_id>', methods=['POST'])
def book_service(provider_id):
    customer_id = session['cust_id']
    subtype_id = request.args.get('subtype_id', type=int)
    doc = request.form.get('date_of_completion')
    remark = request.form['remark']
    date_of_completion = datetime.strptime(doc, '%Y-%m-%d').date() if doc else None
    existing_request = ServiceRequest.query.filter_by(
        provider_id=provider_id, customer_id=customer_id, status='requested'
    ).first()

    if existing_request:
        return redirect(url_for('main.cust_home'))

    new_request = ServiceRequest(
        provider_id=provider_id,
        customer_id=customer_id,
        subtype_id=subtype_id,
        status='requested',
        date_of_completion = date_of_completion,
        remarks = remark
    )
    db.session.add(new_request)
    db.session.commit()

    return redirect(url_for('main.cust_home'))

@app1.route('/delete_service_request/<int:request_id>', methods=['POST'])
def delete_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if service_request:
        db.session.delete(service_request)
        db.session.commit()
    return redirect(url_for('main.cust_home'))

@app1.route('/change_request_date/<int:request_id>', methods=['POST'])
def change_request_date(request_id):
    new_date = request.form.get('requested_date')
    date_of_completion = datetime.strptime(new_date, '%Y-%m-%d').date()
    rem = request.form.get('remarks')
    service_request = ServiceRequest.query.get(request_id)
    if service_request:
        service_request.date_of_completion = date_of_completion
        service_request.remarks = rem
        db.session.commit()
    return redirect(url_for('main.cust_home'))




@app1.route('/prov_home', methods=['GET', 'POST'])
def prov_home():
    if 'prov_id' not in session:
        return "Not Signed In"

    provider = Provider.query.filter_by(id=session['prov_id']).first()
    service_req = ServiceRequest.query.filter_by(provider_id=session['prov_id']).order_by(desc(ServiceRequest.date_of_request)).all()

    mapped_requests = [
        (
            service, 
            Customer.query.filter_by(id=service.customer_id).first(), 
            Review.query.filter_by(service_request_id=service.id).first()
        )
        for service in service_req
    ]
    if request.method == 'POST' and "profileForm" in request.form:
        provider.name = request.form['name']
        provider.email = request.form['email']
        provider.contact = request.form['contact']
        provider.experience = request.form['exp']
        provider.pincode = request.form['pincode']
        provider.address = request.form['address']
        
        password = request.form['password']
        if password:
            provider.password = password
        session['prov_name'] = provider.name
        db.session.commit()
    total_requests = ServiceRequest.query.filter_by(provider_id=provider.id).count()
    unique_customers = db.session.query(ServiceRequest.customer_id).filter_by(provider_id=provider.id).distinct().count()
    pending_requests = ServiceRequest.query.filter_by(provider_id=provider.id, status='requested').count()
    active_requests = ServiceRequest.query.filter_by(provider_id=provider.id, status='assigned').count()
    finished_requests = ServiceRequest.query.filter_by(provider_id=provider.id, status='closed').count()
    account_balance = provider.balance 
    rating = provider.rating

    def status_chart():
        status_counts = db.session.query(ServiceRequest.status, func.count(ServiceRequest.status)) \
            .filter_by(provider_id=provider.id) \
            .group_by(ServiceRequest.status) \
            .all()

        if status_counts:
            statuses, counts = zip(*status_counts)
            fig, ax = plt.subplots()
            ax.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        else:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.axis('off')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close(fig)
        return base64.b64encode(img.getvalue()).decode('utf8')

    # Bar chart: Completed services over time
    def service_status_chart(provider_id):
        # Query to get counts of services grouped by status
        status_counts = db.session.query(
            ServiceRequest.status, 
            func.count(ServiceRequest.id)
        ).filter(ServiceRequest.provider_id == provider_id).group_by(ServiceRequest.status).all()

        # Extract statuses and counts
        statuses, counts = zip(*status_counts) if status_counts else ([], [])
        
        fig, ax = plt.subplots()
        ax.bar(statuses, counts, color='skyblue')
        ax.set_xlabel('Service Status')
        ax.set_ylabel('Number of Requests')
        ax.set_title('Service Requests by Status')
        
        # Save the plot as a base64-encoded image
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close(fig)
        return base64.b64encode(img.getvalue()).decode('utf8')



    # Generate the charts
    status_pie_chart = status_chart()
    service_status_bar_chart =service_status_chart(provider.id)



    results = []
    if request.method == 'POST' and "profileForm" not in request.form:
        name = request.form.get('name', '')
        status = request.form.get('status', '')
        date = request.form.get('date', '')
        addr = request.form.get('address', '')
        contact = request.form.get('contact','')
        # Query customers and services based on the filters
        query = db.session.query(Customer, ServiceRequest).join(ServiceRequest, Customer.id == ServiceRequest.customer_id)
        query = query.filter(ServiceRequest.provider_id == session['prov_id'])
        if name:
            query = query.filter(Customer.name.ilike(f"%{name}%"))
        if addr:
            query = query.filter(Customer.address.ilike(f"%{addr}%"))
        if contact:
            query = query.filter(Customer.contact.ilike(f"%{contact}%"))
        if status:
            query = query.filter(ServiceRequest.status == status)
        if date:
            query = query.filter(func.date(ServiceRequest.date_of_completion) == date)
        results = query.all()
    
    current_date = datetime.today()
    return render_template("prov_home.html", provider=provider, services=mapped_requests, customers=results,total_requests=total_requests,
        unique_customers=unique_customers,
        pending_requests=pending_requests,
        active_requests=active_requests,
        finished_requests=finished_requests,
        account_balance=account_balance,
        rating=rating,
        status_pie_chart=status_pie_chart,
        service_status_chart = service_status_bar_chart,
        today = current_date
    )


@app1.route('/delete/<int:service_id>', methods=['GET', 'POST'])
def deleteServ(service_id):
    service = ServiceCategory.query.get_or_404(service_id)
    
    subtypes = ServiceSubtype.query.filter_by(category_id=service.id).all()

    for subtype in subtypes:
        service_requests = ServiceRequest.query.filter_by(subtype_id=subtype.id).all()
        for request in service_requests:
            reviews = Review.query.filter_by(service_request_id=request.id).all()
            for review in reviews:
                db.session.delete(review)
            
            db.session.delete(request)
        
        providers = Provider.query.filter_by(subtype_id=subtype.id).all()
        for provider in providers:
            db.session.delete(provider)
        db.session.delete(subtype)
    db.session.delete(service)

    db.session.commit()

    return redirect(url_for('main.admin_home'))


@app1.route("/delete_subtype/<int:subtype_id>", methods=["POST"])
def deleteSubtype(subtype_id):
    subtype = ServiceSubtype.query.get(subtype_id)
    if subtype:
        service_requests = ServiceRequest.query.filter_by(subtype_id=subtype.id).all()
        for request in service_requests:
            reviews = Review.query.filter_by(service_request_id=request.id).all()
            for review in reviews:
                db.session.delete(review)
            db.session.delete(request)

        providers = Provider.query.filter_by(subtype_id=subtype.id).all()
        for provider in providers:
            db.session.delete(provider)
        db.session.delete(subtype)
        db.session.commit()

    return redirect(url_for("main.admin_home"))


@app1.route('/accept_request/<int:request_id>', methods=['POST'])
def accept_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'assigned'  # Update status to assigned
    db.session.commit()
    return redirect(url_for('main.prov_home'))

@app1.route('/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'rejected'  # Update status to closed
    db.session.commit()
    return redirect(url_for('main.prov_home'))

@app1.route('/completed_request/<int:request_id>', methods=['POST'])
def completed_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'completed'  # Update status to closed
    db.session.commit()
    return redirect(url_for('main.prov_home'))

@app1.route('/close_pay/<int:request_id>', methods=['POST'])
def close_pay(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    print('hi')
    print(service_request) 
    print(service_request.remarks) 
    if service_request.status == 'completed':
        rating = request.form.get('rating')
        review_text = request.form.get('review', '').strip()
        review = Review(
            service_request_id=request_id,
            customer_id=service_request.customer_id,
     
            provider_id=service_request.provider_id,
            rating=int(rating),
            comment=review_text, 
        )
        db.session.add(review)
        
        provider = Provider.query.get(service_request.provider_id)
        if provider:
            # Calculate the new rating (average of all reviews)
            reviews = Review.query.filter_by(provider_id=provider.id).all()
            total_rating = sum([r.rating for r in reviews])
            provider.rating = total_rating / len(reviews) if reviews else 0
            db.session.commit()
        
        provider_balance_update = ServiceSubtype.query.get(service_request.subtype_id)
        if provider_balance_update:
            provider.balance += provider_balance_update.base_price  # Add base price to balance
            db.session.commit()
        
        service_request.status = 'closed'
        db.session.commit()
    
    return redirect(url_for('main.cust_home'))

@app1.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    service = ServiceSubtype.query.get_or_404(service_id)

    if request.method == 'POST':
        service.name = request.form['service_name']
        service.description = request.form['description']
        service.base_price = request.form['price']
        db.session.commit()
        return redirect(url_for('main.admin_home'))
    