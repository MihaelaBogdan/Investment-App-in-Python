import tkinter as tk
from tkinter import ttk, messagebox
from stock_analysis import Stock
from export_utils import export_to_excel
from auth import process_login, process_registration
import os
import pandas as pd

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.report_dir = "rapoarte"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

        self.title("")
        self.geometry("1200x800")

        self.analysis = Stock(self)

        # Header
        header = tk.Frame(self, bg="#004d00", height=50)
        header.pack(fill=tk.X)
        title = tk.Label(header, text="CM Invest", bg="#004d00", fg="white", font=("Arial", 24))
        title.pack(pady=10)

        # Sidebar
        sidebar = tk.Frame(self, bg="#e6ffe6", width=200)
        sidebar.pack(fill=tk.Y, side=tk.LEFT)

        sidebar_buttons = [
            ("Home", self.show_home),
            ("Analize", self.show_analysis),
            ("Rapoarte", self.show_reports),
            ("Setări", self.show_settings),
            ("Ajutor", self.show_help),
            ("Autentificare", self.show_login),
            ("Portofoliu", self.show_portfolio) 
        ]

        for text, command in sidebar_buttons:
            button = tk.Button(sidebar, text=text, bg="#e6ffe6", font=("Arial", 14), relief=tk.FLAT, command=command)
            button.pack(fill=tk.X, pady=5, padx=5)

        self.main = tk.Frame(self, bg="white")
        self.main.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

       
        self.filter_frame = tk.Frame(self.main, bg="white", height=50)
        self.filter_frame.pack(fill=tk.X, padx=10, pady=10)

        filter_label = tk.Label(self.filter_frame, text="Filtre:", bg="white", font=("Arial", 14))
        filter_label.pack(side=tk.LEFT, padx=5)

        self.period_filter = ttk.Combobox(self.filter_frame, values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"])
        self.period_filter.pack(side=tk.LEFT, padx=5)

        stock_label = tk.Label(self.filter_frame, text="Nume:", bg="white", font=("Arial", 14))
        stock_label.pack(side=tk.LEFT, padx=5)

        self.stock_entry = tk.Entry(self.filter_frame, font=("Arial", 14))
        self.stock_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(self.filter_frame, text="Caută", bg="#004d00", fg="white", font=("Arial", 14), command=self.search_stocks)
        search_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(self.filter_frame, text="Export", bg="#004d00", fg="white", font=("Arial", 14), command=self.export_to_excel)
        self.export_button.pack(side=tk.LEFT, padx=5)
        self.export_button.config(state=tk.DISABLED)

        prediction_period_label = tk.Label(self.filter_frame, text="Perioadă Predicție:", bg="white", font=("Arial", 14))
        prediction_period_label.pack(side=tk.LEFT, padx=5)

        self.prediction_period = ttk.Combobox(self.filter_frame, values=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"])
        self.prediction_period.pack(side=tk.LEFT, padx=5)

        self.predict_button = tk.Button(self.filter_frame, text="Predicție", bg="#004d00", fg="white", font=("Arial", 14), command=self.train_and_predict)
        self.predict_button.pack(side=tk.LEFT, padx=5)
        self.predict_button.config(state=tk.DISABLED)

        # grafic si tabel
        self.graph_frame = tk.Frame(self.main, bg="white")
        self.graph_frame.pack(fill=tk.X, padx=10, pady=10)
        self.graph_label = tk.Label(self.graph_frame, text="", bg="white", font=("Arial", 14))
        self.graph_label.pack()

        self.table_frame = tk.Frame(self.main, bg="white")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = None
        self.figure = None

     # Footer
        footer = tk.Frame(self, bg="#004d00", height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer_label = tk.Label(footer, text="", bg="#004d00", fg="white", font=("Arial", 10))
        footer_label.pack(pady=5)
#functii sidebar
    def show_home(self):
        self.clear_main_frame()
        self.filter_frame.pack(fill=tk.X, padx=10, pady=10)
        self.graph_frame.pack(fill=tk.X, padx=10, pady=10)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if self.analysis.df is not None:
            self.analysis.plot_prediction_graph()
            combined_df = pd.concat([self.analysis.df, self.analysis.future_df], axis=1) if self.analysis.future_df is not None else self.analysis.df
            self.update_table(combined_df)
        else:
            self.graph_label.config(text="Nu există date pentru a afișa.")

        self.export_button.config(state=tk.NORMAL if self.analysis.df is not None else tk.DISABLED)
        self.predict_button.config(state=tk.NORMAL if self.analysis.df is not None else tk.DISABLED)

    def show_analysis(self):
        self.clear_main_frame()
        messagebox.showinfo("Analize", "Aceasta este secțiunea de analize.")

    def show_reports(self):
        self.clear_main_frame()
        reports_frame = tk.Frame(self.main, bg="white")
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        reports_label = tk.Label(reports_frame, text="Rapoarte Generate", bg="white", font=("Arial", 18))
        reports_label.pack(pady=10)

        reports_listbox = tk.Listbox(reports_frame, font=("Arial", 14))
        reports_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for report in os.listdir(self.report_dir):
            reports_listbox.insert(tk.END, report)

        reports_listbox.bind('<<ListboxSelect>>', self.load_report)

        self.main_frame = reports_frame

    def show_settings(self):
        self.clear_main_frame()
        settings_frame = tk.Frame(self.main, bg="white")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        settings_label = tk.Label(settings_frame, text="Setări", bg="white", font=("Arial", 18))
        settings_label.pack(pady=10)

    def show_help(self):
        self.clear_main_frame()
        messagebox.showinfo("Ajutor", "Aceasta este secțiunea de ajutor.")

    def show_login(self):
        self.clear_main_frame()
        login_frame = tk.Frame(self.main, bg="white")
        login_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        email_label = tk.Label(login_frame, text="Email:", bg="white", font=("Arial", 14))
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(login_frame, font=("Arial", 14))
        self.email_entry.pack(pady=5)

        password_label = tk.Label(login_frame, text="Parolă:", bg="white", font=("Arial", 14))
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show='*', font=("Arial", 14))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(login_frame, text="Autentificare", bg="#004d00", fg="white", font=("Arial", 14), command=self.process_login)
        login_button.pack(pady=10)

        register_button = tk.Button(login_frame, text="Cont Nou", bg="#004d00", fg="white", font=("Arial", 14), command=self.show_register)
        register_button.pack(pady=5)

        self.main_frame = login_frame

    def show_register(self):
        self.clear_main_frame()
        register_frame = tk.Frame(self.main, bg="white")
        register_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        register_label = tk.Label(register_frame, text="Înregistrare", bg="white", font=("Arial", 18))
        register_label.pack(pady=10)

        name_label = tk.Label(register_frame, text="Nume:", bg="white", font=("Arial", 14))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        email_label = tk.Label(register_frame, text="Email:", bg="white", font=("Arial", 14))
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.email_entry.pack(pady=5)

        password_label = tk.Label(register_frame, text="Parolă:", bg="white", font=("Arial", 14))
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(register_frame, show='*', font=("Arial", 14))
        self.password_entry.pack(pady=5)

        register_button = tk.Button(register_frame, text="Înregistrare", bg="#004d00", fg="white", font=("Arial", 14), command=self.process_registration)
        register_button.pack(pady=10)

        self.main_frame = register_frame

    def show_portfolio(self):
        self.clear_main_frame()
        portfolio_frame = tk.Frame(self.main, bg="white")
        portfolio_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        portfolio_label = tk.Label(portfolio_frame, text="Portofoliu", bg="white", font=("Arial", 18))
        portfolio_label.pack(pady=10)

       
        portfolio_data = self.get_portfolio_data()  
        if portfolio_data:
            self.update_table(portfolio_data)
        else:
            no_data_label = tk.Label(portfolio_frame, text="Nu există date pentru portofoliu.", bg="white", font=("Arial", 14))
            no_data_label.pack(pady=10)

        self.main_frame = portfolio_frame

    def clear_main_frame(self):
        for widget in self.main.winfo_children():
            widget.pack_forget()

    def update_table(self, df):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if df is not None and not df.empty:
            columns = list(df.columns)
            tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W, width=100)

            for index, row in df.iterrows():
                tree.insert('', 'end', values=list(row))

            tree.pack(fill=tk.BOTH, expand=True)

    def load_report(self, event):
        selected_report = event.widget.get(event.widget.curselection())
        report_path = os.path.join(self.report_dir, selected_report)

        if os.path.isfile(report_path):
            df = pd.read_excel(report_path, sheet_name="Date Acțiuni")
            self.update_table(df)

    def search_stocks(self):
        stock_name = self.stock_entry.get()
        period = self.period_filter.get()
        if stock_name and period:
            self.analysis.load_stock_data(stock_name, period)
            self.show_home()

    def export_to_excel(self):
        try:
            filename = export_to_excel(self.analysis.df, self.report_dir, self.analysis.future_df, self.analysis.figure)
            messagebox.showinfo("Export", f"Raportul a fost exportat cu succes la {filename}.")
        except Exception as e:
            messagebox.showerror("Export", f"Eroare la exportul raportului: {e}")

    def train_and_predict(self):
      
        pass

    def process_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        process_login(email, password)

    def process_registration(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        process_registration(name, email, password)

    def get_portfolio_data(self):
        
        return pd.DataFrame() 
