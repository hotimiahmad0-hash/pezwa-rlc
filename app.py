import streamlit as st
import math

# --- PENGATURAN HALAMAN & SESSION STATE ---
st.set_page_config(page_title="PEZWA - Pengolah Data Praktikum", layout="centered")

# Mengatur state untuk navigasi agar tombol "Kembali ke Dashboard" berfungsi
if 'menu_utama' not in st.session_state:
    st.session_state.menu_utama = "Dashboard"

def pindah_ke_dashboard():
    st.session_state.menu_utama = "Dashboard"

# --- SIDEBAR (PILIHAN MENU) ---
st.sidebar.title("Navigasi PEZWA")
menu_options = ["Dashboard", "1. Praktikum Rangkaian RLC", "2. Praktikum Lainnya (Segera)"]

# Membaca pilihan dari sidebar, dengan sinkronisasi ke session_state
pilihan_menu = st.sidebar.radio("Pilih Halaman:", menu_options, index=menu_options.index(st.session_state.menu_utama))
st.session_state.menu_utama = pilihan_menu

# ==========================================
# HALAMAN 1: DASHBOARD
# ==========================================
if st.session_state.menu_utama == "Dashboard":
    st.title("DASHBOARD PEZWA")
    st.subheader("Hello PEZWANIAN! 👋")
    st.write("Selamat datang di aplikasi pengolahan data praktikum.")
    st.info("Silakan buka panel di sebelah kiri (Sidebar) lalu klik opsi **1. Praktikum Rangkaian RLC** untuk memulai perhitungan.")

# ==========================================
# HALAMAN 2: PRAKTIKUM RANGKAIAN RLC
# ==========================================
elif st.session_state.menu_utama == "1. Praktikum Rangkaian RLC":
    st.title("⚡ Praktikum Rangkaian RLC")
    
    # Memilih Sub-Praktikum
    sub_praktikum = st.selectbox(
        "Pilih Bagian Sub Praktikum:",
        ["-- Pilih Sub Praktikum --", "1. Rangkaian RC Seri", "2. Rangkaian RL Seri", "3. Rangkaian RLC Seri"]
    )

    if sub_praktikum != "-- Pilih Sub Praktikum --":
        st.markdown("---")
        st.write(f"### Masukkan Data Eksperimen: {sub_praktikum}")
        
        # Kolom input agar rapi (dibagi 2 kolom)
        col1, col2 = st.columns(2)
        
        # Input umum untuk semua opsi
        with col1:
            f = st.number_input("Frekuensi (Hz)", min_value=0.0, value=50.0)
            R = st.number_input("Besar Hambatan (Ω)", min_value=0.0, value=100.0)
            VR = st.number_input("Tegangan Resistor (VR dalam Volt)", min_value=0.0, value=10.0)
        with col2:
            Vtot = st.number_input("Tegangan Sirkuit (Vtot dalam Volt)", min_value=0.0, value=12.0)
            
        # Variabel khusus per opsi
        C = L = VC = VL = 0
        if sub_praktikum in ["1. Rangkaian RC Seri", "3. Rangkaian RLC Seri"]:
            with col1:
                C = st.number_input("Besar Kapasitor (F)", value=0.0001, format="%f")
            with col2:
                VC = st.number_input("Tegangan Kapasitor (VC dalam Volt)", min_value=0.0, value=5.0)
                
        if sub_praktikum in ["2. Rangkaian RL Seri", "3. Rangkaian RLC Seri"]:
            with col1:
                L = st.number_input("Besar Induktor (H)", value=0.5, format="%f")
            with col2:
                VL = st.number_input("Tegangan Induktor (VL dalam Volt)", min_value=0.0, value=5.0)

        # Tombol Proses
        if st.button("Hitung Hasil Praktikum"):
            st.markdown("---")
            st.write("### Result / Hasil Pengerjaan")
            
            # --- BLOK PERHITUNGAN MATEMATIKA ---
            omega = 2 * math.pi * f
            I = VR / R if R != 0 else 0 # Menghitung arus (I = VR / R)
            
            if sub_praktikum == "1. Rangkaian RC Seri":
                V_hitung = math.sqrt(VR**2 + VC**2)
                st.write("**1. √ (VR^2 + VC^2)**")
                st.latex(rf"\sqrt{{{VR}^2 + {VC}^2}} = {V_hitung:.3f} \text{{ Volt}}")
                
                XC = 1 / (omega * C) if (omega * C) != 0 else 0
                Z = math.sqrt(R**2 + XC**2)
                fasa = math.atan(-XC / R) if R != 0 else 0
                
            elif sub_praktikum == "2. Rangkaian RL Seri":
                V_hitung = math.sqrt(VR**2 + VL**2)
                st.write("**1. √ (VR^2 + VL^2)**")
                st.latex(rf"\sqrt{{{VR}^2 + {VL}^2}} = {V_hitung:.3f} \text{{ Volt}}")
                
                XL = omega * L
                Z = math.sqrt(R**2 + XL**2)
                fasa = math.atan(XL / R) if R != 0 else 0
                
            elif sub_praktikum == "3. Rangkaian RLC Seri":
                V_hitung = math.sqrt(VR**2 + (VL - VC)**2)
                st.write("**1. √ [VR^2 + (VL - VC)^2]**")
                st.latex(rf"\sqrt{{{VR}^2 + ({VL} - {VC})^2}} = {V_hitung:.3f} \text{{ Volt}}")
                
                XL = omega * L
                XC = 1 / (omega * C) if (omega * C) != 0 else 0
                Z = math.sqrt(R**2 + (XL - XC)**2)
                fasa = math.atan((XL - XC) / R) if R != 0 else 0

            # --- HASIL LANJUTAN (Nomor 2 sampai 5) ---
            st.write(f"**2. Impedansi Rangkaian (Z):** {Z:.3f} Ω")
            st.write(f"**3. Sudut Fasa (φ):** {fasa:.3f} RAD")
            
            P_av = Vtot * I * math.cos(fasa)
            st.write(f"**4. Daya Rata-rata (P_av):** {P_av:.3f} Watt")
            
            PR = (VR**2) / R if R != 0 else 0
            st.write(f"**5. PR = (VR^2)/R:** {PR:.3f} Watt")
            
            # --- CEKBOX SELESAI ---
            st.markdown("---")
            selesai = st.checkbox("Selesai")
            if selesai:
                st.success("Semangat jan lemes-lemes ngelapraknya! 🚀")
                if st.button("Kembali ke Dashboard"):
                    pindah_ke_dashboard()
                    st.rerun()

# ==========================================
# HALAMAN 3: OPSI DLL
# ==========================================
elif st.session_state.menu_utama == "2. Praktikum Lainnya (Segera)":
    st.title("🚧 Modul Sedang Disusun")
    st.write("Modul ini akan diedit dan ditambahkan yang lainnya nanti di GitHub.")
