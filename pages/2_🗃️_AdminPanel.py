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

# Check if the 'id' column already exists before adding it
mycursor.execute("SHOW COLUMNS FROM data LIKE 'id'")
result = mycursor.fetchone()

if result is None:
    mycursor.execute("ALTER TABLE data ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

# Create Streamlit App
def main():
    st.title("Admin Panel Operations")

    # Display Options for CRUD Operations
    option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete"))

    # Perform Selected CRUD Operations
    if option == "Create":
        st.subheader("Create a Data")
        # Remove 'id' from the user input since it's auto-incremented
        nomor_pegawai = st.text_input("Enter Nomor Pegawai")
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
            try:
                # Exclude 'id' from the INSERT statement
                sql = "INSERT INTO data (nomor_pegawai, nama, bulan, leads, prospect, hot, spk, do, jabatan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (nomor_pegawai, nama, bulan, leads, prospect, hot, spk, do, jabatan)
                mycursor.execute(sql, val)
                conn.commit()
                st.success("Data Created Successfully!!!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif option == "Read":
        st.subheader("Read Database")
        mycursor.execute("SELECT * FROM data")
        result = mycursor.fetchall()

        # Mendapatkan nama kolom dari tabel
        column_names = [i[0] for i in mycursor.description]

        # Membuat DataFrame dari hasil query
        df = pd.DataFrame(result, columns=column_names)

        # Mengganti nama kolom pertama
        df.rename(columns={column_names[0]: 'ID',
                           column_names[1]: 'Nomor Pegawai',
                           column_names[2]: 'Nama',
                           column_names[3]: 'Bulan',
                           column_names[4]: 'Leads',
                           column_names[5]: 'Prospect',
                           column_names[6]: 'Hot',
                           column_names[7]: 'SPK',
                           column_names[8]: 'DO',
                           column_names[9]: 'Jabatan'}, inplace=True)

        # Menampilkan data sebagai tabel
        st.table(df)


    elif option == "Update":
        st.subheader("Update a Data")

        # Pilih bulan untuk menentukan record yang akan di-update
        selected_month = st.date_input("Select Month")

        mycursor.execute("SELECT * FROM data WHERE bulan = %s", (selected_month,))
        existing_data = mycursor.fetchall()
        # Tampilkan dropdown untuk memilih data berdasarkan nama
        selected_data = st.selectbox("Select Data to Update", [f"{data[2]} ({data[1]})" for data in existing_data])

        # Ambil data terpilih berdasarkan nama
        # selected_nomor_pegawai = selected_data.split(" ")[-1][1:-1]
        existing_data = mycursor.fetchall()

        # # Check if the list is not empty before accessing its elements
        # filtered_data = [data for data in existing_data if data[1] == selected_nomor_pegawai]

        # Ambil semua data untuk bulan yang dipilih
        mycursor.execute("SELECT * FROM data WHERE bulan = %s", (selected_month,))
        existing_data = mycursor.fetchone()

        if existing_data:
            nama = st.text_input("Enter New Name", value=selected_data)
            leads = st.number_input("Enter New Leads", min_value=0, value=existing_data[4])
            prospect = st.number_input("Enter New Prospect", min_value=0, value=existing_data[5])
            hot = st.number_input("Enter New Hot", min_value=0, value=existing_data[6])
            spk = st.number_input("Enter New SPK", min_value=0, value=existing_data[7])
            do = st.number_input("Enter New DO", min_value=0, value=existing_data[8])

            # Pilihan jabatan menggunakan drop-down menu
            jabatan_options = ["Sales Senior", "Sales Trainee"]
            jabatan = st.selectbox("Select New Position", jabatan_options, index=jabatan_options.index(existing_data[9]))

        
          

        if st.button("Update"):
                sql = "UPDATE data SET nama=%s, leads=%s, prospect=%s, hot=%s, spk=%s, do=%s, jabatan=%s WHERE bulan=%s AND nomor_pegawai=%s"
                val = (nama, leads, prospect, hot, spk, do, jabatan, selected_month, nomor_pegawai)
                mycursor.execute(sql, val)
                conn.commit()
                st.success("Data Updated Successfully!!!")
        else:
            st.warning("Selected data not found.")


   
    elif option == "Delete":
        st.subheader("Delete a Data")
        nomor_pegawai_to_delete = st.text_input("Enter Nomor Pegawai to delete data")
        
        if st.button("Show Data"):
            # Query to fetch data based on the provided nomor_pegawai
            try:
                select_query = "SELECT * FROM data WHERE nomor_pegawai=%s"
                mycursor.execute(select_query, (nomor_pegawai_to_delete,))
                result = mycursor.fetchall()

                if result:
                    st.write("Data to be deleted:")
                    for data in result:
                        st.write(f"ID: {data[0]}")
                        st.write(f"Bulan: {data[3]}")
                        st.write(f"Nama: {data[2]}")
                        # Add other fields as needed

                    # Allow the user to select which ID to delete
                    id_to_delete = st.selectbox("Select ID to delete", [data[0] for data in result])

                    # Show the delete button after displaying the data
                    if st.button("Delete"):
                        try:
                            # Delete the data based on the selected id
                            delete_query = "DELETE FROM data WHERE id=%s"
                            mycursor.execute(delete_query, (id_to_delete,))
                            conn.commit()

                            # Check if any rows were affected (data deleted)
                            if mycursor.rowcount > 0:
                                st.success("Data Deleted Successfully!!!")
                            else:
                                st.warning("Data with selected ID does not exist in the database")
                        except Exception as e:
                            st.error(f"An error occurred during deletion: {e}")
                else:
                    st.warning("Nomor Pegawai does not exist in the database")
            except Exception as e:
                st.error(f"An error occurred during data retrieval: {e}")

if __name__ == "__main__":
    main()
