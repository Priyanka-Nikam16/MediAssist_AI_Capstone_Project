
from backend.MCP.connector import get_db_connection


def Search_patients(patient_name: str):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT patient_id, patient_code, patient_name, gender, age,
               phone, diagnosis, blood_group, city
        FROM patients
        WHERE patient_name ILIKE %s
           OR patient_code ILIKE %s
        ORDER BY patient_id
        LIMIT 10
                   
    """, (f"%{patient_name}%", f"%{patient_name}%"))

    rows = cursor.fetchall()
    print("rows:",rows)
    cursor.close()
    conn.close()

    return [
        {
            "patient_id": row[0],
            "patient_code": row[1],
            "patient_name": row[2],
            "gender": row[3],
            "age": row[4],
            "phone": row[5],
            "diagnosis": row[6],
            "blood_group": row[7],
            "city": row[8]
        }
        for row in rows
    ]


def Get_patient_history(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.patient_id,
            p.patient_code,
            p.patient_name,
            p.diagnosis,
            p.admission_date,
            p.discharge_date,
            a.admission_reason,
            a.ward,
            a.admitted_on,
            a.discharged_on,
            pr.medication_name,
            pr.dosage,
            pr.prescription_date
        FROM patients p
        LEFT JOIN admissions a ON p.patient_id = a.patient_id
        LEFT JOIN prescriptions pr ON p.patient_id = pr.patient_id
        WHERE p.patient_id = %s
        ORDER BY a.admitted_on DESC, pr.prescription_date DESC
    """, (patient_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "patient_id": row[0],
            "patient_code": row[1],
            "patient_name": row[2],
            "diagnosis": row[3],
            "admission_date": str(row[4]) if row[4] else None,
            "discharge_date": str(row[5]) if row[5] else None,
            "admission_reason": row[6],
            "ward": row[7],
            "admitted_on": str(row[8]) if row[8] else None,
            "discharged_on": str(row[9]) if row[9] else None,
            "medication_name": row[10],
            "dosage": row[11],
            "prescription_date": str(row[12]) if row[12] else None
        }
        for row in rows
    ]


def Get_lab_results(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lab_id, patient_id, test_name, result, report_date
        FROM lab_results
        WHERE patient_id = %s
        ORDER BY report_date DESC
        LIMIT 10
    """, (patient_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "lab_id": row[0],
            "patient_id": row[1],
            "test_name": row[2],
            "result": row[3],
            "report_date": str(row[4]) if row[4] else None
        }
        for row in rows
    ]


def Get_payment_summary(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bill_id, patient_id, amount, insurance_provider, payment_status
        FROM billing
        WHERE patient_id = %s
        ORDER BY bill_id DESC
    """, (patient_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "bill_id": row[0],
            "patient_id": row[1],
            "amount": float(row[2]) if row[2] else 0,
            "insurance_provider": row[3],
            "payment_status": row[4]
        }
        for row in rows
    ]