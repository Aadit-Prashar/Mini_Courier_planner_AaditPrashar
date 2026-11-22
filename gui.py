import tkinter as tk
from tkinter import ttk, messagebox

from data_manager import load_parcels, add_parcel, delete_parcel, update_status, load_graph
from sorting import sort_by_priority
from knapsack import optimize_parcels
from dijkstra import dijkstra, get_path
from tsp import nearest_neighbour
from performance import compare_performance

NAVY = "#14213D"
NAVY_2 = "#1D3557"
BLUE = "#3B82F6"
BG = "#F4F7FB"
WHITE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#667085"
GREEN = "#16A34A"
RED = "#DC2626"
AMBER = "#D97706"


class CourierApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("QuickRoute | Courier Operations")
        self.root.geometry("1250x790")
        self.root.minsize(1050, 680)
        self.root.configure(bg=BG)

        self.capacity = 12
        self.selected_parcels = []
        self.graph = load_graph()

        self.setup_styles()
        self.build_shell()
        self.show_page("Dashboard")
        self.refresh_dashboard()

    def update_card_value(self, card, value):
        card.value_label.config(text=value)

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=34,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#E8EEF6",
            foreground=NAVY,
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", TEXT)]
        )

        style.configure("TCombobox", padding=5)

    def build_shell(self):
        self.sidebar = tk.Frame(self.root, bg=NAVY, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=NAVY)
        brand.pack(fill="x", padx=20, pady=(25, 30))

        tk.Label(
            brand,
            text="↗",
            bg="#243B64",
            fg="#93C5FD",
            font=("Segoe UI", 22, "bold"),
            width=2
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            brand,
            text="QuickRoute",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="COURIER OPERATIONS",
            bg=NAVY,
            fg="#9FB2D0",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            bg=NAVY,
            fg="#8295B4",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=22, pady=(0, 10))

        self.nav_buttons = {}

        for name, glyph in [
            ("Dashboard", "▦"),
            ("Parcel Manager", "▤"),
            ("Route Planner", "⌁"),
            ("Performance", "◫")
        ]:
            btn = tk.Button(
                self.sidebar,
                text=f"  {glyph}   {name}",
                anchor="w",
                font=("Segoe UI", 11),
                relief="flat",
                bd=0,
                bg=NAVY,
                fg="#D8E2F2",
                activebackground=NAVY_2,
                activeforeground=WHITE,
                padx=18,
                pady=13,
                command=lambda n=name: self.show_page(n)
            )

            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = btn

        bottom = tk.Frame(self.sidebar, bg=NAVY)
        bottom.pack(side="bottom", fill="x", padx=20, pady=20)

        tk.Label(
            bottom,
            text="DAA MINI PROJECT",
            bg=NAVY,
            fg="#8295B4",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            bottom,
            text="Route & load optimization",
            bg=NAVY,
            fg="#D8E2F2",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(5, 0))

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.header = tk.Frame(self.main, bg=WHITE, height=65)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.page_heading = tk.Label(
            self.header,
            text="Dashboard",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 17, "bold")
        )
        self.page_heading.pack(side="left", padx=28)

        tk.Label(
            self.header,
            text="MINI COURIER PLANNER",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="right", padx=28)

        self.page_area = tk.Frame(self.main, bg=BG)
        self.page_area.pack(fill="both", expand=True, padx=24, pady=22)

        self.pages = {}

        for name in [
            "Dashboard",
            "Parcel Manager",
            "Route Planner",
            "Performance"
        ]:
            self.pages[name] = tk.Frame(self.page_area, bg=BG)

        self.build_dashboard()
        self.build_parcel_page()
        self.build_route_page()
        self.build_performance_page()

    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()

        self.pages[name].pack(fill="both", expand=True)
        self.page_heading.config(text=name)

        for nav, button in self.nav_buttons.items():
            button.config(
                bg=NAVY_2 if nav == name else NAVY,
                fg=WHITE if nav == name else "#D8E2F2"
            )

    def section_title(self, parent, title, subtitle=None):
        tk.Label(
            parent,
            text=title,
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                parent,
                text=subtitle,
                bg=BG,
                fg=MUTED,
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(4, 15))
        else:
            tk.Frame(parent, bg=BG, height=14).pack()

    def card(self, parent, title, value, note="", accent=BLUE):
        box = tk.Frame(
            parent,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )

        box.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Frame(
            box,
            bg=accent,
            width=5
        ).pack(side="left", fill="y")

        inner = tk.Frame(box, bg=WHITE)
        inner.pack(fill="both", expand=True, padx=15, pady=14)

        tk.Label(
            inner,
            text=title.upper(),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        value_label = tk.Label(
            inner,
            text=value,
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 23, "bold")
        )
        value_label.pack(anchor="w", pady=(5, 0))

        if note:
            tk.Label(
                inner,
                text=note,
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(4, 0))

        box.value_label = value_label
        return box

    # ---------------- Dashboard ----------------

    def build_dashboard(self):
        page = self.pages["Dashboard"]

        self.section_title(
            page,
            "Operations overview",
            "Quick snapshot of your parcel and delivery workload."
        )

        self.dash_cards = tk.Frame(page, bg=BG)
        self.dash_cards.pack(fill="x", pady=(0, 18))

        lower = tk.Frame(page, bg=BG)
        lower.pack(fill="both", expand=True)

        left = tk.Frame(
            lower,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(
            left,
            text="Vehicle capacity",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 8))

        self.capacity_text = tk.Label(
            left,
            text="",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 11)
        )
        self.capacity_text.pack(anchor="w", padx=18)

        self.capacity_canvas = tk.Canvas(
            left,
            height=28,
            bg="#E8EEF6",
            highlightthickness=0
        )
        self.capacity_canvas.pack(fill="x", padx=18, pady=12)

        self.capacity_note = tk.Label(
            left,
            text="",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.capacity_note.pack(anchor="w", padx=18)

        tk.Label(
            left,
            text="Priority overview",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=18, pady=(25, 8))

        self.priority_summary = tk.Label(
            left,
            text="",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 11),
            justify="left"
        )
        self.priority_summary.pack(anchor="w", padx=18, pady=(0, 20))

        right = tk.Frame(
            lower,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="Recent parcel activity",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self.recent_table = ttk.Treeview(
            right,
            columns=("id", "destination", "status"),
            show="headings",
            height=8
        )

        for col, label, width in [
            ("id", "Parcel ID", 110),
            ("destination", "Destination", 150),
            ("status", "Status", 130)
        ]:
            self.recent_table.heading(col, text=label)
            self.recent_table.column(col, width=width, anchor="center")

        self.recent_table.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        actions = tk.Frame(page, bg=BG)
        actions.pack(fill="x", pady=(16, 0))

        self.action_button(actions, "＋  Add parcel", self.open_add_dialog, BLUE)
        self.action_button(actions, "⌁  Plan route", lambda: self.show_page("Route Planner"), GREEN)
        self.action_button(actions, "↻  Refresh", self.refresh_dashboard, NAVY_2)

    def refresh_dashboard(self):
        if not hasattr(self, "dash_cards"):
            return

        for child in self.dash_cards.winfo_children():
            child.destroy()

        parcels = load_parcels()
        total_weight = sum(p["weight"] for p in parcels)
        pending = sum(p["status"] == "Pending" for p in parcels)
        delivered = sum(p["status"] == "Delivered" for p in parcels)
        high = sum(p["priority"] == "High" for p in parcels)
        medium = sum(p["priority"] == "Medium" for p in parcels)
        low = sum(p["priority"] == "Low" for p in parcels)

        row = self.dash_cards

        self.card(row, "Total parcels", str(len(parcels)), "All records", BLUE)
        self.card(row, "Pending", str(pending), "Awaiting delivery", AMBER)
        self.card(row, "Delivered", str(delivered), "Completed", GREEN)
        self.card(row, "Total weight", f"{total_weight:.1f} kg", f"Vehicle limit: {self.capacity} kg", "#7C3AED")

        self.capacity_text.config(
            text=f"{total_weight:.1f} kg loaded against {self.capacity} kg capacity"
        )

        self.capacity_canvas.delete("all")
        self.capacity_canvas.update_idletasks()

        width = max(self.capacity_canvas.winfo_width(), 300)
        ratio = min(total_weight / self.capacity, 1) if self.capacity else 0

        self.capacity_canvas.create_rectangle(
            0, 0, width, 28,
            fill="#E8EEF6",
            outline=""
        )

        self.capacity_canvas.create_rectangle(
            0, 0, width * ratio, 28,
            fill=GREEN if ratio <= 1 else RED,
            outline=""
        )

        self.capacity_note.config(
            text=f"{ratio * 100:.1f}% of dashboard capacity used (all parcel records)"
        )

        self.priority_summary.config(
            text=f"High priority     {high}\nMedium priority  {medium}\nLow priority       {low}"
        )

        for rowid in self.recent_table.get_children():
            self.recent_table.delete(rowid)

        for p in parcels[-8:][::-1]:
            self.recent_table.insert(
                "",
                "end",
                values=(p["parcel_id"], p["destination"], p["status"])
            )

    def action_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=16,
            pady=10,
            cursor="hand2"
        )
        btn.pack(side="left", padx=(0, 10))

    # ---------------- Parcel Manager ----------------

    def build_parcel_page(self):
        page = self.pages["Parcel Manager"]

        self.section_title(
            page,
            "Parcel management",
            "Search, add, sort, remove and update parcel records."
        )

        toolbar = tk.Frame(page, bg=BG)
        toolbar.pack(fill="x", pady=(0, 12))

        self.search_var = tk.StringVar()

        search = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=30
        )
        search.pack(side="left", padx=(0, 8), ipady=7)

        self.search_var.trace_add("write", lambda *_: self.refresh_parcels())

        tk.Button(
            toolbar,
            text="＋ Add parcel",
            command=self.open_add_dialog,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Sort priority",
            command=self.sort_parcels,
            bg=NAVY_2,
            fg=WHITE,
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Delete selected",
            command=self.delete_selected,
            bg=RED,
            fg=WHITE,
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_parcels,
            bg="#64748B",
            fg=WHITE,
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5)

        table_wrap = tk.Frame(
            page,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        table_wrap.pack(fill="both", expand=True)

        cols = ("id", "destination", "weight", "priority", "cost", "status")

        self.parcel_table = ttk.Treeview(
            table_wrap,
            columns=cols,
            show="headings"
        )

        labels = {
            "id": "Parcel ID",
            "destination": "Destination",
            "weight": "Weight (kg)",
            "priority": "Priority",
            "cost": "Delivery Cost",
            "status": "Status"
        }

        widths = {
            "id": 120,
            "destination": 180,
            "weight": 120,
            "priority": 120,
            "cost": 140,
            "status": 140
        }

        for c in cols:
            self.parcel_table.heading(c, text=labels[c])
            self.parcel_table.column(c, width=widths[c], anchor="center")

        vs = ttk.Scrollbar(
            table_wrap,
            orient="vertical",
            command=self.parcel_table.yview
        )

        self.parcel_table.configure(yscrollcommand=vs.set)
        self.parcel_table.pack(side="left", fill="both", expand=True)
        vs.pack(side="right", fill="y")

        self.parcel_table.tag_configure("High", foreground="#B91C1C")
        self.parcel_table.tag_configure("Medium", foreground="#B45309")
        self.parcel_table.tag_configure("Low", foreground="#166534")

        bottom = tk.Frame(page, bg=BG)
        bottom.pack(fill="x", pady=12)

        tk.Label(
            bottom,
            text="Set selected status:",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.status_var = tk.StringVar(value="Delivered")

        ttk.Combobox(
            bottom,
            textvariable=self.status_var,
            values=["Pending", "Delivered"],
            state="readonly",
            width=14
        ).pack(side="left", padx=10)

        tk.Button(
            bottom,
            text="Update status",
            command=self.change_status,
            bg=GREEN,
            fg=WHITE,
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.refresh_parcels()

    def refresh_parcels(self):
        if not hasattr(self, "parcel_table"):
            return

        for rowid in self.parcel_table.get_children():
            self.parcel_table.delete(rowid)

        parcels = load_parcels()
        query = self.search_var.get().lower() if hasattr(self, "search_var") else ""

        for p in parcels:
            if query and query not in str(p["parcel_id"]).lower() and query not in str(p["destination"]).lower():
                continue

            self.parcel_table.insert(
                "",
                "end",
                values=(
                    p["parcel_id"],
                    p["destination"],
                    p["weight"],
                    p["priority"],
                    p["delivery_cost"],
                    p["status"]
                ),
                tags=(p["priority"],)
            )

    def sort_parcels(self):
        sorted_list = sort_by_priority(load_parcels())

        for rowid in self.parcel_table.get_children():
            self.parcel_table.delete(rowid)

        query = self.search_var.get().lower()

        for p in sorted_list:
            if query and query not in p["parcel_id"].lower() and query not in p["destination"].lower():
                continue

            self.parcel_table.insert(
                "",
                "end",
                values=(
                    p["parcel_id"],
                    p["destination"],
                    p["weight"],
                    p["priority"],
                    p["delivery_cost"],
                    p["status"]
                ),
                tags=(p["priority"],)
            )

    def delete_selected(self):
        selected = self.parcel_table.selection()

        if not selected:
            messagebox.showwarning("Select parcel", "Please select a parcel row first.")
            return

        parcel_id = self.parcel_table.item(selected[0], "values")[0]

        if messagebox.askyesno("Confirm deletion", f"Delete parcel {parcel_id}?"):
            if delete_parcel(parcel_id):
                self.refresh_parcels()
                self.refresh_dashboard()
                messagebox.showinfo("Deleted", "Parcel removed.")
            else:
                messagebox.showerror("Error", "Could not delete that parcel.")

    def change_status(self):
        selected = self.parcel_table.selection()

        if not selected:
            messagebox.showwarning("Select parcel", "Please select a parcel row first.")
            return

        parcel_id = self.parcel_table.item(selected[0], "values")[0]

        if update_status(parcel_id, self.status_var.get()):
            self.refresh_parcels()
            self.refresh_dashboard()
            messagebox.showinfo("Updated", "Parcel status updated.")
        else:
            messagebox.showerror("Error", "Status update failed.")

    def open_add_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add parcel")
        dialog.configure(bg=BG)
        dialog.geometry("420x580")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="New parcel",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=24, pady=(20, 4))

        tk.Label(
            dialog,
            text="Enter parcel details below.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=24, pady=(0, 14))

        form = tk.Frame(dialog, bg=BG)
        form.pack(fill="x", padx=24)

        entries = {}

        fields = [
            ("Parcel ID", "id"),
            ("Destination", "destination"),
            ("Weight (kg)", "weight"),
            ("Delivery Cost", "cost")
        ]

        for label, key in fields:
            tk.Label(
                form,
                text=label,
                bg=BG,
                fg=TEXT,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(7, 2))

            ent = tk.Entry(
                form,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )
            ent.pack(fill="x", ipady=6)
            entries[key] = ent

        tk.Label(
            form,
            text="Priority",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(7, 2))

        priority = ttk.Combobox(
            form,
            values=["High", "Medium", "Low"],
            state="readonly"
        )
        priority.pack(fill="x")
        priority.set("Medium")

        def save():
            try:
                parcel_id = entries["id"].get().strip()
                destination = entries["destination"].get().strip()
                weight = float(entries["weight"].get())
                cost = float(entries["cost"].get())
                parcel_priority = priority.get()

                if not parcel_id or not destination or not parcel_priority:
                    messagebox.showerror(
                        "Missing fields",
                        "Please fill in every field.",
                        parent=dialog
                    )
                    return

                if weight <= 0 or cost < 0:
                    messagebox.showerror(
                        "Invalid values",
                        "Weight must be positive and cost cannot be negative.",
                        parent=dialog
                    )
                    return

                parcel = {
                    "parcel_id": parcel_id,
                    "destination": destination,
                    "weight": weight,
                    "priority": parcel_priority,
                    "delivery_cost": cost,
                    "status": "Pending"
                }

                result = add_parcel(parcel)

                if result:
                    self.refresh_parcels()
                    self.refresh_dashboard()
                    dialog.destroy()

                    messagebox.showinfo(
                        "Success",
                        "Parcel added successfully!"
                    )
                else:
                    messagebox.showerror(
                        "Duplicate ID",
                        "This parcel ID already exists.",
                        parent=dialog
                    )

            except ValueError:
                messagebox.showerror(
                    "Invalid values",
                    "Weight and Delivery Cost must be numbers.",
                    parent=dialog
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Something went wrong:\n{e}",
                    parent=dialog
                )

        tk.Button(
            form,
            text="Save Parcel",
            command=save,
            bg=GREEN,
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(fill="x", pady=20)

    # ---------------- Route Planner ----------------

    def build_route_page(self):
        page = self.pages["Route Planner"]

        self.section_title(
            page,
            "Route planning & load optimization",
            "Choose a starting point and vehicle capacity, then optimize the load and route."
        )

        controls = tk.Frame(
            page,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        controls.pack(fill="x", pady=(0, 12))

        locations = sorted(self.graph.keys())

        tk.Label(
            controls,
            text="Starting location",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, padx=14, pady=15)

        self.start_var = tk.StringVar(
            value="Delhi" if "Delhi" in locations else (locations[0] if locations else "")
        )

        ttk.Combobox(
            controls,
            textvariable=self.start_var,
            values=locations,
            state="readonly",
            width=18
        ).grid(row=0, column=1, padx=6)

        tk.Label(
            controls,
            text="Capacity (kg)",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=2, padx=14)

        self.capacity_entry = tk.Entry(controls, width=8, font=("Segoe UI", 10))
        self.capacity_entry.insert(0, str(self.capacity))
        self.capacity_entry.grid(row=0, column=3, padx=6)

        tk.Button(
            controls,
            text="Optimize load",
            command=self.optimize_load,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            padx=12,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=4, padx=10)

        tk.Button(
            controls,
            text="Calculate route",
            command=self.calculate_route,
            bg=GREEN,
            fg=WHITE,
            relief="flat",
            padx=12,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=5, padx=5)

        summary = tk.Frame(page, bg=BG)
        summary.pack(fill="x", pady=(0, 10))

        self.route_weight_card = self.card(
            summary, "Selected weight", "--", "Load selection", BLUE
        )

        self.route_value_card = self.card(
            summary, "Delivery value", "--", "Knapsack objective", GREEN
        )

        self.route_distance_card = self.card(
            summary, "Route distance", "--", "Calculated tour", "#7C3AED"
        )

        tk.Label(
            page,
            text="Selected parcels",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(6, 6))

        wrap = tk.Frame(
            page,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        wrap.pack(fill="x", pady=(0, 12))

        cols = ("id", "destination", "weight", "priority", "cost")

        self.route_table = ttk.Treeview(
            wrap,
            columns=cols,
            show="headings",
            height=5
        )

        headings = {
            "id": "Parcel ID",
            "destination": "Destination",
            "weight": "Weight (kg)",
            "priority": "Priority",
            "cost": "Delivery Cost"
        }

        for c in cols:
            self.route_table.heading(c, text=headings[c])
            self.route_table.column(c, width=130, anchor="center")

        self.route_table.pack(fill="x")

        tk.Label(
            page,
            text="Planned delivery tour",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(2, 6))

        self.route_output = tk.Text(
            page,
            height=7,
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=TEXT,
            relief="solid",
            bd=1,
            wrap="word",
            padx=12,
            pady=10
        )
        self.route_output.pack(fill="both", expand=True)

        self.selected_parcels = []

    def optimize_load(self):
        try:
            capacity = float(self.capacity_entry.get())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid capacity", "Capacity must be a positive number.")
            return

        parcels = load_parcels()
        selected, weight, value = optimize_parcels(parcels, capacity)
        self.selected_parcels = selected

        for row in self.route_table.get_children():
            self.route_table.delete(row)

        for p in selected:
            self.route_table.insert(
                "",
                "end",
                values=(
                    p["parcel_id"],
                    p["destination"],
                    p["weight"],
                    p["priority"],
                    p["delivery_cost"]
                )
            )

        self.route_output.delete("1.0", tk.END)

        self.route_output.insert(
            tk.END,
            f"Load optimization complete\n\n"
            f"Capacity: {capacity:g} kg\n"
            f"Selected: {len(selected)} of {len(parcels)} parcels\n"
            f"Weight used: {weight:.2f} kg\n"
            f"Delivery-cost objective: {value:.2f}\n\n"
            "Algorithm: 0/1 Knapsack Dynamic Programming"
        )

        self.update_card_value(self.route_weight_card, f"{weight:.2f} kg")
        self.update_card_value(self.route_value_card, f"{value:.2f}")
        self.update_card_value(self.route_distance_card, "--")

    def calculate_route(self):
        try:
            if not self.selected_parcels:
                self.optimize_load()
                if not self.selected_parcels:
                    messagebox.showwarning(
                        "No parcels",
                        "No parcels were selected for routing."
                    )
                    return

            start = self.start_var.get()
            graph = load_graph()

            if not graph:
                messagebox.showerror("Error", "The road graph is empty.")
                return

            if start not in graph:
                messagebox.showerror(
                    "Invalid start",
                    f"{start} is not present in the road graph."
                )
                return

            destinations = list(dict.fromkeys(
                p["destination"] for p in self.selected_parcels
            ))

            missing = [d for d in destinations if d not in graph]

            if missing:
                messagebox.showerror(
                    "Destination not found",
                    "These destinations are missing from the graph:\n\n"
                    + ", ".join(missing)
                )
                return

            stops = list(destinations)

            if start not in stops:
                stops.insert(0, start)

            matrix = {}
            paths = {}

            for source in stops:
                distances, previous = dijkstra(graph, source)
                matrix[source] = {}

                for destination in stops:
                    matrix[source][destination] = distances.get(
                        destination, float("inf")
                    )

                    try:
                        if destination == source:
                            paths[(source, destination)] = [source]
                        else:
                            paths[(source, destination)] = get_path(
                                previous, destination
                            )
                    except Exception:
                        paths[(source, destination)] = []

            route, total = nearest_neighbour(matrix, start)

            if not route:
                messagebox.showerror(
                    "Route error",
                    "The routing algorithm could not generate a route."
                )
                return

            self.update_card_value(
                self.route_distance_card, f"{total:.2f} km"
            )

            self.route_output.delete("1.0", tk.END)

            lines = ["DELIVERY TOUR", f"Start: {start}", ""]

            for i in range(len(route) - 1):
                a, b = route[i], route[i + 1]
                leg = matrix.get(a, {}).get(b, float("inf"))
                path = paths.get((a, b), [])

                path_text = (
                    " -> ".join(path) if path
                    else f"{a} -> {b}"
                )

                lines.append(
                    f"{i+1}. {a} -> {b} | {leg:.2f} km"
                )
                lines.append(f"   Shortest path: {path_text}")

            lines.extend([
                "",
                f"Total tour distance: {total:.2f} km",
                "",
                "Algorithms: Dijkstra (shortest paths) + "
                "Nearest Neighbour (stop ordering)"
            ])

            self.route_output.insert(tk.END, "\n".join(lines))

        except Exception as e:
            messagebox.showerror(
                "Route calculation failed",
                f"An error occurred while calculating the route:\n\n{e}"
            )
            print("Route calculation error:", e)
    # ---------------- Performance ----------------

    def build_performance_page(self):
        page = self.pages["Performance"]

        self.section_title(
            page,
            "Algorithm performance laboratory",
            "Benchmark the four algorithms and compare measured execution times."
        )

        controls = tk.Frame(
            page,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        controls.pack(fill="x", pady=(0, 12))

        locations = sorted(self.graph.keys())

        tk.Label(
            controls,
            text="Starting location",
            bg=WHITE,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, padx=14, pady=15)

        self.performance_start = tk.StringVar(
            value="Delhi" if "Delhi" in locations else (locations[0] if locations else "")
        )

        ttk.Combobox(
            controls,
            textvariable=self.performance_start,
            values=locations,
            state="readonly",
            width=18
        ).grid(row=0, column=1, padx=6)

        tk.Label(
            controls,
            text="Capacity (kg)",
            bg=WHITE,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=2, padx=14)

        self.performance_capacity = tk.Entry(controls, width=8)
        self.performance_capacity.insert(0, "12")
        self.performance_capacity.grid(row=0, column=3, padx=6)

        tk.Button(
            controls,
            text="Run benchmark",
            command=self.run_performance_test,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            padx=15,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=4, padx=15)

        tableframe = tk.Frame(
            page,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        tableframe.pack(fill="x", pady=(0, 14))

        self.performance_table = ttk.Treeview(
            tableframe,
            columns=("algorithm", "time", "complexity"),
            show="headings",
            height=4
        )

        for col, label, width in [
            ("algorithm", "Algorithm", 220),
            ("time", "Average execution time (ms)", 260),
            ("complexity", "Theoretical complexity", 300)
        ]:
            self.performance_table.heading(col, text=label)
            self.performance_table.column(col, width=width, anchor="center")

        self.performance_table.pack(fill="x")

        chartframe = tk.Frame(
            page,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#E5EAF2"
        )
        chartframe.pack(fill="both", expand=True, pady=(0, 12))

        tk.Label(
            chartframe,
            text="Measured time comparison",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=16, pady=12)

        self.performance_canvas = tk.Canvas(
            chartframe,
            bg=WHITE,
            height=240,
            highlightthickness=0
        )
        self.performance_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.performance_result = tk.Label(
            page,
            text="Run a benchmark to populate the results.",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 11, "bold")
        )
        self.performance_result.pack(anchor="w")

    def run_performance_test(self):
        try:
            capacity = float(self.performance_capacity.get())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid capacity", "Capacity must be a positive number.")
            return

        start = self.performance_start.get()
        parcels, graph = load_parcels(), load_graph()

        results = compare_performance(parcels, graph, capacity, start)

        complexities = {
            "Bubble Sort": "O(n²)",
            "Knapsack DP": "O(nW)",
            "Dijkstra": "O((V+E) log V)",
            "Nearest Neighbour": "O(n²)"
        }

        times_ms = {
            name: seconds * 1000
            for name, seconds in results.items()
        }

        for rowid in self.performance_table.get_children():
            self.performance_table.delete(rowid)

        for name, ms in times_ms.items():
            self.performance_table.insert(
                "",
                "end",
                values=(
                    name,
                    f"{ms:.6f}",
                    complexities.get(name, "—")
                )
            )

        self.draw_bars(times_ms)

        fastest = min(times_ms, key=times_ms.get)

        self.performance_result.config(
            text=f"Fastest measured in this test: {fastest} "
                 f"({times_ms[fastest]:.6f} ms)"
        )

    def draw_bars(self, times):
        canvas = self.performance_canvas
        canvas.delete("all")
        canvas.update_idletasks()

        width = max(canvas.winfo_width(), 500)
        maxval = max(times.values()) if times else 1
        maxval = max(maxval, 1e-12)

        names = list(times.keys())
        left, top, right = 170, 20, width - 120
        usable = max(right - left, 150)
        rowheight = 45

        for i, name in enumerate(names):
            y = top + i * rowheight
            value = times[name]
            length = max(2, (value / maxval) * usable)

            canvas.create_text(
                left - 12,
                y + 12,
                text=name,
                anchor="e",
                fill=TEXT,
                font=("Segoe UI", 10)
            )

            canvas.create_rectangle(
                left,
                y,
                left + length,
                y + 24,
                fill=BLUE,
                outline=""
            )

            canvas.create_text(
                left + length + 8,
                y + 12,
                text=f"{value:.6f} ms",
                anchor="w",
                fill=TEXT,
                font=("Segoe UI", 9)
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = CourierApp(root)
    root.mainloop()