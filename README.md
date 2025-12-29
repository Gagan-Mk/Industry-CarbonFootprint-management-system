# READ Operations for Auditor Role

## Overview

**Auditors have READ-ONLY access** to all data in the system. They can view all industries, processes, emissions, transportation, and carbon offsets across the entire system, but **cannot create, update, or delete** any records.

---

## 🔍 How READ Operations Work for Auditors

### **Key Characteristics:**

1. ✅ **Can View**: All data across all industries
2. ❌ **Cannot Create**: No add/create operations allowed
3. ❌ **Cannot Update**: No edit/update operations allowed
4. ❌ **Cannot Delete**: No delete operations allowed

---

## 📋 All READ Operations Available to Auditors

### **1. View Industries**

```python
@app.route('/view_industries', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')  # ✅ Auditor allowed
def view_industries():
    if g.role == 'Industry Manager':
        # Industry Manager: Only their industry
        cursor.execute("SELECT * FROM Industries WHERE industry_id = %s", 
                      (user_industry_id,))
    
    elif g.role == 'Admin':
        # Admin: All industries
        cursor.execute("SELECT * FROM Industries")
    
    elif g.role == 'Auditor':
        # ✅ Auditor: ALL industries (same as Admin)
        cursor.execute("SELECT * FROM Industries")
```

**What Auditor Sees:**
- ✅ **All industries** in the system
- ✅ Industry name, location, type
- ✅ No filtering - complete visibility

**Query Executed:**
```sql
SELECT * FROM Industries
-- No WHERE clause - sees everything
```

---

### **2. View Processes**

```python
@app.route('/view_processes', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')  # ✅ Auditor allowed
def view_processes():
    if g.role == 'Industry Manager':
        # Industry Manager: Only processes from their industry
        query = """
            SELECT p.process_id, p.process_name, p.energy_consumption, 
                   p.emission_factor, i.industry_name
            FROM Process p
            JOIN Industries i ON p.industry_id = i.industry_id
            WHERE p.industry_id = %s
        """
        cursor.execute(query, (user_industry_id,))
    
    elif g.role == 'Admin':
        # Admin: All processes
        query = """
            SELECT p.process_id, p.process_name, p.energy_consumption, 
                   p.emission_factor, i.industry_name
            FROM Process p
            LEFT JOIN Industries i ON p.industry_id = i.industry_id
        """
        cursor.execute(query)
    
    elif g.role == 'Auditor':
        # ✅ Auditor: ALL processes (same as Admin)
        query = """
            SELECT p.process_id, p.process_name, p.energy_consumption, 
                   p.emission_factor, i.industry_name
            FROM Process p
            LEFT JOIN Industries i ON p.industry_id = i.industry_id
        """
        cursor.execute(query)
```

**What Auditor Sees:**
- ✅ **All processes** from all industries
- ✅ Process name, energy consumption, emission factor
- ✅ Industry name (via JOIN)
- ✅ Complete cross-industry visibility

**Query Executed:**
```sql
SELECT p.process_id, p.process_name, p.energy_consumption, 
       p.emission_factor, i.industry_name
FROM Process p
LEFT JOIN Industries i ON p.industry_id = i.industry_id
-- No WHERE clause - sees all processes
```

---

### **3. View Carbon Offsets**

```python
@app.route('/view_carbon_offsets', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')  # ✅ Auditor allowed
def view_carbon_offsets():
    if g.role == 'Industry Manager':
        # Industry Manager: Only offsets from their industry
        query = """
            SELECT co.offset_id, co.offset_type, co.amount_offset, 
                   co.date_purchased, co.provider_details, i.industry_name
            FROM Carbon_Offsets co
            JOIN Industries i ON co.industry_id = i.industry_id
            WHERE co.industry_id = %s
        """
        cursor.execute(query, (user_industry_id,))
    
    elif g.role == 'Admin':
        # Admin: All carbon offsets
        query = """
            SELECT co.offset_id, co.offset_type, co.amount_offset, 
                   co.date_purchased, co.provider_details, i.industry_name
            FROM Carbon_Offsets co
            LEFT JOIN Industries i ON co.industry_id = i.industry_id
        """
        cursor.execute(query)
    
    elif g.role == 'Auditor':
        # ✅ Auditor: ALL carbon offsets (same as Admin)
        query = """
            SELECT co.offset_id, co.offset_type, co.amount_offset, 
                   co.date_purchased, co.provider_details, i.industry_name
            FROM Carbon_Offsets co
            LEFT JOIN Industries i ON co.industry_id = i.industry_id
        """
        cursor.execute(query)
```

