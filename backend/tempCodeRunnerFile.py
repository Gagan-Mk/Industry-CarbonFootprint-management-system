import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, abort
import mysql.connector
from werkzeug.security import generate_password_hash
from functools import wraps
from flask import jsonify
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE'] = 'icfms'  # Your database name
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'maitreya'  # Your MySQL password


# Create a connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        database=app.config['MYSQL_DATABASE'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD']
    )
    return connection

# Role-based access control
def role_required(*roles):
    """Decorator to restrict access based on roles."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not hasattr(g, 'role') or g.role not in roles:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return wrapped
    return decorator


@app.before_request
def load_user_data():
    """Load the user's role and ID into the global g object."""
    if 'username' in session:
        g.username = session['username']  # Use session['username']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch the user's role_id directly from the USER table using username
        cursor.execute("SELECT role_id FROM USER WHERE username = %s", (g.username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            g.role_id = user['role_id']
            
            # Role mapping
            role_mapping = {
                1: 'Admin',
                2: 'Industry Manager',
                3: 'Auditor'
            }
            
            g.role = role_mapping.get(g.role_id, 'Unknown')
        else:
            g.role = None
    else:
        g.role = None
        g.username = None
        
# @app.before_request
# def load_user_role():
#     """Load the user's role into the global `g` object."""
#     if 'user_id' in session:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT role FROM Users WHERE user_id = %s", (session['user_id'],))
#         user = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if user:
#             g.role = user['role']
#         else:
#             g.role = None
#     else:
#         g.role = None



# Route for the home page (show the form)
@app.route('/')
def home():
    return render_template('home.html') 
# index page 
@app.route('/index')
def index():
    return render_template('index.html') 
@app.route('/signup')
def signup():
    return render_template('signup.html')  # Ensure you have a signup.html in your templates

# @app.route('/admin_login')
# def admin_login():
#     return render_template('admin_login.html')  # Example admin login route

# @app.route('/auditor_signup')
# def auditor_signup():
#     return render_template('auditor_signup.html') # Example auditor signup route

@app.route('/carbon')
def carbon():
    return render_template('carbon.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/trans.html')
def trans():
    return render_template('trans.html')

@app.route('/emission_s')
def emission_s():
    return render_template('emission_s.html')

@app.route('/industry')
def industry():
    return render_template('industry.html')
    

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    session.pop('role_id', None)    # Remove the role_id from the session
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))  # Redirect back to home page


# Route for handling industry regs
@app.route('/add_industry', methods=['POST'])
def add_industry():
    industry_name = request.form['industry_name']
    location = request.form['location']
    industry_type = request.form['industry_type']

    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert data into Industries table
    try:
        query = """
        INSERT INTO Industries (industry_name, location, industry_type) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (industry_name, location, industry_type))
        connection.commit()
        flash("Industry data has been successfully added.", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

    return render_template('index.html')




# Route to add a new process
@app.route('/add_process', methods=['POST'])
def add_process():
    # Retrieve form data
    process_name = request.form.get('process_name')
    energy_consumption = request.form.get('energy_consumption')
    emission_factor = request.form.get('emission_factor')
    industry_id = request.form.get('industry_id')

    # Insert into the Process table
    query = """
        INSERT INTO Process (process_name, energy_consumption, emission_factor, industry_id)
        VALUES (%s, %s, %s, %s)
    """
    values = (process_name, energy_consumption, emission_factor, industry_id)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        # Return a success message
        return jsonify(message="Process added successfully!"), 200
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify(error=str(err)), 500
    finally:
        cursor.close()
        connection.close()



# inserting transportation details 
@app.route('/add_transportation', methods=['POST'])
@role_required('Admin', 'Industry Manager')  # Ensure the user has permission
def add_transportation():
    # Get form data
    vehicle_type = request.form['vehicle_type']
    distance_travelled = request.form['distance_travelled']
    fuel_consumption = request.form['fuel_consumption']

    try:
        # Get the logged-in user's industry_id
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT industry_id FROM USER WHERE username = %s", (g.username,))
        user_data = cursor.fetchone()

        if not user_data or not user_data['industry_id']:
            flash("You are not assigned to any industry.", "warning")
            return jsonify({"message": "You are not assigned to any industry."}), 400

        industry_id = user_data['industry_id']  # Get the industry_id for the logged-in user

        # Insert data into the Transportation table
        query = """
        INSERT INTO Transportation (vehicle_type, distance_travelled, fuel_consumption, industry_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (vehicle_type, distance_travelled, fuel_consumption, industry_id))
        connection.commit()
        flash("Transportation data has been successfully added.", "success")

        # Return a success message
        return render_template('index.html')

    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
        connection.rollback()
        return jsonify({"message": f"Error adding transportation data: {err}"}), 500

    finally:
        cursor.close()
        connection.close()
        




