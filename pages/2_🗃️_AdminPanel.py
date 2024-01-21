import mysql.connector
import streamlit as st
import pandas as pd


# Establish a connection to MySQL Server

conn = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12678617",
    password="FtL1h1vtpZ",
    database="sql12678617"
)
mycursor = conn.cursor()
print("Connection Established")
st.set_page_config(
    page_title="Admin Panel",
    page_icon="🗃️",
    )
# Create Streamlit App
def main():
    st.title("Admin Panel Operations")

    # Display Options for CRUD Operations
    option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete"))

    # Perform Selected CRUD Operations
    if option == "Create":
        st.subheader("Create a Data")
        nama = st.text_input("Enter Name")
        bulan = st.date_input("Select Month")
        leads = st.number_input("Enter Leads", min_value=0)
        prospect = st.number_input("Enter Prospect", min_value=0)
        hot = st.number_input("Enter Hot", min_value=0)
        spk = st.number_input("Enter SPK", min_value=0)
        do = st.number_input("Enter DO", min_value=0)

        # Pilihan jabatan menggunakan drop-down menu
        jabatan_options = ["Sales Senior", "Sales Trainee"]
        jabatan = st.selectbox("Select Position", jabatan_options)

        if st.button("Create"):
            sql = "INSERT INTO data (nama, bulan, leads, prospect, hot, spk, do, jabatan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (nama, bulan, leads, prospect, hot, spk, do, jabatan)
            mycursor.execute(sql, val)
            conn.commit()
            st.success("Data Created Successfully!!!")

    elif option == "Read":
        st.subheader("Read Database")
        mycursor.execute("SELECT * FROM data")
        result = mycursor.fetchall()

        # Mendapatkan nama kolom dari tabel
        column_names = [i[0] for i in mycursor.description]

        # Membuat DataFrame dari hasil query
        df = pd.DataFrame(result, columns=column_names)

        # Mengganti nama kolom pertama
        df.rename(columns={
                           column_names[0]: 'Nama',
                           column_names[1]: 'Bulan',
                           column_names[2]: 'Leads',
                           column_names[3]: 'Prospect',
                           column_names[4]: 'Hot',
                           column_names[5]: 'SPK',
                           column_names[6]: 'DO',
                           column_names[7]: 'Jabatan'}, inplace=True)

        # Menampilkan data sebagai tabel
        st.table(df)
        
    elif option == "Update":
        st.subheader("Update a Data")

        # Pilih bulan untuk menentukan record yang akan di-update
        selected_month = st.date_input("Select Month")

        # Ambil data sebelumnya
        mycursor.execute("SELECT * FROM data WHERE bulan = %s", (selected_month,))
        existing_data = mycursor.fetchone()

        # Jika data ditemukan, tampilkan formulir update
        if existing_data:
            nama = st.text_input("Enter New Name", value=existing_data[1])
            leads = st.number_input("Enter New Leads", min_value=0, value=existing_data[3])
            prospect = st.number_input("Enter New Prospect", min_value=0, value=existing_data[4])
            hot = st.number_input("Enter New Hot", min_value=0, value=existing_data[5])
            spk = st.number_input("Enter New SPK", min_value=0, value=existing_data[6])
            do = st.number_input("Enter New DO", min_value=0, value=existing_data[7])

            # Pilihan jabatan menggunakan drop-down menu
            jabatan_options = ["Sales Senior", "Sales Trainee"]
            jabatan = st.selectbox("Select New Position", jabatan_options, index=jabatan_options.index(existing_data[8]))

            if st.button("Update"):
                sql = "UPDATE data SET nomor_pegawai=%s, nama=%s, leads=%s, prospect=%s, hot=%s, spk=%s, do=%s, jabatan=%s WHERE bulan=%s"
                val = (nomor_pegawai, nama, leads, prospect, hot, spk, do, jabatan, selected_month)
                mycursor.execute(sql, val)
                conn.commit()
                st.success("Data Updated Successfully!!!")
        else:
            st.warning("Data not found for the selected month.")

    elif option == "Delete":
        st.subheader("Delete a Data")
        nomor_pegawai = st.text_input("Enter Nomor Pegawai")
    if st.button("Delete"):
        try:
            sql = "DELETE FROM data WHERE nomor_pegawai=%s"
            val = (nomor_pegawai,)
            mycursor.execute(sql, val)
            conn.commit()

            # Periksa apakah ada baris yang terpengaruh (data terhapus)
            if mycursor.rowcount > 0:
                st.success("Data Deleted Successfully!!!")
            else:
                st.warning("Nomor Pegawai does not exist in the database")
        except Exception as e:
            st.error(f"An error occurred: {e}")
if __name__ == "__main__":
    main()