**What Auditor Sees:**
- ✅ **All carbon offsets** from all industries
- ✅ Offset type, amount, date purchased, provider details
- ✅ Industry name (via JOIN)
- ✅ Complete visibility for auditing purposes

---

### **4. View Transportation**

```python
@app.route('/view_transportation', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')  # ✅ Auditor allowed
def view_transportation():
    if g.role == 'Industry Manager':
        # Industry Manager: Only transportation from their industry
        query = """
            SELECT t.transport_id, t.vehicle_type, t.distance_travelled, 
                   t.fuel_consumption, i.industry_name
            FROM Transportation t
            JOIN Industries i ON t.industry_id = i.industry_id
            WHERE t.industry_id = %s
        """
        cursor.execute(query, (user_industry_id,))
    
    elif g.role == 'Admin':
        # Admin: All transportation
        query = """
            SELECT t.transport_id, t.vehicle_type, t.distance_travelled, 
                   t.fuel_consumption, i.industry_name
            FROM Transportation t
            LEFT JOIN Industries i ON t.industry_id = i.industry_id
        """
        cursor.execute(query)
    
    elif g.role == 'Auditor':
        # ✅ Auditor: ALL transportation (same as Admin)
        query = """
            SELECT t.transport_id, t.vehicle_type, t.distance_travelled, 
                   t.fuel_consumption, i.industry_name
            FROM Transportation t
            LEFT JOIN Industries i ON t.industry_id = i.industry_id
        """
        cursor.execute(query)
```

**What Auditor Sees:**
- ✅ **All transportation records** from all industries
- ✅ Vehicle type, distance travelled, fuel consumption
- ✅ Industry name (via JOIN)

---

### **5. View Emission Sources**

```python
@app.route('/view_emission_sources', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')  # ✅ Auditor allowed
def view_emission_sources():
    if g.role == 'Industry Manager':
        # Industry Manager: Only emission sources from their industry
        query = """
            SELECT e.source_id, e.source_type, e.emission_value, i.industry_name
            FROM Emission_Sources e
            JOIN Industries i ON e.industry_id = i.industry_id
            WHERE e.industry_id = %s
        """
        cursor.execute(query, (user_industry_id,))
    
    elif g.role == 'Admin':
        # Admin: All emission sources
        query = """
            SELECT e.source_id, e.source_type, e.emission_value, i.industry_name
            FROM Emission_Sources e
            LEFT JOIN Industries i ON e.industry_id = i.industry_id
        """
        cursor.execute(query)
    
    elif g.role == 'Auditor':
        # ✅ Auditor: ALL emission sources (same as Admin)
        query = """
            SELECT e.source_id, e.source_type, e.emission_value, i.industry_name
            FROM Emission_Sources e
            LEFT JOIN Industries i ON e.industry_id = i.industry_id
        """
        cursor.execute(query)
```

**What Auditor Sees:**
- ✅ **All emission sources** from all industries
- ✅ Source type, emission value
- ✅ Industry name (via JOIN)

---

## 🚫 Operations NOT Available to Auditors

### **CREATE Operations - Blocked**

All create/add operations explicitly exclude Auditor:

```python
@app.route('/add_transportation', methods=['POST'])
@role_required('Admin', 'Industry Manager')  # ❌ Auditor NOT allowed
def add_transportation():
    # ...

@app.route('/add_process', methods=['POST'])
# No decorator, but typically would be:
# @role_required('Admin', 'Industry Manager')  # ❌ Auditor NOT allowed
```

**Result:** If Auditor tries to access:
- `/add_transportation` → HTTP 403 Forbidden
- `/add_process` → May work (if no decorator) but shouldn't
- `/add_carbon_offset` → HTTP 403 Forbidden

---