import datetime  # Import datetime module

@app.route('/add_carbon_offset', methods=['POST'])
def add_carbon_offset():
    provider_details = request.form['provider_details']  # Provider details
    offset_type = request.form['offset_type']
    offset_quantity = request.form['offset_quantity']
    date_purchased = request.form['date_purchased']  # Date purchased (from form)

    username = session.get('username')  # Get username from session

    if not username:
        return jsonify({"error": "User is not logged in!"}), 403

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch `industry_id` from the database using the username
    cursor.execute("SELECT industry_id FROM User WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if not user_data or not user_data['industry_id']:
        return jsonify({"error": "Industry ID not found for the user!"}), 404

    industry_id = user_data['industry_id']  # Extract industry_id

    # Debug: Log or print the `industry_id` value
    print(f"Debug: Retrieved industry_id = {industry_id}")
    # Alternatively, you can use logging
    app.logger.debug(f"Retrieved industry_id = {industry_id}")

    # Default `date_purchased` to NOW() if not provided
    if not date_purchased:
        date_purchased = datetime.datetime.now().strftime('%Y-%m-%d')

    # Insert data into the `Carbon_Offsets` table
    try:
        query = """
        INSERT INTO Carbon_Offsets (offset_type, amount_offset, provider_details, date_purchased, industry_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (offset_type, offset_quantity, provider_details, date_purchased, industry_id))
        connection.commit()
        flash("Carbon offset data has been successfully added.", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

    return render_template('index.html')



# Route to handle emission source form submission
@app.route('/add_emission_source', methods=['GET', 'POST'])
def add_emission_source():
    username = session.get('username')  # Fetch username from session

    if not username:
        flash("User is not logged in!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            # Retrieve form data
            source_type = request.form['source_type']
            emission_value = request.form['emission_value']

            # Fetch the user's industry_id from the User table
            cursor.execute("SELECT industry_id FROM User WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user or not user['industry_id']:
                flash("Industry ID not found for the logged-in user!", "danger")
                return redirect(url_for('index'))

            industry_id = user['industry_id']  # Extract industry_id

            # Insert the emission source with the provided data
            insert_query = """
            INSERT INTO Emission_Sources (source_type, emission_value, industry_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (source_type, emission_value, industry_id))
            conn.commit()

            flash("Emission source added successfully!", "success")
            return redirect(url_for('index'))

        # If the request method is GET, just render the form
        return render_template('add_emission_source.html')

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))


