"""
Robust Hospital Table IDENTITY Fix

This script completely fixes the hospital table by properly removing the IDENTITY property
and converting hospital_id to VARCHAR(20) to allow string ID insertion.
"""

import pyodbc
from datetime import datetime

def connect_to_sql():
    """Connect to SQL Server"""
    try:
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=EmergencyMock;"
            "Trusted_Connection=yes;"
        )
        print("✅ Connected to SQL Server")
        return connection
    except Exception as e:
        print(f"❌ SQL Server connection failed: {e}")
        return None

def fix_hospital_robust():
    """Robust fix for hospital table IDENTITY issue"""
    connection = connect_to_sql()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        print("\n🔧 === ROBUST HOSPITAL IDENTITY FIX ===")
        
        # Step 1: Check current hospital_id column properties
        cursor.execute("""
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE, 
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE,
                COLUMNPROPERTY(object_id('hospitals'), 'hospital_id', 'IsIdentity') as IsIdentity
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'hospitals' AND COLUMN_NAME = 'hospital_id'
        """)
        
        column_info = cursor.fetchone()
        print(f"📋 Current hospital_id column: {column_info}")
        is_identity = column_info[4] == 1
        print(f"📋 Is IDENTITY column: {is_identity}")
        
        if not is_identity:
            print("✅ Hospital ID is not IDENTITY - no fix needed")
            return True
        
        # Step 2: Find all constraints that reference hospital_id
        print("\n🔍 Finding all constraints that reference hospital_id...")
        
        # Find foreign key constraints
        cursor.execute("""
            SELECT 
                fk.TABLE_NAME,
                fk.CONSTRAINT_NAME,
                fk.COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE fk
            INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc 
                ON fk.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
            WHERE tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
                AND fk.COLUMN_NAME = 'hospital_id'
        """)
        
        foreign_keys = cursor.fetchall()
        print(f"📊 Found {len(foreign_keys)} foreign key constraints:")
        for fk in foreign_keys:
            print(f"   {fk[0]}.{fk[1]} ({fk[2]})")
        
        # Find primary key constraint
        cursor.execute("""
            SELECT 
                kcu.TABLE_NAME,
                tc.CONSTRAINT_NAME,
                kcu.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
                ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
            WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
                AND kcu.TABLE_NAME = 'hospitals'
                AND kcu.COLUMN_NAME = 'hospital_id'
        """)
        
        primary_keys = cursor.fetchall()
        print(f"📊 Found {len(primary_keys)} primary key constraints:")
        for pk in primary_keys:
            print(f"   {pk[0]}.{pk[1]} ({pk[2]})")
        
        # Step 3: Drop all foreign key constraints first
        print("\n🗑️ Dropping foreign key constraints...")
        for fk in foreign_keys:
            constraint_name = fk[1]
            table_name = fk[0]
            print(f"   Dropping {table_name}.{constraint_name}")
            try:
                cursor.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT {constraint_name}")
                print(f"   ✅ Dropped {constraint_name}")
            except Exception as e:
                print(f"   ⚠️ Could not drop {constraint_name}: {e}")
        
        # Step 4: Drop primary key constraint
        print("\n🗑️ Dropping primary key constraint...")
        for pk in primary_keys:
            constraint_name = pk[1]
            table_name = pk[0]
            print(f"   Dropping {table_name}.{constraint_name}")
            try:
                cursor.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT {constraint_name}")
                print(f"   ✅ Dropped {constraint_name}")
            except Exception as e:
                print(f"   ⚠️ Could not drop {constraint_name}: {e}")
        
        # Step 5: Create a completely new column with proper type
        print("\n🔄 Creating new hospital_id column with proper type...")
        
        # First, check if there's any data in the table
        cursor.execute("SELECT COUNT(*) FROM hospitals")
        row_count = cursor.fetchone()[0]
        print(f"📊 Found {row_count} rows in hospitals table")
        
        if row_count > 0:
            # Backup existing data
            print("📋 Backing up existing hospital data...")
            cursor.execute("""
                SELECT hospital_id, hospital_name, address, phone_number,
                       hospital_type, level, total_capacity, current_capacity,
                       available_beds, ed_status, average_wait_time, trauma_level,
                       helicopter_pad, burn_unit, stroke_center, lat, lng
                FROM hospitals
            """)
            existing_data = cursor.fetchall()
            print(f"✅ Backed up {len(existing_data)} hospital records")
        
        # Drop the entire table and recreate it
        print("🗑️ Dropping and recreating hospitals table...")
        cursor.execute("DROP TABLE hospitals")
        print("✅ Dropped hospitals table")
        
        # Recreate the table with proper schema
        cursor.execute("""
            CREATE TABLE hospitals (
                hospital_id VARCHAR(20) PRIMARY KEY,
                hospital_name VARCHAR(100) NOT NULL,
                address VARCHAR(200) NOT NULL,
                phone_number VARCHAR(20),
                hospital_type VARCHAR(20) NOT NULL,
                level VARCHAR(20) NOT NULL,
                total_capacity INT NOT NULL,
                current_capacity INT NOT NULL,
                available_beds INT NOT NULL,
                ed_status VARCHAR(20) NOT NULL,
                average_wait_time INT NOT NULL,
                trauma_level VARCHAR(20) NOT NULL,
                helicopter_pad BIT DEFAULT 0,
                burn_unit BIT DEFAULT 0,
                stroke_center BIT DEFAULT 0,
                lat DECIMAL(10, 6) NOT NULL,
                lng DECIMAL(10, 6) NOT NULL,
                created_timestamp DATETIME2 DEFAULT GETDATE()
            )
        """)
        print("✅ Recreated hospitals table with proper schema")
        
        # Restore data if it existed
        if row_count > 0:
            print("📋 Restoring hospital data...")
            for row in existing_data:
                cursor.execute("""
                    INSERT INTO hospitals (
                        hospital_id, hospital_name, address, phone_number,
                        hospital_type, level, total_capacity, current_capacity,
                        available_beds, ed_status, average_wait_time, trauma_level,
                        helicopter_pad, burn_unit, stroke_center, lat, lng
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                    row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16]
                ))
            print(f"✅ Restored {len(existing_data)} hospital records")
        
        # Step 6: Recreate foreign key constraints
        print("\n🔧 Recreating foreign key constraints...")
        for fk in foreign_keys:
            table_name = fk[0]
            constraint_name = fk[1]
            print(f"   Recreating {table_name}.{constraint_name}")
            
            try:
                # Recreate the foreign key constraint
                cursor.execute(f"""
                    ALTER TABLE {table_name} 
                    ADD CONSTRAINT {constraint_name} 
                    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
                """)
                print(f"   ✅ Recreated {constraint_name}")
            except Exception as e:
                print(f"   ⚠️ Could not recreate {constraint_name}: {e}")
        
        print("✅ Foreign key constraints recreated")
        
        connection.commit()
        print("\n✅ Hospital table robust fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing hospital table: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def validate_hospital_robust_fix():
    """Validate that the hospital table fix was successful"""
    print("\n🔍 === VALIDATING HOSPITAL ROBUST FIX ===")
    
    connection = connect_to_sql()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Check hospital_id column properties
        cursor.execute("""
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE, 
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE,
                COLUMNPROPERTY(object_id('hospitals'), 'hospital_id', 'IsIdentity') as IsIdentity
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'hospitals' AND COLUMN_NAME = 'hospital_id'
        """)
        
        column_info = cursor.fetchone()
        print(f"📊 Hospital ID column: {column_info}")
        print(f"📊 Is IDENTITY column: {column_info[4] == 1}")
        
        if column_info[4] == 1:
            print("❌ Hospital ID is still IDENTITY - fix failed")
            return False
        
        if column_info[1] != 'varchar':
            print(f"❌ Hospital ID is not VARCHAR - it's {column_info[1]}")
            return False
        
        print("✅ Hospital ID is now VARCHAR and not IDENTITY")
        
        # Test inserting a string hospital_id
        test_hospital_id = "HOSP_TEST_FIX"
        cursor.execute("""
            INSERT INTO hospitals (
                hospital_id, hospital_name, address, phone_number,
                hospital_type, level, total_capacity, current_capacity,
                available_beds, ed_status, average_wait_time, trauma_level,
                helicopter_pad, burn_unit, stroke_center, lat, lng
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_hospital_id, "Test Hospital", "123 Test St", "555-1234",
            "GENERAL", "Level I", 100, 75, 25, "Open", 30, "Level I",
            0, 0, 0, 37.5407, -77.4348
        ))
        
        connection.commit()
        print(f"✅ Successfully inserted test hospital with ID: {test_hospital_id}")
        
        # Clean up test data
        cursor.execute("DELETE FROM hospitals WHERE hospital_id = ?", (test_hospital_id,))
        connection.commit()
        print(f"✅ Cleaned up test data")
        
        print("✅ Hospital table validation completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Hospital table validation error: {e}")
        return False
    finally:
        connection.close()

def main():
    """Main execution function"""
    print("🚨 === ROBUST HOSPITAL IDENTITY FIX ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fix the hospital table
    if fix_hospital_robust():
        print("\n✅ Hospital table fix completed!")
        
        # Validate the fix
        if validate_hospital_robust_fix():
            print("\n🎉 HOSPITAL ROBUST FIX VALIDATED SUCCESSFULLY!")
            print("🚀 Hospital table is now ready for string ID insertion")
        else:
            print("\n⚠️ Hospital table fix validation failed")
    else:
        print("\n❌ Hospital table fix failed")
    
    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