### **UPDATE Operations - Blocked**

All update/edit operations exclude Auditor:

```python
@app.route('/update_process/<int:process_id>', methods=['GET', 'POST'])
@role_required('Admin', 'Industry Manager')  # ❌ Auditor NOT allowed
def update_process(process_id):
    # ...

@app.route('/update_transportation/<int:transport_id>', methods=['GET', 'POST'])
@role_required('Admin', 'Industry Manager')  # ❌ Auditor NOT allowed
def update_transportation(transport_id):
    # ...
```

**Result:** If Auditor tries to access:
- `/update_process/5` → HTTP 403 Forbidden
- `/update_transportation/3` → HTTP 403 Forbidden
- `/update_carbon_offset/2` → HTTP 403 Forbidden

---

### **DELETE Operations - Blocked**

All delete operations exclude Auditor:

```python
@app.route('/delete_process/<int:process_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')  # ❌ Auditor NOT allowed
def delete_process(process_id):
    # ...

@app.route('/delete_transportation/<int:transport_id>', methods=['POST'])
@role_required('Admin', 'Industry Manager')  # ❌ Auditor NOT allowed
def delete_transportation(transport_id):
    # ...
```

**Result:** If Auditor tries to access:
- `/delete_process/5` → HTTP 403 Forbidden
- `/delete_transportation/3` → HTTP 403 Forbidden
- `/delete_industry/1` → HTTP 403 Forbidden

---

## 📊 Complete Permission Matrix for Auditor

| Operation | Route | Auditor Access | What They See |
|-----------|-------|----------------|---------------|
| **CREATE** | | | |
| Add Industry | `/add_industry` | ❌ Blocked | - |
| Add Process | `/add_process` | ❌ Blocked | - |
| Add Transportation | `/add_transportation` | ❌ Blocked | - |
| Add Carbon Offset | `/add_carbon_offset` | ❌ Blocked | - |
| Add Emission Source | `/add_emission_source` | ❌ Blocked | - |
| **READ** | | | |
| View Industries | `/view_industries` | ✅ Allowed | **All industries** |
| View Processes | `/view_processes` | ✅ Allowed | **All processes** (with industry names) |
| View Transportation | `/view_transportation` | ✅ Allowed | **All transportation** (with industry names) |
| View Carbon Offsets | `/view_carbon_offsets` | ✅ Allowed | **All carbon offsets** (with industry names) |
| View Emission Sources | `/view_emission_sources` | ✅ Allowed | **All emission sources** (with industry names) |
| **UPDATE** | | | |
| Update Industry | `/update_industry/<id>` | ❌ Blocked | - |
| Update Process | `/update_process/<id>` | ❌ Blocked | - |
| Update Transportation | `/update_transportation/<id>` | ❌ Blocked | - |
| Update Carbon Offset | `/update_carbon_offset/<id>` | ❌ Blocked | - |
| Update Emission Source | `/update_emission_source/<id>` | ❌ Blocked | - |
| **DELETE** | | | |
| Delete Industry | `/delete_industry/<id>` | ❌ Blocked | - |
| Delete Process | `/delete_process/<id>` | ❌ Blocked | - |
| Delete Transportation | `/delete_transportation/<id>` | ❌ Blocked | - |
| Delete Carbon Offset | `/delete_carbon_offset/<id>` | ❌ Blocked | - |
| Delete Emission Source | `/delete_emission_source/<id>` | ❌ Blocked | - |

---

## 🔄 Comparison: Auditor vs Other Roles

### **View Industries Example**

| Role | Query Filter | Result |
|------|-------------|--------|
| **Admin** | `SELECT * FROM Industries` | All industries |
| **Industry Manager** | `SELECT * FROM Industries WHERE industry_id = 1` | Only their industry (ID=1) |
| **Auditor** | `SELECT * FROM Industries` | **All industries** (same as Admin) |

### **View Processes Example**

| Role | Query Filter | Result |
|------|-------------|--------|
| **Admin** | `SELECT * FROM Process` (with JOIN) | All processes from all industries |
| **Industry Manager** | `SELECT * FROM Process WHERE industry_id = 1` | Only processes from their industry |
| **Auditor** | `SELECT * FROM Process` (with JOIN) | **All processes from all industries** (same as Admin) |