# Route to render the industry manager registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        industry_name = request.form['industry_name']
        industry_address = request.form['industry_address']
        industry_type = request.form['industry_type']
        industry_contact = request.form['industry_contact']
        manager_name = request.form['manager_name']
        manager_email = request.form['manager_email']
        manager_phone = request.form['manager_phone']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('index'))

        # Hash the password
        # hashed_password = generate_password_hash(password)

        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert industry details
            industry_query = """
                INSERT INTO Industries (industry_name, location, industry_type)
                VALUES (%s, %s, %s)
            """
            cursor.execute(industry_query, (industry_name, industry_address, industry_type))
            industry_id = cursor.lastrowid  # Get the industry_id of the newly inserted industry

            # Insert user details with manager role (assuming role_id 2 is for 'Industry Manager')
            user_query = """
                INSERT INTO USER (username, email, password, role_id, industry_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(user_query, (username, manager_email, password, 2, industry_id))

            # Commit the changes
            conn.commit()

            flash("User registered successfully!", "success")
            return redirect(url_for('home'))

        except mysql.connector.Error as err:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {err}", "danger")
            return redirect(url_for('home'))

        finally:
            # Close the database connection
            cursor.close()
            conn.close()

    # If request method is GET, render the registration form
    return render_template('index.html')



# login-in 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']  # Get the role_id from the form

        # Debugging: print values to console
        print(f"Username: {username}, Password: {password}, Role ID: {role_id}")

        # Get the database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to check the user in the database
        cursor.execute("SELECT * FROM USER WHERE username = %s AND role_id = %s", (username, role_id))
        user = cursor.fetchone()

        # Debugging: check the result
        print(f"User from database: {user}")

        # Validate the password (if found)
        if user and user[3] == password:  # Assuming user[3] is the password field
            session['username'] = username  # Store username in session
            session['role_id'] = role_id    # Store role_id in session
            session.permanent = True 
            print(f"Session user_id set: {session.get('user_id')}")  # Debugging line
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         role_id = request.form['role_id']

#         connection = get_db_connection()
#         cursor = connection.cursor()

#         cursor.execute("SELECT * FROM USER WHERE username = %s AND role_id = %s", (username, role_id))
#         user = cursor.fetchone()

#         if user and user[3] == password:  # Assuming user[3] is the password field
#             session['username'] = username
#             session['role_id'] = role_id
#             session['user_id'] = user[0]  # Store user_id in session for further reference
#             session['industry_id'] = user[5]  # Assuming user[5] is the industry_id

#             flash('Login successful!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid username or password', 'danger')
#             return redirect(url_for('login'))

#     return render_template('login.html')





# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('admin_login'))

        # Hash the password before saving it (use a library like werkzeug.security)
        # hashed_password = generate_password_hash(password)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert the new admin user
            query = """
            INSERT INTO USER (username, email, password, role_id, industry_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            role_id = 1  # Assuming '1' is for admin
            industry_id = None  # Use None for NULL in SQL

            cursor.execute(query, (username, email, password, role_id, industry_id))
            connection.commit()

            flash("Admin account created successfully!", "success")
            return redirect(url_for('home'))  # Redirect to home page

        except mysql.connector.Error as err:
            connection.rollback()  # Rollback in case of error
            flash(f"Error: {err}", "danger")
            return redirect(url_for('admin_login'))

        finally:
            cursor.close()
            connection.close()

    return render_template('admin_login.html')  # Render the signup form template


# Auditor signip

@app.route('/auditor_signup', methods=['GET', 'POST'])
def auditor_signup():
    if request.method == 'POST':
        username = request.form['username']
        auditor_email = request.form['auditor_email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('auditor_signup'))

        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch role_id for 'Auditor'
            cursor.execute("SELECT role_id FROM ROLE WHERE role_name = 'Auditor'")
            role = cursor.fetchone()
            if not role:
                flash("Role 'Auditor' not found in the database!", "danger")
                return redirect(url_for('auditor_signup'))
            role_id = role[0]  # Extract the role_id value
            
            # Fetch an industry_id (you can adapt this based on form input if necessary)
            industry_id = None  # Set to None if you don't need an industry association
            cursor.execute("SELECT industry_id FROM Industries LIMIT 1")  # Example: Get first industry
            industry = cursor.fetchone()
            if industry:
                industry_id = industry[0]

            # Insert auditor data into the USER table
            query = """
            INSERT INTO USER (username, email, password, role_id, industry_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, auditor_email, password, role_id, industry_id))
            connection.commit()

            flash("Auditor registered successfully!", "success")
            return redirect(url_for('home'))

        except mysql.connector.Error as err:
            connection.rollback()  # Rollback transaction on error
            flash(f"Database error: {err}", "danger")
            return redirect(url_for('auditor_signup'))

        finally:
            cursor.close()
            connection.close()

    return render_template('auditor_signup.html')



# to view industry 

# rectriced view only 
@app.route('/view_industries', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')
def view_industries():
    print(f"User Role: {g.role}")  # Add this line for debugging

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Role-based filtering
        if g.role == 'Industry Manager':
            # Fetch the logged-in user's industry_id from the USER table using username
            cursor.execute("SELECT industry_id FROM USER WHERE username = %s", (g.username,))
            user_data = cursor.fetchone()
            print(f"Fetched User Data: {user_data}")

            if user_data and user_data['industry_id']:
                # Fetch details for the user's assigned industry
                assigned_industry_id = user_data['industry_id']
                cursor.execute("SELECT * FROM Industries WHERE industry_id = %s", (assigned_industry_id,))
            else:
                flash("You are not assigned to any industry.", "warning")
                industries = []
                return render_template('view_industries.html', industries=industries)

        elif g.role == 'Admin':
            # Admin can view all industries
            cursor.execute("SELECT * FROM Industries")
        
        elif g.role == 'Auditor':
            # Admin can view all industries
            cursor.execute("SELECT * FROM Industries")
            
        industries = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        industries = []

    finally:
        cursor.close()
        connection.close()

    return render_template('view_industries.html', industries=industries)



# to delete
@app.route('/delete_industry/<int:industry_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')
def delete_industry(industry_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Restrict Industry Managers to only their assigned industry
        if g.role == 'Industry Manager':
            cursor.execute("""
                SELECT * 
                FROM Industries 
                WHERE industry_id = %s AND manager_id = %s
            """, (industry_id, g.username))
        elif g.role == 'Admin':
            cursor.execute("SELECT * FROM Industries WHERE industry_id = %s", (industry_id,))
        
        industry = cursor.fetchone()

        if not industry:
            flash("You do not have permission to delete this industry or it doesn't exist.", "danger")
            return redirect(url_for('view_industries'))
    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        return redirect(url_for('view_industries'))
    finally:
        cursor.close()
        connection.close()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Industries WHERE industry_id = %s", (industry_id,))
        connection.commit()
        flash("Industry deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error deleting industry: {err}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_industries'))

# to update
from flask import render_template, request, redirect, url_for, flash
import mysql.connector

@app.route('/update_industry/<int:industry_id>', methods=['GET', 'POST'])
def update_industry(industry_id):
    # Database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'GET':
        # Fetch the current details of the industry
        cursor.execute("SELECT * FROM Industries WHERE industry_id = %s", (industry_id,))
        industry = cursor.fetchone()

        if industry is None:
            flash("Industry not found!", 'danger')
            return redirect(url_for('view_industries'))

        # Render the template with the current industry details in the form
        return render_template('update_industry.html', industry=industry)

    elif request.method == 'POST':
        # Safely get form data with .get() to avoid KeyError
        industry_name = request.form.get('industry_name')
        location = request.form.get('location')
        industry_type = request.form.get('industry_type')

        # Validate the inputs
        if not industry_name or not location or not industry_type:
            flash("All fields are required.", 'danger')
            return redirect(url_for('update_industry', industry_id=industry_id))

        try:
            # Update the industry in the database
            cursor.execute("""
                UPDATE Industries
                SET industry_name = %s, location = %s, industry_type = %s
                WHERE industry_id = %s
            """, (industry_name, location, industry_type, industry_id))

            connection.commit()

            flash("Industry updated successfully!", 'success')
            return redirect(url_for('view_industries'))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
            return redirect(url_for('update_industry', industry_id=industry_id))

        finally:
            cursor.close()
            connection.close()


# process view
@app.route('/view_processes', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')
def view_processes():
    print(f"User Role: {g.role}")  # Debugging: Print the user's role

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Role-based filtering
        if g.role == 'Industry Manager':
            # Fetch the logged-in user's industry_id from the USER table using username
            cursor.execute("SELECT industry_id FROM USER WHERE username = %s", (g.username,))
            user_data = cursor.fetchone()
            print(f"Fetched User Data: {user_data}")

            if user_data and user_data['industry_id']:
                # Fetch details for the user's assigned industry
                assigned_industry_id = user_data['industry_id']
                query = """
                    SELECT p.process_id, p.process_name, p.energy_consumption, p.emission_factor, i.industry_name
                    FROM Process p
                    JOIN Industries i ON p.industry_id = i.industry_id
                    WHERE p.industry_id = %s
                """
                cursor.execute(query, (assigned_industry_id,))
            else:
                flash("You are not assigned to any industry.", "warning")
                processes = []
                return render_template('view_processes.html', processes=processes)

        elif g.role == 'Admin':
            # Admin can view all processes
            query = """
                SELECT p.process_id, p.process_name, p.energy_consumption, p.emission_factor, i.industry_name
                FROM Process p
                LEFT JOIN Industries i ON p.industry_id = i.industry_id
            """
            cursor.execute(query)
        
        elif g.role == 'Auditor':
            # Admin can view all processes
            query = """
                SELECT p.process_id, p.process_name, p.energy_consumption, p.emission_factor, i.industry_name
                FROM Process p
                LEFT JOIN Industries i ON p.industry_id = i.industry_id
            """
            cursor.execute(query)

        processes = cursor.fetchall()

        print(f"Fetched Processes: {processes}")  # Debugging: Print the fetched processes

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        processes = []

    finally:
        cursor.close()
        connection.close()

    return render_template('view_processes.html', processes=processes)

# delete process
@app.route('/delete_process/<int:process_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')
def delete_process(process_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Restrict Industry Managers to only their assigned processes
        if g.role == 'Industry Manager':
            cursor.execute("""
                SELECT * 
                FROM Processes 
                WHERE process_id = %s AND industry_id = (SELECT industry_id FROM USER WHERE username = %s)
            """, (process_id, g.username))
        elif g.role == 'Admin':
            cursor.execute("SELECT * FROM Processes WHERE process_id = %s", (process_id,))
        
        process = cursor.fetchone()

        if not process:
            flash("You do not have permission to delete this process or it doesn't exist.", "danger")
            return redirect(url_for('view_processes'))
    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        return redirect(url_for('view_processes'))
    finally:
        cursor.close()
        connection.close()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Processes WHERE process_id = %s", (process_id,))
        connection.commit()
        flash("Process deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error deleting process: {err}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_processes'))

# update
@app.route('/update_process/<int:process_id>', methods=['GET', 'POST'])
@role_required('Admin', 'Industry Manager')
def update_process(process_id):
    # Database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'GET':
        # Fetch the current details of the process
        cursor.execute("SELECT * FROM Process WHERE process_id = %s", (process_id,))
        process = cursor.fetchone()

        if process is None:
            flash("Process not found!", 'danger')
            return redirect(url_for('view_processes'))

        # Render the template with the current process details in the form
        return render_template('update_process.html', process=process)

    elif request.method == 'POST':
        # Safely get form data with .get() to avoid KeyError
        process_name = request.form.get('process_name')
        energy_consumption = request.form.get('energy_consumption')
        emission_factor = request.form.get('emission_factor')

        # Validate the inputs
        if not process_name or not energy_consumption or not emission_factor:
            flash("All fields are required.", 'danger')
            return redirect(url_for('update_process', process_id=process_id))

        try:
            # Update the process in the database
            cursor.execute("""
                UPDATE Process
                SET process_name = %s, energy_consumption = %s, emission_factor = %s
                WHERE process_id = %s
            """, (profcess_name, energy_consumption, emission_factor, process_id))

            connection.commit()

            flash("Process updated successfully!", 'success')
            return redirect(url_for('view_processes'))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
            return redirect(url_for('update_process', process_id=process_id))

        finally:
            cursor.close()
            connection.close()
    
    
# View carbon offsets
@app.route('/view_carbon_offsets', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')
def view_carbon_offsets():
    print(f"User Role: {g.role}")  # Debugging: Print the user's role

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Role-based filtering
        if g.role == 'Industry Manager':
            # Fetch the logged-in user's industry_id from the USER table using username
            cursor.execute("SELECT industry_id FROM USER WHERE username = %s", (g.username,))
            user_data = cursor.fetchone()
            print(f"Fetched User Data: {user_data}")

            if user_data and user_data['industry_id']:
                # Fetch details for the user's assigned industry
                assigned_industry_id = user_data['industry_id']
                query = """
                    SELECT co.offset_id, co.offset_type, co.amount_offset, co.date_purchased, co.provider_details, i.industry_name
                    FROM Carbon_Offsets co
                    JOIN Industries i ON co.industry_id = i.industry_id
                    WHERE co.industry_id = %s
                """
                cursor.execute(query, (assigned_industry_id,))
            else:
                flash("You are not assigned to any industry.", "warning")
                carbon_offsets = []
                return render_template('view_carbon_offsets.html', carbon_offsets=carbon_offsets)

        elif g.role == 'Admin':
            # Admin can view all carbon offsets
            query = """
                SELECT co.offset_id, co.offset_type, co.amount_offset, co.date_purchased, co.provider_details, i.industry_name
                FROM Carbon_Offsets co
                LEFT JOIN Industries i ON co.industry_id = i.industry_id
            """
            cursor.execute(query)
            
        elif g.role == 'Auditor':
            # Admin can view all carbon offsets
            query = """
                SELECT co.offset_id, co.offset_type, co.amount_offset, co.date_purchased, co.provider_details, i.industry_name
                FROM Carbon_Offsets co
                LEFT JOIN Industries i ON co.industry_id = i.industry_id
            """
            cursor.execute(query)

        carbon_offsets = cursor.fetchall()

        print(f"Fetched Carbon Offsets: {carbon_offsets}")  # Debugging: Print the fetched offsets

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        carbon_offsets = []

    finally:
        cursor.close()
        connection.close()

    return render_template('view_carbon_offsets.html', carbon_offsets=carbon_offsets)


# Delete carbon offset
@app.route('/delete_carbon_offset/<int:offset_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')
def delete_carbon_offset(offset_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Restrict Industry Managers to only their assigned carbon offsets
        if g.role == 'Industry Manager':
            cursor.execute("""
                SELECT * 
                FROM Carbon_Offsets 
                WHERE offset_id = %s AND industry_id = (SELECT industry_id FROM USER WHERE username = %s)
            """, (offset_id, g.username))
        elif g.role == 'Admin':
            cursor.execute("SELECT * FROM Carbon_Offsets WHERE offset_id = %s", (offset_id,))
        
        carbon_offset = cursor.fetchone()

        if not carbon_offset:
            flash("You do not have permission to delete this carbon offset or it doesn't exist.", "danger")
            return redirect(url_for('view_carbon_offsets'))
    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        return redirect(url_for('view_carbon_offsets'))
    finally:
        cursor.close()
        connection.close()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Carbon_Offsets WHERE offset_id = %s", (offset_id,))
        connection.commit()
        flash("Carbon offset deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error deleting carbon offset: {err}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_carbon_offsets'))


# Update carbon offset
@app.route('/update_carbon_offset/<int:offset_id>', methods=['GET', 'POST'])
@role_required('Admin', 'Industry Manager')
def update_carbon_offset(offset_id):
    # Database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'GET':
        # Fetch the current details of the carbon offset
        cursor.execute("SELECT * FROM Carbon_Offsets WHERE offset_id = %s", (offset_id,))
        carbon_offset = cursor.fetchone()

        if carbon_offset is None:
            flash("Carbon offset not found!", 'danger')
            return redirect(url_for('view_carbon_offsets'))

        # Render the template with the current carbon offset details in the form
        return render_template('update_carbon_offset.html', carbon_offset=carbon_offset)

    elif request.method == 'POST':
        # Safely get form data with .get() to avoid KeyError
        offset_type = request.form.get('offset_type')
        amount_offset = request.form.get('amount_offset')
        provider_details = request.form.get('provider_details')

        # Validate the inputs
        if not offset_type or not amount_offset or not provider_details:
            flash("All fields are required.", 'danger')
            return redirect(url_for('update_carbon_offset', offset_id=offset_id))

        try:
            # Update the carbon offset in the database
            cursor.execute("""
                UPDATE Carbon_Offsets
                SET offset_type = %s, amount_offset = %s, provider_details = %s
                WHERE offset_id = %s
            """, (offset_type, amount_offset, provider_details, offset_id))

            connection.commit()

            flash("Carbon offset updated successfully!", 'success')
            return redirect(url_for('view_carbon_offsets'))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
            return redirect(url_for('update_carbon_offset', offset_id=offset_id))

        finally:
            cursor.close()
            connection.close()



# View transportation
@app.route('/view_transportation', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')
def view_transportation():
    print(f"User Role: {g.role}")  # Debugging: Print the user's role

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Role-based filtering
        if g.role == 'Industry Manager':
            # Fetch the logged-in user's industry_id from the USER table using username
            cursor.execute("SELECT industry_id FROM USER WHERE username = %s", (g.username,))
            user_data = cursor.fetchone()
            print(f"Fetched User Data: {user_data}")

            if user_data and user_data['industry_id']:
                # Fetch details for the user's assigned industry
                assigned_industry_id = user_data['industry_id']
                query = """
                    SELECT t.transport_id, t.vehicle_type, t.distance_travelled, t.fuel_consumption, i.industry_name
                    FROM Transportation t
                    JOIN Industries i ON t.industry_id = i.industry_id
                    WHERE t.industry_id = %s
                """
                cursor.execute(query, (assigned_industry_id,))
            else:
                flash("You are not assigned to any industry.", "warning")
                transportation = []
                return render_template('view_transportation.html', transportation=transportation)

        elif g.role == 'Admin':
            # Admin can view all transportation entries
            query = """
                SELECT t.transport_id, t.vehicle_type, t.distance_travelled, t.fuel_consumption, i.industry_name
                FROM Transportation t
                LEFT JOIN Industries i ON t.industry_id = i.industry_id
            """
            cursor.execute(query)
            
        elif g.role == 'Auditor':
            # Admin can view all transportation entries
            query = """
                SELECT t.transport_id, t.vehicle_type, t.distance_travelled, t.fuel_consumption, i.industry_name
                FROM Transportation t
                LEFT JOIN Industries i ON t.industry_id = i.industry_id
            """
            cursor.execute(query)

        transportation = cursor.fetchall()

        print(f"Fetched Transportation: {transportation}")  # Debugging: Print the fetched transportation

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        transportation = []

    finally:
        cursor.close()
        connection.close()

    return render_template('view_transportation.html', transportation=transportation)


# Delete transportation entry
# Delete transportation
@app.route('/delete_transportation/<int:transport_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')
def delete_transportation(transport_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Restrict Industry Managers to only their assigned transportation records
        if g.role == 'Industry Manager':
            cursor.execute("""
                SELECT * 
                FROM Transportation 
                WHERE transport_id = %s AND industry_id = (SELECT industry_id FROM USER WHERE username = %s)
            """, (transport_id, g.username))
        elif g.role == 'Admin':
            cursor.execute("SELECT * FROM Transportation WHERE transport_id = %s", (transport_id,))
        
        transportation = cursor.fetchone()

        if not transportation:
            flash("You do not have permission to delete this transportation record or it doesn't exist.", "danger")
            return redirect(url_for('view_transportation'))
    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        return redirect(url_for('view_transportation'))
    finally:
        cursor.close()
        connection.close()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Transportation WHERE transport_id = %s", (transport_id,))
        connection.commit()
        flash("Transportation record deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error deleting transportation record: {err}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_transportation'))

# Update transportation entry

@app.route('/update_transportation/<int:transport_id>', methods=['GET', 'POST'])
@role_required('Admin', 'Industry Manager')
def update_transportation(transport_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'GET':
        # Fetch the current details of the transportation record
        cursor.execute("SELECT * FROM Transportation WHERE transport_id = %s", (transport_id,))
        transportation = cursor.fetchone()

        if transportation is None:
            flash("Transportation record not found!", 'danger')
            return redirect(url_for('view_transportation'))

        # Pass the fetched record to the template
        return render_template('update_transportation.html', transportation=transportation)

    elif request.method == 'POST':
        # Get form data
        vehicle_type = request.form.get('vehicle_type')
        distance_travelled = request.form.get('distance_travelled')
        fuel_consumption = request.form.get('fuel_consumption')

        # Validate the inputs
        if not vehicle_type or not distance_travelled or not fuel_consumption:
            flash("All fields are required.", 'danger')
            return redirect(url_for('update_transportation', transport_id=transport_id))

        try:
            # Update the record in the database
            cursor.execute("""
                UPDATE Transportation
                SET vehicle_type = %s, distance_travelled = %s, fuel_consumption = %s
                WHERE transport_id = %s
            """, (vehicle_type, distance_travelled, fuel_consumption, transport_id))
            connection.commit()

            flash("Transportation record updated successfully!", 'success')
            return redirect(url_for('view_transportation'))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
            return redirect(url_for('update_transportation', transport_id=transport_id))

        finally:
            cursor.close()
            connection.close()
    
    
    
# View emission sources
@app.route('/view_emission_sources', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')
def view_emission_sources():
    print(f"User Role: {g.role}")  # Debugging: Print the user's role

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Role-based filtering
        if g.role == 'Industry Manager':
            # Fetch the logged-in user's industry_id from the USER table using username
            cursor.execute("SELECT industry_id FROM USER WHERE username = %s", (g.username,))
            user_data = cursor.fetchone()

            if user_data and user_data['industry_id']:
                # Fetch details for the user's assigned industry
                assigned_industry_id = user_data['industry_id']
                query = """
                    SELECT e.source_id, e.source_type, e.emission_value, i.industry_name
                    FROM Emission_Sources e
                    JOIN Industries i ON e.industry_id = i.industry_id
                    WHERE e.industry_id = %s
                """
                cursor.execute(query, (assigned_industry_id,))
            else:
                flash("You are not assigned to any industry.", "warning")
                emission_sources = []
                return render_template('view_emission_sources.html', emission_sources=emission_sources)

        elif g.role == 'Admin':
            # Admin can view all emission sources
            query = """
                SELECT e.source_id, e.source_type, e.emission_value, i.industry_name
                FROM Emission_Sources e
                LEFT JOIN Industries i ON e.industry_id = i.industry_id
            """
            cursor.execute(query)
            
        elif g.role == 'Auditor':
            # Admin can view all emission sources
            query = """
                SELECT e.source_id, e.source_type, e.emission_value, i.industry_name
                FROM Emission_Sources e
                LEFT JOIN Industries i ON e.industry_id = i.industry_id
            """
            cursor.execute(query)

        emission_sources = cursor.fetchall()

        print(f"Fetched Emission Sources: {emission_sources}")  # Debugging: Print the fetched data

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        emission_sources = []

    finally:
        cursor.close()
        connection.close()

    return render_template('view_emission_sources.html', emission_sources=emission_sources)


# Delete emission source
@app.route('/delete_emission_source/<int:source_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')
def delete_emission_source(source_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Restrict Industry Managers to only their assigned emission sources
        if g.role == 'Industry Manager':
            cursor.execute("""
                SELECT * 
                FROM Emission_Sources 
                WHERE source_id = %s AND industry_id = (SELECT industry_id FROM USER WHERE username = %s)
            """, (source_id, g.username))
        elif g.role == 'Admin':
            cursor.execute("SELECT * FROM Emission_Sources WHERE source_id = %s", (source_id,))
        
        emission_source = cursor.fetchone()

        if not emission_source:
            flash("You do not have permission to delete this emission source record or it doesn't exist.", "danger")
            return redirect(url_for('view_emission_sources'))

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
        return redirect(url_for('view_emission_sources'))
    finally:
        cursor.close()
        connection.close()

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Emission_Sources WHERE source_id = %s", (source_id,))
        connection.commit()
        flash("Emission source record deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error deleting emission source record: {err}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_emission_sources'))

# Update emission source
@app.route('/update_emission_source/<int:source_id>', methods=['GET', 'POST'])
@role_required('Admin', 'Industry Manager')
def update_emission_source(source_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch emission source data from the database
        cursor.execute("""
            SELECT * FROM Emission_Sources WHERE source_id = %s
        """, (source_id,))
        emission_source = cursor.fetchone()

        if not emission_source:
            flash("Emission source not found.", "danger")
            return redirect(url_for('view_emission_sources'))

        # Handle the form submission (POST)
        if request.method == 'POST':
            # Get updated data from the form
            source_type = request.form['source_type']
            emission_value = request.form['emission_value']

            # Update the emission source record in the database
            cursor.execute("""
                UPDATE Emission_Sources
                SET source_type = %s, emission_value = %s
                WHERE source_id = %s
            """, (source_type, emission_value, source_id))
            connection.commit()
            flash("Emission source updated successfully.", "success")
            return redirect(url_for('view_emission_sources'))

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "danger")
    finally:
        cursor.close()
        connection.close()

    # Pass the emission source data to the template
    return render_template('update_emission_source.html', emission_source=emission_source)


import pymysql 
from flask import render_template, request, jsonify

@app.route('/get_carbon_offset', methods=['GET', 'POST'])
def get_carbon_offset():
    if request.method == 'POST':
        # Get the industry_id from the form data (JSON body)
        data = request.get_json()
        industry_id = data.get('industry_id')

        # Check if the industry_id is provided
        if not industry_id:
            return jsonify({"error": "Industry ID is required"}), 400

        # Connect to the MySQL database
        connection = get_db_connection()

        try:
            # Create a cursor object using the connection
            cursor = connection.cursor(dictionary=True)

            # Execute the query to get the total carbon offset for the given industry_id
            cursor.execute("SELECT get_total_carbon_offset(%s) AS total_offset", (industry_id,))

            # Fetch the result
            result = cursor.fetchone()

            if result:
                return jsonify({"total_offset": result['total_offset']})
            else:
                return jsonify({"error": "No data found for the given industry_id"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            # Always close the connection
            connection.close()
    
    # If it's a GET request, render the form page (get_carbon_offset.html)
    return render_template('get_carbon_offset.html')

if __name__ == '__main__':
    app.run(debug=True)