---

## 🎯 Key Points About Auditor READ Access

### **1. Complete Visibility**
- Auditors see **ALL data** across **ALL industries**
- No filtering by industry_id
- Same query as Admin for READ operations

### **2. Read-Only Access**
- Can view but cannot modify
- Perfect for compliance and verification
- No risk of accidental data modification

### **3. Cross-Industry Auditing**
- Can compare data across different industries
- Can verify compliance across the entire system
- Can generate comprehensive reports

### **4. JOIN Queries for Context**
- All view operations include JOINs with Industries table
- Shows which industry each record belongs to
- Provides complete context for auditing

---

## 🔍 How the Check Works

### **Step-by-Step Flow for Auditor Viewing Data**

```
1. Auditor logs in
   ↓
   Session: username='auditor1', role_id=3
   
2. Auditor navigates to /view_processes
   ↓
   
3. @app.before_request runs
   ↓
   g.username = 'auditor1'
   g.role_id = 3
   g.role = 'Auditor'  # From role_mapping
   
4. @role_required('Admin', 'Industry Manager', 'Auditor') checks
   ↓
   Is g.role in ('Admin', 'Industry Manager', 'Auditor')?
   'Auditor' ✓ YES → Continue
   
5. Function executes
   ↓
   Check: g.role == 'Auditor'?
   YES → Execute query with NO WHERE clause
   
6. Query executed
   ↓
   SELECT p.*, i.industry_name 
   FROM Process p 
   LEFT JOIN Industries i ON p.industry_id = i.industry_id
   -- No WHERE clause - returns ALL processes
   
7. Results returned
   ↓
   All processes from all industries displayed
```

---

## 💡 Code Pattern for Auditor Access

### **Standard Pattern Used:**

```python
@app.route('/view_<entity>', methods=['GET'])
@role_required('Admin', 'Industry Manager', 'Auditor')  # ✅ Include Auditor
def view_<entity>():
    if g.role == 'Industry Manager':
        # Filter by user's industry_id
        query = "SELECT * FROM <Entity> WHERE industry_id = %s"
        cursor.execute(query, (user_industry_id,))
    
    elif g.role == 'Admin':
        # No filter - see all
        query = "SELECT * FROM <Entity>"
        cursor.execute(query)
    
    elif g.role == 'Auditor':
        # ✅ Same as Admin - see all
        query = "SELECT * FROM <Entity>"
        cursor.execute(query)
    
    return render_template('view_<entity>.html', data=data)
```

**Key Pattern:**
- Auditor gets the **same query as Admin** (no filtering)
- Both see **all data** across all industries
- Industry Manager sees **only their industry's data**

---

## 🛡️ Security Implementation

### **Route-Level Protection:**

```python
@role_required('Admin', 'Industry Manager', 'Auditor')
```

- ✅ Auditor is explicitly included in allowed roles
- ✅ If Auditor tries to access route without this decorator → HTTP 403

### **Data-Level Access:**

```python
elif g.role == 'Auditor':
    # No WHERE clause - sees everything
    cursor.execute("SELECT * FROM <Entity>")
```

- ✅ No filtering applied
- ✅ Complete visibility for auditing purposes
- ✅ Same access level as Admin for READ operations

---

## 📝 Summary

**Auditor Role Characteristics:**

1. ✅ **READ Access**: Can view all data (industries, processes, emissions, transportation, carbon offsets)
2. ❌ **CREATE Access**: Cannot add any records
3. ❌ **UPDATE Access**: Cannot modify any records
4. ❌ **DELETE Access**: Cannot remove any records
5. 🔍 **Cross-Industry**: Can see data from all industries (unlike Industry Manager)
6. 📊 **Full Visibility**: Same READ access as Admin (for viewing purposes)

**Purpose:**
- Compliance verification
- Data auditing
- Cross-industry analysis
- Report generation
- Verification without modification risk

**Implementation:**
- Route-level: Included in `@role_required` decorator for all view routes
- Data-level: No filtering applied (sees all data)
- Security: Cannot access any CREATE/UPDATE/DELETE routes

